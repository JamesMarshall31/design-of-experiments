# Our Design of experiment class

import pandas as pd
import itertools
import math


class Factorial():
    def full_factorial_2level(dic_factors):
        """
        Creates a Two-level full factorial design from the dictionary of factors entered,
        if more than two levels are given for each factor the maximum and minimum values will be selected

        Parameters:
            dic_factors: The dictionary of factors to be included in the full factorial's design

        Returns:
            df: A dataframe of the two-level full factorial resulting from the factors entered

        Example:
            >> import design
            >> Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3]}
            >> design.Factorial.full_factorial_2level(Factors)
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
            >> import design
            >> Factors = {'Height':[1.6,1.8,2],'Width':[0.2,0.3,0.4]}
            >> design.Factorial.full_factorial(Factors)
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
            >> import design
            >> Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3],'Temp':[10,20],'Pressure':[100,200]}
            >> design.Factorial.frac_fact_2level(Factors,10)
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
