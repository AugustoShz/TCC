from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats

df_dataset_processed_data = pd.read_csv('..\DatasetsTratados\processed_data.csv', sep=',', index_col=None)
df_dataset_processed_vacinacao = pd.read_csv('..\DatasetsTratados\processed_vacinacao.csv', sep=',', index_col=None)
df_dataset_filtered_by_vacinacao_date_data = pd.read_csv('..\DatasetsTratados/filtered_by_vaccination_dates_data.csv', sep=',', index_col=None)

# df_worldwide = df_dataset_processed_data.loc[df_dataset_processed_data['ISO3'] == 'BRA']
df_worldwide = df_dataset_processed_data.loc[df_dataset_processed_data['ISO3'] == 'BRA']
df_worldwide_after_vaccine = df_dataset_filtered_by_vacinacao_date_data.loc[df_dataset_filtered_by_vacinacao_date_data['ISO3'] == 'BRA']

df_filtered = df_dataset_processed_vacinacao.loc[df_dataset_processed_vacinacao['iso_code'] == 'BRA']

x=np.array(df_worldwide["Updated"])
yTotalConfirmed=np.array(df_worldwide["Confirmed"])
yTotalDeaths=np.array(df_worldwide["Deaths"])
yTotalRecovered=np.array(df_worldwide["Recovered"])

yAfterVaccineConfirmed=np.array(df_worldwide["Confirmed"])
yAfterVaccineDeaths=np.array(df_worldwide["Deaths"])
yAfterVaccineRecovered=np.array(df_worldwide["Recovered"])

xVacinacao = np.array(df_filtered['date'])
yVacinacao = np.array(df_filtered['total_vaccinations'])

# plt.plot(x, yConfirmed, color='red', label='Casos Confirmados')
# plt.plot(x, yDeaths, color='black', label="Mortes")
# plt.plot(x, yRecovered, color='green',label="Recuperados")

# plt.plot(xVacinacao, yVacinacao, color = 'orange', label='Total de vacinações')

# plt.legend()
# plt.title("Casos Totais")
# plt.xlabel("Data de atualização")
# plt.ylabel("Quantidade")
# plt.xticks(range(0,301,30))
# plt.show()
def formatDate(date):
  formated = pd.to_datetime(date, format='%Y-%m-%d')
  return formated

start_date = pd.to_datetime(df_dataset_processed_data['Updated'].min()) + pd.offsets.MonthEnd(0) - pd.offsets.MonthBegin(1)
end_date = pd.to_datetime(df_dataset_processed_data['Updated'].max()) + pd.offsets.MonthEnd(0)

#pd.DateOffset(months=13)


month_offset = 0

df_dataset_processed_data['Updated'] = df_dataset_processed_data['Updated'].apply(formatDate)
df_ksvalues_confirmed_recovered = []
df_ksvalues_deaths_recovered = []

while(start_date + pd.DateOffset(months=month_offset) <= end_date):

  x = start_date + pd.DateOffset(months=month_offset)
  y = start_date + pd.DateOffset(months=(month_offset+1))
  
  start_range = df_dataset_processed_data['Updated'] >= x
  end_range = df_dataset_processed_data['Updated'] < y
  between_range = start_range & end_range
  df_filtered_dates = df_dataset_processed_data.loc[between_range]
  
  yFilteredByDateConfirmed=np.array(df_filtered_dates["Confirmed"])
  yFilteredByDateDeaths=np.array(df_filtered_dates["Deaths"])
  yFilteredByDateRecovered=np.array(df_filtered_dates["Recovered"])

  ks_stat_confirmed_recovered, ks_p_value_confirmed_recovered = stats.ks_2samp(yFilteredByDateRecovered, yFilteredByDateConfirmed)
  df_ksvalues_confirmed_recovered.append({
    'month': x, 
    'stat': ks_stat_confirmed_recovered, 
    'p': ks_p_value_confirmed_recovered
  })

  ks_stat_deaths_recovered, ks_p_value_deaths_recovered = stats.ks_2samp(yFilteredByDateRecovered, yFilteredByDateDeaths)
  df_ksvalues_deaths_recovered.append({
    'month': x, 
    'stat': ks_stat_deaths_recovered, 
    'p': ks_p_value_deaths_recovered
  })
  
  month_offset+=1

df_ksvalues_confirmed_recovered = pd.DataFrame(df_ksvalues_confirmed_recovered)
df_ksvalues_deaths_recovered = pd.DataFrame(df_ksvalues_deaths_recovered)

print(df_ksvalues_confirmed_recovered)
print(df_ksvalues_deaths_recovered)

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

