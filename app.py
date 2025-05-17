import os
import requests
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from ExtratorPalavraChave.extrator_keywords import extrair_keywords_com_embeddings

load_dotenv()

app = Flask(__name__)

NESTJS_BASE_URL = "http://localhost:3003"
MONGO_URI = os.getenv("MONGO_URI")

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client.get_database("Cluster0")
keywords_collection = mongo_db["keywords"]

@app.route('/extrair-keywords', methods=['POST'])
def extrair_keywords():
    data = request.get_json()

    chamado_id = data.get('chamado_id')
    descricao = data.get('descricao', '')
    tipo_importacao = data.get('tipo_importacao')

    if not chamado_id or not descricao or not tipo_importacao:
        return jsonify({"erro": "Campos obrigatórios: chamado_id, descricao, tipo_importacao"}), 400

    resultado_completo = extrair_keywords_com_embeddings(descricao, top_n=3)
    palavras_chave = [item["keyword"] for item in resultado_completo]

    try:
        documentos = [{"keyword": item["keyword"], "embedding": item["embedding"]} for item in resultado_completo]
        if documentos:
            keywords_collection.insert_many(documentos)
    except Exception as e:
        return jsonify({"erro": "Erro ao salvar no MongoDB", "detalhes": str(e)}), 500

    try:
        response = requests.patch(
            f"{NESTJS_BASE_URL}/chamados/atualizar-keywords/{chamado_id}",
            json={"keywords": palavras_chave},
            timeout=5
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": "Falha ao atualizar keywords no backend", "detalhes": str(e)}), 500

    return jsonify({
        "chamado_id": chamado_id,
        "palavras_chave": palavras_chave,
        "status": "keywords atualizadas com sucesso (MongoDB + PostgreSQL)"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
