import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from sklearn.cluster import DBSCAN
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from streamlit_folium import folium_static
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Função para exportar gráficos como PNG
def exportar_grafico(fig):
    buf = BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    return buf

# Carregar dados com cache
@st.cache_data
def carregar_dados():
    df = pd.read_csv('crime_segunda_area.csv')
    df['hora'] = pd.to_datetime(df['hora'], format='%H:%M', errors='coerce').dt.hour
    df['peso'] = df['tipo_crime'].map({
        'furto': 2,
        'roubo': 3,
        'vandalismo': 1,
        'tráfico': 4,
        'homicídio': 5,
        'feminicídio': 5
    }).fillna(1)
    return df

df = carregar_dados()

# Sidebar - Filtros
st.sidebar.title("🔍 Filtros")
tipos_crime = df['tipo_crime'].unique().tolist()
tipos_selecionados = st.sidebar.multiselect("Selecione os tipos de crime", tipos_crime, default=tipos_crime)
hora_selecionada = st.sidebar.selectbox("Selecione o horário", ["Geral"] + list(range(24)), index=0)

# Filtrar dados com base nos filtros
df_filtrado = df[df['tipo_crime'].isin(tipos_selecionados)]
if hora_selecionada != "Geral":
    df_filtrado = df_filtrado[df_filtrado['hora'] == int(hora_selecionada)]

# Abas do dashboard
tab1, tab2, tab3 = st.tabs(["🔍 Análise Exploratória", "🧹 Pré-processamento", "🧪 Teste de Modelo"])

