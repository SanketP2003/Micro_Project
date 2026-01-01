import os

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')

# Base directory
BASE_DIR = os.path.dirname(__file__)

# SQLite Database configuration
SQLITE_DATABASE = os.path.join(BASE_DIR, 'database', 'study_tool.db')

# Upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

def init_app(app):
    """Initialize application configuration"""
    app.config.from_object(__name__)
    
    # Ensure database directory exists
    db_dir = os.path.dirname(SQLITE_DATABASE)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Ensure upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
