#from keywordGenerator import keywordGenerator
from Databases.mongoConection import conectarMongo
from dotenv import load_dotenv
load_dotenv()

def getDatabaseKeywordsMongo():
    db = conectarMongo()

    colecao = db['keywords']

    keywords = colecao.find()
    return keywords
