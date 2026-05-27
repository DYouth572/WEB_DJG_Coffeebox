"""
Vercel serverless function entry point for Django
"""
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
from django.core.wsgi import get_wsgi_application

# Get the WSGI application
django_app = get_wsgi_application()

# Vercel serverless function handler
def handler(event, context):
    """
    Vercel serverless function handler that converts Vercel events to WSGI format
    """
    from django.core.handlers.wsgi import WSGIHandler
    from io import BytesIO
    
    # Create WSGI handler
    wsgi_handler = WSGIHandler()
    
    # Extract request information from Vercel event
    method = event.get('method', 'GET')
    path = event.get('path', '/')
    query_string = event.get('query', '')
    headers = event.get('headers', {})
    body = event.get('body', '')
    
    # Build WSGI environ
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': query_string,
        'SERVER_NAME': headers.get('host', 'localhost'),
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': BytesIO(body.encode() if body else b''),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': True,
        'wsgi.run_once': False,
    }
    
    # Add headers to environ
    for key, value in headers.items():
        key_upper = key.upper().replace('-', '_')
        if key_upper not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key_upper}'] = value
        else:
            environ[key_upper] = value
    
    # Set content length
    if body:
        environ['CONTENT_LENGTH'] = str(len(body))
    
    # Call WSGI application
    response_body = []
    status_code = 200
    response_headers = []
    
    def start_response(status, headers):
        nonlocal status_code, response_headers
        # Parse status code from status string (e.g., "200 OK" or "500 Internal Server Error")
        try:
            status_code = int(status.split(' ')[0])
        except (ValueError, IndexError):
            status_code = 500  # Default to 500 if parsing fails
        response_headers = headers
        return response_body.append
    
    # Execute the WSGI app
    response_iter = wsgi_handler(environ, start_response)
    
    # Collect response body
    for chunk in response_iter:
        if isinstance(chunk, str):
            response_body.append(chunk)
        else:
            response_body.append(chunk.decode('utf-8'))
    
    # Convert headers to dict
    headers_dict = {}
    for key, value in response_headers:
        headers_dict[key] = value
    
    # Return Vercel response format
    body_content = ''.join(response_body)
    # Ensure body is string (Vercel expects string)
    if isinstance(body_content, bytes):
        body_content = body_content.decode('utf-8')
    
    return {
        'statusCode': status_code,
        'headers': headers_dict,
        'body': body_content,
    }

# For Vercel Python runtime
app = handler
