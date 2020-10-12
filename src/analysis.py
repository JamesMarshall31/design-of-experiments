import numpy as np
import design
import pandas as pd
import itertools


def fit_two_level_screening(df):
    n = len(df.index)
    p_columns_list = list(df.columns)[:-1]
    # Creating the T matrix
    # ------------------------
    t_matrix = np.ones((n, n), dtype=int)
    count = 1
    for i in df.columns[0:-1]:
        high = max(df[i])
        low = min(df[i])
        df[i] = (df[i].map({high: 1, low: -1}))
        t_matrix[count] = df[i]
        count += 1

    rows_remaining = n - (len(df.columns))
    t_rows = []  # we are technically making the transpose of the T matrix as we are adding to the rows
    r = 2
    combination_check = 0
    for x in range(1, count):
        t_rows.append(x)
    while rows_remaining > 0:
        for combination in itertools.combinations(t_rows, r):
            string =''
            for i in combination:
                string = string + p_columns_list[i-1] + '*'
            t_matrix[count] = 1
            string = string[:-1]        # Get rid of asterisk
            p_columns_list.append(string)
            for i in range(r):
                t_matrix[count] = t_matrix[count] * t_matrix[combination[i]]
            rows_remaining -= 1
            count += 1
            combination_check += 1
            if combination_check == len(list(itertools.combinations(t_rows, r))):
                r += 1
                combination_check = 0
                break
            if rows_remaining == 0:
                break
    t_matrix = t_matrix/np.sqrt(n)      # to normalize

    # Using the T matrix to get the contrasts
    # ---------------------------------------
    results = np.array(df['Yield']).reshape(n, 1)
    Contrasts = np.matmul(t_matrix, results)        # The first index is the intercept contrast
    Contrasts = Contrasts[1:n]

    # Calculating Lenth's Pseudo-Standard Error
    # ---------------------------------------
    v = 1.5 * np.median(abs(Contrasts))
    PSE = 1.5 * np.median(abs(Contrasts[abs(Contrasts) < (2.5 * v)]))

    # Calculate Lenth t-ratios for each contrast
    # -----------------------------------------
    t_ratios = abs(Contrasts/PSE)

    # Run Monte Carlo simulations to generate contrasts
    # -----------------------------------------
    sim_t_ratio = []
    for i in range(10000):
        simulation = np.array(np.random.normal(0, PSE, n-1))
        v_sim = 1.5 * np.median(abs(simulation))
        PSE_sim = 1.5 * np.median(abs(simulation[abs(simulation) < (2.5 * v_sim)]))
        sim_t_ratio.append(abs(simulation / PSE_sim))
    # Reorder these t-values so our t-values can be found in relation to it
    simulated_t_reordered = np.zeros((n-1, 10000))
    for j in range(n-1):
        for i in range(10000):
            simulated_t_reordered[j][i] = sim_t_ratio[i][j]
        simulated_t_reordered[j] = np.sort(simulated_t_reordered[j])
    p_value = []
    for j in range(n-1):
        for i in range(10000):
            if t_ratios[j][0] < simulated_t_reordered[j][i]:
                p_value.append(1 - (i / 10000))
                break
    p_values = pd.DataFrame(p_value,index=p_columns_list,columns=['Individual p-Value'])
    return p_values


'''factors = {'Temp':[-1,1],'Concentration':[-1,1],'Enzyme':[-1,1]}
df = design.full_factorial_2level(factors)
df['Yield'] = [60,52,54,45,72,83,68,80]
print(fit_two_level_screening(df))'''