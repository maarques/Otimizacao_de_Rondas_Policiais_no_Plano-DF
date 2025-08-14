
# Otimização de Rondas: Uma Abordagem Preditiva para Segurança Urbana

## A Problemática: A Ineficiência das Rondas Tradicionais

A segurança urbana é um desafio constante nas grandes cidades. Tradicionalmente, o patrulhamento de rondas policiais ou de segurança privada opera de forma reativa, muitas vezes baseando-se em rotas fixas, aleatórias ou na intuição dos agentes. Este modelo tradicional apresenta falhas significativas:

  * **Baixa Eficiência**: Recursos valiosos, como tempo e pessoal, são desperdiçados em áreas de baixo risco, enquanto zonas críticas podem ficar desprotegidas.
  * **Modelo Reativo**: A ação ocorre, na maioria das vezes, *após* um incidente ter sido relatado, com pouca capacidade de prevenção.
  * **Falta de Base Analítica**: As decisões sobre onde e quando patrulhar raramente são fundamentadas em uma análise profunda dos dados históricos de criminalidade, ignorando padrões sazonais, horários de pico e a concentração geográfica de diferentes tipos de crimes.

Este cenário resulta em uma alocação de recursos abaixo do ideal e em uma capacidade limitada de antecipar e prevenir crimes de forma proativa.

## O Desafio: Da Reação à Predição

O desafio central deste projeto é transformar o modelo de patrulhamento de reativo para **preditivo e inteligente**. Como podemos utilizar o grande volume de dados criminais para não apenas entender o passado, mas também para prever o futuro e otimizar as operações de segurança no presente?

Para isso, é necessário superar os seguintes obstáculos:

1.  **Identificar Padrões Ocultos**: Analisar um conjunto de dados complexo para encontrar correlações entre diversas variáveis, como tipo de crime, localização (latitude/longitude), horário, dia da semana, e até mesmo características demográficas das vítimas.
2.  **Construir um Modelo Preditivo**: Desenvolver um modelo de machine learning robusto, capaz de prever as coordenadas geográficas de futuros incidentes com base nas variáveis mais influentes.
3.  **Tornar a Análise Acessível**: Criar uma ferramenta que traduza os resultados complexos da análise de dados em insights visuais e acionáveis, permitindo que gestores de segurança tomem decisões mais rápidas e informadas.

## A Solução: Análise de Dados para Rondas Otimizadas

Este projeto enfrenta o desafio proposto através de uma solução completa de análise de dados e machine learning. Utilizando um dataset de ocorrências criminais na Asa Sul (Brasília), aplicamos técnicas de ciência de dados para construir um sistema que otimiza as rotas de patrulhamento.

### Funcionalidades Principais

  * **Análise Exploratória (EDA)**: Uma profunda investigação dos dados para descobrir as "zonas quentes" (hotspots), os horários de maior risco para crimes específicos (como tráfico e homicídios entre 21h e 23h) e os perfis demográficos mais afetados.
  * **Pré-processamento de Dados**: Técnicas de limpeza, tratamento de valores ausentes e engenharia de features para preparar os dados para os modelos preditivos.
  * **Modelagem Preditiva**: Implementação de modelos de regressão de alta performance (Random Forest e XGBoost) para prever a latitude e longitude de futuros crimes com base em fatores como horário, tipo de crime e nível de risco da região.
  * **Visualização Geográfica Interativa**: Utilização de mapas de calor e clusters (Folium) para visualizar a densidade criminal por região e horário, tornando os padrões facilmente identificáveis.
  * **Dashboard Interativo (Streamlit)**: Uma interface web amigável que permite a qualquer usuário explorar os dados, filtrar por tipo de crime ou horário, e visualizar os insights da análise sem precisar de conhecimento técnico em programação.

## Como Começar

### Pré-requisitos

  * Python 3.x
  * pip (gerenciador de pacotes do Python)

### Instalação

1.  Clone o repositório:
    ```bash
    git clone https://github.com/miguelcandido21/otimizacao_rondas.git
    ```
2.  Navegue até o diretório do projeto:
    ```bash
    cd otimizacao_rondas
    ```
3.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

### Execução

Para iniciar o dashboard interativo, execute o seguinte comando no seu terminal:

```bash
streamlit run app.py
```

## Tecnologias Utilizadas

  * **Linguagem**: Python
  * **Análise de Dados**: Pandas, NumPy
  * **Machine Learning**: Scikit-learn, XGBoost
  * **Visualização**: Matplotlib, Seaborn, Folium
  * **Dashboard**: Streamlit
  * **Desenvolvimento**: Jupyter Notebook
