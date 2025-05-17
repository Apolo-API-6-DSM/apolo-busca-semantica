import re
import nltk
from nltk import tokenize
from PreProcessamento.anomalizer import anomalizer

def preProcessamento(texto):
    texto = anomalizer(texto.lower())
    texto = cleanStopWords(texto)
    return texto

def cleanStopWords(texto):

    tokenizer = tokenize.WhitespaceTokenizer()
    texto = tokenizer.tokenize(texto)

    texto_tratado = []
    #stop_words = nltk.corpus.stopwords.words('portuguese') + ["person"]
    stop_words = ["person"]
    for palavra in texto:
        if(palavra in stop_words):
            continue
        texto_tratado.append(palavra)

    return ' '.join(texto_tratado)