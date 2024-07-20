# importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.offline as pf
import plotly.graph_objects as po
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

# lendo os arquivos csv utilizando a biblioteca Pandas
pacientes = pd.read_csv('dados_pacientes.csv', sep=';')
clinicos = pd.read_csv('dados_clinicos.csv', sep=';')
estados = pd.read_csv('estado_regiao.csv', sep=';', encoding='latin-1')

# realizando uma análise descritiva dos dataframes
pacientes.info()
estados.info()
clinicos.info()

# realizando a média da coluna "qtde_filhos" e arrendondando para 2 casas decimais
media = pacientes['qtde_filhos'].mean()
media_arr = round(media, 2)

# inserindo a média arredondada nas colunas onde estavam vazias
# inserindo uma variável categórica na coluna "classe_trabalho"
pacientes['qtde_filhos'].fillna(media_arr, inplace=True)
pacientes['classe_trabalho'].fillna('Funcionário Setor Privado', inplace=True)

# juntando dois dataframes
pacientes_estados = pd.merge(pacientes, estados, on='id_estado')
pacientes_estados.sort_values('id_cliente')
pacientes_estados.reset_index(drop=True)

# juntando dois dataframes
tabela_completa = pd.merge(pacientes_estados, clinicos, on='id_cliente')
tabela_completa.sort_values('id_cliente')
tabela_completa.reset_index(drop=True)


def calcular_wcss(dados_clientes):
  imputer = SimpleImputer(strategy='mean') # Replace missing values with the mean
  dados_clientes_imputed = imputer.fit_transform(dados_clientes) 
  wcss = []
  for k in range(1,11):
    kmeans = KMeans(n_clusters = k)
    kmeans.fit(X=dados_clientes_imputed)
    wcss.append(kmeans.inertia_)
  return wcss

# criando um dataframe somente com as colunas 'peso' e 'colesterol'
dados_clientes = tabela_completa[['peso', 'colesterol']]
dados_clientes.head()

wcss_clientes = calcular_wcss(dados_clientes)
for i in range(len(wcss_clientes)):
  print(f'o cluster {i} possui possui o valor de WCSS: {wcss_clientes[i]}')

grafico_wcss = px.line(x= range(1,11),
                        y= wcss_clientes)
fig = po.Figure(grafico_wcss)
fig.update_layout(title= 'Calculando o WCSS',
                  xaxis_title= 'Número de Clusters',
                  yaxis_title= 'Valor dos Clusters',
                  template= 'plotly_white')
fig.show()

imputer = SimpleImputer(strategy='mean') # Replace missing values with the mean
dados_clientes_imputed = imputer.fit_transform(dados_clientes) 
kmeans_clientes = KMeans(n_clusters = 3,
                         random_state = 42,
                         init= 'k-means++',
                         n_init = 10)
tabela_completa['cluster'] = kmeans_clientes.fit_predict(dados_clientes_imputed)

cluster_clientes = tabela_completa
cluster_clientes.loc[cluster_clientes['cluster']==1, 'nome cluster'] = 'Baixo Risco'
cluster_clientes.loc[cluster_clientes['cluster']==0, 'nome cluster'] = 'Risco Moderado'
cluster_clientes.loc[cluster_clientes['cluster']==2, 'nome cluster'] = 'Alto Risco'
centroide_cluster = kmeans_clientes.cluster_centers_

# 
grafico = px.scatter(x= tabela_completa['peso'],
                      y = tabela_completa['colesterol'],
                      color=tabela_completa['cluster'])
grafico_centroide = px.scatter(x= centroide_cluster[:,0], y=centroide_cluster[:,1], size=[7,7,7])
grafico_final = po.Figure(data = grafico.data + grafico_centroide.data)
grafico_final.update_layout(title = 'Analise de Cluster',
                            xaxis_title = 'Peso',
                            yaxis_title = 'Colesterol')
grafico_final.show()

cluster_clientes.loc[cluster_clientes['cluster']==1, 'nome cluster'] = 'Baixo Risco'
cluster_clientes.loc[cluster_clientes['cluster']==0, 'nome cluster'] = 'Risco Moderado'
cluster_clientes.loc[cluster_clientes['cluster']==2, 'nome cluster'] = 'Alto Risco'

LE = LabelEncoder()
cluster_clientes['regiao_number'] = LE.fit_transform(cluster_clientes['regiao'])

plt.figure(figsize=(10, 7))
sns.histplot(cluster_clientes['regiao_number'], kde=True, kde_kws={'bw_adjust': 1.5})
plt.xlabel('Região')
plt.ylabel('Frequência')
plt.title('Distribuição de clientes por Regiões')
plt.show()
