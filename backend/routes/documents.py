import os
import sys
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.database import Document, Dialogue, Summary
from services.youtube_service import process_youtube_video, is_valid_youtube_url
from services.pdf_service import process_pdf, is_allowed_file
from config import UPLOAD_FOLDER

documents_bp = Blueprint('documents', __name__, url_prefix='/api/documents')

@documents_bp.route('', methods=['GET'])
def get_documents():
    """Get all documents"""
    try:
        documents = Document.get_all()
        return jsonify({
            'success': True,
            'documents': documents
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@documents_bp.route('/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get a specific document by ID"""
    try:
        document = Document.get_by_id(doc_id)
        if not document:
            return jsonify({
                'success': False,
                'error': 'Document not found'
            }), 404
        
        # Get related data
        dialogues = Dialogue.get_by_document(doc_id)
        summaries = Summary.get_by_document(doc_id)
        
        return jsonify({
            'success': True,
            'document': document,
            'dialogues': dialogues,
            'summaries': summaries
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@documents_bp.route('/youtube', methods=['POST'])
def upload_youtube():
    """Process a YouTube video URL"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        url = data.get('url', '').strip()
        title = data.get('title', '').strip()
        
        # Validate URL is provided
        if not url:
            return jsonify({
                'success': False,
                'error': 'YouTube URL is required'
            }), 400
        
        # Validate YouTube URL format
        if not is_valid_youtube_url(url):
            return jsonify({
                'success': False,
                'error': 'Invalid YouTube URL. Please provide a valid YouTube video URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID or https://youtu.be/VIDEO_ID)'
            }), 400
        
        # Process the YouTube video
        try:
            video_data = process_youtube_video(url, title)
        except ValueError as ve:
            # Handle validation errors from youtube_service
            return jsonify({
                'success': False,
                'error': str(ve)
            }), 400
        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Error processing YouTube video: {str(e)}'
            }), 500
        
        # Save to database
        doc_id = Document.create(
            title=video_data['title'],
            doc_type='youtube',
            content=video_data['transcript'],
            source_url=url
        )
        
        # Get the created document
        document = Document.get_by_id(doc_id)
        
        return jsonify({
            'success': True,
            'message': 'YouTube video processed successfully',
            'document': document
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

@documents_bp.route('/pdf', methods=['POST'])
def upload_pdf():
    """Upload and process a PDF file"""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Validate file type
        if not is_allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only PDF files are allowed'
            }), 400
        
        # Get optional title from form data
        title = request.form.get('title', '').strip()
        
        # Save the file
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Process the PDF
        try:
            pdf_data = process_pdf(file_path, title)
        except Exception as e:
            # Clean up file if processing fails
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({
                'success': False,
                'error': f'Error processing PDF: {str(e)}'
            }), 500
        
        # Save to database
        doc_id = Document.create(
            title=pdf_data['title'],
            doc_type='pdf',
            content=pdf_data['content'],
            source_url=file_path
        )
        
        # Get the created document
        document = Document.get_by_id(doc_id)
        
        return jsonify({
            'success': True,
            'message': 'PDF uploaded and processed successfully',
            'document': document
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

@documents_bp.route('/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a document"""
    try:
        document = Document.get_by_id(doc_id)
        if not document:
            return jsonify({
                'success': False,
                'error': 'Document not found'
            }), 404
        
        # Delete associated file if it's a PDF
        if document['type'] == 'pdf' and document['source_url']:
            file_path = document['source_url']
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Delete from database
        Document.delete(doc_id)
        
        return jsonify({
            'success': True,
            'message': 'Document deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
