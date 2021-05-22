import pandas as pd
import os

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