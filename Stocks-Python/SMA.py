import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


dataslice = pd.read_csv('stock_data-GOOGL.csv')
dataslice = dataslice[(dataslice['timestamp']>'2012-11-02') & (dataslice['timestamp']<= '2019-11-04')]
# print(dataslice.head())
dataslice['SMA'] = ''
dataslice['SMA'] = dataslice.iloc[:,1].rolling(window=50).mean()
weights = np.arange(1,51)
dataslice['WMA'] = dataslice.iloc[:,1].rolling(window=50).apply(lambda wts: np.dot(wts, weights)/weights.sum(), raw=True)

print(dataslice)

plt.figure(figsize=[15,10])
plt.grid(True)
plt.plot(range(dataslice.shape[0]),dataslice['close'],label='data')
plt.plot(range(dataslice.shape[0]),dataslice['SMA'],label='SMA')
plt.plot(range(dataslice.shape[0]),dataslice['WMA'],label='WMA')

plt.xticks(range(0,dataslice.shape[0],100),dataslice['timestamp'].loc[::100],rotation=90)

plt.legend(loc=2)
plt.show()