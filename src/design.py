# Our Design of experiment class

import urllib.request
import pandas as pd
import itertools
import math
import lhsmdu
import numpy as np


def full_factorial_2level(dic_factors):
    """
    Creates a Two-level full factorial design from the dictionary of factors entered,
    if more than two levels are given for each factor the maximum and minimum values will be selected

    Parameters:
        dic_factors: The dictionary of factors to be included in the full factorial's design

    Returns:
        df: A dataframe of the two-level full factorial resulting from the factors entered

    Example:
        >>> import design
        >>> Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3]}
        >>> design.Factorial.full_factorial_2level(Factors)
           Height  Width  Depth
        0     1.6    0.2    0.2
        1     1.6    0.2    0.3
        2     1.6    0.4    0.2
        3     1.6    0.4    0.3
        4     2.0    0.2    0.2
        5     2.0    0.2    0.3
        6     2.0    0.4    0.2
        7     2.0    0.4    0.3
    """
    # df is the dataframe that will be returned.
    df = pd.DataFrame()
    # factor_levels will be filled with the levels of each factor and
    # used when iterating through the runs of the design.
    factor_levels = []
    # factor_names is filled at the same time as factor_levels and
    # is used at the end to correctly name the columns of the dataframe.
    factor_names = []

    # This for loop fills up factor_levels with the maximum and minimum of each factor,
    # as well as filling up factor_names.
    for name in dic_factors:
        factor_names.append(name)
        factor_levels.append([min(dic_factors[name]), max(dic_factors[name])])

    # This for loop will run through each combination(technically product) and build up
    # the dataframe df with each loop.
    for run in itertools.product(*factor_levels, repeat=1):
        run = list(run)
        s_add = pd.Series(run)
        df = pd.concat([df, s_add], axis=1, ignore_index=True)
    # The dataframe is made with the runs being the columns, we want them to be the rows
    # hence the need to transpose.
    df = df.transpose()
    # The column headers are initially labelled '0','1','2' etc.., the line below
    # renames them by relating them to the factor_names list made earlier
    df = df.rename(columns=lambda x: factor_names[x])
    return df


def full_factorial(dic_factors):
    """
    Creates a full factorial design from the dictionary of factors, but does not choose
    highest and lowest levels of each factor.

    Parameters:
        dic_factors: The dictionary of factors to be included in the full factorial's design

    Returns:
        df: A dataframe of the full factorial resulting from the factors entered

    Example:
        >>> import design
        >>> Factors = {'Height':[1.6,1.8,2],'Width':[0.2,0.3,0.4]}
        >>> design.Factorial.full_factorial(Factors)
            Height  Width
        0     1.6    0.2
        1     1.6    0.3
        2     1.6    0.4
        3     1.8    0.2
        4     1.8    0.3
        5     1.8    0.4
        6     2.0    0.2
        7     2.0    0.3
        8     2.0    0.4
    """
    # The variables initialised below play the same role here as in the two level
    # full factorial above.
    df = pd.DataFrame()
    factor_levels = []
    factor_names = []
    # This for loop plays the same role as the for loop in the two level
    # but does not take the maximum and minimum factor levels, so does not reduce
    # the design to a two level design automatically.
    for name in dic_factors:
        factor_names.append(name)
        factor_levels.append(dic_factors[name])

    # This for loop functions the same as its two level counterpart.
    for run in itertools.product(*factor_levels, repeat=1):
        run = list(run)
        s_add = pd.Series(run)
        df = pd.concat([df, s_add], axis=1, ignore_index=True)
    # As in the two level, the dataframe must be transposed and renamed.
    df = df.transpose()
    df = df.rename(columns=lambda x: factor_names[x])
    return df


