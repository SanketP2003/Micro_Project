import React, { useState } from 'react'

const API_BASE_URL = 'http://localhost:5000/api'

function Tool() {
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [youtubeTitle, setYoutubeTitle] = useState('')
  const [pdfTitle, setPdfTitle] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [documents, setDocuments] = useState([])

  const handleYoutubeSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    setError('')

    try {
      const response = await fetch(`${API_BASE_URL}/documents/youtube`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: youtubeUrl,
          title: youtubeTitle || undefined,
        }),
      })

      const data = await response.json()

      if (response.ok && data.success) {
        setMessage(data.message || 'YouTube video processed successfully!')
        setYoutubeUrl('')
        setYoutubeTitle('')
        fetchDocuments()
      } else {
        setError(data.error || 'Failed to process YouTube video')
      }
    } catch (err) {
      setError(`Network error: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handlePdfUpload = async (e) => {
    e.preventDefault()
    setLoading(true)
    setMessage('')
    setError('')

    const fileInput = document.getElementById('pdfFile')
    const file = fileInput?.files[0]

    if (!file) {
      setError('Please select a PDF file')
      setLoading(false)
      return
    }

    const formData = new FormData()
    formData.append('file', file)
    if (pdfTitle) {
      formData.append('title', pdfTitle)
    }

    try {
      const response = await fetch(`${API_BASE_URL}/documents/pdf`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (response.ok && data.success) {
        setMessage(data.message || 'PDF uploaded successfully!')
        fileInput.value = ''
        setPdfTitle('')
        fetchDocuments()
      } else {
        setError(data.error || 'Failed to upload PDF')
      }
    } catch (err) {
      setError(`Network error: ${err.message}`)
    } finally {
      setLoading(false)
    }
  }

  const fetchDocuments = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/documents`)
      const data = await response.json()

      if (response.ok && data.success) {
        setDocuments(data.documents || [])
      }
    } catch (err) {
      console.error('Error fetching documents:', err)
    }
  }

  React.useEffect(() => {
    fetchDocuments()
  }, [])

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>Study Tool - Document Processor</h1>

      {message && (
        <div style={{ padding: '10px', backgroundColor: '#d4edda', color: '#155724', marginBottom: '20px', borderRadius: '4px' }}>
          {message}
        </div>
      )}

      {error && (
        <div style={{ padding: '10px', backgroundColor: '#f8d7da', color: '#721c24', marginBottom: '20px', borderRadius: '4px' }}>
          {error}
        </div>
      )}

      <div style={{ marginBottom: '30px' }}>
        <h2>Process YouTube Video</h2>
        <form onSubmit={handleYoutubeSubmit}>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="youtubeUrl" style={{ display: 'block', marginBottom: '5px' }}>
              YouTube URL (required):
            </label>
            <input
              id="youtubeUrl"
              type="text"
              value={youtubeUrl}
              onChange={(e) => setYoutubeUrl(e.target.value)}
              placeholder="https://www.youtube.com/watch?v=..."
              required
              style={{ width: '100%', padding: '8px', fontSize: '14px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="youtubeTitle" style={{ display: 'block', marginBottom: '5px' }}>
              Title (optional):
            </label>
            <input
              id="youtubeTitle"
              type="text"
              value={youtubeTitle}
              onChange={(e) => setYoutubeTitle(e.target.value)}
              placeholder="My YouTube Video"
              style={{ width: '100%', padding: '8px', fontSize: '14px' }}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '10px 20px',
              backgroundColor: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Processing...' : 'Process YouTube Video'}
          </button>
        </form>
      </div>

      <div style={{ marginBottom: '30px' }}>
        <h2>Upload PDF</h2>
        <form onSubmit={handlePdfUpload}>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="pdfFile" style={{ display: 'block', marginBottom: '5px' }}>
              PDF File (required):
            </label>
            <input
              id="pdfFile"
              type="file"
              accept=".pdf"
              required
              style={{ width: '100%', padding: '8px', fontSize: '14px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="pdfTitle" style={{ display: 'block', marginBottom: '5px' }}>
              Title (optional):
            </label>
            <input
              id="pdfTitle"
              type="text"
              value={pdfTitle}
              onChange={(e) => setPdfTitle(e.target.value)}
              placeholder="My PDF Document"
              style={{ width: '100%', padding: '8px', fontSize: '14px' }}
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            style={{
              padding: '10px 20px',
              backgroundColor: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Uploading...' : 'Upload PDF'}
          </button>
        </form>
      </div>

      <div>
        <h2>Documents ({documents.length})</h2>
        {documents.length === 0 ? (
          <p>No documents yet. Upload a PDF or process a YouTube video to get started.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {documents.map((doc) => (
              <li
                key={doc.id}
                style={{
                  padding: '15px',
                  marginBottom: '10px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                }}
              >
                <strong>{doc.title}</strong> <span style={{ color: '#666' }}>({doc.type})</span>
                <br />
                <small style={{ color: '#999' }}>
                  Created: {new Date(doc.created_at).toLocaleString()}
                </small>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default Tool
