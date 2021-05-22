import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df_dataset_processed_data = pd.read_csv('..\DatasetsTratados\processed_data.csv', sep=',', index_col=None)
df_dataset_processed_vacinacao = pd.read_csv('..\DatasetsTratados\processed_vacinacao.csv', sep=',', index_col=None)
df_dataset_filtered_by_vacinacao_date_data = pd.read_csv('..\DatasetsTratados/filtered_by_vaccination_dates_data.csv', sep=',', index_col=None)

df_worldwide = df_dataset_processed_data.loc[df_dataset_processed_data['ISO3'] == 'WWW']
# df_worldwide = df_dataset_filtered_by_vacinacao_date_data.loc[df_dataset_filtered_by_vacinacao_date_data['ISO3'] == 'WWW']

x=np.array(df_worldwide["Updated"])
yConfirmed=np.array(df_worldwide["Confirmed"])
yDeaths=np.array(df_worldwide["Deaths"])
yRecovered=np.array(df_worldwide["Recovered"])

plt.plot(x, yConfirmed, color='red', label='Casos Confirmados')
plt.plot(x, yDeaths, color='black', label="Mortes")
plt.plot(x, yRecovered, color='green',label="Recuperados")
plt.legend()
plt.title("Casos Totais")
plt.xlabel("Data de atualização")
plt.ylabel("Quantidade")
plt.xticks(range(0,481,30))
plt.show()