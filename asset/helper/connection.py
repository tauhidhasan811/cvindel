import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="ass",
        user="postgres",
        password="10101010"
    )
