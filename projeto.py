import streamlit as st
import pandas as pd
import plotly_express as px
import altair as alt


st.set_page_config(layout='wide',
                   page_title='Peso vs Colesterol',
                   page_icon='https://cdn-icons-png.flaticon.com/512/6124/6124016.png',)

def pagina_inicial():
    st.header('Correlação entre Peso Corporal e Níveis de Colesterol')
    st.caption('Estudos indicam que há uma correlação positiva entre o aumento do peso corporal \
                 e o aumento dos níveis de colesterol. À medida que o peso de uma pessoa aumenta, \
                 seus níveis de colesterol tendem a subir linearmente, aumentando o risco de doenças cardiovasculares.')
    texto = 'A relação entre colesterol e peso é um tema de grande importância na área da saúde, pois ambos são fatores de risco críticos para diversas doenças crônicas. Este projeto visa investigar como o peso corporal e os níveis de colesterol interagem para influenciar a saúde cardiovascular. Focaremos na coleta e análise de dados obtidos através de medições de peso e níveis de colesterol (HDL, LDL e triglicerídeos) de pessoas entrevistadas, divididas entre masculino e feminino, em diversas faixas etárias. O objetivo é identificar padrões que possam ajudar na prevenção e no tratamento de doenças cardiovasculares, promovendo uma melhor qualidade de vida. Além disso, o projeto pretende elaborar recomendações práticas para a população em geral e para profissionais de saúde, baseadas nas descobertas obtidas.'
    st.write(texto) 
    return pagina_inicial

def pagina_principal():
    @st.cache_data
    def carregar_arquivo1():
        arquivo1 = pd.read_csv('dados_pacientes.csv', sep= ';')
        return arquivo1
    def carregar_arquivo2():
        arquivo2 = pd.read_csv('dados_clinicos.csv', sep=';')
        return arquivo2

    pacientes = carregar_arquivo1()
    clinicos = carregar_arquivo2()

    df_clinicos = clinicos.dropna(subset=['peso'])
    clinicos_final = df_clinicos.iloc[:70]
        
    clinicos_masc = clinicos_final[clinicos_final['genero'].str.contains('Masculino')]    
    clinicos_fem = clinicos_final[clinicos_final['genero'].str.contains('Feminino')]

    st.title('Relatório: Relação entre Colesterol e Peso')
    st.subheader('Introdução')
    
    st.write('Este relatório analisa a relação entre o peso corporal e os níveis de colesterol em uma amostra composta por homens e mulheres. Os dados foram obtidos através de medições de peso e níveis de colesterol dos entrevistados e organizados em um gráfico de dispersão para facilitar a visualização e a análise das correlações.')

    st.subheader('Análise do Gráfico')
    st.write('O gráfico de dispersão apresentado mostra a relação entre o peso (eixo X) e o colesterol (eixo Y) para a amostra estudada. Cada ponto no gráfico representa um indivíduo, com o peso variando de aproximadamente 100 a 200 quilogramas e os níveis de colesterol variando de 100 a 220 quilogramas.')

    st.subheader('Observações')
    st.subheader('1. Correlação Positiva:')

    st.write('O gráfico indica uma correlação positiva forte entre peso e colesterol. À medida que o peso aumenta, os níveis de colesterol também aumentam. \
             A linha formada pelos pontos de dados é bastante próxima de uma linha reta, sugerindo que o aumento no peso está consistentemente associado ao aumento nos níveis de colesterol.')
    
    st.subheader('2. Distribuição dos Dados:')

    st.write('Os dados parecem estar distribuídos de forma linear, com poucos desvios significativos da tendência geral. \
             Não há evidências de agrupamentos distintos ou outliers significativos que desviem da linha de tendência principal.')
    
    st.subheader('3. Intervalos de Peso e Colesterol:')

    st.write('A faixa de peso observada varia de 100 a 200 quilogramas. \
             A faixa de colesterol observada varia de 100 a 220 quilogramas, mostrando uma ampla variação nos níveis de colesterol dentro da amostra estudada.')

    st.subheader('Conclusão')
    st.write('Os dados apresentados no gráfico sugerem uma forte correlação positiva entre o peso corporal e os níveis de colesterol em homens e mulheres. Este achado é consistente com a literatura existente que indica que o aumento do peso corporal está frequentemente associado a níveis mais elevados de colesterol, um fator de risco conhecido para doenças cardiovasculares. Recomenda-se uma análise adicional para explorar possíveis intervenções que possam ajudar a controlar o peso e, consequentemente, os níveis de colesterol na população geral.')
    
    selecione = st.selectbox('Selecione', ['Masculino', 'Feminino', 'Masculino e Feminino'],)

    if selecione == 'Masculino':
        figura_masc = px.scatter(clinicos_masc, x='peso', y='colesterol', color=None)
        st.plotly_chart(figura_masc, theme='streamlit' ,use_container_width=True)
        chart_masc = alt.Chart(clinicos_masc).mark_line().encode(x='peso',y='colesterol')
        st.altair_chart(chart_masc, use_container_width=True)
    elif selecione == 'Feminino':
        figura_fem = px.scatter(clinicos_fem, x='peso', y='colesterol', color=None)
        st.plotly_chart(figura_fem, theme='streamlit' ,use_container_width=True)
        chart_fem = alt.Chart(clinicos_fem).mark_line().encode(x='peso',y='colesterol')
        st.altair_chart(chart_fem, use_container_width=True)
    elif selecione == 'Masculino e Feminino':
        figura = px.scatter(clinicos_final, x='peso', y='colesterol', color='genero')
        st.plotly_chart(figura, theme='streamlit' ,use_container_width=True)
        chart = alt.Chart(clinicos_final).mark_line().encode(x='peso',y='colesterol')
        st.altair_chart(chart, use_container_width=True)
    return pagina_principal

def pagina_contato():
    st.title("Sobre mim")
    st.write('[Perfil Linkedin](https://www.linkedin.com/in/caioomontes)')
    st.write('[Instagram](https://www.instagram.com/caiomontes)')
    return pagina_contato

# Criação da sidebar para navegação
st.sidebar.title("MENU")
pagina_selecionada = st.sidebar.radio("Ir para", ["Página Inicial", "Gráficos e Relatórios", "Contato"])

# Exibição da página selecionada
if pagina_selecionada == "Página Inicial":
    pagina_inicial()
elif pagina_selecionada == "Gráficos e Relatórios":
    pagina_principal()
elif pagina_selecionada == "Contato":
    pagina_contato()