import psycopg2

DB_HOST = "localhost"
DB_NAME = "fyp2"
DB_USER = "akarah"
DB_PORT = "5432"
DB_PASSWORD = "betah1234"

def connect_to_database():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Connected to the database.")
        return connection
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_database_connection(connection):
    if connection:
        connection.close()
        print("PostgreSQL connection is closed")