def frac_fact_2level(dic_factors, runs):
    """
    Returns a fractional factorial based on the dictionary of factors entered and the runs entered,
     the number of runs of the design will be the next lowest power of 2 from the runs entered
     i.e 9->8, 8->8

    Parameters:
        dic_factors: The dictionary of factors to be included in the fractional factorial's design.

        runs: The number of runs the design can use - if the number of runs causes the design's resolution
        to be less than three then it will not work.

    returns:
        df: A dataframe of the runs for the fractional factorial resulting from the factors and runs entered.

    Example:
        >>> import design
        >>> Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3],'Temp':[10,20],'Pressure':[100,200]}
        >>> design.Factorial.frac_fact_2level(Factors,10)
            Height  Width  Depth  Temp  Pressure
        0     1.6    0.2    0.2    20       200
        1     1.6    0.2    0.3    20       100
        2     1.6    0.4    0.2    10       200
        3     1.6    0.4    0.3    10       100
        4     2.0    0.2    0.2    10       100
        5     2.0    0.2    0.3    10       200
        6     2.0    0.4    0.2    20       100
        7     2.0    0.4    0.3    20       200
    """
    df = pd.DataFrame()
    factor_levels = []
    factor_names = []
    # this for loop fills up factor_levels and factor_names arrays
    for name in dic_factors:
        factor_names.append(name)
        factor_levels.append([min(dic_factors[name]), max(dic_factors[name])])

    # If runs entered isn't a power of 2 this will set it to the
    # next lowest power of 2.
    runs = int((1 << (runs).bit_length()) / 2)
    # The fractional factorial is generated from a base full factorial
    # see https://www.itl.nist.gov/div898/handbook/pri/section3/pri3342.htm
    # the line below determines the level of this full fact level
    full_fact_level = int(math.log(runs, 2))

    # This for loop creates the base Full Factorial from which the
    # fractional factorial will be generated
    for run in itertools.product([-1, 1], repeat=full_fact_level):
        run = list(run)
        s_add = pd.Series(run)
        df = pd.concat([df, s_add], axis=1, ignore_index=True)
    df = df.transpose()
    # factors_remaining will be used in the coming loops - it measures how many columns
    # are left to be added to the fractional factorial.
    factors_remaining = len(factor_names) - full_fact_level
    # count will be used for the creation of new columns in the dataframe.
    count = 0
    # df_cols is quite literally a list of the column headers in the dataframe
    # the columns are automatically name as if in an array 0,1,2 etc..
    df_cols = []
    # r is used in the itertools combination function, it is set to two as
    # the first columns of the fractional factorial are the two combinations,
    # it is incremented as higher combinations are required.
    r = 2
    # r will need to be incremented when all combinations at its current level have been
    # added, combination check is used in a conditional that will increase r and
    # reinitialise the for loop that r is used in.
    combination_check = 0

    # This for loop fills up df_cols with the columns already made in the base full factorial
    for x in range((len(dic_factors) - factors_remaining)):
        df_cols.append(x)

    # The while loop is here to reinitialise the for loop once r has changed, and
    # to stop the for loop creating too many columns once factors_remaining is 0.
    while factors_remaining > 0:
        # As each new column is the combination of columns from the base full factorial
        # this for loop goes through each combination and creates these columns.
        for combination in itertools.combinations(df_cols, r):
            # We initialise the values as 1 so that we can multiply them by however much
            # is necessary in the coming for loop.
            df[full_fact_level + count] = 1

            # The for loop here goes up to r because if r is two the result will be the multiplication
            # of two columns, if r is three, three columns etc..
            for i in range(r):
                df[full_fact_level + count] = df[full_fact_level + count] * df[combination[i]]
            count += 1
            factors_remaining -= 1
            combination_check += 1

            # If we have run through all combinations with this 'r' value
            # we should increase r.
            if combination_check == len(list(itertools.combinations(df_cols, r))):
                r += 1
                combination_check = 0
                break
            # If there are no factors left then we should stop adding columns.
            if factors_remaining == 0:
                break

    # The dataframe is currently -1 and 1, this for loop assigns the right levels to
    # each factor using the factor_levels list
    for i in range(len(dic_factors)):
        df[i] = df[i].apply(lambda y: factor_levels[i][0] if y == -1 else factor_levels[i][1])
    df = df.rename(columns=lambda y: factor_names[y])
    return df


