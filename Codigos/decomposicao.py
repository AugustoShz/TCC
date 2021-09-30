import numpy as np
from pandas import read_csv, to_datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams

# Set figure width to 12 and height to 9
plt.rcParams['figure.figsize'] = [12, 9]

df = read_csv('..\DatasetsTratados\processed_data.csv', sep=',', index_col='Updated')
df.index = to_datetime(df.index)

df_worldwide = df.loc[df['ISO3'] == 'WWW']
series = df_worldwide['Confirmed']


result = seasonal_decompose(np.array(series), model='multiplicative', period=4)

rcParams['figure.figsize'] = 10, 5
result.plot()
plt.figure(figsize=(40,10))
plt.show()