from sqlalchemy import func, create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Supondo que engine já foi definido anteriormente e os modelos Produto e Fornecedor foram definidos conforme o exemplo anterior.

# declarative_base é o ORM propriamente dito
Base = declarative_base()

# define a estrutura da model Fornecedor
class Fornecedor(Base):
    __tablename__ = 'fornecedores'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    telefone = Column(String(20))
    email = Column(String(50))
    endereco = Column(String(100))

class Produto(Base):
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    descricao = Column(String(200))
    preco = Column(Float)
    quantidade = Column(Integer)
    fornecedor_id = Column(Integer, ForeignKey('fornecedores.id')) #define uma chave estrangeira

    # estabelece o relacionamento entre as tabelas
    fornecedor = relationship(Fornecedor, backref='produtos')

# Conectar ao ao banco de dados SQLite em memória 
engine = create_engine('sqlite:///desafio.db')
print("Conexão com SQLite estabelecida.")

Session = sessionmaker(bind=engine)
session = Session()

# realiza uma query com join entre protudos e fornecedores
resultado = session.query(
    Fornecedor.nome,
    func.sum(Produto.preco).label('total_preco')
).join(Produto, Fornecedor.id == Produto.fornecedor_id
).group_by(Fornecedor.nome).all()

for nome, total_preco in resultado:
    print(f"Fornecedor: {nome}, Total Preço: {total_preco}")