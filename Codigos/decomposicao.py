import numpy as np
from pandas import read_csv, to_datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from pylab import rcParams
from scipy.optimize import curve_fit

# Set figure width to 12 and height to 9
plt.rcParams['figure.figsize'] = [12, 9]

df = read_csv('../DatasetsTratados/filtered_by_vaccination_dates_data.csv', sep=',', index_col='Updated')
df.index = to_datetime(df.index)

def decompose(country, serie):
  df_worldwide = df.loc[df['ISO3'] == country]
  series = df_worldwide[serie]

  result = seasonal_decompose(np.array(series), model='multiplicative', period=4)

  rcParams['figure.figsize'] = 10, 5
  # result.plot()
  
  # plt.title('ISO3: %s - Column: %s' % (country, serie))
  # plt.show()

  return result

worlwide_confirmed = decompose('WWW', 'Confirmed')
worlwide_recovered = decompose('WWW', 'Recovered')
worlwide_deaths = decompose('WWW', 'Deaths')
country_confirmed = decompose('BRA', 'Confirmed')
country_recovered = decompose('BRA', 'Recovered')
country_deaths = decompose('BRA', 'Deaths')

def baseFuncTanh(x, a, b, c):
  return a * np.tanh(b * x) + c
  
def baseFuncSinh(x, a, b, c):
  return a * np.sinh(b * x) + c

def baseFuncLog10(x, a, b, c):
  return a * np.log(b * x) + c

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

  xdata = np.linspace(0, 1, len(data))
  popt, pcov = curve_fit(func, xdata, data, p0=[1,1,1],bounds=[1,160000000])

  print( pcov)
  print(popt)
  plt.plot(xdata, data, 'b-', label='Tendência')

  plt.plot(xdata, func(xdata, *popt), 'r-',
          label='Ajuste: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

  plt.xlabel('x')
  plt.ylabel('y')
  plt.title(title)
  plt.legend()
  plt.show()


nonLinearRegression(worlwide_confirmed.trend, baseFuncSinh, 'Função de ajuste: Seno Hiperbólico - Casos Confirmados - Mundial')
nonLinearRegression(worlwide_recovered.trend, baseFuncSinh, 'Função de ajuste: Seno Hiperbólico - Recuperados - Mundial')

nonLinearRegression(worlwide_deaths.trend, baseFuncTanh, 'Função de ajuste: Tangente Hiperbólica - Mortes - Mundial')
nonLinearRegression(country_confirmed.trend, baseFuncTanh, 'Função de ajuste: Tangente Hiperbólica - Casos Confirmados - Brasil')
nonLinearRegression(country_recovered.trend, baseFuncTanh, 'Função de ajuste: Tangente Hiperbólica - Recuperados - Brasil')
nonLinearRegression(country_deaths.trend, baseFuncTanh, 'Função de ajuste: Tangente Hiperbólica - Mortes - Brasil')