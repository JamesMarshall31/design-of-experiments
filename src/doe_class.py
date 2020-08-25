# Our Design of experiment class

import pandas as pd
import itertools

class Factorial():
    def full_factorial(num_factors):
        df = pd.DataFrame()
        for run in itertools.product([-1, 1],repeat=num_factors)
            s_add = pd.Series(run)
            df = pd.concat([df,s_add],axis=1,ignore_index=True)
        return df.transpose()


