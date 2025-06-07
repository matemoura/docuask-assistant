import sqlite3
import hashlib
from datetime import datetime

DB_PATH = "docuask.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def setup_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        sector TEXT NOT NULL,
        revision INTEGER NOT NULL,
        status TEXT NOT NULL, -- 'current' ou 'obsolete'
        file_path TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Usuário {username} já existe.")
    finally:
        conn.close()

def get_all_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password_hash FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def add_document(name, sector, revision, status, file_path):
    conn = connect_db()
    cursor = conn.cursor()
    timestamp = datetime.now()
    cursor.execute("""
    INSERT INTO documents (name, sector, revision, status, file_path, created_at) 
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, sector, revision, status, file_path, timestamp))
    conn.commit()
    conn.close()

def set_document_obsolete(name, sector):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE documents SET status = 'obsolete' 
    WHERE name = ? AND sector = ? AND status = 'current'
    """, (name, sector))
    conn.commit()
    conn.close()
    
def get_latest_documents():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT d1.*
    FROM documents d1
    LEFT JOIN documents d2 ON d1.name = d2.name AND d1.revision < d2.revision
    WHERE d2.id IS NULL AND d1.status = 'current'
    """)
    docs = cursor.fetchall()
    conn.close()

    return [dict(zip([column[0] for column in cursor.description], row)) for row in docs]

def get_obsolete_documents():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, sector, revision, created_at FROM documents WHERE status = 'obsolete' ORDER BY sector, name, revision")
    docs = cursor.fetchall()
    conn.close()
    return [dict(zip([column[0] for column in cursor.description], row)) for row in docs]

if __name__ == '__main__':
    print("Configurando banco de dados...")
    setup_database()
    print("Adicionando usuário 'admin' com senha 'admin'...")
    add_user("admin", "admin")
    print("Configuração concluída.")