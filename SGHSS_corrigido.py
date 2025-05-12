
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone

app = FastAPI()

# Customização do Swagger com autenticação Bearer
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SGHSS",
        version="0.1.0",
        description="Sistema de Gestão Hospitalar e Serviços de Saúde com autenticação JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Simulando banco de dados
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

# Simulando credenciais de médicos
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
medicos_credenciais = {
    "bruno": {"nome": "Dr. Bruno Alves", "senha": pwd_context.hash("senha123")},
    "fernanda": {"nome": "Dra. Fernanda Costa", "senha": pwd_context.hash("senha456")},
}

# Configurações JWT
SECRET_KEY = "chave_super_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # Necessário para proteger rotas

def verificar_senha(senha_plana, senha_hash):
    return pwd_context.verify(senha_plana, senha_hash)

def autenticar_medico(username: str, senha: str):
    medico = medicos_credenciais.get(username)
    if not medico:
        return False
    if not verificar_senha(senha, medico["senha"]):
        return False
    return medico

def criar_token_acesso(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expira = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expira, "sub": data["sub"]})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def obter_medico_atual(token: str = Depends(oauth2_scheme)):
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in medicos_credenciais:
            raise credenciais_invalidas
        return medicos_credenciais[username]
    except JWTError:
        raise credenciais_invalidas

# Modelo de entrada para login
class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginData):
    medico = autenticar_medico(data.username, data.password)
    if not medico:
        raise HTTPException(status_code=400, detail="Usuário ou senha inválidos")
    access_token = criar_token_acesso(data={"sub": data.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Rotas do sistema
@app.post("/pacientes/")
def criar_paciente(nome: str, data_nascimento: str, cpf: str, endereco: str):
    paciente_id = len(pacientes_db) + 1
    pacientes_db[paciente_id] = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    return {"mensagem": "Paciente criado com sucesso", "id": paciente_id}

@app.get("/pacientes/{id}")
async def obter_paciente(id: int, medico: dict = Depends(obter_medico_atual)):
    paciente = pacientes_db.get(id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
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


# Como executar:
# uvicorn SGHSS_corrigido:app --reload
# Acesse em: http://127.0.0.1:8000/docs