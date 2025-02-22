from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError 

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

# Conectar ao SQLite em memória para criar o arquivo 'meubanco.db'
engine = create_engine('sqlite:///desafio.db')
print("Conexão com SQLite estabelecida.")

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insere novos registros de fornecedores
try:
    with Session() as session:
        fornecedores = [
            Fornecedor(nome='Fornecedor A',telefone='48992526235',email='pedro@gmail.com',endereco='Av. Mauro Ramos nº 2005 Centro Florianopolis SC'),
            Fornecedor(nome='Fornecedor B',telefone='21985256325',email='joao@gmail.com',endereco='Rua São João nº 105 Bom Sucesso Rio de Janeiro RJ'),
            Fornecedor(nome='Fornecedor C',telefone='61985452685',email='paula@gmail.com',endereco='SQS 414 Bl B Apto 105 Asa Sul Brasilia DF')
        ]
        session.add_all(fornecedores)
        session.commit()
except SQLAlchemyError as e:
    print(f"Erro ao inserir fornecedores: {e}")
finally:
    print('Fornecedores inseridos com sucesso')

# Insere novos registros de produtos
try:
    with Session() as session:
        produtos = [
            Produto(nome='Calça jeans',descricao='Calça estilo jeans cor preta',preco=159.60,quantidade=10, fornecedor_id = 1),
            Produto(nome='Camisa polo',descricao='Camisa polo em linho',preco=58.90,quantidade=50, fornecedor_id = 1),
            Produto(nome='Moletom',descricao='Moletom estilo colegial',preco=201.58,quantidade=20, fornecedor_id = 2),
            Produto(nome='Sapatenis',descricao='Sapatênis em couro',preco=359.60,quantidade=30, fornecedor_id = 3)
        ]
        session.add_all(produtos)
        session.commit()
except SQLAlchemyError as e:
    print(f"Erro ao inserir produtos: {e}")
finally :
    print("Produtos inseridos com sucesso.")


#consultar os dados inseridos
for produto in session.query(Produto).all():
    print(f"Produto: {produto.nome}, Fornecedor: {produto.fornecedor.nome}")