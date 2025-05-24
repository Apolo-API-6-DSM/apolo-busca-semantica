from keybert import KeyBERT
from sentence_transformers import SentenceTransformer
from PreProcessamento.preProcessamento import preProcessamento

modelo = SentenceTransformer('all-MiniLM-L6-v2')
kw_model = KeyBERT(model=modelo)

def extrair_keywords_com_embeddings(texto: str, top_n: int = 5):
    if not texto.strip():
        return []
    texto = preProcessamento(texto)
    keywords = kw_model.extract_keywords(
        texto,
        keyphrase_ngram_range=(1, 2),
        stop_words=None,
        top_n=top_n
    )

    resultados = []
    for palavra, score in keywords:
        embedding = modelo.encode(palavra, convert_to_numpy=True).tolist()
        resultados.append({
            "keyword": palavra,
            "embedding": embedding
        })

    return resultados


