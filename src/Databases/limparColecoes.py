
#from keywordGenerator import keywordGenerator
from mongoConection import conectarMongo
from dotenv import load_dotenv
load_dotenv()



db = conectarMongo()

# Lista de coleções a esvaziar
colecoes = [
    "interacoes",
    "interacoes_alternativas",
    "interacoes_alternativas_processadas",  # ajuste se necessário, nome está cortado na imagem
    "interacoes_processadas",
    "keywords"
]

# Esvaziar cada coleção
for nome in colecoes:
    resultado = db[nome].delete_many({})
    print(f"{nome}: {resultado.deleted_count} documentos deletados.")