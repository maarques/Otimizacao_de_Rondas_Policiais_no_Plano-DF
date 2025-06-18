import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
from faker import Faker

fake = Faker('pt_BR')

# Na função random_datetime()
def random_datetime():
    start = datetime(2020, 1, 1)
    end = datetime(2025, 12, 31)
    delta_days = (end - start).days

    # Distribuição normal com leve viés noturno (média 19h, desvio 5h)
    hora = int(np.random.normal(loc=23, scale=5)) % 24  # Média 23h, desvio 5h
    return start + timedelta(
        days=random.randint(0, delta_days),
        hours=hora,
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

# Tipos de crime com pesos mais equilibrados
tipos_crime = ["furto", "roubo", "homicídio", "tráfico", "vandalismo", "feminicídio"]
pesos_tipos = {
    'dia_normal': [30, 20, 10, 15, 20, 5],  # Distribuição mais equilibrada
    'final_semana': [25, 20, 15, 20, 15, 5],
    'feriado': [20, 15, 20, 25, 15, 5]
}

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

# Coordenadas dos setores da Asa Sul (com variação espacial)
setores_asa_sul = {
    "Eixo L Sul": [
        (-15.8260, -47.9120),  # Centro do Eixo L Sul
        (-15.8247, -47.9100),  # Próximo ao Clube do Exército
        (-15.8285, -47.9140),  # Região da Praça dos Três Poderes
        (-15.8220, -47.9080)   # Área comercial da Asa Sul
    ],
    "W3 Sul": [
        (-15.817760, -47.913787),  # SQS 314
        (-15.814581, -47.909281),  # SQS 212
        (-15.811360, -47.904775),  # SQS 112
        (-15.806983, -47.899453),  # SQS 108
        (-15.800748, -47.893874),  # SQS 104
        (-15.816951, -47.902616),  # Centro da W3 Sul
        (-15.817344, -47.907337),  # Expansão leste
        (-15.818286, -47.899531)   # Sul da W3 Sul
    ],
    "L2 Sul": [
        (-15.8300, -47.9080),  # Centro da L2 Sul
        (-15.8280, -47.9050),  # Próximo à CLS 208
        (-15.8250, -47.9020),  # Região comercial
        (-15.8220, -47.8990),  # Área residencial
        (-15.821972, -47.920525),  # Centro-norte da L2 Sul
        (-15.831757, -47.921340),  # Extremo norte da L2 Sul
        (-15.824573, -47.925245)   # Nordeste da L2 Sul
    ],
    "Novo Setor 1": [  # Áreas com alta densidade
        (-15.808346, -47.891342),  # Ponto central
        (-15.8100, -47.8950),      # Sudoeste
        (-15.8050, -47.8850),      # Sul
        (-15.804471, -47.891790),  # Sudoeste
        (-15.816681, -47.901966),  # Centro-oeste
        (-15.809755, -47.884687),  # Sul do setor
        (-15.815680, -47.901966)   # Leste do Novo Setor 1
    ]
}

# Função para gerar variação espacial
def gerar_variacao(lat_base, lon_base):
    lat = lat_base + random.uniform(-0.007, 0.007)  # Variação de 700 metros
    lon = lon_base + random.uniform(-0.007, 0.007)
    return lat, lon

# Geração dos dados
num_registros = 30000
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

    # Ajuste de horário: aumentar chance de crime entre 21h e 3h
    if 21 <= hora or hora <= 3:  # Agora focado nas 21h–3h
        if tipo in ['homicídio', 'tráfico']:
            tipo = random.choice([tipo] * 5 + random.choices(tipos_crime, weights=pesos_tipos[tipo_dia], k=2))  # Priorizar mais

    # Gerar nome completo e CPF com Faker
    nome = fake.name()
    cpf_formatado = fake.cpf()

    # Idade com maior incidência em 14–23 e 60–75
    if random.random() < 0.5:
        idade = random.randint(14, 23)
    elif random.random() < 0.2:
        idade = random.randint(60, 75)
    else:
        idade = random.randint(7, 90)

    # Escolher setor aleatório na Asa Sul
    via_aleatoria = random.choice(list(setores_asa_sul.keys()))
    lat_base, lon_base = random.choice(setores_asa_sul[via_aleatoria])
    lat, lon = gerar_variacao(lat_base, lon_base)
    rua = via_aleatoria

    # Gerar endereço personalizado
    formato = random.choice(enderecos_asa_sul)
    if "{bloco}" in formato:
        endereco = formato.format(rua=rua, bloco=random.choice(blocos), num=random.randint(100, 999))
    elif "{lote}" in formato:
        endereco = formato.format(rua=rua, lote=random.choice(lotes), sala=random.choice(salas))
    elif "{edificio}" in formato:
        endereco = formato.format(rua=rua, edificio=random.choice(edificios), unidade=random.choice(unidades))

    # Gerar email e telefone
    email = fake.email()
    telefone = fake.phone_number()

    # Inserir NaN esporadicamente (Dependendo da coluna)
    if random.random() < 0.03:
        nome = np.nan
    if random.random() < 0.08:
        idade = np.nan
    if random.random() < 0.01:
        tipo = np.nan
    if random.random() < 0.2:
        email = np.nan
    if random.random() < 0.07:
        telefone = np.nan
    if random.random() < 0.09:
        endereco = np.nan

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
print("✅ Arquivo 'crime_segunda_area.csv' criado com sucesso!")