import numpy as np
import design
import pandas as pd
import itertools


def lpse(df):
    """
    Calculates Lenth's pseudo standard error for the entered dataframe, assumes the last column contains
    the results.
    :param df:
    :return:
    """
    Contrasts = []
    for i in range(len(df.index)-1):
        Contrasts.append(df.iloc[i+1]['Yield']-df.iloc[i]['Yield'])
    Contrasts = np.array(Contrasts)
    v = 1.5 * np.median(abs(Contrasts))
    PSE = 1.5 * np.median(abs(Contrasts[abs(Contrasts)<(2.5*v)]))
    return PSE

def p_values(df):
    n = len(df.index)
    results = np.array(df['Yield']).reshape(n,1)
    t_transpose = make_matrix(df)
    Contrasts = np.matmul(t_transpose,results)
    v = 1.5 * np.median(abs(Contrasts))
    PSE = 1.5 * np.median(abs(Contrasts[abs(Contrasts) < (2.5 * v)]))
    real_t_ratio = Contrasts/PSE
    simulations = []
    sim_t_ratio = []
    for i in range(10000):
        simulation = np.array(np.random.normal(0, PSE, n))
        v_sim = 1.5 * np.median(abs(simulation))
        PSE_sim = 1.5 * np.median(abs(simulation[abs(simulation) < (2.5 * v_sim)]))
        sim_t_ratio.append(simulation/PSE_sim)
    simulated_t_reordered = np.zeros((8,10000))
    for j in range (n):
        for i in range(10000):
            simulated_t_reordered[j][i] = sim_t_ratio[i][j]
        simulated_t_reordered[j] = np.sort(simulated_t_reordered[j])
    p_value = []
    for j in range(n):
        for i in range(10000):
            if real_t_ratio[j][0]<simulated_t_reordered[j][i]:
                p_value.append(1 - (i / 10000))
                break

    return p_value

def make_matrix(df):
    n = len(df.index)
    t_matrix = np.ones((n,n), dtype=int)
    count = 1
    for i in df.columns[0:-1]:
        high = max(df[i])
        low = min(df[i])
        df[i] = (df[i].map({high:1,low:-1}))
        t_matrix[count] = df[i]
        count += 1

    rows_remaining = n - (len(df.columns))
    t_rows = [] # we are technically making the transpose of the T matrix as we are adding to the rows
    r = 2
    combination_check = 0
    for x in range(1,count):
        t_rows.append(x)
    while rows_remaining > 0:
        for combination in itertools.combinations(t_rows, r):
            t_matrix[count] = 1
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
    return t_matrix