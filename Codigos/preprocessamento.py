import pandas as pd
import os

df_dataset_original_vacinacao = pd.read_csv('..\Datasets\country_vaccinations.csv', sep=',', index_col=None)
df_dataset_original_data = pd.read_csv('..\Datasets\Bing-COVID19-Data.csv', sep=',', index_col=None)

#remover atributos desnecessários
df_dataset_removed_vacinacao = df_dataset_original_vacinacao.drop(['daily_vaccinations_raw', 'daily_vaccinations', 'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'daily_vaccinations_per_million', 'source_name', 'source_website'], axis = 1)
df_dataset_removed_data = df_dataset_original_data.drop(['ID','Latitude', 'Longitude', 'ISO2', 'AdminRegion1', 'AdminRegion2'], axis = 1)

#Verificar quais colunas estão vazias e zerar

values = {'total_vaccinations': 0, 'people_vaccinated': 0, 'people_fully_vaccinated': 0}
df_filled_vacinacao = df_dataset_removed_vacinacao.fillna(value=values)

# colunas = df_filled_vacinacao.isna().sum()/df_filled_vacinacao.shape[0]

values = {'ConfirmedChange': 0, 'Deaths': 0, "DeathsChange": 0, "Recovered": 0, "RecoveredChange": 0, "ISO3": "WWW"}
df_filled_data = df_dataset_removed_data.fillna(value=values)

# colunas = df_filled_data.isna().sum()/df_filled_data.shape[0]

def formatVaccinationDate(date):
  formated = pd.to_datetime(date, format='%Y-%m-%d')
  return formated

def formatDataDate(date):
  formated = pd.to_datetime(date, format='%m/%d/%Y')
  return formated

df_filled_vacinacao['date'] = df_filled_vacinacao['date'].apply(formatVaccinationDate)
df_filled_data['Updated'] = df_filled_data['Updated'].apply(formatDataDate)


dir = '../DatasetsTratados'

if not os.path.exists(dir):
    os.mkdir(dir)

df_filled_vacinacao.to_csv(dir + '/processed_vacinacao.csv', index=False)
df_filled_data.to_csv(dir + '/processed_data.csv', index=False)