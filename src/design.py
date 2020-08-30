# Our Design of experiment class


import numpy as np
import pandas as pd
import itertools
import math

class Factorial():
    def full_factorial_2level(dic_factors):
        """
        Creates a Two-level full factorial design, from the dictionary of Factors entered

        example:

        Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3]}
        doe_class.Factorial.full_factorial(Factors)

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
        df = pd.DataFrame()
        factor_levels = []
        factor_names = []
        for name in dic_factors:
            factor_names.append(name)
            factor_levels.append([min(dic_factors[name]),max(dic_factors[name])])
        runs = int((1<<(runs-1).bit_length())/2) # if runs entered isn't a power of 2 this this will set it to the
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
