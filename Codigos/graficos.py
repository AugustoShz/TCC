from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats

plt.rcParams.update({'font.size': 18})

df_dataset_processed_data = pd.read_csv('..\DatasetsTratados\processed_data.csv', sep=',', index_col=None)
df_dataset_processed_vacinacao = pd.read_csv('..\DatasetsTratados\processed_vacinacao.csv', sep=',', index_col=None)
df_dataset_filtered_by_vacinacao_date_data = pd.read_csv('..\DatasetsTratados/filtered_by_vaccination_dates_data.csv', sep=',', index_col=None)

# df_worldwide = df_dataset_processed_data.loc[df_dataset_processed_data['ISO3'] == 'BRA']
df_worldwide = df_dataset_processed_data.loc[df_dataset_processed_data['ISO3'] == 'WWW']
df_worldwide_after_vaccine = df_dataset_filtered_by_vacinacao_date_data.loc[df_dataset_filtered_by_vacinacao_date_data['ISO3'] == 'WWW']

df_country = df_dataset_processed_data.loc[df_dataset_processed_data['ISO3'] == 'BRA']
df_country_after_vaccine = df_dataset_filtered_by_vacinacao_date_data.loc[df_dataset_filtered_by_vacinacao_date_data['ISO3'] == 'BRA']

df_filtered = df_dataset_processed_vacinacao.loc[df_dataset_processed_vacinacao['iso_code'] == 'WWW']

x=np.array(df_worldwide["Updated"])
yTotalConfirmed=np.array(df_worldwide["Confirmed"])
yTotalDeaths=np.array(df_worldwide["Deaths"])
yTotalRecovered=np.array(df_worldwide["Recovered"])

yAfterVaccineConfirmed=np.array(df_worldwide["Confirmed"])
yAfterVaccineDeaths=np.array(df_worldwide["Deaths"])
yAfterVaccineRecovered=np.array(df_worldwide["Recovered"])

xVacinacao = np.array(df_filtered['date'])
yVacinacao = np.array(df_filtered['total_vaccinations'])

# plt.plot(x, yTotalConfirmed, color='red', label='Confirmados')
# plt.plot(x, yTotalDeaths, color='black', label="Mortes")
# plt.plot(x, yTotalRecovered, color='green',label="Recuperados")

# plt.legend()
# plt.title("Gráfico de mortes - Mudial")
# plt.xlabel("Data de atualização")
# plt.ylabel("Quantidade")
# plt.xticks(range(0,len(x),len(x)//8))
# plt.show()

def formatDate(date):
  formated = pd.to_datetime(date, format='%Y-%m-%d')
  return formated

start_date = pd.to_datetime(df_dataset_processed_data['Updated'].min()) + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1)
end_date = pd.to_datetime(df_dataset_processed_data['Updated'].max()) + pd.offsets.MonthEnd(0)

#pd.DateOffset(months=13)


month_offset = 1

df_worldwide['Updated'] = df_worldwide['Updated'].apply(formatDate)
df_country['Updated'] = df_country['Updated'].apply(formatDate)
df_ksvalues_confirmed_recovered = []
df_ksvalues_deaths_recovered = []
df_ksvalues_deaths_confirmed = []

