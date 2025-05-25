from keybert import KeyBERT
from PreProcessamento.preProcessamento import preProcessamento
from sentence_transformers import SentenceTransformer

# Carregue uma única vez e compartilhe o modelo
shared_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(model=shared_model)

def keywordGenerator(texto):
    texto = preProcessamento(texto)
    
    keywords = kw_model.extract_keywords(
        texto,
        top_n=3,
        keyphrase_ngram_range=(1, 2),
        use_maxsum=True,
        nr_candidates=20
    )

    keywords = [keyword for keyword, score in keywords]

    embeddings = [shared_model.encode(kw).tolist() for kw in keywords]

    return {"keywords": keywords, "embedding": embeddings}
