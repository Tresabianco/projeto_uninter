import pytest
from fastapi.testclient import TestClient
from SGHSS import app  # Certifique-se de que seu arquivo principal chama-se SGHSS.py

client = TestClient(app)

# Testando o endpoint de criação de pacientes
def test_criar_paciente():
    resposta = client.post("/pacientes/", params={
        "nome": "Carlos Souza",
        "data_nascimento": "1988-07-25",
        "cpf": "123.456.789-10",
        "endereco": "Rua C, 789"
    })
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Paciente criado com sucesso"

# Testando o endpoint de obtenção de paciente existente
def test_obter_paciente_existente():
    resposta = client.get("/pacientes/3")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "João da Silva"

# Testando o endpoint de obtenção de paciente inexistente
def test_obter_paciente_inexistente():
    resposta = client.get("/pacientes/99")
    assert resposta.status_code == 200
    assert resposta.json() == {"erro": "Paciente não encontrado"}

# Testando o endpoint de criação de médicos
def test_criar_medico():
    resposta = client.post("/medicos/", params={
        "nome": "Dr. Rodrigo Santos",
        "especialidade": "Ortopedia",
        "crm": "11223-SP"
    })
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Médico criado com sucesso"

# Testando o endpoint de obtenção de médico existente
def test_obter_medico_existente():
    resposta = client.get("/medicos/1")
    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Dr. Bruno Alves"

# Testando a criação de uma consulta válida
def test_criar_consulta():
    resposta = client.post("/consultas/", params={
        "paciente_id": 1,
        "medico_id": 1,
        "data_hora": "2025-03-25 14:00"
    })
    assert resposta.status_code == 200
    assert resposta.json()["mensagem"] == "Consulta criada com sucesso"

# Testando o endpoint de obtenção de consulta existente
def test_obter_consulta_existente():
    resposta = client.get("/consultas/1")
    assert resposta.status_code == 200
    assert "paciente_id" in resposta.json()

# Testando o endpoint de obtenção de consulta inexistente
def test_obter_consulta_inexistente():
    resposta = client.get("/consultas/99")
    assert resposta.status_code == 200
    assert resposta.json() == {"erro": "Consulta não encontrada"}

# Testando o endpoint principal
def test_home():
    resposta = client.get("/")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Consultas marcadas no Sistema de Gestão Hospitalar e de Serviços de Saúde (SGHSS)"}


