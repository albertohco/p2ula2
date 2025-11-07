from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re

app = FastAPI(title="Sistema de Padronização de Nomes e Emails")

# Configuração do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./usuarios.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy para o banco de dados
class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    email = Column(String, unique=True, index=True)

# Criação das tabelas
Base.metadata.create_all(bind=engine)

# Modelo Pydantic para validação de dados
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr

# Função para padronizar nome
def padronizar_nome(nome: str) -> str:
    # Remove espaços extras e converte para lowercase
    nome = " ".join(nome.split()).lower()

    # Capitaliza cada palavra
    nome = nome.title()

    # Tratamento para nomes com 'da', 'de', 'do', 'das', 'dos'
    preposicoes = ['Da', 'De', 'Do', 'Das', 'Dos']
    palavras = nome.split()
    nome_final = []
    
    for palavra in palavras:
        if palavra in preposicoes:
            nome_final.append(palavra.lower())
        else:
            nome_final.append(palavra)
    
    return " ".join(nome_final)

# Função para padronizar email
def padronizar_email(nome: str) -> str:
    # Remove acentos
    from unicodedata import normalize
    nome = normalize('NFKD', nome).encode('ASCII', 'ignore').decode('ASCII')
    
    # Converte para minúsculas e substitui espaços por pontos
    email = nome.lower().replace(' ', '.')
    
    # Remove caracteres especiais
    email = re.sub(r'[^a-z0-9.]', '', email)
    
    # Remove pontos duplicados
    email = re.sub(r'\.+', '.', email)
    
    # Remove ponto no início ou fim
    email = email.strip('.')
    
    return f"{email}@empresa.com.br"

@app.get("/")
async def bem_vindo():
    return {"message": "Bem-vindo ao Sistema de Padronização de Nomes e Emails"}
  
@app.post("/usuarios/")
async def criar_usuario(usuario: UsuarioBase):
    nome_padronizado = padronizar_nome(usuario.nome)
    email_padronizado = padronizar_email(nome_padronizado)
    
    db = SessionLocal()
    try:
        novo_usuario = Usuario(nome=nome_padronizado, email=email_padronizado)
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return {
            "id": novo_usuario.id,
            "nome": novo_usuario.nome,
            "email": novo_usuario.email,
            "detalhes": {
                "nome_original": usuario.nome,
                "nome_padronizado": nome_padronizado,
                "email_gerado": email_padronizado
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.get("/usuarios/")
async def listar_usuarios():
    db = SessionLocal()
    try:
        usuarios = db.query(Usuario).all()
        return usuarios
    finally:
        db.close()
    