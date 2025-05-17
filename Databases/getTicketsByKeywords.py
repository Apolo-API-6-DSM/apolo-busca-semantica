from Databases.postgressConection import connectionWithoutCommit

def getTicketsByKeywords():
    return connectionWithoutCommit(queryGetTicketsByKeywords)

def queryGetTicketsByKeywords(cursor, keywords):
    sql = 'SELECT * FROM "Chamado" WHERE keywords && %s;'
    cursor.execute(sql, (keywords,))
    return cursor.fetchall()