import pandas as pd
import os

df_dataset_original_vacinacao = pd.read_csv('..\Datasets\country_vaccinations.csv', sep=',', index_col=None)
df_dataset_original_data = pd.read_csv('..\Datasets\Bing-COVID19-Data.csv', sep=',', index_col=None)

#remover atributos desnecessários
df_dataset_removed_vacinacao = df_dataset_original_vacinacao.drop(['daily_vaccinations_raw', 'daily_vaccinations', 'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'daily_vaccinations_per_million', 'source_name', 'source_website'], axis = 1)
df_dataset_removed_data = df_dataset_original_data.drop(['ID','Latitude', 'Longitude', 'ISO2'], axis = 1)

#Aplicar ISO3 no Worldwide
df_worldwide = df_dataset_removed_data['Country_Region'] == 'Worldwide'

df_dataset_removed_data.loc[df_worldwide, 'ISO3'] = 'WWW'

#Remover todos que não possuem ISO3
df_without_iso = df_dataset_removed_data['ISO3'].notnull()

df_dataset_removed_data = df_dataset_removed_data.loc[df_without_iso]

#Remover todos que possuem admin1 e admin2
with_adminRegion1 = df_dataset_removed_data['AdminRegion1'].isnull()
with_adminRegion2 = df_dataset_removed_data['AdminRegion1'].isnull()

df_with_anyRegion = with_adminRegion1 | with_adminRegion2

df_dataset_removed_data = df_dataset_removed_data.loc[df_with_anyRegion]

df_dataset_removed_data = df_dataset_removed_data.drop(['AdminRegion1', 'AdminRegion2'], axis = 1)

#Remover dados zerados da vacinação
withoutTotal = df_dataset_original_vacinacao['total_vaccinations'].notnull()
df_dataset_removed_vacinacao = df_dataset_removed_vacinacao.loc[withoutTotal]



#Verificar quais colunas estão vazias e zerar

values = {'total_vaccinations': 0, 'people_vaccinated': 0, 'people_fully_vaccinated': 0}
df_filled_vacinacao = df_dataset_removed_vacinacao.fillna(value=values)

# colunas = df_filled_vacinacao.isna().sum()/df_filled_vacinacao.shape[0]

values = {'ConfirmedChange': 0, 'Deaths': 0, "DeathsChange": 0, "Recovered": 0, "RecoveredChange": 0}
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


df_filled_vacinacao['day'] = df_filled_vacinacao['date'].dt.day
df_filled_vacinacao['month'] = df_filled_vacinacao['date'].dt.month
df_filled_vacinacao['year'] = df_filled_vacinacao['date'].dt.year

df_filled_data['day'] = df_filled_data['Updated'].dt.day
df_filled_data['month'] = df_filled_data['Updated'].dt.month
df_filled_data['year'] = df_filled_data['Updated'].dt.year

#26<->29/03/2021 todos os países
days = df_filled_data['Updated'] == '2021-03-25'
df_days = df_filled_data.loc[days]


for index, row in df_days:
  print(row)
  #for i in range(26,29):
    #df_filled_data.add({'Updated':'2021-03-'+str(i),'Confirmed': row['Confirmed'],'ConfirmedChange': 0, 'Deaths': row['Deaths'], 'DeathsChange': 0, 'Recovered': row['Recovered'],'RecoveredChange': 0, 'Country_Region': row['Country_Region'], 'ISO3': row['ISO3']})

df_filled_data.sort_values(by=['ISO3', 'Updated'], inplace=True)

dir = '../DatasetsTratados'

if not os.path.exists(dir):
    os.mkdir(dir)

df_filled_vacinacao.to_csv(dir + '/processed_vacinacao.csv', index=False)
df_filled_data.to_csv(dir + '/processed_data.csv', index=False)