import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np
from faker import Faker

fake = Faker('pt_BR')

# Zonas proibidas (lagos e parques)
zonas_proibidas = [
    (-15.7900, -47.8790, 0.002),  # Parque Dona Sarah Kubitschek
    (-15.7890, -47.8940, 0.002),  # Lago Parque das Nações
    (-15.7850, -47.8950, 0.002)   # Lago Sul
]

# Pesos por região
crime_pesos_por_regiao = {
    "Eixo L Sul": [35, 25, 10, 15, 25, 10],  # Furto e Vandalismo pesam mais
    "W3 Sul": [20, 20, 15, 35, 10, 10],      # Tráfico e Homicídio pesam mais
    "W4 Sul": [10, 15, 10, 20, 10, 45],       # Feminicídio pesa mais
    "W5 Sul": [10, 15, 35, 30, 10, 10],       # Homicídio e Tráfico pesam mais
    "L2 Sul": [10, 10, 30, 20, 10, 40],       # Homicídio e Feminicídio pesam mais
    "Novo Setor 1": [10, 30, 10, 10, 30, 10], # Roubo e Vandalismo pesam mais
    "Nova Região 1": [25, 10, 5, 15, 30, 5],  # Furto/Vandalismo
    "Nova Região 2": [5, 30, 10, 10, 5, 30],  # Roubo/Furto
    "Nova Região 3": [15, 5, 30, 25, 10, 15]  # Tráfico/Homicídio
}

# Padrões por região
padroes_por_regiao = {
    "W3 Sul": {"idade_min": 14, "idade_max": 25, "crimes_prioritarios": ["tráfico", "homicídio"]},
    "W4 Sul": {"idade_min": 20, "idade_max": 60, "crimes_prioritarios": ["feminicídio", "homicídio"]},
    "W5 Sul": {"idade_min": 14, "idade_max": 30, "crimes_prioritarios": ["tráfico", "roubo"]},
    "Eixo L Sul": {"idade_min": 50, "idade_max": 70, "crimes_prioritarios": ["furto", "vandalismo"]},
    "L2 Sul": {"idade_min": 20, "idade_max": 40, "crimes_prioritarios": ["homicídio", "roubo"]},
    "Novo Setor 1": {"idade_min": 14, "idade_max": 25, "crimes_prioritarios": ["roubo", "vandalismo"]},
    "Nova Região 1": {"idade_min": 18, "idade_max": 35, "crimes_prioritarios": ["furto", "vandalismo"]},
    "Nova Região 2": {"idade_min": 25, "idade_max": 50, "crimes_prioritarios": ["roubo", "furto"]},
    "Nova Região 3": {"idade_min": 16, "idade_max": 30, "crimes_prioritarios": ["tráfico", "homicídio"]}
}

# Feriados fictícios
feriados = [
    "2020-04-10", "2020-04-12", "2020-04-21", "2020-05-01", "2020-09-07", "2020-10-12", "2020-11-02", "2020-11-15", "2020-12-25",
    "2021-04-02", "2021-04-04", "2021-04-21", "2021-05-01", "2021-09-07", "2021-10-12", "2021-11-02", "2021-11-15", "2021-12-25",
    "2022-04-15", "2022-04-17", "2022-04-21", "2022-05-01", "2022-09-07", "2022-10-12", "2022-11-02", "2022-11-15", "2022-12-25",
    "2023-04-07", "2023-04-09", "2023-04-21", "2023-05-01", "2023-09-07", "2023-10-12", "2023-11-02", "2023-11-15", "2023-12-25",
    "2024-03-29", "2024-03-31", "2024-04-21", "2024-05-01", "2024-09-07", "2024-10-12", "2024-11-02", "2024-11-15", "2024-12-25",
    "2025-04-18", "2025-04-20", "2025-04-21", "2025-05-01", "2025-09-07", "2025-10-12", "2025-11-02", "2025-11-15", "2025-12-25"
]

# Tipos de crime e pesos
tipos_crime = ["furto", "roubo", "homicídio", "tráfico", "vandalismo", "feminicídio"]
pesos_tipos = {
    'dia_normal': [30, 20, 10, 15, 20, 5],
    'final_semana': [25, 20, 15, 20, 15, 5],
    'feriado': [20, 15, 20, 25, 15, 5]
}

