import os

def is_allowed_file(filename):
    """Check if the file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

def extract_text_from_pdf(file_path):
    """
    Extract text content from a PDF file.
    This is a placeholder that should be replaced with actual PDF extraction logic.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        # TODO: Implement actual PDF text extraction
        # In production, you would use PyPDF2 or pdfplumber:
        # import PyPDF2
        # with open(file_path, 'rb') as file:
        #     pdf_reader = PyPDF2.PdfReader(file)
        #     text = ''
        #     for page in pdf_reader.pages:
        #         text += page.extract_text()
        #     return text
        
        raise NotImplementedError(
            "PDF text extraction is not yet implemented. "
            "Install PyPDF2 or pdfplumber and implement the extraction logic."
        )
    
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def process_pdf(file_path, title=None):
    """
    Process a PDF file and extract its content.
    Returns a dictionary with PDF information and text content.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError("PDF file not found")
    
    # Extract text from PDF
    try:
        content = extract_text_from_pdf(file_path)
    except NotImplementedError:
        # For now, use placeholder content
        filename = os.path.basename(file_path)
        content = f"Content extracted from {filename} would appear here."
    
    # Generate title if not provided
    if not title:
        title = os.path.basename(file_path).replace('.pdf', '')
    
    return {
        'title': title,
        'content': content,
        'file_path': file_path
    }
