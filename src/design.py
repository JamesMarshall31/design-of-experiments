# Our Design of experiment class


import numpy as np
import pandas as pd
import itertools

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

        for level in dic_factors:
            factor_names.append(level)
            for x in range(len(dic_factors[level])):
                factor_levels.append(dic_factors[level][x])

        for run in itertools.product([-1, 1],repeat=len(dic_factors)):
            run = list(run)
            for i in range(len(run)):
                if run[i]==-1:
                    run[i]=factor_levels[2*i]
                else:
                    run[i]=factor_levels[2*i+1]

            s_add = pd.Series(run)
            df = pd.concat([df,s_add],axis=1,ignore_index=True)
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