def plackett_burman(dic_factors, runs):
    """
    Returns a Plackett-Burman design where the number of runs is the next multiple of four
    higher than the number of runs entered if the runs given isn't a multiple of four.

    """
    # Plackett-Burman designs are made using hadamard matrices
    # the hadamard matrices are taken in via an online library
    factor_names = []
    factor_levels = []
    # this for loop fills up factor_levels and factor_names arrays
    for name in dic_factors:
        factor_names.append(name)
        factor_levels.append([min(dic_factors[name]), max(dic_factors[name])])
    # The links to the various URLs of the hadamard matrices are stored in this dictionary
    url_dictionary = {8: "http://neilsloane.com/hadamard/had.8.txt",
                      12: "http://neilsloane.com/hadamard/had.12.txt",
                      16: "http://neilsloane.com/hadamard/had.16.0.txt",
                      20: "http://neilsloane.com/hadamard/had.20.hall.n.txt",
                      24: "http://neilsloane.com/hadamard/had.24.pal.txt",
                      28: "http://neilsloane.com/hadamard/had.28.pal2.txt",
                      32: "http://neilsloane.com/hadamard/had.32.pal.txt"}
    # Conditional changes run number to be a multiple of four
    if runs % 4 != 0:
        runs = runs + (4 - (runs % 4))

    file = urllib.request.urlopen(url_dictionary.get(runs))
    array = []
    # This for loop takes the lines of the hadamard matrices and places them into the array variable
    for line in file:
        # decoded_line stores each line in a way that can be interacted with
        decoded_line = line.decode("utf-8")
        # Conditional breaks the for loop when the table has been read completely
        if decoded_line[0] == 'H':
            break
        # The array is appended with the current row of the table, excluding the new line
        array.append(list(decoded_line.split('\n')[0]))
    # Array is currently a square, so only the columns are taken that are needed for the number of factors entered
    df = pd.DataFrame(array[(runs - len(dic_factors)):])
    df = df.transpose()
    # The dataframe is currently '+' and '-' so this for loop converts to the factor levels entered in the dictionary
    for i in range(len(dic_factors)):
        df[i] = df[i].apply(lambda y: factor_levels[i][0] if y == '-' else factor_levels[i][1])
    df = df.rename(columns=lambda y: factor_names[y])
    return df


def box_behnken(dic_factors):
    """
    Creates a dataframe for a Box-Behken experimental design based on the factors given.

    Parameters:
        dic_factors: The dictionary of factors to be included in the Box-Behnken design.

    Returns:
        df: The dataframe containing the Box-Behnken design.

    Examples:
        >>> import design
        >>> Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3],'Temp':[10,20],'Pressure':[100,200]}
        >>> design.box_behnken(Factors)
            Height  Width  Depth  Temp  Pressure
        0      1.6    0.2   0.25  15.0     150.0
        1      1.6    0.4   0.25  15.0     150.0
        2      1.6    0.3   0.20  15.0     150.0
        3      1.6    0.3   0.30  15.0     150.0
        4      1.6    0.3   0.25  10.0     150.0
        5      1.6    0.3   0.25  20.0     150.0
        6      1.6    0.3   0.25  15.0     100.0
        7      1.6    0.3   0.25  15.0     200.0
        8      2.0    0.2   0.25  15.0     150.0
        9      2.0    0.4   0.25  15.0     150.0
        10     2.0    0.3   0.20  15.0     150.0
        11     2.0    0.3   0.30  15.0     150.0
        12     2.0    0.3   0.25  10.0     150.0
        13     2.0    0.3   0.25  20.0     150.0
        14     2.0    0.3   0.25  15.0     100.0
        15     2.0    0.3   0.25  15.0     200.0
        16     1.8    0.2   0.20  15.0     150.0
        17     1.8    0.2   0.30  15.0     150.0
        18     1.8    0.2   0.25  10.0     150.0
        19     1.8    0.2   0.25  20.0     150.0
        20     1.8    0.2   0.25  15.0     100.0
        21     1.8    0.2   0.25  15.0     200.0
        22     1.8    0.4   0.20  15.0     150.0
        23     1.8    0.4   0.30  15.0     150.0
        24     1.8    0.4   0.25  10.0     150.0
        25     1.8    0.4   0.25  20.0     150.0
        26     1.8    0.4   0.25  15.0     100.0
        27     1.8    0.4   0.25  15.0     200.0
        28     1.8    0.3   0.20  10.0     150.0
        29     1.8    0.3   0.20  20.0     150.0
        30     1.8    0.3   0.20  15.0     100.0
        31     1.8    0.3   0.20  15.0     200.0
        32     1.8    0.3   0.30  10.0     150.0
        33     1.8    0.3   0.30  20.0     150.0
        34     1.8    0.3   0.30  15.0     100.0
        35     1.8    0.3   0.30  15.0     200.0
        36     1.8    0.3   0.25  10.0     100.0
        37     1.8    0.3   0.25  10.0     200.0
        38     1.8    0.3   0.25  20.0     100.0
        39     1.8    0.3   0.25  20.0     200.0
        40     1.8    0.3   0.25  15.0     150.0
        41     1.8    0.3   0.25  15.0     150.0
        42     1.8    0.3   0.25  15.0     150.0
        43     1.8    0.3   0.25  15.0     150.0
        44     1.8    0.3   0.25  15.0     150.0
    """
    df = pd.DataFrame()
    factor_levels = []
    factor_names = []
    # this for loop fills up factor_levels and factor_names arrays
    for name in dic_factors:
        factor_names.append(name)
        # This conditional creates a middle factor by averaging the two highest and lowest when too many
        # or too few levels are given, else sorts the three given and sets the levels that way
        if len(dic_factors[name]) != 3:
            factor_levels.append(
                [min(dic_factors[name]), (min(dic_factors[name]) + max(dic_factors[name])) / 2, max(dic_factors[name])])
        else:
            factor_levels.append(
                [sorted(dic_factors[name])[0], sorted(dic_factors[name])[1], sorted(dic_factors[name])[2]])
    # This for loop will go through too many iterations, generating +1,+1,+1 designs which aren't needed,
    # so a conditional is added to cut it down
    for run in itertools.product([-1, 1, 0], repeat=len(dic_factors)):
        run = list(run)
        if run.count(1) < 3 and run.count(-1) < 3 and run.count(0) == len(dic_factors) - 2:
            s_add = pd.Series(run)
            df = pd.concat([df, s_add], axis=1, ignore_index=True)
    # for loop adds default centre runs
    for i in range(len(dic_factors)):
        centre_points = [0,0,0,0,0]
        df = pd.concat([df, pd.Series(centre_points[:len(dic_factors)])], axis=1, ignore_index=True)
    df = df.transpose()
    # for loop takes the -1, 0, +1 to the corresponding three factor levels for each factor
    for i in range(len(dic_factors)):
        df[i] = df[i].apply(
            lambda y: factor_levels[i][0] if y == -1 else (factor_levels[i][1] if y == 0 else factor_levels[i][2]))
    df = df.rename(columns=lambda y: factor_names[y])
    return df


