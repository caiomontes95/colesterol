import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.offline as pf
import plotly.graph_objects as po
from sklearn.cluster import KMeans

pacientes = pd.read_csv('dados_pacientes.csv', sep=';')
clinicos = pd.read_csv('dados_clinicos.csv', sep=';')
estados = pd.read_csv('estado_regiao.csv', sep=';', encoding='latin-1')

pacientes.info()
estados.info()
clinicos.info()

media = pacientes['qtde_filhos'].mean()
media_arr = round(media, 2)
media_arr

pacientes['qtde_filhos'].fillna(media_arr, inplace=True)
pacientes.isna().sum()
print(pacientes.classe_trabalho.value_counts())

pacientes['classe_trabalho'].fillna('Funcionário Setor Privado', inplace=True)

pacientes_estados = pd.merge(pacientes, estados, on='id_estado')
pacientes_estados.sort_values('id_cliente')
pacientes_estados.reset_index(drop=True)

tabela_completa = pd.merge(pacientes_estados, clinicos, on='id_cliente')
tabela_completa.sort_values('id_cliente')
tabela_completa.reset_index(drop=True)

def calcular_wcss(dados_clientes):
  wcss = []
  for k in range(1,11):
    kmeans = KMeans(n_clusters = k)
    kmeans.fit(X=dados_clientes)
    wcss.append(kmeans.inertia_)
  return wcss

dados_clientes = tabela_completa[['peso', 'colesterol']]
dados_clientes.head()

plt.figure(figsize=(12, 7))
sns.histplot(cluster_clientes['salario'], kde=True, kde_kws={'bw_adjust': 1.5})
plt.xlabel('Salário')
plt.ylabel('Frequência')
plt.title('Distribuição de Salários')
plt.show()

