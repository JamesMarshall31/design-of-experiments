# Our Design of experiment class

import numpy as np
import pandas as pd
import itertools

class Factorial():
    def full_factorial(dic_factors):
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

