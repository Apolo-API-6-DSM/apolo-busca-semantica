import psycopg2.extras
from Databases.postgressConection import connectionWithoutCommitKeywords

def getTicketsByKeywords(keywords, limit, offset):
    return connectionWithoutCommitKeywords(
        queryGetTicketsByKeywords, keywords, limit, offset
    )

def queryGetTicketsByKeywords(cursor, keywords, limit, offset):
    # Usa DictCursor para retornar dicionários
    cursor = cursor.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Total de registros
    count_sql = 'SELECT COUNT(*) FROM "Chamado" WHERE keywords ?| %s;'
    cursor.execute(count_sql, (keywords,))
    total = cursor.fetchone()[0]

    # Consulta paginada
    sql = 'SELECT * FROM "Chamado" WHERE keywords ?| %s LIMIT %s OFFSET %s;'
    cursor.execute(sql, (keywords, limit, offset))
    resultados = cursor.fetchall()

    return [dict(row) for row in resultados], total