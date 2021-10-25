import numpy as np
from pandas import read_csv, to_datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams
from scipy.optimize import curve_fit

# Set figure width to 12 and height to 9
plt.rcParams['figure.figsize'] = [12, 9]

df_data = read_csv('../DatasetsTratados/processed_data.csv', sep=',', index_col='Updated')
df_data.index = to_datetime(df_data.index)

startDate =  df_data.index.min()
endDate = to_datetime('2021-10-01', format='%Y-%m-%d') # df_data.index.max()
# endDate = df_data.index.max()

df_tofilterstart = df_data.index >= startDate
df_tofilterend = df_data.index <= endDate

df_tofilter = df_tofilterstart & df_tofilterend

df_filtered = df_data.loc[df_tofilter]

minDate = df_filtered.index.min()
maxDate = df_filtered.index.max()

def decompose(df, country, serie):
  df_worldwide = df.loc[df['ISO3'] == country]
  series = df_worldwide[serie]
  
  result = seasonal_decompose(np.array(series), model='multiplicative', period=4)

  rcParams['figure.figsize'] = 10, 5
  # result.plot()
  
  # plt.title('ISO3: %s - Column: %s' % (country, serie))
  # plt.show()

  return result

worlwide_confirmed = decompose(df_filtered, 'WWW', 'Confirmed')
worlwide_recovered = decompose(df_filtered, 'WWW', 'Recovered')
worlwide_deaths = decompose(df_filtered, 'WWW', 'Deaths')
brazil_confirmed = decompose(df_filtered, 'BRA', 'Confirmed')
brazil_recovered = decompose(df_filtered, 'BRA', 'Recovered')
brazil_deaths = decompose(df_filtered, 'BRA', 'Deaths')
argentina_confirmed = decompose(df_filtered, 'ARG', 'Confirmed')
argentina_recovered = decompose(df_filtered, 'ARG', 'Recovered')
argentina_deaths = decompose(df_filtered, 'ARG', 'Deaths')

def baseFuncLog(x, a, b):
  return a * np.log(x) + b

def nonLinearRegression(data, func, title):
  for i in range(len(data)):
    if(np.isnan(data[i])):
      if(i == 0): 
        aux = data[i+1]
        aux2 = 1
        while(np.isnan(aux)): 
          aux2 = aux2+1
          aux = data[i+aux2]

        data[i] = aux
      else: data[i] = data[i-1]
      
  xdata = np.linspace(minDate.value, maxDate.value, len(data))
  print(xdata)
  
  xdataInTime = np.linspace(minDate.value, maxDate.value, len(data))
  xdataInTime = to_datetime(xdataInTime)
  teste = np.polyfit(np.log(xdata), data, 1)

  # popt, pcov = curve_fit(func, xdata, data, p0=[1,1,1],bounds=[1,160000000])

  plt.plot(xdataInTime, data, 'b-', label='Tendência')

  plt.plot(xdataInTime, func(xdata, teste[0], teste[1]), 'r-',
          label='Ajuste: a=%5.3f, b=%5.3f' % tuple(teste))

  plt.xlabel('Data de atualização')
  plt.ylabel('Quantidade')
  plt.title(title)
  plt.legend()
  plt.show()


nonLinearRegression(worlwide_confirmed.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Casos Confirmados - Mundial')
nonLinearRegression(worlwide_recovered.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Recuperados - Mundial')
nonLinearRegression(worlwide_deaths.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Mortes - Mundial')

nonLinearRegression(brazil_confirmed.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Casos Confirmados - Brasil')
nonLinearRegression(brazil_recovered.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Recuperados - Brasil')
nonLinearRegression(brazil_deaths.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Mortes - Brasil')

nonLinearRegression(argentina_confirmed.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Casos Confirmados - Argentina')
nonLinearRegression(argentina_recovered.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Recuperados - Argentina')
nonLinearRegression(argentina_deaths.trend, baseFuncLog, 'Função de ajuste: a log(x) + b - Mortes - Argentina')