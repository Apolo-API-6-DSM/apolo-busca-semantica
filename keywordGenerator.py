from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from PreProcessamento.preProcessamento import preProcessamento
texto = "Solicitante Thaylla Paiva Instalar 2 novos computadores na mesa do planejamento para o uso dos estagiários."


def keywordGenerator(texto):
    texto = preProcessamento(texto)
    kw_model = KeyBERT(model='all-MiniLM-L6-v2')
    keywords = kw_model.extract_keywords(texto, top_n=5)
    keywords = [keyword for keyword, score in keywords]
    model = SentenceTransformer("paraphrase-MiniLM-L3-v2")
    embeddings = []
    for kw in keywords:
        embeddings.append(model.encode(kw).tolist())
    return {"keywords":keywords, "embedding":embeddings}

