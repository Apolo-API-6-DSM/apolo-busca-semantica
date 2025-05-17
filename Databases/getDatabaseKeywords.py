from keywordGenerator import keywordGenerator
from Databases.mongoConection import conectarMongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

def getDatabaseKeywordsMongo():
    db = conectarMongo()

    colecao = db['keywords']

    keywords = colecao.find()
    return keywords

def getDatabaseKeywordsMock():
    textos = [
        "Solicitante Angelo Chaves Solicito a liberação da obra 95 nos logins das colaboradas Lara Pietra e Jessica Jenifer.",
        "Solicitante Monitoramento Foi verificado através do monitoramento que o switch T0849 se encontra offline desde dia 09032023 às 1811hrs",
        "Identificado que o switches e antenas estão offline.",
        "Solicitante Ingridy Horrana Solicitar alteração do nome do email citado anteriormente pela Maria de Lourdes Leticia Silva dos Santos Técnica de Segurança do Trabalho 63991048711",
        "Posso personalizar o layout do sistema de acordo com a identidade visual da minha empresa?",
    ]
    banco_embeddings = []
    for texto in textos:
        banco_embeddings.append(keywordGenerator(texto))
    banco_tratado = []
    for descricao in banco_embeddings:
        print(descricao["keywords"])
        i = 0
        for keyword in descricao["keywords"]:
            banco_tratado.append({
                "keyword":keyword,
                "embedding":descricao["embedding"][i]
            })
            i += 1

    return banco_tratado