# Setores da Asa Sul com variação espacial
setores_asa_sul = {
    "Eixo L Sul": [(-15.8260, -47.9120), (-15.8247, -47.9100), (-15.8285, -47.9140), (-15.8220, -47.9080)],
    "W3 Sul": [(-15.817760, -47.913787), (-15.814581, -47.909281), (-15.811360, -47.904775), (-15.806983, -47.899453), (-15.800748, -47.893874), (-15.816951, -47.902616), (-15.817344, -47.907337), (-15.818286, -47.899531)],
    "L2 Sul": [(-15.8300, -47.9080), (-15.8280, -47.9050), (-15.8250, -47.9020), (-15.8220, -47.8990), (-15.821972, -47.920525), (-15.831757, -47.921340), (-15.824573, -47.925245)],
    "Novo Setor 1": [(-15.808346, -47.891342), (-15.8100, -47.8950), (-15.8050, -47.8850), (-15.804471, -47.891790), (-15.816681, -47.901966), (-15.809755, -47.884687), (-15.815680, -47.901966)]
}

# Mapeamento de risco por região
risco_mapa = {
    "W3 Sul": 4,
    "W4 Sul": 5,
    "W5 Sul": 4,
    "Eixo L Sul": 2,
    "L2 Sul": 5,
    "Novo Setor 1": 3,
    "Nova Região 1": 3,
    "Nova Região 2": 2,
    "Nova Região 3": 4
}

# Endereços típicos da Asa Sul
enderecos_asa_sul = ["{rua} Bloco {bloco}, Ap {num}", "{rua} Lote {lote}, Sala {sala}", "{rua} Edifício {edificio}, Unidade {unidade}"]
blocos = ["A", "B", "C", "D"]
lotes = list(range(1, 50))
salas = list(range(100, 300))
edificios = ["Alpha", "Bravo", "Delta", "Omega", "Prime", "Center"]
unidades = list(range(101, 250))

# Função para data/hora noturna
def random_datetime():
    start = datetime(2020, 1, 1)
    end = datetime(2025, 12, 31)
    delta_days = (end - start).days
    hora = int(np.random.normal(loc=23, scale=5)) % 24
    return start + timedelta(days=random.randint(0, delta_days), hours=hora, minutes=random.randint(0, 59))

# Função para variação espacial com base no tipo de crime
def gerar_variacao(lat_base, lon_base, tipo_crime):
    if tipo_crime in ['tráfico', 'homicídio']:
        lat = lat_base + random.uniform(-0.003, 0.003)  # 100m
        lon = lon_base + random.uniform(-0.003, 0.003)
    else:
        lat = lat_base + random.uniform(-0.004, 0.004)  # 200m
        lon = lon_base + random.uniform(-0.004, 0.004)
    return lat, lon

# Função para gerar idade com base na região e tipo de crime
def gerar_idade(rua, tipo_crime):
    padrao = padroes_por_regiao.get(rua, {"idade_min": 14, "idade_max": 70})
    if tipo_crime in padrao.get("crimes_prioritarios", []):
        idade = random.randint(padrao["idade_min"], padrao["idade_max"])
    else:
        if random.random() < 0.4:
            idade = int(np.random.normal(loc=20, scale=5))  # Jovens
        elif random.random() < 0.2:
            idade = int(np.random.normal(loc=65, scale=5))  # Idosos
        else:
            idade = random.randint(7, 90)  # Aleatório
    return min(max(idade, 7), 90)

# Definição de crimes prioritários por região
crimes_regioes_prioritarias = {
    "tráfico": ["W3 Sul", "Nova Região 3"],
    "feminicídio": ["W4 Sul"],
    "roubo": ["Novo Setor 1", "Nova Região 2"],
    "furto": ["Eixo L Sul", "Nova Região 1"],
    "vandalismo": ["Novo Setor 1", "Nova Região 1"],
    "homicídio": ["W3 Sul", "L2 Sul", "Nova Região 3"]
}

