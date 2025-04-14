from fastapi import FastAPI

app = FastAPI()

# Banco de dados simulado
pacientes_db = {
    1: {"nome": "Jorge Ramos", "data_nascimento": "1990-05-20", "cpf": "123.456.789-00", "endereco": "Rua A, 123"},
    2: {"nome": "Maria Oliveira", "data_nascimento": "1985-10-15", "cpf": "987.654.321-00", "endereco": "Rua B, 456"}
}

medicos_db = {
    1: {"nome": "Dr. Bruno Alves", "especialidade": "Cardiologia", "crm": "12345-SP"},
    2: {"nome": "Dra. Fernanda Costa", "especialidade": "Dermatologia", "crm": "67890-RJ"}
}

consultas_db = {
    1: {"paciente": "Jorge Ramos", "medico": "Dr. Bruno Alves", "data_hora": "2025-03-20 10:00"},
    2: {"paciente": "Maria Oliveira", "medico": "Dra. Fernanda Costa", "data_hora": "2025-03-21 15:30"}
}

@app.post("/pacientes/")
def criar_paciente(nome: str, data_nascimento: str, cpf: str, endereco: str):
    paciente_id = len(pacientes_db) + 1
    pacientes_db[paciente_id] = {"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}
    return {"mensagem": "Paciente criado com sucesso", "id": paciente_id}

@app.get("/pacientes/{id}")
def obter_paciente(id: int):
    paciente = pacientes_db.get(id)
    if not paciente:
        return {"erro": "Paciente não encontrado"}
    return paciente

@app.post("/medicos/")
def criar_medico(nome: str, especialidade: str, crm: str):
    medico_id = len(medicos_db) + 1
    medicos_db[medico_id] = {"nome": nome, "especialidade": especialidade, "crm": crm}
    return {"mensagem": "Médico criado com sucesso", "id": medico_id}

@app.get("/medicos/{id}")
def obter_medico(id: int):
    medico = medicos_db.get(id)
    if not medico:
        return {"erro": "Médico não encontrado"}
    return medico

@app.post("/consultas/")
def criar_consulta(paciente: str, medico: str, data_hora: str):
    consulta_id = len(consultas_db) + 1
    consultas_db[consulta_id] = {"paciente": paciente, "medico": medico, "data_hora": data_hora}
    return {"mensagem": "Consulta criada com sucesso", "id": consulta_id}

@app.get("/consultas/{id}")
def obter_consulta(id: int):
    consulta = consultas_db.get(id)
    if not consulta:
        return {"erro": "Consulta não encontrada"}
    return consulta

@app.get("/")
def home():
    return {"mensagem": "Consultas marcadas no Sistema de Gestão Hospitalar e de Serviços de Saúde (SGHSS)"}

#uvicorn SGHSS:app --reload (usar no terminal para rodar o API no navegador ou no Postman do endereço: http://127.0.0.1:8000)



