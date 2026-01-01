import sqlite3
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config import SQLITE_DATABASE

def get_db_connection():
    """Create a database connection"""
    connection = sqlite3.connect(SQLITE_DATABASE)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    """Initialize the database with required tables"""
    try:
        connection = get_db_connection()
        with connection:
            # Documents table
            connection.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    type TEXT CHECK(type IN ('pdf', 'youtube')) NOT NULL,
                    content TEXT,
                    source_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Dialogues table
            connection.execute("""
                CREATE TABLE IF NOT EXISTS dialogues (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
                )
            """)
            
            # Summaries table
            connection.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
                )
            """)
            
            # User questions table
            connection.execute("""
                CREATE TABLE IF NOT EXISTS user_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id) ON DELETE CASCADE
                )
            """)
        
        print("Database initialized successfully!")
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False
    finally:
        if connection:
            connection.close()

class Document:
    @staticmethod
    def create(title, doc_type, content=None, source_url=None):
        """Create a new document"""
        connection = get_db_connection()
        try:
            cursor = connection.execute(
                """INSERT INTO documents (title, type, content, source_url) 
                   VALUES (?, ?, ?, ?)""",
                (title, doc_type, content, source_url)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()
    
    @staticmethod
    def get_all():
        """Get all documents"""
        connection = get_db_connection()
        try:
            documents = connection.execute(
                "SELECT * FROM documents ORDER BY created_at DESC"
            ).fetchall()
            return [dict(doc) for doc in documents]
        finally:
            connection.close()
    
    @staticmethod
    def get_by_id(doc_id):
        """Get a document by ID"""
        connection = get_db_connection()
        try:
            document = connection.execute(
                "SELECT * FROM documents WHERE id = ?", (doc_id,)
            ).fetchone()
            return dict(document) if document else None
        finally:
            connection.close()
    
    @staticmethod
    def update(doc_id, title=None, content=None):
        """Update a document"""
        connection = get_db_connection()
        try:
            if title and content:
                connection.execute(
                    """UPDATE documents 
                       SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP 
                       WHERE id = ?""",
                    (title, content, doc_id)
                )
            elif title:
                connection.execute(
                    """UPDATE documents 
                       SET title = ?, updated_at = CURRENT_TIMESTAMP 
                       WHERE id = ?""",
                    (title, doc_id)
                )
            elif content:
                connection.execute(
                    """UPDATE documents 
                       SET content = ?, updated_at = CURRENT_TIMESTAMP 
                       WHERE id = ?""",
                    (content, doc_id)
                )
            connection.commit()
            return True
        finally:
            connection.close()
    
    @staticmethod
    def delete(doc_id):
        """Delete a document"""
        connection = get_db_connection()
        try:
            connection.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            connection.commit()
            return True
        finally:
            connection.close()

class Dialogue:
    @staticmethod
    def create(document_id, content):
        """Create a new dialogue"""
        connection = get_db_connection()
        try:
            cursor = connection.execute(
                "INSERT INTO dialogues (document_id, content) VALUES (?, ?)",
                (document_id, content)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()
    
    @staticmethod
    def get_by_document(document_id):
        """Get all dialogues for a document"""
        connection = get_db_connection()
        try:
            dialogues = connection.execute(
                "SELECT * FROM dialogues WHERE document_id = ?", (document_id,)
            ).fetchall()
            return [dict(d) for d in dialogues]
        finally:
            connection.close()

class Summary:
    @staticmethod
    def create(document_id, content):
        """Create a new summary"""
        connection = get_db_connection()
        try:
            cursor = connection.execute(
                "INSERT INTO summaries (document_id, content) VALUES (?, ?)",
                (document_id, content)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()
    
    @staticmethod
    def get_by_document(document_id):
        """Get all summaries for a document"""
        connection = get_db_connection()
        try:
            summaries = connection.execute(
                "SELECT * FROM summaries WHERE document_id = ?", (document_id,)
            ).fetchall()
            return [dict(s) for s in summaries]
        finally:
            connection.close()

class UserQuestion:
    @staticmethod
    def create(document_id, question, answer=None):
        """Create a new user question"""
        connection = get_db_connection()
        try:
            cursor = connection.execute(
                "INSERT INTO user_questions (document_id, question, answer) VALUES (?, ?, ?)",
                (document_id, question, answer)
            )
            connection.commit()
            return cursor.lastrowid
        finally:
            connection.close()
    
    @staticmethod
    def get_by_document(document_id):
        """Get all questions for a document"""
        connection = get_db_connection()
        try:
            questions = connection.execute(
                "SELECT * FROM user_questions WHERE document_id = ?", (document_id,)
            ).fetchall()
            return [dict(q) for q in questions]
        finally:
            connection.close()
