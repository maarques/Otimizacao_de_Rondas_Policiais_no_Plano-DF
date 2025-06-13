import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

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

# Nomes fictícios (curtos, comuns no DF)
nomes = ["João Silva", "Ana Maria", "Carlos Oliveira", "Mariana Costa", "Lucas Almeida",
         "Fernanda Lima", "Rafael Souza", "Tatiane Santos", "Bruno Rodrigues", "Aline Moura"]

sobrenomes = ["Silva", "Souza", "Oliveira", "Costa", "Almeida", "Lima", "Rodrigues", "Santos", "Pereira", "Carvalho"]

# Tipos de crime com pesos ajustáveis
tipos_crime = ["furto", "roubo", "homicídio", "tráfico", "vandalismo", "feminicídio"]
pesos_tipos = {
    'dia_normal': [30, 20, 5, 15, 20, 5],
    'final_semana': [25, 25, 10, 20, 15, 5],
    'feriado': [20, 30, 15, 20, 10, 5]
}

# Regiões mais perigosas (zonas quentes dentro da Asa Sul)
zonas_quentes = {
    "SQS 105": (-15.7932, -47.8815),
    "SQS 106": (-15.7912, -47.8830),
    "W3 Sul": (-15.7950, -47.8800)
}

ruas_comuns = ["CLS 403", "SQS 104", "SQS 107", "SQS 108"]
lat_central = -15.7942
lon_central = -47.8825

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

    # Gerar nome aleatório
    nome = random.choice(nomes) + " " + random.choice(sobrenomes)

    # Gerar CPF do Distrito Federal (primeiro dígito 0)
    cpf = f"0{random.randint(100_000_000, 199_999_999)}"

    # Calcular dígitos verificadores (opcionalmente simplificado)
    def calcular_digitos(cpf_base):
        def calcula_digito(d):
            soma = sum(int(i)*d for i, d in zip(cpf_base, range(len(cpf_base)+1, 1, -1)))
            resto = soma % 11
            return str(0 if resto < 2 else 11 - resto)
        cpf_base += calcula_digito(cpf_base)
        cpf_base += calcula_digito(cpf_base)
        return f"{cpf_base[:3]}.{cpf_base[3:6]}.{cpf_base[6:9]}-{cpf_base[9:]}"
    
    cpf_formatado = calcular_digitos(cpf)

    # Idade com maior incidência em 14–23 e 60–70
    if random.random() < 0.7:
        idade = random.randint(14, 23)
    elif random.random() < 0.2:
        idade = random.randint(60, 70)
    else:
        idade = random.randint(7, 90)

    # Escolher localização com base em zonas quentes
    if random.random() < 0.6:
        rua, (lat_base, lon_base) = random.choice(list(zonas_quentes.items()))
        lat = lat_base + random.uniform(-0.001, 0.001)
        lon = lon_base + random.uniform(-0.001, 0.001)
    else:
        rua = random.choice(ruas_comuns)
        lat = lat_central + random.uniform(-0.005, 0.005)
        lon = lon_central + random.uniform(-0.005, 0.005)

    # Inserir NaN esporadicamente (~5% dos registros)
    if random.random() < 0.05:
        nome = np.nan
    if random.random() < 0.05:
        idade = np.nan
    if random.random() < 0.05:
        tipo = np.nan
    if random.random() < 0.05:
        hora = np.nan

    data.append({
        'latitude': lat,
        'longitude': lon,
        'data': data_str,
        'hora': data_hora.strftime('%H:%M') if not isinstance(hora, float) else np.nan,
        'tipo_crime': tipo,
        'bairro': 'Asa Sul',
        'rua': rua,
        'tipo_dia': tipo_dia,
        'ano': data_hora.year,
        'nome': nome,
        'cpf': cpf_formatado,
        'idade': idade
    })

# Criar DataFrame e salvar CSV
df = pd.DataFrame(data)
df.to_csv('crimes_asa_sul_2020_2025_com_pessoas.csv', index=False)
print("✅ Arquivo 'crimes_asa_sul_2020_2025_com_pessoas.csv' criado com sucesso!")