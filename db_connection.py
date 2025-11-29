import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="biometric_attendance_control",
            user="postgres",
            password="gadex008"
        )
        return conn

    except Exception as e:
        print("Error conectando a PostgreSQL:", e)
        return None
