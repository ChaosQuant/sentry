from api import *
import datetime as dt
import numpy as np
import numpy.matlib as matlib
import pandas as pd


n = 300
m = 300


index = pd.date_range(dt.datetime(1990, 1, 1), dt.datetime(1990, 1, 1) + dt.timedelta(days=m-1))
index = np.repeat(index, n)

df = pd.DataFrame(np.random.randn(n*m, 3), columns=['ROE', 'ETOP', 'closePrice'], index=index)
df['c'] = matlib.repmat(np.linspace(0, n-1, n, dtype=int), 1, m)[0]
df['sw1'] = 1
df['sw1'].iloc[0::2] = 0

t = CSTopN((LAST('ROE') - LAST('ETOP')) / LAST('closePrice'), 3, groups='sw1')

res = t.transform(df)

res[res.transformed == 1]