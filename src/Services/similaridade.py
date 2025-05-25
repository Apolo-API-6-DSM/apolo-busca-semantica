import pprint
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from Databases.getDatabaseKeywords import getDatabaseKeywordsMongo
from Services.keywordGenerator import keywordGenerator


def similarityComparison(prompt):
    # Extrai keywords e seus embeddings
    prompt_data = keywordGenerator(prompt)
    print(prompt_data["keywords"])
    prompt_embeddings = np.array(prompt_data['embedding'])

    # Calcula a média dos embeddings do prompt
    prompt_mean_embedding = np.mean(prompt_embeddings, axis=0).reshape(1, -1)

    keyWordsDataBase = getDatabaseKeywordsMongo()
    resultados = []

    for item in keyWordsDataBase:
        database_embedding = np.array(item['embedding']).reshape(1, -1)

        # Calcula a similaridade entre o embedding médio do prompt e o embedding da keyword do banco
        score = cosine_similarity(database_embedding, prompt_mean_embedding)[0][0]

        resultados.append({
            "keyword": item["keyword"],
            "score": round(score, 4)
        })

    # Ordena e filtra os top resultados
    resultados_ordenados = sorted(resultados, key=lambda x: x["score"], reverse=True)
    top_resultados = [r for r in resultados_ordenados if r["score"] >= 0.5][:5]
    keywords = [item["keyword"] for item in top_resultados]
    print(keywords)
    return keywords


"""# Exemplo de uso
top_resultados = similarityComparison("me traga chamados que relatam errados")
print(top_resultados)
"""