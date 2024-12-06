import numpy as np
import polars as pl

arr = [[1, 2, 3], [4, 5, 6]]
print(arr)

data = np.array(arr)
print('\n data\n', data)
print('\n data.T\n', data.T)

df = pl.from_numpy(np.array(arr).T, 
                   # schema=["a", "b"], 
                   orient="row")
print(df)

gf = pl.DataFrame(arr, 
                  orient= 'col')
print(gf)