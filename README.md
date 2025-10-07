🚨 **Otimização de Rondas: Abordagem Preditiva para Segurança Urbana**
📍 **Localização e Foco:** Plano Piloto, Asa Sul (DF) | **Status:** ✅ Em Desenvolvimento

---

### 📖 Visão Geral do Projeto

Este projeto propõe uma solução inteligente para o patrulhamento de segurança, transformando o modelo tradicionalmente reativo em um sistema preditivo e otimizado.
Utilizando técnicas avançadas de Ciência de Dados e Machine Learning, o objetivo é antecipar a ocorrência de crimes, prevendo suas coordenadas geográficas, e assim, otimizar as rotas de rondas policiais ou de segurança na região da Asa Sul, Brasília (DF).

O coração da solução é um modelo de **Machine Learning (XGBoost)** treinado com dados criminais para identificar padrões sazonais, temporais e geográficos que influenciam a criminalidade.

---

### 🎯 A Problemática: Da Reação à Predição

O patrulhamento tradicional é frequentemente ineficiente devido a:

* **Rotas Fixas ou Aleatórias:** Desperdício de recursos em áreas de baixo risco.
* **Natureza Reativa:** A ação policial ocorre após o incidente ser reportado.
* **Falta de Análise:** Decisões de patrulhamento baseadas em intuição, ignorando padrões complexos de criminalidade.

**Nosso Desafio:** Como usar o Big Data de ocorrências criminais para prever o futuro e alocar recursos de forma proativa?

---

### 💡 A Solução: Preditiva e Inteligente

A abordagem do projeto é dividida em etapas analíticas e de desenvolvimento para garantir uma ferramenta robusta e acionável:

* **Modelagem Preditiva Técnica:** Regressão e Classificação de Alta Performance (XGBoost e Random Forest).

  * **Objetivo:** Prever as coordenadas geográficas (latitude e longitude) de futuros incidentes com base em variáveis contextuais (tipo de crime, horário, dia da semana).
  * **Resultado:** O modelo atinge uma acurácia notável (ex: 63% do XGBoost) na identificação dos "hotspots" de crime.

* **Visualização e Usabilidade**

  * **Visualização Geográfica:** Uso de mapas interativos (**Folium**) para criar Mapas de Calor e clusters, traduzindo a densidade criminal em insights visuais.
  * **Dashboard Interativo:** Uma interface amigável (**Streamlit**) permite que gestores de segurança explorem dados, visualizem previsões e tomem decisões informadas rapidamente.

---

### 🔑 Estratégia de Dados: Dados Sintéticos Baseados em Regras

Um obstáculo fundamental em projetos de análise de criminalidade é o acesso a dados reais sensíveis.
Para contornar essa questão legal e ética, este projeto implementou uma estratégia diferenciada:

Não foram utilizados dados aleatórios, mas sim **dados sintéticos gerados proceduralmente** com base em regras e padrões realistas observados em segurança pública.

Os scripts (`dados_asa_sul.py` e `Dados Fake.py`) simulam a complexidade do mundo real, incorporando lógicas como:

* **Pesos Geográficos:** Crimes como "Tráfico" ocorrem com maior frequência em áreas específicas (ex: W3 Sul).
* **Influência Temporal:** Crimes mais graves têm maior peso durante a noite e feriados.
* **Perfis Demográficos:** Geração de perfis de vítimas sintéticas associadas a tipos de crimes específicos (ex: vítimas de "Furto" em áreas residenciais são mais velhas).

Essa metodologia garante que o modelo de Machine Learning seja treinado em dados que possuem correlações realistas a serem descobertas, resultando em um desempenho válido e significativo.

---

### ⚙️ Tecnologias Utilizadas

| Categoria         | Tecnologia                | Uso Principal                                      |
| ----------------- | ------------------------- | -------------------------------------------------- |
| Linguagem         | **Python**                | Linguagem principal de desenvolvimento             |
| Data Science      | **Pandas, NumPy**         | Manipulação e pré-processamento de dados           |
| Machine Learning  | **Scikit-learn, XGBoost** | Implementação e avaliação dos modelos preditivos   |
| Visualização      | **Matplotlib, Seaborn**   | Geração de gráficos e análises exploratórias (EDA) |
| Visualização Geo. | **Folium**                | Criação de mapas de calor e clusters interativos   |
| Interface         | **Streamlit**             | Desenvolvimento do dashboard interativo            |
| Ambiente          | **Jupyter Notebook**      | Análise Exploratória de Dados (`padroes.ipynb`)    |

---

### 🚀 Como Começar

Siga os passos abaixo para clonar o repositório e executar o dashboard na sua máquina local.

#### Pré-requisitos

Certifique-se de ter o **Python 3.x** e o **pip** instalados.

#### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/maarques/Otimizacao_de_Rondas_Policiais_no_Plano-DF.git
```

#### 2️⃣ Navegue até o Diretório

```bash
cd Otimizacao_de_Rondas_Policiais_no_Plano-DF
```

#### 3️⃣ Instale as Dependências

Todas as bibliotecas necessárias estão listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

#### 4️⃣ Execute o Dashboard Interativo

Inicie a aplicação **Streamlit** no seu terminal.
O dashboard será aberto automaticamente no seu navegador padrão.

```bash
streamlit run app.py
```

---

### 📂 Estrutura do Projeto

```plaintext
Otimizacao_de_Rondas_Policiais_no_Plano-DF/
├── .gitignore                 # Arquivos a serem ignorados pelo Git
├── README.md                  # Este arquivo
├── requirements.txt           # Dependências do projeto
├── app.py                     # Aplicação principal (Dashboard Streamlit)
├── padroes.ipynb              # Jupyter Notebook com a Análise Exploratória (EDA) e Modelagem
├── Dados Fake.py              # Script de Geração de Dados Sintéticos (Geral)
└── dados_asa_sul.py           # Script de Geração de Dados Sintéticos (Específico para Asa Sul)
```

---

### 🤝 Contribuição e Contato

Sinta-se à vontade para abrir **Issues** para relatar bugs ou sugerir melhorias.

**Autores:**

* [@maarques](https://github.com/maarques)
* [@MiguelCandido21](https://github.com/MiguelCandido21)
* [@SamuelMota321](https://github.com/SamuelMota321)
