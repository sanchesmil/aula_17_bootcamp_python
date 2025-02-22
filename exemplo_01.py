from sqlalchemy import create_engine

# Conectar ao SQLite em memória para criar o arquivo 'meubanco.db'
engine = create_engine('sqlite:///meubanco.db', echo=True)

print("Conexão com SQLite estabelecida.")

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

# declarative_base é o ORM propriamente dito
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)

# define as sessões no SQLAlchemy (que englobam o inicio e a finalização de uma transação) 
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# cria um novo usuario
novo_usuario = Usuario(nome='João', idade=28)
session.add(novo_usuario)
session.commit()

print("Usuário inserido com sucesso.")

#consultar os dados inseridos
usuario = session.query(Usuario).filter_by(nome='João').first()
print(f"Usuário encontrado: {usuario.nome}, Idade: {usuario.idade}")