while(start_date + pd.DateOffset(months=month_offset) <= end_date):
  x = start_date + pd.DateOffset(months=month_offset)
  y = start_date + pd.DateOffset(months=(month_offset+1))

  start_range = df_worldwide['Updated'] >= x
  end_range = df_worldwide['Updated'] < y
  between_range = start_range & end_range
  df_filtered_dates_worldwide = df_worldwide.loc[between_range]
  
  start_range = df_country['Updated'] >= x
  end_range = df_country['Updated'] < y
  between_range = start_range & end_range
  df_filtered_dates_country = df_country.loc[between_range]
  
  yFilteredByDateConfirmedWorldwide=np.array(df_filtered_dates_worldwide["Confirmed"])
  yFilteredByDateDeathsWorldwide=np.array(df_filtered_dates_worldwide["Deaths"])
  yFilteredByDateRecoveredWorldwide=np.array(df_filtered_dates_worldwide["Recovered"])
  
  yFilteredByDateConfirmedCountry=np.array(df_filtered_dates_country["Confirmed"])
  yFilteredByDateDeathsCountry=np.array(df_filtered_dates_country["Deaths"])
  yFilteredByDateRecoveredCountry=np.array(df_filtered_dates_country["Recovered"])


  integralConfirmedWorldwide = np.trapz(yFilteredByDateConfirmedWorldwide, dx=5)
  integralRecoveredWorldwide = np.trapz(yFilteredByDateRecoveredWorldwide, dx=5)
  integralDeathsWorldwide = np.trapz(yFilteredByDateDeathsWorldwide, dx=5)

  integralConfirmedCountry = np.trapz(yFilteredByDateConfirmedCountry, dx=5)
  integralRecoveredCountry = np.trapz(yFilteredByDateRecoveredCountry, dx=5)
  integralDeathsCountry = np.trapz(yFilteredByDateDeathsCountry, dx=5)

  ks_stat_confirmed_recovered, ks_p_value_confirmed_recovered = stats.ks_2samp(yFilteredByDateRecoveredWorldwide, yFilteredByDateConfirmedWorldwide)
  df_ksvalues_confirmed_recovered.append({
    'month': x,
    'stat': ks_stat_confirmed_recovered, 
    'p': ks_p_value_confirmed_recovered,
    'maxDiff':  max(yFilteredByDateConfirmedWorldwide - yFilteredByDateRecoveredWorldwide),
    'integral': integralConfirmedCountry - integralRecoveredCountry,
    'integralPercentage': min(integralRecoveredCountry / integralConfirmedCountry, 1),
    'countryAndWorldDiff': (integralConfirmedWorldwide - integralRecoveredWorldwide) - (integralConfirmedCountry - integralRecoveredCountry)
  })

  ks_stat_deaths_recovered, ks_p_value_deaths_recovered = stats.ks_2samp(yFilteredByDateRecoveredWorldwide, yFilteredByDateDeathsWorldwide)
  df_ksvalues_deaths_recovered.append({
    'month': x, 
    'stat': ks_stat_deaths_recovered, 
    'p': ks_p_value_deaths_recovered,
    'maxDiff':  max(yFilteredByDateRecoveredWorldwide - yFilteredByDateDeathsWorldwide),
    'integral': integralRecoveredCountry - integralDeathsCountry,
    'integralPercentage':  min(integralDeathsCountry / integralRecoveredCountry, 1),
    'countryAndWorldDiff': (integralRecoveredWorldwide - integralDeathsWorldwide) - (integralRecoveredCountry - integralDeathsCountry)
  })

  print(integralConfirmedWorldwide, integralDeathsWorldwide)

  ks_stat_deaths_confirmed, ks_p_value_deaths_confirmed = stats.ks_2samp(yFilteredByDateConfirmedWorldwide, yFilteredByDateDeathsWorldwide)
  df_ksvalues_deaths_confirmed.append({
    'month': x, 
    'stat': ks_stat_deaths_confirmed, 
    'p': ks_p_value_deaths_confirmed,
    'maxDiff':  max(yFilteredByDateConfirmedWorldwide - yFilteredByDateDeathsWorldwide),
    'integral': integralConfirmedCountry - integralDeathsCountry,
    'integralPercentage':  min(integralDeathsCountry / integralConfirmedCountry, 1),
    'countryAndWorldDiff': (integralConfirmedWorldwide - integralDeathsWorldwide) - (integralConfirmedCountry - integralDeathsCountry)
  })
  
  month_offset+=1

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


# plt.plot(df_ksvalues_confirmed_recovered['month'], df_ksvalues_confirmed_recovered['stat'], color='blue', label='stat')
# plt.plot(df_ksvalues_deaths_recovered['month'], df_ksvalues_deaths_recovered['stat'], color='blue', label='stat')
# plt.plot(df_ksvalues_deaths_confirmed['month'], df_ksvalues_deaths_confirmed['stat'], color='blue', label='stat')

plt.legend()
plt.title("Diferença de integrais em porcentagem - Argentina")
plt.xlabel("Data de atualização")
plt.ylabel("Quantidade")
plt.xticks(rotation='horizontal')
plt.show()

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

