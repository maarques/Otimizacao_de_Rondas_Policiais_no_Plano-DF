import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
from faker import Faker

fake = Faker('pt_BR')

# Função para gerar data/hora entre 2020 e 2025
def random_datetime():
    start = datetime(2020, 1, 1)
    end = datetime(2025, 12, 31)
    delta_days = (end - start).days
    return start + timedelta(
        days=random.randint(0, delta_days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

# Feriados fictícios (exemplo dos anos de 2020 a 2025 em Brasília)
feriados = [
    "2020-04-10", "2020-04-12", "2020-04-21", "2020-05-01", "2020-09-07", "2020-10-12", "2020-11-02", "2020-11-15", "2020-12-25",
    "2021-04-02", "2021-04-04", "2021-04-21", "2021-05-01", "2021-09-07", "2021-10-12", "2021-11-02", "2021-11-15", "2021-12-25",
    "2022-04-15", "2022-04-17", "2022-04-21", "2022-05-01", "2022-09-07", "2022-10-12", "2022-11-02", "2022-11-15", "2022-12-25",
    "2023-04-07", "2023-04-09", "2023-04-21", "2023-05-01", "2023-09-07", "2023-10-12", "2023-11-02", "2023-11-15", "2023-12-25",
    "2024-03-29", "2024-03-31", "2024-04-21", "2024-05-01", "2024-09-07", "2024-10-12", "2024-11-02", "2024-11-15", "2024-12-25",
    "2025-04-18", "2025-04-20", "2025-04-21", "2025-05-01", "2025-09-07", "2025-10-12", "2025-11-02", "2025-11-15", "2025-12-25"
]

# Tipos de crime com pesos ajustáveis
tipos_crime = ["furto", "roubo", "homicídio", "tráfico", "vandalismo", "feminicídio"]
pesos_tipos = {
    'dia_normal': [30, 20, 5, 15, 20, 5],
    'final_semana': [25, 25, 10, 20, 15, 5],
    'feriado': [20, 30, 15, 20, 10, 5]
}

# Geração dos dados
num_registros = 15000
data = []

for _ in range(num_registros):
    data_hora = random_datetime()
    data_str = data_hora.strftime('%Y-%m-%d')
    hora = data_hora.hour

    # Verificar se é final de semana ou feriado
    if data_hora.weekday() in [4, 5]:  # sexta (4), sábado (5)
        tipo_dia = 'final_semana'
    elif data_str in feriados:
        tipo_dia = 'feriado'
    else:
        tipo_dia = 'dia_normal'

    # Peso de tipos de crime conforme o dia
    tipo = random.choices(tipos_crime, weights=pesos_tipos[tipo_dia], k=1)[0]

    # Ajuste de horário: aumentar chance de crime entre 20h e 3h
    if 20 <= hora or hora < 3:
        if tipo in ['homicídio', 'tráfico']:
            tipo = random.choice([tipo] * 3 + random.choices(tipos_crime, k=1))

    # Gerar nome completo e CPF com Faker
    nome = fake.name()
    cpf_formatado = fake.cpf()

    # Idade com maior incidência em 14–23 e 60–70
    if random.random() < 0.7:
        idade = random.randint(14, 23)
    elif random.random() < 0.2:
        idade = random.randint(60, 70)
    else:
        idade = random.randint(7, 90)

    # Gerar coordenadas aleatórias na área destacada
    lat = round(random.uniform(-15.8000, -15.7800), 6)  # Latitude
    lon = round(random.uniform(-47.8900, -47.8700), 6)  # Longitude

    # Adicionar pequena variação para evitar pontos exatos repetidos
    lat += random.uniform(-0.0005, 0.0005)
    lon += random.uniform(-0.0005, 0.0005)

    # Simular ruas aleatórias dentro da Asa Sul
    rua = f"SQS {random.randint(105, 109)}" if random.random() < 0.6 else f"W{random.choice(['3', '4'])} Sul"

    # Gerar email e telefone
    email = fake.email()
    telefone = fake.phone_number()

    # Inserir NaN esporadicamente (~5% dos registros)
    if random.random() < 0.05:
        nome = np.nan
    if random.random() < 0.05:
        idade = np.nan
    if random.random() < 0.05:
        tipo = np.nan
    if random.random() < 0.05:
        hora = np.nan
    if random.random() < 0.05:
        email = np.nan
    if random.random() < 0.05:
        telefone = np.nan

    data.append({
        'latitude': lat,
        'longitude': lon,
        'data': data_str,
        'hora': data_hora.strftime('%H:%M'),
        'tipo_crime': tipo,
        'bairro': 'Asa Sul',
        'rua': rua,
        'tipo_dia': tipo_dia,
        'ano': data_hora.year,
        'nome': nome,
        'cpf': cpf_formatado,
        'idade': idade,
        'email': email,
        'telefone': telefone
    })

# Criar DataFrame e salvar CSV
df = pd.DataFrame(data)

# Garantir que coordenadas são numéricas
df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

# Remover linhas com coordenadas inválidas
df = df.dropna(subset=['latitude', 'longitude'])

# Salvar o CSV final
df.to_csv('crimes_asa_sul_2020_2025_com_pessoas_endereco2.csv', index=False)
print("✅ Arquivo 'crimes_asa_sul_2020_2025_com_pessoas_endereco.csv' criado com sucesso!")