# Aba 1: Análise Exploratória (EDA)
with tab1:
    st.header("🔍 Análise Exploratória de Dados (EDA)")
    
    # 1. Tabela de dados
    st.subheader("Primeras Linhas do Dataset")
    st.dataframe(df.head(10))
    
    # 2. Crimes por Tipo
    with st.expander("🚨 Crimes por Tipo", expanded=True):
        crimes_por_tipo = df_filtrado['tipo_crime'].value_counts().reset_index()
        crimes_por_tipo.columns = ['tipo_crime', 'quantidade']
        crimes_por_tipo['porcentagem'] = (crimes_por_tipo['quantidade'] / len(df_filtrado)) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            plt.figure(figsize=(8, 4))
            sns.barplot(data=crimes_por_tipo, x='quantidade', y='tipo_crime', palette='viridis', dodge=False)
            plt.title("Frequência de Tipos de Crime", fontsize=12)
            plt.xlabel("Quantidade", fontsize=10)
            plt.ylabel("Tipo de Crime", fontsize=10)
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            st.pyplot(plt.gcf())
            st.download_button(
                label="📥 Exportar Gráfico de Barras",
                data=exportar_grafico(plt.gcf()),
                file_name=f"grafico_tipo_{hora_selecionada}.png",
                mime="image/png"
            )
            plt.close()
        
        with col2:
            plt.figure(figsize=(6, 4))
            plt.pie(crimes_por_tipo['quantidade'], labels=crimes_por_tipo['tipo_crime'], autopct='%1.1f%%', startangle=90)
            plt.title("Distribuição de Crimes por Tipo", fontsize=12)
            plt.axis('equal')
            plt.tight_layout()
            st.pyplot(plt.gcf())
            st.download_button(
                label="📥 Exportar Gráfico de Pizza",
                data=exportar_grafico(plt.gcf()),
                file_name=f"grafico_tipo_pizza_{hora_selecionada}.png",
                mime="image/png"
            )
            plt.close()
    
    # 3. Crimes por Hora do Dia
    if hora_selecionada == "Geral":
        with st.expander("⏰ Crimes por Hora do Dia", expanded=True):
            df_hora = df['hora'].value_counts().sort_index()
            colors = ['orange' if h >= 19 or h <= 4 else 'skyblue' for h in df_hora.index]
            
            plt.figure(figsize=(10, 4))
            sns.barplot(x=df_hora.index, y=df_hora.values, palette=colors)
            plt.title("Quantidade de Crimes por Hora do Dia", fontsize=12)
            plt.xlabel("Hora", fontsize=10)
            plt.ylabel("Quantidade", fontsize=10)
            plt.xticks(range(0, 24))
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            st.pyplot(plt.gcf())
            st.download_button(
                label="📥 Exportar Gráfico de Hora",
                data=exportar_grafico(plt.gcf()),
                file_name=f"grafico_hora_{hora_selecionada}.png",
                mime="image/png"
            )
            plt.close()
    
    # 4. Crimes por Região (Top 10)
    with st.expander("🏠 Crimes por Região", expanded=True):
        crimes_por_rua = df_filtrado['rua'].value_counts().reset_index()
        crimes_por_rua.columns = ['rua', 'quantidade']
        top_ruas = crimes_por_rua.head(10)
        
        plt.figure(figsize=(10, 4))
        sns.barplot(data=top_ruas, x='quantidade', y='rua', palette='viridis', dodge=False)
        plt.title("Top 10 Regiões com Mais Crimes", fontsize=12)
        plt.xlabel("Quantidade", fontsize=10)
        plt.ylabel("Região", fontsize=10)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        st.download_button(
            label="📥 Exportar Gráfico de Região",
            data=exportar_grafico(plt.gcf()),
            file_name=f"grafico_regiao_{hora_selecionada}.png",
            mime="image/png"
        )
        plt.close()
    
    # 5. Risco por Região
    with st.expander("⚠️ Risco por Região", expanded=True):
        risco_por_rua = df_filtrado.groupby('rua')['peso'].sum().reset_index(name='risco_total')
        risco_por_rua = risco_por_rua.sort_values(by='risco_total', ascending=False).head(5)
        
        plt.figure(figsize=(10, 4))
        sns.barplot(data=risco_por_rua, x='risco_total', y='rua', palette='viridis', dodge=False)
        plt.title("Risco por Região (Gravidade Acumulada)", fontsize=12)
        plt.xlabel("Risco Total", fontsize=10)
        plt.ylabel("Região", fontsize=10)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        st.download_button(
            label="📥 Exportar Gráfico de Risco",
            data=exportar_grafico(plt.gcf()),
            file_name=f"risco_regiao_{hora_selecionada}.png",
            mime="image/png"
        )
        plt.close()
        st.dataframe(risco_por_rua.style.format({'risco_total': '{:.0f}'}))
    
    # 6. Crimes Graves (Homicídio e Tráfico)
    with st.expander("💀 Crimes Graves (Homicídio e Tráfico) por Hora", expanded=True):
        crimes_graves = df[df['tipo_crime'].isin(['homicídio', 'tráfico'])]
        if hora_selecionada != "Geral":
            crimes_graves = crimes_graves[crimes_graves['hora'] == int(hora_selecionada)]
        
        horarios_risco = crimes_graves['hora'].value_counts().sort_index()
        
        plt.figure(figsize=(10, 4))
        sns.barplot(x=horarios_risco.index, y=horarios_risco.values, palette='coolwarm', dodge=False)
        plt.title("Horários com Mais Crimes Graves", fontsize=12)
        plt.xlabel("Hora", fontsize=10)
        plt.ylabel("Quantidade", fontsize=10)
        plt.xticks(range(0, 24, 2))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        st.download_button(
            label="📥 Exportar Gráfico de Crimes Graves",
            data=exportar_grafico(plt.gcf()),
            file_name=f"grafico_graves_{hora_selecionada}.png",
            mime="image/png"
        )
        plt.close()
    
    # 7. Crimes Noturnos (19h–04h)
    with st.expander("🌙 Crimes Noturnos (19h–04h)", expanded=True):
        crimes_noturnos = df[df['hora'].between(19, 23, inclusive='both') | (df['hora'] <= 4)]
        crimes_noturnos = crimes_noturnos[crimes_noturnos['tipo_crime'].isin(tipos_selecionados)]
        
        frequencia_crimes = crimes_noturnos['tipo_crime'].value_counts().reset_index()
        frequencia_crimes.columns = ['tipo_crime', 'quantidade']
        frequencia_crimes['porcentagem'] = (frequencia_crimes['quantidade'] / len(crimes_noturnos)) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            plt.figure(figsize=(8, 4))
            sns.barplot(data=frequencia_crimes, x='quantidade', y='tipo_crime', palette='viridis', dodge=False)
            plt.title("Frequência de Crimes Noturnos", fontsize=12)
            plt.xlabel("Quantidade", fontsize=10)
            plt.ylabel("Tipo de Crime", fontsize=10)
            plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            st.pyplot(plt.gcf())
            st.download_button(
                label="📥 Exportar Gráfico de Crimes Noturnos",
                data=exportar_grafico(plt.gcf()),
                file_name=f"grafico_noturno_barras_{hora_selecionada}.png",
                mime="image/png"
            )
            plt.close()
        
        with col2:
            plt.figure(figsize=(6, 4))
            plt.pie(frequencia_crimes['quantidade'], labels=frequencia_crimes['tipo_crime'], autopct='%1.1f%%', startangle=90)
            plt.title("Distribuição de Crimes Noturnos", fontsize=12)
            plt.axis('equal')
            plt.tight_layout()
            st.pyplot(plt.gcf())
            st.download_button(
                label="📥 Exportar Gráfico de Pizza",
                data=exportar_grafico(plt.gcf()),
                file_name=f"grafico_noturno_pizza_{hora_selecionada}.png",
                mime="image/png"
            )
            plt.close()
        
        st.markdown(f"**Crimes noturnos:** {len(crimes_noturnos)} ({(len(crimes_noturnos)/len(df)*100):.2f}%)")
        st.dataframe(frequencia_crimes[['tipo_crime', 'quantidade', 'porcentagem']].style.format({'porcentagem': '{:.2f}%'}))
    
    # 8. Distribuição de Idade
    with st.expander("👶 Distribuição de Crimes por Idade", expanded=True):
        df_idade = df_filtrado['idade'].dropna().astype(int)
        
        plt.figure(figsize=(10, 4))
        sns.histplot(df_idade, bins=20, kde=True, color='teal')
        plt.title("Distribuição de Crimes por Idade", fontsize=12)
        plt.xlabel("Idade", fontsize=10)
        plt.ylabel("Quantidade", fontsize=10)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        st.download_button(
            label="📥 Exportar Gráfico de Idade",
            data=exportar_grafico(plt.gcf()),
            file_name=f"grafico_idade_{hora_selecionada}.png",
            mime="image/png"
        )
        plt.close()
    
    # 9. Tendência Anual de Crimes
    with st.expander("📅 Tendência de Crimes por Ano", expanded=True):
        df['ano'] = pd.to_datetime(df['data']).dt.year
        crimes_por_ano = df_filtrado['ano'].value_counts().sort_index()
        
        plt.figure(figsize=(10, 4))
        sns.lineplot(x=crimes_por_ano.index, y=crimes_por_ano.values, marker='o', color='skyblue')
        plt.title("Tendência de Crimes por Ano", fontsize=12)
        plt.xlabel("Ano", fontsize=10)
        plt.ylabel("Quantidade", fontsize=10)
        plt.grid(linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        st.download_button(
            label="📥 Exportar Gráfico de Ano",
            data=exportar_grafico(plt.gcf()),
            file_name=f"grafico_ano_{hora_selecionada}.png",
            mime="image/png"
        )
        plt.close()
    with st.expander("🌍 Mapa de Correlação", expanded=True):
        from scipy.stats import f_oneway
        import numpy as np

        def correlation_ratio(categories, measurements):
            # Garantir que measurements seja numérico
            measurements = pd.to_numeric(measurements, errors='coerce')
            
            # Remover valores nulos
            valid_idx = ~np.isnan(measurements)
            categories = categories[valid_idx]
            measurements = measurements[valid_idx]
            
            # Agrupar idades por tipo de crime
            groups = [measurements[categories == c] for c in np.unique(categories)]
            
            # Verificar se todos os grupos têm pelo menos uma amostra
            groups = [g for g in groups if len(g) > 0]
            
            if len(groups) < 2:
                return 0  # Não é possível calcular com apenas um grupo
            
            # Calcular F e variâncias
            f, _ = f_oneway(*groups)
            SS_total = np.sum((measurements - np.mean(measurements))**2)
            SS_between = np.sum([len(g) * (np.mean(g) - np.mean(measurements))**2 for g in groups])
            
            return SS_between / SS_total
        # Garantir que idade seja numérica
        df['idade'] = pd.to_numeric(df['idade'], errors='coerce')

        # Alinhar categorias e medidas
        df_clean = df[['tipo_crime', 'idade']].dropna()
        categorias = df_clean['tipo_crime']
        idades = df_clean['idade']

        # Calcular correlation ratio
        print("Correlation Ratio (idade vs tipo_crime):", correlation_ratio(categorias, idades))
        # Função para calcular correlação entre qualquer par de colunas
        from scipy.stats import chi2_contingency

        # Calcular Cramér's V
        def cramers_v(x, y):
            confusion_matrix = pd.crosstab(x, y)
            chi2 = chi2_contingency(confusion_matrix)[0]
            n = confusion_matrix.sum().sum()
            phi2 = chi2 / n
            r, k = confusion_matrix.shape
            return np.sqrt(phi2 / min(k-1, r-1))

        print("Cramér’s V (tipo_crime vs rua):", cramers_v(df['tipo_crime'], df['rua']))
        def mixed_correlation(df):
            cols = df.columns
            result = pd.DataFrame(index=cols, columns=cols)
            
            for col1 in cols:
                for col2 in cols:
                    if pd.api.types.is_numeric_dtype(df[col1]) and pd.api.types.is_numeric_dtype(df[col2]):
                        # Correlação de Pearson
                        result.loc[col1, col2] = df[[col1, col2]].corr().iloc[0, 1]
                    elif (pd.api.types.is_categorical_dtype(df[col1]) or df[col1].dtype == 'object') and (pd.api.types.is_numeric_dtype(df[col2])):
                        # Correlation Ratio (categórico vs numérico)
                        result.loc[col1, col2] = correlation_ratio(df[col1], df[col2])
                    elif (pd.api.types.is_numeric_dtype(df[col1])) and (pd.api.types.is_categorical_dtype(df[col2]) or df[col2].dtype == 'object'):
                        # Correlation Ratio (numérico vs categórico)
                        result.loc[col1, col2] = correlation_ratio(df[col2], df[col1])
                    else:
                        # Cramér’s V (categórico vs categórico)
                        result.loc[col1, col2] = cramers_v(df[col1], df[col2])
            return result.astype(float)
        # Limpar dados
        df_clean = df[["latitude","longitude",'tipo_crime', 'rua', 'tipo_dia', 'idade', 'ano',"hora"]].dropna()

        # Calcular correlação mista
        mixed_corr = mixed_correlation(df_clean)

        # Plotar heatmap
        plt.figure(figsize=(8, 6))
        sns.heatmap(mixed_corr, annot=True, cmap='coolwarm', fmt='.2f')
        plt.title("Mapa de Calor de Correlação (Numéricas e Categóricas)")
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.close()

    # 10. Mapa Dinâmico por Hora
    with st.expander("🗺️ Mapa de Crimes", expanded=True):
        mapa = folium.Map(location=[-15.7942, -47.8825], zoom_start=13, tiles='CartoDB positron')
        
        # Adicionar marcadores com cluster
        if not df_filtrado.empty:
            marker_cluster = MarkerCluster().add_to(mapa)
            for _, row in df_filtrado.sample(n=min(500, len(df_filtrado)), random_state=42).iterrows():
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=f"{row['tipo_crime']} - {row['rua']}",
                    icon=folium.Icon(color='red', icon='info-sign')
                ).add_to(marker_cluster)
            
            # Adicionar heatmap
            heat_data = [[row['latitude'], row['longitude']] for _, row in df_filtrado.iterrows()]
            HeatMap(heat_data, radius=15, blur=20, max_zoom=16).add_to(mapa)
            
            # Adicionar clusters espaciais com DBSCAN
            coords = df_filtrado[['latitude', 'longitude']].values
            if len(coords) >= 5:
                db = DBSCAN(eps=0.003, min_samples=5).fit(coords)
                labels = db.labels_
                unique_labels = set(labels)
                
                for label in unique_labels:
                    if label == -1:
                        continue
                    cluster = coords[labels == label]
                    centroid = np.mean(cluster, axis=0)
                    count = len(cluster)
                    folium.CircleMarker(
                        location=[centroid[0], centroid[1]],
                        radius=10,
                        color='darkred',
                        fill=True,
                        fill_color='darkred',
                        popup=f"Cluster com {count} crimes"
                    ).add_to(mapa)
            
            # Mostrar hora no mapa (se não for Geral)
            if hora_selecionada != "Geral":
                folium.Marker(
                    location=[-15.7942, -47.8825],
                    icon=folium.DivIcon(html=f'<div style="font-weight: bold; color: red; font-size: 16px;">{hora_selecionada}h</div>')
                ).add_to(mapa)
            else:
                folium.Marker(
                    location=[-15.7942, -47.8825],
                    icon=folium.DivIcon(html=f'<div style="font-weight: bold; color: red; font-size: 16px;">Todos os Horários</div>')
                ).add_to(mapa)
            
            folium_static(mapa, width=1000, height=500)
    st.markdown("### 🔍 **Insights Principais**")
    st.markdown("- Crimes noturnos (19h–4h): 67.7% dos registros")
    st.markdown("- Regiões de alto risco: Novo Setor 1, W3 Sul")
    st.markdown("- Crimes graves (homicídio/tráfico) mais comuns entre 21h e 23h")
    st.markdown("- Jovens (14–25 anos) mais envolvidos em tráfico e homicídio")
    st.markdown("- Há dados nulos que precisam ser tratados")
    st.markdown("- necessário tratar os valores de hora que eram string para numérico")
    st.markdown("- necessário tratar vários valores strings para que a IA seja eficaz")
    st.markdown("- Horário influencia na quantidade de crime e tipo de crime")
    st.markdown("- uma área é a mais perigosa, a quadra 108 Sul")