def central_composite(dic_factors):
    """
    Creates a Central Composite design for the factors given

    Parameters:
        dic_factors: The dictionary of factors to be included in the Central Composite design.

    Returns:
        df: The dataframe containing the Central Composite design.

    Examples:
        >>> import design
        >>> Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3],'Temp':[10,20],'Pressure':[100,200]}
        >>> design.central_composite(Factors)
            Height     Width     Depth       Temp    Pressure
        0   1.600000  0.200000  0.200000  10.000000  100.000000
        1   1.600000  0.200000  0.200000  10.000000  200.000000
        2   1.600000  0.200000  0.200000  20.000000  100.000000
        3   1.600000  0.200000  0.200000  20.000000  200.000000
        4   1.600000  0.200000  0.300000  10.000000  100.000000
        5   1.600000  0.200000  0.300000  10.000000  200.000000
        6   1.600000  0.200000  0.300000  20.000000  100.000000
        7   1.600000  0.200000  0.300000  20.000000  200.000000
        8   1.600000  0.400000  0.200000  10.000000  100.000000
        9   1.600000  0.400000  0.200000  10.000000  200.000000
        10  1.600000  0.400000  0.200000  20.000000  100.000000
        11  1.600000  0.400000  0.200000  20.000000  200.000000
        12  1.600000  0.400000  0.300000  10.000000  100.000000
        13  1.600000  0.400000  0.300000  10.000000  200.000000
        14  1.600000  0.400000  0.300000  20.000000  100.000000
        15  1.600000  0.400000  0.300000  20.000000  200.000000
        16  2.000000  0.200000  0.200000  10.000000  100.000000
        17  2.000000  0.200000  0.200000  10.000000  200.000000
        18  2.000000  0.200000  0.200000  20.000000  100.000000
        19  2.000000  0.200000  0.200000  20.000000  200.000000
        20  2.000000  0.200000  0.300000  10.000000  100.000000
        21  2.000000  0.200000  0.300000  10.000000  200.000000
        22  2.000000  0.200000  0.300000  20.000000  100.000000
        23  2.000000  0.200000  0.300000  20.000000  200.000000
        24  2.000000  0.400000  0.200000  10.000000  100.000000
        25  2.000000  0.400000  0.200000  10.000000  200.000000
        26  2.000000  0.400000  0.200000  20.000000  100.000000
        27  2.000000  0.400000  0.200000  20.000000  200.000000
        28  2.000000  0.400000  0.300000  10.000000  100.000000
        29  2.000000  0.400000  0.300000  10.000000  200.000000
        30  2.000000  0.400000  0.300000  20.000000  100.000000
        31  2.000000  0.400000  0.300000  20.000000  200.000000
        32  2.275683  0.300000  0.250000  15.000000  150.000000
        33  1.324317  0.300000  0.250000  15.000000  150.000000
        34  1.800000  0.537841  0.250000  15.000000  150.000000
        35  1.800000  0.062159  0.250000  15.000000  150.000000
        36  1.800000  0.300000  0.368921  15.000000  150.000000
        37  1.800000  0.300000  0.131079  15.000000  150.000000
        38  1.800000  0.300000  0.250000  26.892071  150.000000
        39  1.800000  0.300000  0.250000   3.107929  150.000000
        40  1.800000  0.300000  0.250000  15.000000  268.920712
        41  1.800000  0.300000  0.250000  15.000000   31.079288
        42  1.800000  0.300000  0.250000  15.000000  150.000000
        43  1.800000  0.300000  0.250000  15.000000  150.000000
        44  1.800000  0.300000  0.250000  15.000000  150.000000
        45  1.800000  0.300000  0.250000  15.000000  150.000000
        46  1.800000  0.300000  0.250000  15.000000  150.000000
    """
    df2 = pd.DataFrame()  # df2 will contain the axial points of the design
    factor_levels = []
    factor_names = []
    alpha = 2 ** (len(dic_factors) / 4)  # this is alpha for rotatability, alpha should eventually be optional
    # this for loop fills up factor_levels and factor_names arrays
    for name in dic_factors:
        factor_names.append(name)
        # This conditional creates a middle factor by averaging the two highest and lowest when too many
        # or too few levels are given, else sorts the three given and sets the levels that way
        if len(dic_factors[name]) != 3:
            factor_levels.append(
                [min(dic_factors[name]), (min(dic_factors[name]) + max(dic_factors[name])) / 2, max(dic_factors[name])])
        else:
            factor_levels.append(
                [sorted(dic_factors[name])[0], sorted(dic_factors[name])[1], sorted(dic_factors[name])[2]])
    # The full factorial design points are made using the full factorial function
    df1 = full_factorial_2level(dic_factors)
    # This for loop creates the dataframe of the axial points
    for i in range(len(dic_factors)):
        run1 = []
        run2 = []
        # extremeplus and extrememinus contain the values for the extreme points of the design
        extremeplus = factor_levels[i][1] + ((factor_levels[i][2] - factor_levels[i][1]) * alpha)
        extrememinus = factor_levels[i][1] - ((factor_levels[i][2] - factor_levels[i][1]) * alpha)
        # This for loop fills up the runs with the centre points for all factors
        for j in range(len(dic_factors)):
            run1.append(factor_levels[j][1])
            run2.append(factor_levels[j][1])
        # run1 and run2 have the extreme points entered in, replacing the centre point they will currently have
        run1[i] = extremeplus
        run2[i] = extrememinus
        # The runs are stored as series to be concatenated to the dataframe
        s_add1 = pd.Series(run1)
        s_add2 = pd.Series(run2)
        df2 = pd.concat([df2, s_add1, s_add2], axis=1, ignore_index=True)
    # The axial dataframe is then transposed and renamed so it can be concated with the full factorial dataframe
    df2 = df2.transpose()
    df2 = df2.rename(columns=lambda y: factor_names[y])
    df = pd.concat([df1, df2], axis=0, ignore_index=True)
    # This for loop adds as many centre points as there are factors entered
    centre_points = []
    for i in range(len(dic_factors)):
        centre_points.append(factor_levels[i][1])
    for j in range(len(dic_factors)):
        df3 = pd.DataFrame([centre_points],columns=list(dic_factors))
        df = df.append(df3,ignore_index=True)
    return df


