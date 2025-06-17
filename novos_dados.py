import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
from faker import Faker
from sklearn.cluster import DBSCAN

fake = Faker('pt_BR')

# Função para gerar coordenadas com clusters dinâmicos (variação diária)
def gerar_variacao(lat_base, lon_base):
    lat = lat_base + random.uniform(-0.005, 0.005)  # Variação de 500 metros
    lon = lon_base + random.uniform(-0.005, 0.005)
    return lat, lon

# Coordenadas dos setores da Asa Sul (base fixa, mas com variação dinâmica)
setores_base = {
    "Eixo L Sul": (-15.8260, -47.9120),
    "W3 Sul": (-15.817760, -47.913787),
    "L2 Sul": (-15.8300, -47.9080),
    "Novo Setor 1": (-15.808346, -47.891342),
    "CLS 208": (-15.8280, -47.9050),
    "SQS 108": (-15.806983, -47.899453),
    "SQS 104": (-15.800748, -47.893874),
    "W4 Sul": (-15.811360, -47.904775)
}

# Pesos de tipos de crime por horário
pesos_tipos_por_hora = {
    'manha': [40, 25, 5, 10, 15, 5],  # 6h–11h
    'tarde': [30, 30, 10, 15, 10, 5],  # 12h–17h
    'noite': [20, 20, 25, 25, 5, 5],   # 18h–5h
    'madrugada': [15, 15, 30, 30, 5, 5]  # 0h–5h
}

# Função para escolher tipo de crime baseado na hora
def escolher_tipo_crime(hora):
    if 6 <= hora < 12:
        return random.choices(tipos_crime, weights=pesos_tipos_por_hora['manha'], k=1)[0]
    elif 12 <= hora < 18:
        return random.choices(tipos_crime, weights=pesos_tipos_por_hora['tarde'], k=1)[0]
    elif 18 <= hora or hora < 3:
        return random.choices(tipos_crime, weights=pesos_tipos_por_hora['noite'], k=1)[0]
    else:
        return random.choices(tipos_crime, weights=pesos_tipos_por_hora['madrugada'], k=1)[0]

# Função para gerar data/hora com distribuição natural
def random_datetime():
    start = datetime(2020, 1, 1)
    end = datetime(2025, 12, 31)
    delta_days = (end - start).days
    # Distribuição normal com leve viés noturno (média 20h, desvio 5h)
    hora = int(np.random.normal(loc=20, scale=5)) % 24
    return start + timedelta(
        days=random.randint(0, delta_days),
        hours=hora,
        minutes=random.randint(0, 59)
    )

# Feriados fictícios
feriados = [
    "2020-04-10", "2020-04-12", "2020-04-21", "2020-05-01",
    "2020-09-07", "2020-10-12", "2020-11-02", "2020-11-15", "2020-12-25"
] * 5  # Repetir para cobrir todos os anos

# Tipos de crime
tipos_crime = ["furto", "roubo", "homicídio", "tráfico", "vandalismo", "feminicídio"]

# Endereços típicos da Asa Sul
enderecos_asa_sul = [
    "{rua} Bloco {bloco}, Ap {num}",
    "{rua} Lote {lote}, Sala {sala}",
    "{rua} Edifício {edificio}, Unidade {unidade}"
]
blocos = ["A", "B", "C", "D"]
lotes = list(range(1, 50))
salas = list(range(100, 300))
edificios = ["Alpha", "Bravo", "Delta", "Omega", "Prime", "Center"]
unidades = list(range(101, 250))

# Probabilidade de crime por setor e tipo de dia (dia_normal, final_semana, feriado)
prob_por_setor = {
    "Eixo L Sul": {
        "dia_normal": 1.0,
        "final_semana": 1.2,
        "feriado": 0.8
    },
    "W3 Sul": {
        "dia_normal": 1.0,
        "final_semana": 1.5,
        "feriado": 0.5
    },
    "L2 Sul": {
        "dia_normal": 1.0,
        "final_semana": 0.8,
        "feriado": 1.3
    },
    "Novo Setor 1": {
        "dia_normal": 1.0,
        "final_semana": 1.1,
        "feriado": 1.5
    },
    "CLS 208": {
        "dia_normal": 1.0,
        "final_semana": 0.7,
        "feriado": 0.5
    },
    "SQS 108": {
        "dia_normal": 1.0,
        "final_semana": 1.3,
        "feriado": 0.7
    },
    "SQS 104": {
        "dia_normal": 1.0,
        "final_semana": 0.9,
        "feriado": 0.6
    },
    "W4 Sul": {
        "dia_normal": 1.0,
        "final_semana": 1.4,
        "feriado": 0.8
    }
}

# Geração dos dados
num_registros = 30000
data = []

for _ in range(num_registros):
    data_hora = random_datetime()
    data_str = data_hora.strftime('%Y-%m-%d')
    hora = data_hora.hour
    dia_semana = data_hora.weekday()  # 0–6 (seg–dom)
    
    # Verificar tipo de dia
    if dia_semana in [4, 5]:  # sexta (4), sábado (5)
        tipo_dia = 'final_semana'
    elif data_str in feriados:
        tipo_dia = 'feriado'
    else:
        tipo_dia = 'dia_normal'

    # Escolher tipo de crime com base na hora
    tipo = escolher_tipo_crime(hora)

    # Escolher setor com base no tipo de dia (dinâmico)
    setores_possiveis = list(setores_base.keys())
    pesos_setor = [prob_por_setor[setor][tipo_dia] for setor in setores_possiveis]
    setor_aleatorio = random.choices(setores_possiveis, weights=pesos_setor, k=1)[0]

    # Gerar variação diária para simular mudança de padrão
    lat_base, lon_base = setores_base[setor_aleatorio]
    lat, lon = gerar_variacao(lat_base, lon_base, escala=0.007)

    # Gerar idade com maior incidência em 14–23 e 60–70
    if random.random() < 0.5:
        idade = random.randint(14, 23)
    elif random.random() < 0.2:
        idade = random.randint(60, 70)
    else:
        idade = random.randint(7, 90)

    # Gerar nome completo e CPF
    nome = fake.name()
    cpf_formatado = fake.cpf()

    # Gerar endereço personalizado
    formato = random.choice(enderecos_asa_sul)
    if "{bloco}" in formato:
        endereco = formato.format(rua=setor_aleatorio, bloco=random.choice(blocos), num=random.randint(100, 999))
    elif "{lote}" in formato:
        endereco = formato.format(rua=setor_aleatorio, lote=random.choice(lotes), sala=random.choice(salas))
    elif "{edificio}" in formato:
        endereco = formato.format(rua=setor_aleatorio, edificio=random.choice(edificios), unidade=random.choice(unidades))

    # Gerar email e telefone
    email = fake.email()
    telefone = fake.phone_number()

    data.append({
        'latitude': lat,
        'longitude': lon,
        'data': data_str,
        'hora': data_hora.strftime('%H:%M'),
        'tipo_crime': tipo,
        'bairro': 'Asa Sul',
        'rua': setor_aleatorio,
        'tipo_dia': tipo_dia,
        'ano': data_hora.year,
        'nome': nome,
        'cpf': cpf_formatado,
        'idade': idade,
        'email': email,
        'telefone': telefone,
        'endereco': endereco
    })

# Criar DataFrame e salvar CSV
df = pd.DataFrame(data)

df["__ERR0O0__"] = "ERRO_404"#Coluna adicionada para ser tratada na Análise exploratória
df["null"] = np.nan
df.to_csv('crime_segunda_area.csv', index=False)
print("✅ Arquivo 'crime_segunda_area.csv' criado com pontos variados e realistas!")