# Aba 2: Pré-processamento
with tab2:
    st.header("🧹 Pré-processamento de Dados")
    st.markdown("""
    ### **Estratégias Adotadas**
    - **Remoção de Colunas Irrelevantes**:  
      - `__ERRO__` e `null` excluídas pois não possuem informações úteis.
    - **Tratamento de Valores Ausentes**:
      - `tipo_crime`: Preenchidos com a **moda** (`furto`, ~1% ausentes).
      - `idade`: Preenchida com a **mediana** (24 anos).
      - `endereco`: Substituído por `"Desconhecido"` (2709 ausências).
      - `email` e `telefone`: Mantidos como `NaN` (~20% e ~7% ausentes).
    - **Codificação de Variáveis Categóricas**:
      - `tipo_crime` e `tipo_dia`: Convertidos via **One-Hot Encoding**.
    - **Normalização de Variáveis Numéricas**:
      - `hora`, `idade`, `risco`: Normalizados com **StandardScaler**.
    - **Objetivo**: Garantir dados limpos e padronizados para modelos de regressão espacial e detecção de padrões.
    """)

    # Mostrar dados brutos
    st.subheader("Primeras Linhas do Dataset Bruto")
    st.dataframe(df.head(10))

    # Valores ausentes antes do tratamento
    st.subheader("Valores Ausentes (Bruto)")
    st.write(df.isna().sum())

    # Tratamento de valores ausentes
    st.subheader("Valores Ausentes (Após Tratamento)")
    df_processado = df.copy()
    
    # Remover colunas irrelevantes
    df_processado.drop(columns=["__ERRO__", "null"], inplace=True)
    
    # Preencher nulos com moda ou mediana
    df_processado['tipo_crime'] = df_processado['tipo_crime'].fillna(df_processado['tipo_crime'].mode()[0])
    df_processado['idade'] = df_processado['idade'].fillna(df_processado['idade'].median())
    df_processado['endereco'] = df_processado['endereco'].fillna("Desconhecido")
    # Deixar email e telefone como NaN se já estiverem assim
    
    # Mostrar valores após tratamento
    st.write(df_processado.isna().sum())

    # Codificação de variáveis categóricas (One-Hot Encoding)
    st.subheader("Codificação de Variáveis Categóricas")
    categorical_cols = ['tipo_crime', 'tipo_dia']
    df_processado = pd.get_dummies(df_processado, columns=categorical_cols, drop_first=True)
    st.code("""
    df = pd.get_dummies(df, columns=['tipo_crime', 'tipo_dia'], drop_first=True)
    """, language='python')
    st.markdown("#### Exemplo das variáveis codificadas:")
    st.dataframe(df_processado[[col for col in df_processado.columns if 'tipo_crime' in col or 'tipo_dia' in col]].head(10))

    # Normalização de variáveis numéricas
    st.subheader("Normalização de Variáveis Numéricas")
    numeric_features = ['hora', 'idade', 'risco']
    
    from sklearn.preprocessing import StandardScaler
    df_processado[numeric_features] = StandardScaler().fit_transform(df_processado[numeric_features])
    
    st.code("""
    from sklearn.preprocessing import StandardScaler
    df[numeric_features] = StandardScaler().fit_transform(df[numeric_features])
    """, language='python')
    st.markdown("#### Exemplo das variáveis normalizadas:")
    st.dataframe(df_processado[numeric_features].head(10).style.format("{:.2f}"))

    # Codificação de `endereco` (alta cardinalidade) usando factorize
    st.subheader("Codificação de Variáveis com Alta Cardinalidade")
    st.markdown("""
    Para variáveis como `endereco`, que têm alta cardinalidade, usamos codificação numérica simples:
    ```python
    df['endereco_code'] = df['endereco'].astype('category').cat.codes
    ```
    Isso evita explosão dimensional com One-Hot Encoding.
    """)
    df_processado['endereco_code'] = df_processado['endereco'].astype('category').cat.codes
    df_processado.drop(columns=['endereco'], inplace=True)  # opcional: remover original após codificação
    st.markdown("#### Exemplo da nova feature codificada:")
    st.dataframe(df_processado[['endereco_code']].head(10))

    # Mapa de correlação entre features
    st.subheader("Matriz de Correlação entre Features")
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_processado.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Mapa de Calor de Correlação entre Features")
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.close()

    # Estatísticas descritivas
    st.subheader("Estatísticas Descritivas")
    st.write(df_processado.describe())

    # Exportação de dados processados
    st.download_button(
        label="📥 Exportar Dados Processados",
        data=df_processado.to_csv(index=False).encode('utf-8'),
        file_name="crimes_processados.csv",
        mime="text/csv"
    )

