from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats

plt.rcParams.update({'font.size': 18})

df_dataset_processed_data = pd.read_csv('..\DatasetsTratados\processed_data.csv', sep=',', index_col=None)
df_dataset_processed_vacinacao = pd.read_csv('..\DatasetsTratados\processed_vacinacao.csv', sep=',', index_col=None)
df_dataset_filtered_by_vacinacao_date_data = pd.read_csv('..\DatasetsTratados/filtered_by_vaccination_dates_data.csv', sep=',', index_col=None)

def formatDate(date):
  formated = pd.to_datetime(date, format='%Y-%m-%d')
  return formated

def crossDataGraphics(countryISO, title, hideConfirmed = False, hideDeaths = False, hideRecovered = False):
  countryName = ''

  if(countryISO == 'WWW'): countryName = 'Mundial'
  if(countryISO == 'BRA'): countryName = 'Brasil'
  if(countryISO == 'ARG'): countryName = 'Argentina'

  df_initial = df_dataset_processed_data.loc[df_dataset_processed_data['ISO3'] == countryISO]
  df_initial_after_vaccine = df_dataset_filtered_by_vacinacao_date_data.loc[df_dataset_filtered_by_vacinacao_date_data['ISO3'] == countryISO]
  df_filtered = df_dataset_processed_vacinacao.loc[df_dataset_processed_vacinacao['iso_code'] == countryISO]

  x=np.array(df_initial["Updated"])
  
  yTotalConfirmed=np.array(df_initial["Confirmed"])
  yTotalDeaths=np.array(df_initial["Deaths"])
  yTotalRecovered=np.array(df_initial["Recovered"])

  yAfterVaccineConfirmed=np.array(df_initial["Confirmed"])
  yAfterVaccineDeaths=np.array(df_initial["Deaths"])
  yAfterVaccineRecovered=np.array(df_initial["Recovered"])

  xVacinacao = np.array(df_filtered['date'])
  yVacinacao = np.array(df_filtered['total_vaccinations'])

  if hideConfirmed == False: plt.plot(x, yTotalConfirmed, color='red', label='Confirmados')
  if hideDeaths == False: plt.plot(x, yTotalDeaths, color='black', label="Mortes")
  if hideRecovered == False: plt.plot(x, yTotalRecovered, color='green',label="Recuperados")

  plt.legend()
  plt.title(title)
  plt.xlabel("Data de atualização")
  plt.ylabel("Quantidade")
  plt.xticks(range(0,len(x),len(x)//8))
  plt.show()

  if(not hideConfirmed and not hideDeaths and not hideRecovered):
    df_initial['Updated'] = df_initial['Updated'].apply(formatDate)
    
    df_ksvalues_confirmed_recovered = []
    df_ksvalues_deaths_recovered = []
    df_ksvalues_deaths_confirmed = []
    
    month_offset = 1

    start_date = pd.to_datetime(df_initial['Updated'].min()) + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1)
    end_date = pd.to_datetime(df_initial['Updated'].max()) + pd.offsets.MonthEnd(0)
    
    while(start_date + pd.DateOffset(months=month_offset) <= end_date):
      x = start_date + pd.DateOffset(months=month_offset)
      y = start_date + pd.DateOffset(months=(month_offset+1))

      start_range = df_initial['Updated'] >= x
      end_range = df_initial['Updated'] < y
      between_range = start_range & end_range
      df_filtered_dates_ = df_initial.loc[between_range]
      
      yFilteredByDateConfirmed=np.array(df_filtered_dates_["Confirmed"])
      yFilteredByDateDeaths=np.array(df_filtered_dates_["Deaths"])
      yFilteredByDateRecovered=np.array(df_filtered_dates_["Recovered"])

      integralConfirmed = np.trapz(yFilteredByDateConfirmed, dx=5)
      integralRecovered = np.trapz(yFilteredByDateRecovered, dx=5)
      integralDeaths = np.trapz(yFilteredByDateDeaths, dx=5)

      if(countryISO == 'ARG'): print(yFilteredByDateRecovered, yFilteredByDateConfirmed, start_date, end_date)

      ks_stat_confirmed_recovered, ks_p_value_confirmed_recovered = stats.ks_2samp(yFilteredByDateRecovered, yFilteredByDateConfirmed)
      df_ksvalues_confirmed_recovered.append({
        'month': x,
        'stat': ks_stat_confirmed_recovered, 
        'p': ks_p_value_confirmed_recovered,
        'maxDiff':  max(yFilteredByDateConfirmed - yFilteredByDateRecovered),
        'integral': integralConfirmed - integralRecovered,
        'integralPercentage': min(integralRecovered / integralConfirmed, 1),
        'countryAndWorldDiff': (integralConfirmed - integralRecovered) - (integralConfirmed - integralRecovered)
      })

      ks_stat_deaths_recovered, ks_p_value_deaths_recovered = stats.ks_2samp(yFilteredByDateRecovered, yFilteredByDateDeaths)
      df_ksvalues_deaths_recovered.append({
        'month': x, 
        'stat': ks_stat_deaths_recovered, 
        'p': ks_p_value_deaths_recovered,
        'maxDiff':  max(yFilteredByDateRecovered - yFilteredByDateDeaths),
        'integral': integralRecovered - integralDeaths,
        'integralPercentage':  min(integralDeaths / integralRecovered, 1),
        'countryAndWorldDiff': (integralRecovered - integralDeaths) - (integralRecovered - integralDeaths)
      })

      ks_stat_deaths_confirmed, ks_p_value_deaths_confirmed = stats.ks_2samp(yFilteredByDateConfirmed, yFilteredByDateDeaths)
      df_ksvalues_deaths_confirmed.append({
        'month': x, 
        'stat': ks_stat_deaths_confirmed, 
        'p': ks_p_value_deaths_confirmed,
        'maxDiff':  max(yFilteredByDateConfirmed - yFilteredByDateDeaths),
        'integral': integralConfirmed - integralDeaths,
        'integralPercentage':  min(integralDeaths / integralConfirmed, 1),
        'countryAndWorldDiff': (integralConfirmed - integralDeaths) - (integralConfirmed - integralDeaths)
      })
      
      month_offset = month_offset + 2

    teste = {}

    for i in range(len(df_ksvalues_confirmed_recovered)):
      # teste[df_ksvalues_confirmed_recovered[i]['month']]= [df_ksvalues_confirmed_recovered[i]['maxDiff'], df_ksvalues_deaths_recovered[i]['maxDiff'], df_ksvalues_deaths_confirmed[i]['maxDiff']]
      # teste[df_ksvalues_confirmed_recovered[i]['month']]= [df_ksvalues_confirmed_recovered[i]['stat'], df_ksvalues_deaths_recovered[i]['stat'], df_ksvalues_deaths_confirmed[i]['stat']]
      # teste[df_ksvalues_confirmed_recovered[i]['month']]= [df_ksvalues_confirmed_recovered[i]['integral'], df_ksvalues_deaths_recovered[i]['integral'], df_ksvalues_deaths_confirmed[i]['integral']]
      teste[df_ksvalues_confirmed_recovered[i]['month']]= [df_ksvalues_confirmed_recovered[i]['integralPercentage'], df_ksvalues_deaths_recovered[i]['integralPercentage'], df_ksvalues_deaths_confirmed[i]['integralPercentage']]
      # teste[df_ksvalues_confirmed_recovered[i]['month']]= [df_ksvalues_confirmed_recovered[i]['countryAndWorldDiff'], df_ksvalues_deaths_recovered[i]['countryAndWorldDiff'], df_ksvalues_deaths_confirmed[i]['countryAndWorldDiff']]
      
    plotdata = pd.DataFrame(teste, index = ['Confirmados x Recuperados', 'Mortes x Recuperados', 'Confirmados x Mortes'])
    plotdata.plot(kind='bar')

    df_ksvalues_confirmed_recovered = pd.DataFrame(df_ksvalues_confirmed_recovered)
    df_ksvalues_deaths_recovered = pd.DataFrame(df_ksvalues_deaths_recovered)
    df_ksvalues_deaths_confirmed = pd.DataFrame(df_ksvalues_deaths_confirmed)


    plt.plot(df_ksvalues_confirmed_recovered['month'], df_ksvalues_confirmed_recovered['stat'], color='blue', label='stat')
    # plt.plot(df_ksvalues_deaths_recovered['month'], df_ksvalues_deaths_recovered['stat'], color='blue', label='stat')
    # plt.plot(df_ksvalues_deaths_confirmed['month'], df_ksvalues_deaths_confirmed['stat'], color='blue', label='stat')

    plt.legend()
    plt.title("Diferença de integrais em porcentagem - %s" % countryName)
    plt.xlabel("Data de atualização")
    plt.ylabel("Quantidade")
    plt.xticks(rotation='horizontal')
    plt.show()
  return df_initial, df_initial_after_vaccine, df_filtered

# crossDataGraphics('BRA', 'Casos totais - Brasil')
crossDataGraphics('ARG', 'Casos totais - Argentina')
crossDataGraphics('WWW', 'Casos totais - Mundial')

# crossDataGraphics('BRA', 'Grafico de mortes - Brasil', True, False, True)
crossDataGraphics('ARG', 'Grafico de mortes - Argentina', True, False, True)
crossDataGraphics('WWW', 'Grafico de mortes - Mundial', True, False, True)





# for x in range(start_date.year, end_date.year):
#     for y in range(start_date.month, end_date.month):
#         #pegar todas as linhas de x e y
#         df_row = df_dataset_processed_data.loc()
         

# #- Calcular KS mês a mês desde o começo da pandemia (Total Casos x Recuperados);
# ks_stat_confirmed_recovered, ks_p_value_confirmed_recovered = stats.ks_2samp(yTotalRecovered, yTotalConfirmed)
# print(ks_stat_confirmed_recovered,ks_p_value_confirmed_recovered) #0.0819277108433735 0.12339296327374008

# #- Calcular KS mês a mês desde o começo da pandemia (Mortes x Recuperados);
# ks_stat_deaths_recovered, ks_p_value_deaths_recovered = stats.ks_2samp(yTotalRecovered, yTotalDeaths)
# print(ks_stat_deaths_recovered,ks_p_value_deaths_recovered) #0.7421686746987952 1.4238698481232616e-111


# #- Calcular KS no período de vacinação (Vacinados x Recuperados);
# ks_stat_vaccine_recovered, ks_p_value_vaccine_recovered = stats.ks_2samp(yAfterVaccineRecovered, yVacinacao)
# print(ks_stat_vaccine_recovered, ks_p_value_vaccine_recovered) #0.35628227194492257 2.0063008809856342e-08

# #- Calcular KS no período de vacinação (Mortes x Recuperados);
# ks_stat_deaths_recovered_adter_vaccine, ks_p_value_deaths_recovered_adter_vaccine = stats.ks_2samp(yAfterVaccineRecovered, yAfterVaccineDeaths)
# print(ks_stat_deaths_recovered_adter_vaccine,ks_p_value_deaths_recovered_adter_vaccine) #0.7421686746987952 1.4238698481232616e-111

# #- Calcular KS no período de vacinação (Vacinados x Mortes);
# ks_stat_vaccine_deaths, ks_p_value_vaccine_deaths = stats.ks_2samp(yAfterVaccineDeaths, yVacinacao)
# print(ks_stat_vaccine_deaths, ks_p_value_vaccine_deaths) #0.9166666666666666 5.742707163737219e-76

