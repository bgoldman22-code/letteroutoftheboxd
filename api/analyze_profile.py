"""
Vercel Python API - Analyze Letterboxd Profile
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

try:
    from letterboxd_scraper import LetterboxdScraper
except ImportError:
    LetterboxdScraper = None


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get request body
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8'))
            
            username = data.get('username')
            if not username:
                self.send_error(400, 'Username is required')
                return
            
            if not LetterboxdScraper:
                self.send_error(500, 'Letterboxd scraper not available')
                return
            
            # Scrape profile
            scraper = LetterboxdScraper()
            profile = scraper.get_user_profile(username)
            
            if not profile:
                self.send_error(404, f'Profile not found for {username}')
                return
            
            # Get ratings
            ratings = scraper.get_user_ratings(username, limit=100)
            loved_movies = [r for r in ratings if r.get('rating', 0) >= 4]
            
            # Enrich with movie data
            loved_movies = scraper.enrich_ratings_with_movie_data(loved_movies[:20])
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'success': True,
                'data': {
                    'profile': profile,
                    'loved_movies': loved_movies,
                    'total_ratings': len(ratings)
                },
                'message': f'Successfully analyzed {username}'
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'message': 'Use POST method with { "username": "letterboxd_username" }',
            'endpoint': '/api/analyze_profile'
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
