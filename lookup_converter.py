import pandas as pd 

a = pd.read_csv('lookup_old.txt', names=['x','y'])

a.x = a.x.astype(int)
a.y = a.y.astype(int)

a.to_csv('lookup.txt', header=False, index=False)
