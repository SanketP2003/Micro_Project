# Study Tool Application

A web application for processing educational content from PDFs and YouTube videos, generating interactive study materials including dialogues, summaries, and Q&A.

## Features

- **YouTube Video Processing**: Extract transcripts from YouTube videos for study purposes
- **PDF Upload**: Upload and extract text content from PDF documents
- **Document Management**: Store and manage processed documents
- **SQLite Database**: Lightweight database for storing documents, dialogues, summaries, and questions

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Project Structure

```
Micro_Project/
├── backend/
│   ├── models/
│   │   └── database.py       # SQLite database models and operations
│   ├── routes/
│   │   └── documents.py      # API routes for document operations
│   ├── services/
│   │   ├── youtube_service.py # YouTube URL validation and processing
│   │   └── pdf_service.py     # PDF text extraction
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Application configuration
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Tool.jsx       # Main UI component
│   │   ├── App.jsx
│   │   ├── main.jsx           # React entry point with Router config
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the Flask server:
```bash
python app.py
```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

## API Endpoints

### Documents

- `GET /api/documents` - Get all documents
- `GET /api/documents/<id>` - Get a specific document with dialogues and summaries
- `POST /api/documents/youtube` - Process a YouTube video
  - Body: `{ "url": "https://youtube.com/...", "title": "optional" }`
- `POST /api/documents/pdf` - Upload and process a PDF file
  - Form data with file and optional title
- `DELETE /api/documents/<id>` - Delete a document

### Health Check

- `GET /health` - Check if the API is running
- `GET /` - Get API information and available endpoints

## Key Features Implemented

### YouTube URL Validation (Fix for 400 BAD REQUEST)

The application now includes robust YouTube URL validation in `backend/services/youtube_service.py`:

- Validates YouTube URL format before processing
- Supports multiple YouTube URL formats:
  - `https://www.youtube.com/watch?v=VIDEO_ID`
  - `https://youtu.be/VIDEO_ID`
  - `https://www.youtube.com/embed/VIDEO_ID`
  - `https://m.youtube.com/watch?v=VIDEO_ID`
- Returns clear error messages for invalid URLs
- Extracts video ID correctly from various URL formats

### Database (SQLite)

- Migrated from MySQL to SQLite for easier deployment
- Automatic database initialization on startup
- Tables for documents, dialogues, summaries, and user questions
- Proper foreign key relationships and constraints

### React Router Configuration

- Fixed React Router deprecation warnings by adding future flags:
  - `v7_startTransition`: Enables React 18 transitions
  - `v7_relativeSplatPath`: Prepares for v7 relative path behavior

## Database Schema

### documents
- `id` - Primary key
- `title` - Document title
- `type` - 'pdf' or 'youtube'
- `content` - Extracted text content
- `source_url` - Original file path or YouTube URL
- `created_at`, `updated_at` - Timestamps

### dialogues
- `id` - Primary key
- `document_id` - Foreign key to documents
- `content` - Dialogue text
- `created_at` - Timestamp

### summaries
- `id` - Primary key
- `document_id` - Foreign key to documents
- `content` - Summary text
- `created_at` - Timestamp

### user_questions
- `id` - Primary key
- `document_id` - Foreign key to documents
- `question` - User's question
- `answer` - Generated answer
- `created_at` - Timestamp

## Future Enhancements

- Implement actual YouTube transcript fetching using `youtube-transcript-api`
- Implement PDF text extraction using `PyPDF2` or `pdfplumber`
- Add dialogue generation using AI models
- Add summary generation
- Add Q&A functionality
- Add user authentication
- Add document search and filtering

## Troubleshooting

### 400 BAD REQUEST on YouTube endpoint

This has been fixed! The issue was caused by missing URL validation. The application now:
1. Validates YouTube URL format before processing
2. Returns clear error messages for invalid URLs
3. Handles various YouTube URL formats correctly

### Database connection issues

The application now uses SQLite instead of MySQL, eliminating connection issues. The database is automatically created in `backend/database/study_tool.db`.

### React Router warnings

Fixed by adding future flags to BrowserRouter in `frontend/src/main.jsx`.

## License

This project is for educational purposes.