# Aba 3: Teste de Modelo (placeholder)
with tab3:
    st.header("🧪 Teste de Modelo")
    
    # Seletor de modelo
    modelo_selecionado = st.selectbox(
        "Selecione o Modelo", 
        ["Random Forest", "XGBoost"]
    )
    
    # Botão para treinamento (evita executar automático)
    if st.button("Treinar e Avaliar Modelo"):
        # Definir variáveis categóricas e numéricas
        categorical_features = ['tipo_crime', 'tipo_dia']
        numeric_features = ['hora', 'idade', 'risco']
        
        # Pipeline de pré-processamento
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ])
        
        # Aplicar pré-processamento
        X = df[['hora', 'idade', 'risco', 'tipo_crime', 'tipo_dia']]
        y = df[['latitude', 'longitude']]
        X_processed = preprocessor.fit_transform(X)
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=0.2, random_state=42
        )
        
        # Treinar modelos
        if modelo_selecionado == "Random Forest":
            model = RandomForestRegressor(
                n_estimators=287,
                max_depth=10,
                min_samples_split=9,
                min_samples_leaf=1,
                random_state=42
            )
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            
        elif modelo_selecionado == "XGBoost":
            model = XGBRegressor(
                n_estimators=289,
                max_depth=3,
                learning_rate=0.0971,
                subsample=0.8934,
                colsample_bytree=0.9926,
                random_state=42
            )
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
        
        # Cálculo das métricas
        mse = mean_squared_error(y_test, preds)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        
        # Exibir métricas
        st.subheader("Métricas do Modelo")
        st.markdown(f"**Modelo**: {modelo_selecionado}")
        st.markdown(f"**MSE (Erro Quadrático Médio)**: {mse:.6f}")
        st.markdown(f"**MAE (Erro Absoluto Médio)**: {mae:.6f}")
        st.markdown(f"**R² (Coeficiente de Determinação)**: {r2:.4f}")
        
        # Criar DataFrame de resultados
        df_resultados = pd.DataFrame({
            'real_lat': y_test.iloc[:, 0],
            'real_lon': y_test.iloc[:, 1],
            'pred_lat': preds[:, 0],
            'pred_lon': preds[:, 1]
        })
        
        # Calcular erro em metros
        def calcular_erro_metros(lat1, lon1, lat2, lon2):
            R = 6371e3  # Raio da Terra em metros
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
            a = np.sin((lat2 - lat1)/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1)/2)**2
            c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
            return R * c
        
        df_resultados['distancia_metros'] = calcular_erro_metros(
            df_resultados['real_lat'], df_resultados['real_lon'],
            df_resultados['pred_lat'], df_resultados['pred_lon']
        )
        
        # Exibir amostra dos resultados
        st.subheader("📊 Predições vs Reais")
        st.dataframe(df_resultados.head(10))
        
        # Estatísticas do erro
        st.markdown(f"**Erro Médio**: {df_resultados['distancia_metros'].mean():.2f} m")
        st.markdown(f"**Erro Máximo**: {df_resultados['distancia_metros'].max():.2f} m")
        
        # Botão para download do CSV
        st.download_button(
            label="📥 Exportar Predições como CSV",
            data=df_resultados.to_csv(index=False).encode('utf-8'),
            file_name=f"previsoes_{modelo_selecionado.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )
        
        # Gráfico de dispersão (Latitude Real vs Preditos)
        st.subheader("📈 Dispersão de Predições")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(df_resultados['real_lat'], df_resultados['pred_lat'], alpha=0.6, color='blue')
        ax.plot([df_resultados['real_lat'].min(), df_resultados['real_lat'].max()],
                [df_resultados['real_lat'].min(), df_resultados['real_lat'].max()], 
                'r--', label='Ideal')
        ax.set_xlabel("Latitude Real")
        ax.set_ylabel("Latitude Preditos")
        ax.legend()
        st.pyplot(fig)
        
        # Gráfico de dispersão (Longitude Real vs Preditos)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.scatter(df_resultados['real_lon'], df_resultados['pred_lon'], alpha=0.6, color='green')
        ax.plot([df_resultados['real_lon'].min(), df_resultados['real_lon'].max()],
                [df_resultados['real_lon'].min(), df_resultados['real_lon'].max()], 
                'r--', label='Ideal')
        ax.set_xlabel("Longitude Real")
        ax.set_ylabel("Longitude Preditos")
        ax.legend()
        st.pyplot(fig)