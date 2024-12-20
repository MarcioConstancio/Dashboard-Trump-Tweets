# Análise de tweets de Donald Trump entre 2009 e 2019

Neste projeto apresento um dashboard feito com Streamlit usando dados referentes a análises de tweets de Donald Trump entre os anos de 2009 e 2019. Os dados foram fornecidos pelo Heitor Sasaki, como parte do desafio #DataGlowUp 38. 

Os gráficos apresentados tem o objetivo de responder às seguintes perguntas: 

1. Quais as palavras mais usadas ao longo deste período ou anualmente?
2. Quais são as principais instituições (pessoas, empresas) mencionadas ao longo dos anos?
3. O período eleitoral ou o período em que esteve  na presidência dos Estados Unidos apresenta alguma alteração quanto ao número de *tweets*?
4. Quais são os *tweets* mais curtidos e quais os mais retuitados?

O dashboard está disponível [aqui](https://marcioconstanciojr-dashboard-trump-tweets.streamlit.app/ ). Sugestões são bem-vindas!

# Quer clonar este projeto para rodar localmente? Siga os passos a seguir.

## Clonar o repositório
```bash
git clone https://github.com/MarcioConstancio/Dashboard-Trump-Tweets.git
cd Dashboard-Trump-Tweets
```

## Criar e ativar o ambiente virtual
``` bash
python -m venv nome-do-ambiente
source nome-do-ambiente/bin/activate  # No Linux/macOS
nome-do-ambiente\Scripts\activate     # No Windows
```

## Instalar dependências
``` bash
pip install -r requirements.txt
```

## Para rodar o dashboard localmente
``` bash
streamlit run dashboard.py
```

## Desativar o ambiente virtual
``` bash
deactivate
```



