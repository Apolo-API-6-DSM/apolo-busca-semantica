import os
import pprint
import requests
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from Services.extrator_keywords import extrair_keywords_com_embeddings
from Services.similaridade import similarityComparison
from Databases.getTicketsByKeywords import getTicketsByKeywords
import uuid
import redis
import json

# Conecta ao Redis local (ajuste se estiver usando Docker ou outro host)
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
load_dotenv()

app = Flask(__name__)

NESTJS_BASE_URL = "http://localhost:3003"
MONGO_URI = os.getenv("MONGO_URI")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client.get_database("Cluster0")
keywords_collection = mongo_db["keywords"]

keywords_collection.create_index("keyword", unique=True)

@app.route('/extrair-keywords', methods=['POST'])
def extrair_keywords():
    data = request.get_json()
    chamados = data.get("chamados", [])

    if not chamados:
        return jsonify({"erro": "A lista de chamados está vazia ou ausente."}), 400

    resultados = []

    for chamado in chamados:
        pprint.pprint(chamado)
        chamado_id = chamado.get('chamadoId')
        descricao = chamado.get('descricao', '')


        if not chamado_id or not descricao:
            resultados.append({
                "chamado_id": chamado_id,
                "erro": "Campos obrigatórios ausentes: chamado_id, descricao"
            })
            continue

        try:
            resultado_completo = extrair_keywords_com_embeddings(descricao, top_n=3)
            palavras_chave = [item["keyword"] for item in resultado_completo]

            for item in resultado_completo:
                keyword = item["keyword"]
                existe = keywords_collection.find_one({"keyword": keyword})
                if not existe:
                    keywords_collection.insert_one({
                        "keyword": keyword,
                        "embedding": item["embedding"]
                    })
                else:
                    print(f"Keyword '{keyword}' já existe no MongoDB. Ignorando inserção.")

            try:
                response = requests.patch(
                    f"{NESTJS_BASE_URL}/chamados/atualizar-keywords/{chamado_id}",
                    json={"keywords": palavras_chave},
                    timeout=5
                )
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                resultados.append({
                    "chamado_id": chamado_id,
                    "erro": "Falha ao atualizar keywords no backend",
                    "detalhes": str(e)
                })
                continue

            resultados.append({
                "chamado_id": chamado_id,
                "palavras_chave": palavras_chave,
                "status": "keywords atualizadas com sucesso (MongoDB + PostgreSQL)"
            })

        except Exception as e:
            resultados.append({
                "chamado_id": chamado_id,
                "erro": "Erro ao processar chamado",
                "detalhes": str(e)
            })

    return jsonify({"resultados": resultados}), 200

@app.route('/busca-semantica', methods=['POST'])
def comparar_similaridade():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({'error': 'Campo "prompt" é obrigatório.'}), 400

    prompt = data['prompt']
    token = data.get('token')

    # Paginação
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    try:
        # Se token foi fornecido, tenta buscar no Redis
        if token and redis_client.exists(token):
            keywords = json.loads(redis_client.get(token))
        else:
            keywords = similarityComparison(prompt)
            token = str(uuid.uuid4())
            redis_client.setex(token, 1800, json.dumps(keywords))  # TTL de 30 min

        resultados, total = getTicketsByKeywords(keywords, limit, offset)

        return jsonify({
            "page": page,
            "limit": limit,
            "total": total,
            "resultados": resultados,
            "token": token
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
