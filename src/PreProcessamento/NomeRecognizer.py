from presidio_analyzer import RecognizerResult, EntityRecognizer
import spacy

# Carregar o modelo spaCy em português
nlp = spacy.load("pt_core_news_lg")

class NomeRecognizer(EntityRecognizer):
    def __init__(self):
        supported_entities = ["PERSON"]
        super().__init__(supported_entities=supported_entities, supported_language="pt")

    def load(self):
        pass

    def analyze(self, text, entities, nlp_artifacts=None):
        resultados = []
        doc = nlp(text)

        palavras_proibidas = {"instalar", "incluir", "solicitar"}

        for ent in doc.ents:
            if ent.label_ == "PER":
                texto_entidade = ent.text.strip()
                palavras = texto_entidade.split()

                # Remove palavras proibidas do final
                while palavras and palavras[-1].lower() in palavras_proibidas:
                    palavras.pop()

                if not palavras:
                    continue

                nome_limpo = " ".join(palavras)

                # Recalcular a posição do nome limpo usando `ent.start_char`
                index_in_ent = ent.text.find(nome_limpo)
                if index_in_ent == -1:
                    continue

                start_index = ent.start_char + index_in_ent
                end_index = start_index + len(nome_limpo)

                resultado = RecognizerResult(
                    entity_type="NOME",
                    start=start_index,
                    end=end_index,
                    score=0.9
                )
                resultados.append(resultado)

        return resultados
