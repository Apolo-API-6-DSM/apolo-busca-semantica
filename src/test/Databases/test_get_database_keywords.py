from Databases.getDatabaseKeywords import getDatabaseKeywordsMongo
import pytest

def test_get_database_keywords_mongo():
    resultado = list(getDatabaseKeywordsMongo())
    print(resultado)

    assert isinstance(resultado, list)