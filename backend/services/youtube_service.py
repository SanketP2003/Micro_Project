import re
from urllib.parse import urlparse, parse_qs

def is_valid_youtube_url(url):
    """
    Validate if the URL is a valid YouTube URL.
    Supports various YouTube URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://m.youtube.com/watch?v=VIDEO_ID
    """
    if not url or not isinstance(url, str):
        return False
    
    # YouTube URL patterns
    youtube_patterns = [
        r'^https?://(?:www\.)?youtube\.com/watch\?.*v=[\w-]+',
        r'^https?://youtu\.be/[\w-]+',
        r'^https?://(?:www\.)?youtube\.com/embed/[\w-]+',
        r'^https?://m\.youtube\.com/watch\?v=[\w-]+'
    ]
    
    for pattern in youtube_patterns:
        if re.match(pattern, url.strip()):
            return True
    
    return False

def extract_video_id(url):
    """
    Extract the video ID from a YouTube URL.
    Returns None if the URL is invalid or video ID cannot be extracted.
    """
    if not is_valid_youtube_url(url):
        return None
    
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Check for different YouTube URL formats
    if parsed_url.hostname in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
        if parsed_url.path == '/watch':
            # Standard watch URL: https://www.youtube.com/watch?v=VIDEO_ID
            query_params = parse_qs(parsed_url.query)
            return query_params.get('v', [None])[0]
        elif parsed_url.path.startswith('/embed/'):
            # Embed URL: https://www.youtube.com/embed/VIDEO_ID
            return parsed_url.path.split('/')[2]
    elif parsed_url.hostname == 'youtu.be':
        # Short URL: https://youtu.be/VIDEO_ID
        return parsed_url.path[1:]
    
    return None

def get_youtube_transcript(url):
    """
    Fetch the transcript/captions for a YouTube video.
    This is a placeholder implementation that should be replaced with
    actual transcript fetching logic using youtube-transcript-api or similar.
    """
    try:
        # Validate YouTube URL first
        if not is_valid_youtube_url(url):
            raise ValueError("Invalid YouTube URL. Please provide a valid YouTube video URL.")
        
        # Extract video ID
        video_id = extract_video_id(url)
        if not video_id:
            raise ValueError("Could not extract video ID from URL. Please check the URL format.")
        
        # TODO: Implement actual transcript fetching
        # For now, return a placeholder for demonstration
        # In production, you would use youtube-transcript-api:
        # from youtube_transcript_api import YouTubeTranscriptApi
        # transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # transcript_text = ' '.join([t['text'] for t in transcript_list])
        # return transcript_text
        
        # Return placeholder content for demonstration
        return f"[Placeholder transcript for YouTube video {video_id}. Install youtube-transcript-api for actual transcript fetching.]"
    
    except ValueError as ve:
        # Re-raise validation errors
        raise ve
    except Exception as e:
        raise Exception(f"Error fetching YouTube transcript: {str(e)}")

def process_youtube_video(url, title=None):
    """
    Process a YouTube video URL and extract its content.
    Returns a dictionary with video information and transcript.
    """
    # Validate URL first
    if not is_valid_youtube_url(url):
        raise ValueError("Invalid YouTube URL. Please provide a valid YouTube video URL.")
    
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Could not extract video ID from URL. Please check the URL format.")
    
    # Get transcript
    transcript = get_youtube_transcript(url)
    
    # Generate title if not provided
    if not title:
        title = f"YouTube Video {video_id}"
    
    return {
        'video_id': video_id,
        'url': url,
        'title': title,
        'transcript': transcript
    }