# Geração dos dados
num_registros = 30000
data = []

for _ in range(num_registros):
    data_hora = random_datetime()
    data_str = data_hora.strftime('%Y-%m-%d')
    hora = data_hora.hour

    # Verificar tipo de dia
    if data_hora.weekday() in [4, 5]:  # sexta (4), sábado (5)
        tipo_dia = 'final_semana'
    elif data_str in feriados:
        tipo_dia = 'feriado'
    else:
        tipo_dia = 'dia_normal'

    # Obter peso baseado no tipo de dia
    base_pesos = pesos_tipos[tipo_dia]

    # Primeiro gerar tipo de crime
    tipo = random.choices(tipos_crime, weights=base_pesos, k=1)[0]

    # Priorizar região com base no tipo de crime
    if tipo in crimes_regioes_prioritarias:
        regioes_prioritarias = crimes_regioes_prioritarias[tipo] * 5 + list(setores_asa_sul.keys())
    else:
        regioes_prioritarias = list(setores_asa_sul.keys())

    # Garantir que a região existe
    via_aleatoria = None
    tentativas = 0
    while tentativas < 10:
        tentativas += 1
        via_aleatoria = random.choice(regioes_prioritarias)
        if via_aleatoria in setores_asa_sul:
            break
    if via_aleatoria not in setores_asa_sul:
        via_aleatoria = random.choice(list(setores_asa_sul.keys()))

    # Obter coordenadas base
    lat_base, lon_base = random.choice(setores_asa_sul[via_aleatoria])

    # Gerar variação com base no tipo de crime
    lat, lon = gerar_variacao(lat_base, lon_base, tipo)

    # Verificar zonas proibidas
    proibido = True
    tentativas = 0
    while proibido and tentativas < 10:
        tentativas += 1
        lat_base, lon_base = random.choice(setores_asa_sul[via_aleatoria])
        lat, lon = gerar_variacao(lat_base, lon_base, tipo)
        proibido = False
        for (lat_p, lon_p, raio) in zonas_proibidas:
            distancia = ((lat - lat_p)**2 + (lon - lon_p)**2)**0.5
            if distancia < raio:
                proibido = True
                break
    if proibido:
        continue  # Ignorar pontos nas zonas proibidas

    rua = via_aleatoria
    regiao_pesos = crime_pesos_por_regiao.get(rua, [1]*6)
    combined_pesos = [b * r for b, r in zip(base_pesos, regiao_pesos)]
    tipo = random.choices(tipos_crime, weights=combined_pesos, k=1)[0]

    # Ajuste de horário: aumentar chance de crime entre 21h e 3h
    if 21 <= hora or hora <= 3:
        padrao = padroes_por_regiao.get(rua, {})
        if tipo in padrao.get("crimes_prioritarios", []):
            tipo = random.choice([tipo] * 5 + random.choices(tipos_crime, weights=combined_pesos, k=2))

    # Gerar idade com base na região e tipo de crime
    idade = gerar_idade(rua, tipo)

    # Gerar endereço
    formato = random.choice(enderecos_asa_sul)
    if "{bloco}" in formato:
        endereco = formato.format(rua=rua, bloco=random.choice(blocos), num=random.randint(100, 999))
    elif "{lote}" in formato:
        endereco = formato.format(rua=rua, lote=random.choice(lotes), sala=random.choice(salas))
    elif "{edificio}" in formato:
        endereco = formato.format(rua=rua, edificio=random.choice(edificios), unidade=random.choice(unidades))

    # Gerar outros dados
    nome = fake.name()
    cpf_formatado = fake.cpf()
    email = fake.email()
    telefone = fake.phone_number()

    # Inserir NaN esporadicamente
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

    risco = risco_mapa.get(rua, 2)

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
        'telefone': telefone,
        'endereco': endereco,
        'risco': risco
    })

# Criar DataFrame e salvar CSV
df = pd.DataFrame(data)
df["__ERRO__"] = "ERRO_404"
df["null"] = np.nan
df.to_csv('crime_segunda_area.csv', index=False)
print("✅ Arquivo 'crime_segunda_area.csv' criado com sucesso!")