from flask import Flask
from flask_cors import CORS
import config
from models.database import init_db
from routes.documents import documents_bp

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load configuration
    config.init_app(app)
    
    # Enable CORS for frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register blueprints
    app.register_blueprint(documents_bp)
    
    # Health check route
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'ok', 'message': 'Study Tool API is running'}, 200
    
    @app.route('/', methods=['GET'])
    def index():
        return {
            'message': 'Welcome to Study Tool API',
            'endpoints': {
                'documents': '/api/documents',
                'upload_youtube': '/api/documents/youtube',
                'upload_pdf': '/api/documents/pdf',
                'health': '/health'
            }
        }, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("Starting Flask server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
