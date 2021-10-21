import numpy as np
from pandas import read_csv, to_datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams

# Set figure width to 12 and height to 9
plt.rcParams['figure.figsize'] = [12, 9]

df = read_csv('../DatasetsTratados/filtered_by_vaccination_dates_data.csv', sep=',', index_col='Updated')
df.index = to_datetime(df.index)

def decompose(country, serie):
  df_worldwide = df.loc[df['ISO3'] == country]
  series = df_worldwide[serie]

  result = seasonal_decompose(np.array(series), model='multiplicative', period=4)

  rcParams['figure.figsize'] = 10, 5
  result.plot()
  
  plt.title('ISO3: %s - Column: %s' % (country, serie))
  plt.show()

  return result

worlwide_confirmed = decompose('WWW', 'Confirmed')
worlwide_recovered = decompose('WWW', 'Recovered')
worlwide_deaths = decompose('WWW', 'Deaths')
country_confirmed = decompose('BRA', 'Confirmed')
country_recovered = decompose('BRA', 'Recovered')
country_deaths = decompose('BRA', 'Deaths')

print(worlwide_confirmed.trend)