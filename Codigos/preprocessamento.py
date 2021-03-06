import pandas as pd
import os

df_dataset_original_vacinacao = pd.read_csv('..\Datasets\country_vaccinations.csv', sep=',', index_col=None)
df_dataset_original_data = pd.read_csv('..\Datasets\Bing-COVID19-Data.csv', sep=',', index_col=None)

def filterColumns(dataset, drop):
  return dataset.drop(drop, axis = 1) 

def preprocessamento():
  #remover atributos desnecessários
  df_dataset_removed_vacinacao = filterColumns(df_dataset_original_vacinacao, ['daily_vaccinations_raw', 'daily_vaccinations', 'total_vaccinations_per_hundred', 'people_vaccinated_per_hundred', 'people_fully_vaccinated_per_hundred', 'daily_vaccinations_per_million', 'source_name', 'source_website'])
  df_dataset_removed_data = filterColumns(df_dataset_original_data, ['ID','Latitude', 'Longitude', 'ISO2'])

  #Aplicar ISO3 no Worldwide
  df_worldwide = df_dataset_removed_data['Country_Region'] == 'Worldwide'
  df_dataset_removed_data.loc[df_worldwide, 'ISO3'] = 'WWW'

  #Remover todos que não possuem ISO3
  df_without_iso = df_dataset_removed_data['ISO3'].notnull()
  df_dataset_removed_data = df_dataset_removed_data.loc[df_without_iso]

  #Remover todos que possuem admin1 e admin2
  with_adminRegion1 = df_dataset_removed_data['AdminRegion1'].isnull()
  # with_adminRegion2 = df_dataset_removed_data['AdminRegion1'].isnull()

  df_with_anyRegion = with_adminRegion1

  df_dataset_removed_data = df_dataset_removed_data.loc[df_with_anyRegion]

  df_dataset_removed_data = df_dataset_removed_data.drop(['AdminRegion1', 'AdminRegion2'], axis = 1)

  #Remover dados zerados da vacinação
  withoutTotal = df_dataset_original_vacinacao['total_vaccinations'].notnull()
  df_dataset_removed_vacinacao = df_dataset_removed_vacinacao.loc[withoutTotal]


  #Verificar quais colunas estão vazias e zerar
  values = {'total_vaccinations': 0, 'people_vaccinated': 0, 'people_fully_vaccinated': 0}
  df_filled_vacinacao = df_dataset_removed_vacinacao.fillna(value=values)

  values = {'ConfirmedChange': 0, 'Deaths': 0, "DeathsChange": 0, "Recovered": 0, "RecoveredChange": 0}
  df_filled_data = df_dataset_removed_data.fillna(value=values)

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

  df_filled_data['Confirmed'] += 1
  df_filled_data['Deaths'] += 1
  df_filled_data['Recovered'] += 1

  df_filled_data.sort_values(by=['ISO3', 'Updated'], inplace=True)

  dir = '../DatasetsTratados'

  if not os.path.exists(dir):
      os.mkdir(dir)

  df_filled_vacinacao.to_csv(dir + '/processed_vacinacao.csv', index=False)
  df_filled_data.to_csv(dir + '/processed_data.csv', index=False)

def tratamento():
  df_dataset_processed_data = pd.read_csv('..\DatasetsTratados\processed_data.csv', sep=',', index_col=None)
  df_dataset_processed_vacinacao = pd.read_csv('..\DatasetsTratados\processed_vacinacao.csv', sep=',', index_col=None)

  start_date = df_dataset_processed_vacinacao['date'].min()
  end_date = df_dataset_processed_vacinacao['date'].max()

  after_start_date = df_dataset_processed_data["Updated"] >= start_date
  before_end_date = df_dataset_processed_data["Updated"] <= end_date
  between_two_dates = after_start_date & before_end_date
  df_filtered_dates = df_dataset_processed_data.loc[between_two_dates]


  #Saving Dataset

  dir = '../DatasetsTratados'

  if not os.path.exists(dir):
      os.mkdir(dir)

  df_filtered_dates.to_csv(dir + '/filtered_by_vaccination_dates_data.csv', index=False)

preprocessamento()
tratamento()