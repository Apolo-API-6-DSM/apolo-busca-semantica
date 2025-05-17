from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def connectionWithoutCommit(func):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        # Executa a função e captura retorno (se houver)
        result = func(cursor)

        conn.commit()  # só se tiver inserts/updates, senão pode tirar
        return result

    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        conn.rollback()

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def connectionWithCommit(func):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cursor = conn.cursor()

        # Executa a função e captura retorno (se houver)
        result = func(cursor)

        conn.commit()  # só se tiver inserts/updates, senão pode tirar
        return result

    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        conn.rollback()

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()