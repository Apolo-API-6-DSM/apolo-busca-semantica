from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from keywordGenerator import keywordGenerator
from Databases.getDatabaseKeywords import getDatabaseKeywords


def similarityComparison(prompt):
    prompt = keywordGenerator(prompt)
    


    keyWordsDataBase = getDatabaseKeywords() #Por enquanto um Mock
    resultados = []
    for item in keyWordsDataBase:
        database_embeddings = np.array(item['embedding'])
        prompt_embeddings = np.array(prompt['embedding'])
        # Calcula similaridade com todas as palavras do prompt
        scores = [cosine_similarity([database_embeddings], [prompt_vec])[0][0] for prompt_vec in prompt_embeddings]
        # Usa a similaridade máxima
        max_score = max(scores)
        resultados.append({
            "keyword": item["keyword"],
            "score": round(max_score, 4)
        })
    print(resultados)
    # Ordena por score (maior para menor)
    resultados_ordenados = sorted(resultados, key=lambda x: x["score"], reverse=True)
    # top 5 com score > 0.7
    top_resultados = [r for r in resultados_ordenados if r["score"] >= 0.7][:5]
    return top_resultados

topresutados = similarityComparison("me traga solicitações que tenham a ver com obras")
print(topresutados)