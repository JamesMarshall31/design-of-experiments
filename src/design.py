# Our Design of experiment class


import numpy as np
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
        df = pd.DataFrame()
        factor_levels =[]
        factor_names=[]

        for name in dic_factors:
            factor_names.append(name)
            factor_levels.append([min(dic_factors[name]),max(dic_factors[name])])
        for run in itertools.product(*factor_levels, repeat=1):
            run = list(run)
            s_add = pd.Series(run)
            df = pd.concat([df, s_add], axis=1, ignore_index=True)
        df = df.transpose()
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
        df = pd.DataFrame()
        factor_levels = []
        factor_names = []
        for name in dic_factors:
            factor_names.append(name)
            factor_levels.append(dic_factors[name])
        for run in itertools.product(*factor_levels, repeat=1):
            run = list(run)
            s_add = pd.Series(run)
            df = pd.concat([df, s_add], axis=1, ignore_index=True)
        df = df.transpose()
        df = df.rename(columns=lambda x: factor_names[x])
        return df

    def frac_fact_2level(dic_factors,runs):
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
            factor_levels.append([min(dic_factors[name]),max(dic_factors[name])])
        runs = int((1<<(runs).bit_length())/2) # if runs entered isn't a power of 2 this this will set it to the
        # next lowest power of 2
        full_fact_level = int(math.log(runs,2))
        for run in itertools.product([-1, 1], repeat=full_fact_level):
            run = list(run)
            s_add = pd.Series(run)
            df = pd.concat([df, s_add], axis=1, ignore_index=True)
        df = df.transpose()
        factors_remaining = len(factor_names)-full_fact_level
        count = 0
        df_cols = []
        r = 2
        combination_check = 0
        for x in range((len(dic_factors) - factors_remaining)):
            df_cols.append(x)
        while factors_remaining>0:
            for combination in itertools.combinations(df_cols, r):
                df[full_fact_level + count] = 1
                for i in range(r):
                    df[full_fact_level+count] = df[full_fact_level+count]*df[combination[i]]
                count += 1
                factors_remaining -= 1
                combination_check+=1
                if combination_check == len(list(itertools.combinations(df_cols, r))):
                    r+=1
                    combination_check=0
                    break
                if factors_remaining==0:
                    break
        # here we need to add columns to the dataframe that are the products of the other columns
        # but the columns chosen to be used will change depending on the factors that are left
        for i in range(len(dic_factors)):
            df[i] = df[i].apply(lambda x: factor_levels[i][0] if x==-1 else factor_levels[i][1])
        df = df.rename(columns=lambda x: factor_names[x])
        return df