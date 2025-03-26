import psycopg2
from app.config import Config

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            port=Config.DB_PORT
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS my_client (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(250) NOT NULL,
                    slug VARCHAR(100) UNIQUE NOT NULL,
                    is_project VARCHAR(30) CHECK (is_project IN ('0', '1')) NOT NULL DEFAULT '0',
                    self_capture CHAR(1) NOT NULL DEFAULT '1',
                    client_prefix CHAR(4) NOT NULL,
                    client_logo VARCHAR(255) NOT NULL DEFAULT 'no-image.jpg',
                    address TEXT DEFAULT NULL,
                    phone_number VARCHAR(50) DEFAULT NULL,
                    city VARCHAR(50) DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NULL,
                    deleted_at TIMESTAMP DEFAULT NULL
                )
            """)
            conn.commit()
        conn.close()