def latin_hypercube(dic_factors, runs):
    """
    Parameters:
        dic_factors: The dictionary of factors to be included in the Latin Hypercube design.

        runs: The number of runs to be used in the design.

    Returns:
        df: The dataframe containing the Latin Hypercube design.

    Example:
        >>> import design
        >>> Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3],'Temp':[10,20],'Pressure':[100,200]}
        >>> design.latin_hypercube(Factors,50)
              Height     Width     Depth       Temp    Pressure
        0   1.814372  0.316126  0.203734  12.633408  150.994350
        1   1.683852  0.327745  0.221157  10.833524  149.235694
        2   1.952938  0.220208  0.212877  14.207334  177.737810
        3   1.921001  0.306165  0.249451  13.747280  195.141219
        4   1.709485  0.286836  0.214973  12.132761  144.060774
        5   1.795442  0.339484  0.263747  16.494926  105.861897
        6   1.849604  0.390856  0.229801  17.768834  157.379054
        7   1.635933  0.295207  0.244843  15.561134  119.353027
        8   1.800514  0.257358  0.232554  19.117071  114.431350
        9   1.748656  0.311259  0.209185  19.573654  147.317771
        10  1.610152  0.200320  0.269825  14.041168  192.787729
        11  1.670380  0.283579  0.270421  11.422384  161.302466
        12  1.914483  0.374190  0.273246  15.253950  110.213186
        13  1.731642  0.363269  0.211263  15.011417  175.315691
        14  1.864093  0.245809  0.235466  10.506234  123.998827
        15  1.856580  0.314574  0.260263  11.787321  152.096424
        16  1.651140  0.262106  0.289432  14.407869  121.954348
        17  1.827840  0.278926  0.223818  12.824422  168.813816
        18  1.780800  0.380327  0.252359  12.290440  171.741507
        19  1.762333  0.224241  0.216475  18.386775  165.564771
        20  1.949560  0.300988  0.285943  10.063231  155.134033
        21  1.646881  0.248638  0.250362  16.701447  163.476898
        22  1.974239  0.379487  0.279709  17.208315  181.757031
        23  1.904317  0.216877  0.292985  18.829669  136.808281
        24  1.899844  0.343903  0.230494  13.197326  198.654066
        25  1.696839  0.329348  0.283741  18.193024  135.335187
        26  1.689936  0.272728  0.218891  19.800988  131.615692
        27  1.823893  0.299159  0.247030  10.790362  191.524570
        28  1.841140  0.210635  0.286718  10.327824  167.595627
        29  1.883991  0.385993  0.277186  18.773584  178.871167
        30  1.932945  0.358221  0.294327  16.890948  125.635668
        31  1.837620  0.370877  0.242782  17.103119  142.240418
        32  1.740477  0.352914  0.265939  14.697769  129.088978
        33  1.624078  0.347985  0.298516  13.933373  132.011517
        34  1.786612  0.351899  0.225313  15.827930  188.649172
        35  1.892142  0.206601  0.254650  14.805995  138.732923
        36  1.656703  0.252798  0.205547  18.461586  184.792345
        37  1.770805  0.270721  0.226262  11.940936  113.390934
        38  1.672266  0.288289  0.275940  15.640371  186.777116
        39  1.600629  0.240123  0.280908  17.934686  126.897387
        40  1.995175  0.237031  0.240472  16.393982  116.475088
        41  1.713062  0.265850  0.256147  17.418780  172.746504
        42  1.964540  0.235473  0.266340  11.334520  196.454539
        43  1.757516  0.366909  0.207040  13.488750  102.146392
        44  1.942405  0.214971  0.290674  13.373628  109.206897
        45  1.985601  0.229702  0.297658  12.435430  101.336426
        46  1.617340  0.321384  0.200862  19.338525  159.238981
        47  1.976837  0.393484  0.258497  16.167623  140.926988
        48  1.877091  0.399951  0.239234  19.788923  182.759572
        49  1.725652  0.332160  0.237414  11.136650  107.726667
    """
    df = pd.DataFrame()
    factor_names = []
    count = 0
    # Creates an array filled with a latin hypercube form 0 to 1
    array = lhsmdu.sample(len(dic_factors), runs)
    # This for loop converts the latin hypercube to have the levels entered into the dictionary of factors
    for name in dic_factors:
        factor_names.append(name)
        low = min(dic_factors[name])
        high = max(dic_factors[name])
        # non_coded stored the array being mapped to fit the levels of the factors entered
        non_coded = np.array(list(map(lambda x: low + ((high - low) * x), array[count])))
        # Converts non_coded (which is currently one column of the final dataframe) to a series
        s_add = pd.Series(non_coded[0][0])
        count += 1
        # Adds the series to the dataframe
        df = pd.concat([df, s_add], ignore_index=True, axis=1)
    df = df.rename(columns=lambda y: factor_names[y])
    return df