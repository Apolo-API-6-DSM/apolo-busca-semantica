from keybert import KeyBERT
from sentence_transformers import SentenceTransformer

modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
kw_model = KeyBERT(model=modelo)

def extrair_keywords_com_embeddings(texto: str, top_n: int = 5):
    if not texto.strip():
        return []

    keywords = kw_model.extract_keywords(
        texto,
        keyphrase_ngram_range=(1, 1),
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
