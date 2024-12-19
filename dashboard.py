import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter
import plotly.graph_objects as go
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import re

####### Ajusta a configuração da plagina
st.set_page_config(page_title="Análise de Tweets de Donald Trump entre 2009 e 2019",
                   layout='wide',
                   menu_items={
        "About": "Este é um dashboard feito com Streamlit!"
    })
## Ajusta o título da página
st.title('Tweets de Donald Trump entre 2009 e 2019')

#Importa o dataframe e ordena por ano
df = pd.read_csv('trump_tweets.csv',index_col='Unnamed: 0')
df = df.sort_values('year')

#Cria uma variáveis que será usada como controle da barra lateral
years = df['year'].unique().tolist()
years.insert(0,'todos os anos')

with st.sidebar:
    year_select = st.sidebar.selectbox('Selecione o ano', years)
    st.write('''
Meu nome é Márcio Constancio Junior e estou iniciando na área de análise de dados. 
Neste dashboard, apresento alguns dados referentes a tweets do Donald Trump no intervalo de 2009 a 2019. 
Os dados foram fornecidos pelo Heitor Sasaki, como parte do desafio #DataGlowup n°38.
''')
    st.write('''
Na primeira linha do dashboard apresento uma nuvem de palavras com as palavras mais mencionadas.
''')
    st.write('''
Na segunda linha são apresentados três gráficos: o primeiro com a contagem de tweets ano a ano, o segundo com as 10 hashtags mais utilizadas e o terceiro gráfico com as top 10 menções.
''')
    st.write('''
Por fim, na terceira linha são apresentados os cinco tweets mais retweetados e os 5 tweets mais curtidos.
             Com exceção do gráfico de contagem de tweets por ano, todos os outros gráficos são recalculados ao escolher o ano no topo desta barral lateral.
''')
    st.write('''
Espero que gostem! Seus comentários são bem-vindos. Para acessar meu linkedin, [clique aqui](http://www.linkedin.com/in/marcio-constancio-junior)               .
''')



#Faz o controle do dataframe que será usado
if year_select == 'todos os anos':
    df_filtered = df
else:
    df_filtered = df[df['year']== year_select]

######### Contagem de tweets por ano########################
contagem_ano = df.groupby('year')['full_text'].count().reset_index(name='num_tweets_ano')

fig_tweeet_ano = px.line(contagem_ano, x='year',
              y='num_tweets_ano',
              title = 'Contagem de tweets por ano',
              markers=True,
              labels={'year': 'Ano', 'num_tweets_ano': 'Numero de tweets por ano'} )
fig_tweeet_ano.update_layout(
    xaxis=dict(tickangle=-45,
               tickfont=dict(size=12),
               title=dict(font=dict(size=20))),  # Rotaciona os rótulos do eixo X e ajusta o tamanho da fonte
    yaxis=dict(tickfont=dict(size=12),
               title=dict(font=dict(size=20)),
               ),
    title_font=dict(size=20)
)
################################################33

#######Contagem de hashtags##############################################################
#Seleciono todas as hashtags não-nulas do dataframe
hashtags = df_filtered['hashtags'][df_filtered['hashtags'].notnull()]
#Faço a divisão das possíveis hashtags duplas: ex: 'TRUMP2016, AmericaGreatAgain' --> 'TRUMP2016', 'AmericaGreatAgain'
all_hashtags = [hashtag.strip() for sublist in hashtags for hashtag in sublist.split(',')]
#Contagem das hastags
hashtag_counts = Counter(all_hashtags)
# Top 10 hashtags mais comuns
top_hashtags = dict(hashtag_counts.most_common(10))
top_10_hashtags = list(top_hashtags.keys())
frequencias = list(top_hashtags.values())

fig_hash = go.Figure(data=[go.Bar(x=frequencias, y=top_10_hashtags, orientation='h')])

# Personalizando o layout
fig_hash.update_layout(
    title=f'Top 10 Hashtags de {year_select}',
    xaxis_title='Frequência',
    yaxis_title='Hashtag')
#######Contagem de hashtags##############################################################

#############TOP Tweets mais retweetados############
#top_five_tweets = df_filtered[['full_text','retweet_count']].nlargest(5,'retweet_count')
top_five_tweets = df_filtered[['retweet_count','full_text']].sort_values(by='retweet_count',ascending=False).head(5).set_index('retweet_count')
#############TOP Tweets mais retweetados#####################

######################Top 5 favoritados#####################
top_favorited = df_filtered[['favorited_count','full_text']].sort_values(by='favorited_count', ascending=False).head(5)
######################Top 5 favoritados#####################

################## TOP 10 mencoes #################################
mencoes = df_filtered['mentions'][df_filtered['mentions'].notnull()]
# Contar mencoes
all_mencoes = [mencao.strip() for sublist in mencoes for mencao in sublist.split(',')]
mencao_counts = Counter(all_mencoes)
# Top 10 mencoes mais comuns
top_mencoes = dict(mencao_counts.most_common(10))

fig_mencao = go.Figure(data=[go.Bar(x=list(top_mencoes.values()), y=list(top_mencoes.keys()), orientation='h')])
fig_mencao.update_layout(
    title=f'Top 10 menções de {year_select}',
    xaxis_title='Frequência',
    yaxis_title='Menção')
################## TOP 10 mencoes #################################

###################### CRIANDO UMA WORDCLOUD EM TEMPO REAL ###############
fundo='black'
texto = " ".join(tweet for tweet in df_filtered['full_text'].dropna())
# Pré-processamento: remove URLs, menções, hashtags e símbolos especiais
texto_limpo = re.sub(r'http\S+|www.\S+|@\w+|#\w+|[^a-zA-Z\s]', '', texto)
# Define as stopwords
stop_words = set(stopwords.words('english'))
    
# Gera a nuvem de palavras
wordcloud = WordCloud(stopwords=stop_words,
                      background_color=fundo,
                      ).generate(texto_limpo)
    
# Plota a nuvem de palavras
fig = plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
###################### CRIANDO UMA WORDCLOUD EM TEMPO REAL ###############


##### Posicionamento dos gráficos e tabelas #####################
with st.container():
    st.pyplot(fig)
    #path_imagens = f'/home/marcio/Documentos/Projetos/dataGlowUp/{year_select}.png' 
    #st.subheader(f'Nuvem de palavras de {year_select}')
    #st.image(path_imagens,use_container_width=True)

with st.container():
    col1, col2,col5 = st.columns(3)
    with col1:
        st.plotly_chart(fig_tweeet_ano, use_container_width=True)
    with col2:
        st.plotly_chart(fig_hash, use_container_width=True)
    with col5:
        st.plotly_chart(fig_mencao,use_container_width=True)

with st.container():
    col3,col4 = st.columns(2)
    with col3:
        st.subheader(f'Top 5 retweets em {year_select}')
        st.dataframe(top_five_tweets, use_container_width=True)
    with col4:
        st.subheader(f'Top 5 mais curtidos em {year_select}')
        st.write(top_favorited[['favorited_count','full_text']].set_index('favorited_count'))



