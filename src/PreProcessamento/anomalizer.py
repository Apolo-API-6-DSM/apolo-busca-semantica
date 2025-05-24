from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from .NomeRecognizer import NomeRecognizer 


configuration = {
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "pt", "model_name": "pt_core_news_lg"}],
    "ner_model_configuration": {
            "model_to_presidio_entity_mapping": {
                "PER": "NOME",
                "PERSON": "NOME",
                "ID": "ID",
                "URL": "URL",
                "EMAIL_ADDRESS":"EMAIL"
            },
            "low_confidence_score_multiplier": 0.4,
        },
}

# Create NLP engine based on configuration
provider = NlpEngineProvider(nlp_configuration=configuration)
nlp_engine = provider.create_engine()

# Pass the created NLP engine and supported_languages to the AnalyzerEngine
analyzer = AnalyzerEngine(
    nlp_engine=nlp_engine, 
    supported_languages=["pt"],
    default_score_threshold=0.7
)
anonymizer = AnonymizerEngine()


nome_recognizer = NomeRecognizer()
analyzer.registry.add_recognizer(nome_recognizer)


url_pattern = Pattern(name="url_pattern", regex=r"https?://[^\s]+", score=0.9)
url_recognizer = PatternRecognizer(supported_entity="URL", patterns=[url_pattern], supported_language="pt")
analyzer.registry.add_recognizer(url_recognizer)


cpf_pattern = Pattern(name="cpf_pattern", regex=r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\b\d{11}\b", score=0.9)
cpf_recognizer = PatternRecognizer(supported_entity="CPF", patterns=[cpf_pattern], supported_language="pt")
analyzer.registry.add_recognizer(cpf_recognizer)

def anomalizer(texto):
    resultados = analyzer.analyze(text=texto, language="pt")


    texto_anonimizado = anonymizer.anonymize(text=texto, analyzer_results=resultados)


    return texto_anonimizado.text
