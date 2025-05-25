import re
import nltk
import spacy
from nltk import tokenize
from PreProcessamento.anomalizer import anomalizer

# Carrega modelo spaCy para português (uma vez só)
nlp = spacy.load("pt_core_news_lg")

def preProcessamento(texto):
    # texto = anomalizer(texto.lower())  # Descomente se quiser usar
    texto = texto.lower()
    texto = cleanStopWords(texto)
    texto = lemmatize(texto)
    return texto

def cleanStopWords(texto):
    tokenizer = tokenize.WhitespaceTokenizer()
    texto = tokenizer.tokenize(texto)

    texto_tratado = []
    stop_words = nltk.corpus.stopwords.words('portuguese') + ["person", "location"]
    for palavra in texto:
        if palavra in stop_words:
            continue
        texto_tratado.append(palavra)

    return ' '.join(texto_tratado)

def lemmatize(texto):
    doc = nlp(texto)
    return ' '.join([token.lemma_ for token in doc if not token.is_punct and not token.is_space])
