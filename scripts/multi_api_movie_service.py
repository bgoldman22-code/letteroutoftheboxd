#!/usr/bin/env python3
"""
Multi-API Movie Data Service
Combines multiple free movie APIs for maximum reliability and data coverage
"""

import os
import json
import requests
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv('.env.local')

class MultiAPIMovieService:
    """Service that combines multiple movie APIs for comprehensive data"""
    
    def __init__(self):
        # API configurations
        self.omdb_key = os.getenv('OMDB_API_KEY', 'trilogy')
        self.watchmode_key = os.getenv('WATCHMODE_API_KEY')
        
        self.apis = {
            'omdb': {
                'base_url': 'http://www.omdbapi.com/',
                'rate_limit': 1000,  # per day
                'requires_key': True
            },
            'free_imdb': {
                'base_url': 'https://imdb.iamidiotareyoutoo.com/',
                'rate_limit': float('inf'),  # No documented limit
                'requires_key': False
            },
            'tastedive': {
                'base_url': 'https://tastedive.com/api/similar',
                'rate_limit': 300,  # per hour
                'requires_key': False
            },
            'watchmode': {
                'base_url': 'https://api.watchmode.com/v1/',
                'rate_limit': 1000,  # per day free tier
                'requires_key': True
            }
        }
        
        # Rate limiting
        self.last_request_time = {}
        self.request_counts = {}
    
    def get_movie_data(self, title: str, year: int = None, imdb_id: str = None) -> Dict[str, Any]:
        """Get comprehensive movie data from multiple APIs"""
        movie_data = {}
        
        # Try OMDb first (most comprehensive)
        omdb_data = self.get_omdb_data(title, year, imdb_id)
        if omdb_data:
            movie_data = omdb_data
            movie_data['primary_source'] = 'omdb'
        
        # Fallback to Free IMDb API
        if not movie_data:
            free_imdb_data = self.get_free_imdb_data(title, year)
            if free_imdb_data:
                movie_data = free_imdb_data
                movie_data['primary_source'] = 'free_imdb'
        
        # Add streaming data from Watchmode
        if movie_data and self.watchmode_key:
            streaming_data = self.get_watchmode_streaming(title, year)
            if streaming_data:
                movie_data['streaming'] = streaming_data
        
        # Get similar movies from TasteDive
        if movie_data:
            similar_movies = self.get_tastedive_similar(title)
            if similar_movies:
                movie_data['similar_movies'] = similar_movies
        
        return movie_data
    
    def get_omdb_data(self, title: str, year: int = None, imdb_id: str = None) -> Dict:
        """Get movie data from OMDb API"""
        params = {
            'apikey': self.omdb_key,
            'type': 'movie'
        }
        
        if imdb_id:
            params['i'] = imdb_id
        else:
            params['t'] = title
            if year:
                params['y'] = year
        
        try:
            response = requests.get(self.apis['omdb']['base_url'], params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return self._normalize_omdb_data(data)
        except Exception as e:
            print(f"OMDb API error: {e}")
        
        return {}
    
    def get_free_imdb_data(self, title: str, year: int = None) -> Dict:
        """Get movie data from Free IMDb API"""
        search_url = f"{self.apis['free_imdb']['base_url']}search"
        params = {'q': title}
        
        try:
            # Search for the movie
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                search_results = response.json()
                if search_results.get('results'):
                    # Find best match
                    best_match = self._find_best_match(search_results['results'], title, year)
                    if best_match:
                        # Get detailed info
                        movie_id = best_match.get('id')
                        if movie_id:
                            detail_url = f"{self.apis['free_imdb']['base_url']}movie"
                            detail_response = requests.get(detail_url, params={'id': movie_id}, timeout=10)
                            if detail_response.status_code == 200:
                                movie_detail = detail_response.json()
                                return self._normalize_free_imdb_data(movie_detail)
        except Exception as e:
            print(f"Free IMDb API error: {e}")
        
        return {}
    
    def get_tastedive_similar(self, title: str, limit: int = 10) -> List[Dict]:
        """Get similar movies from TasteDive API"""
        params = {
            'q': f'movie:{title}',
            'type': 'movies',
            'info': 1,
            'limit': limit
        }
        
        try:
            response = requests.get(self.apis['tastedive']['base_url'], params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                similar = data.get('Similar', {}).get('Results', [])
                return [
                    {
                        'title': movie.get('Name', ''),
                        'description': movie.get('wTeaser', ''),
                        'url': movie.get('wUrl', ''),
                        'youtube_trailer': movie.get('yUrl', '')
                    }
                    for movie in similar
                ]
        except Exception as e:
            print(f"TasteDive API error: {e}")
        
        return []
    
    def get_watchmode_streaming(self, title, year=None):
        """Get streaming availability from Watchmode API"""
        if not self.watchmode_key:
            return {}
            
        try:
            # First search for the title
            search_url = f"{self.apis['watchmode']['base_url']}autocomplete-search/"
            params = {
                'apiKey': self.watchmode_key,
                'search_value': title,
                'search_type': 1  # Movies only
            }
            
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code != 200:
                return {}
                
            search_results = response.json()
            if not search_results.get('results'):
                return {}
            
            # Find the best match (optionally filter by year)
            movie_id = None
            for result in search_results['results']:
                if year and result.get('year') and abs(int(result['year']) - int(year)) > 1:
                    continue
                movie_id = result['id']
                break
            
            if not movie_id:
                movie_id = search_results['results'][0]['id']
            
            # Get streaming sources for the movie
            sources_url = f"{self.apis['watchmode']['base_url']}title/{movie_id}/sources/"
            params = {'apiKey': self.watchmode_key}
            
            response = requests.get(sources_url, params=params, timeout=10)
            if response.status_code != 200:
                return {}
            
            sources_data = response.json()
            streaming_sources = []
            
            for source in sources_data:
                streaming_sources.append({
                    'name': source.get('name', ''),
                    'type': source.get('type', ''),  # subscription, rent, buy, etc.
                    'url': source.get('web_url', ''),
                    'price': source.get('price', 0),
                    'currency': source.get('currency', 'USD')
                })
            
            return {
                'streaming_sources': streaming_sources,
                'total_sources': len(streaming_sources)
            }
            
        except Exception as e:
            print(f"Error fetching Watchmode data: {e}")
            return {}
    
    def search_movies(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for movies across multiple APIs"""
        results = []
        
        # Try OMDb search first
        omdb_results = self._search_omdb(query, limit)
        results.extend(omdb_results)
        
        # If not enough results, try Free IMDb
        if len(results) < limit:
            free_imdb_results = self._search_free_imdb(query, limit - len(results))
            results.extend(free_imdb_results)
        
        return results[:limit]
    
    def _search_omdb(self, query: str, limit: int) -> List[Dict]:
        """Search OMDb API"""
        results = []
        params = {
            'apikey': self.omdb_key,
            's': query,
            'type': 'movie'
        }
        
        try:
            response = requests.get(self.apis['omdb']['base_url'], params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    search_results = data.get('Search', [])
                    for movie in search_results[:limit]:
                        results.append(self._normalize_omdb_search_result(movie))
        except Exception as e:
            print(f"OMDb search error: {e}")
        
        return results
    
    def _search_free_imdb(self, query: str, limit: int) -> List[Dict]:
        """Search Free IMDb API"""
        results = []
        search_url = f"{self.apis['free_imdb']['base_url']}search"
        params = {'q': query}
        
        try:
            response = requests.get(search_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                search_results = data.get('results', [])
                for movie in search_results[:limit]:
                    results.append(self._normalize_free_imdb_search_result(movie))
        except Exception as e:
            print(f"Free IMDb search error: {e}")
        
        return results
    
    def _normalize_omdb_data(self, data: Dict) -> Dict:
        """Normalize OMDb API response to standard format"""
        return {
            'title': data.get('Title', ''),
            'year': self._safe_int(data.get('Year')),
            'director': data.get('Director', ''),
            'cast': self._parse_cast(data.get('Actors', '')),
            'genres': self._parse_genres(data.get('Genre', '')),
            'plot_summary': data.get('Plot', ''),
            'runtime': data.get('Runtime', ''),
            'imdb_rating': data.get('imdbRating', ''),
            'imdb_id': data.get('imdbID', ''),
            'poster_url': data.get('Poster', ''),
            'ratings': self._parse_ratings(data.get('Ratings', [])),
            'source': 'omdb'
        }
    
    def _normalize_omdb_search_result(self, movie: Dict) -> Dict:
        """Normalize OMDb search result"""
        return {
            'title': movie.get('Title', ''),
            'year': self._safe_int(movie.get('Year')),
            'imdb_id': movie.get('imdbID', ''),
            'poster_url': movie.get('Poster', ''),
            'source': 'omdb'
        }
    
    def _normalize_free_imdb_data(self, data: Dict) -> Dict:
        """Normalize Free IMDb API response to standard format"""
        movie = data
        return {
            'title': movie.get('title', movie.get('Title', '')),
            'year': self._safe_int(movie.get('year', movie.get('Year', 0))),
            'director': movie.get('director', movie.get('Director', '')),
            'cast': self._parse_cast(movie.get('cast', movie.get('Actors', ''))),
            'genres': self._parse_genres(movie.get('genre', movie.get('Genre', ''))),
            'plot_summary': movie.get('plot', movie.get('Plot', '')),
            'runtime': movie.get('runtime', movie.get('Runtime', '')),
            'imdb_rating': movie.get('rating', movie.get('imdbRating', '')),
            'imdb_id': movie.get('imdb_id', movie.get('imdbID', '')),
            'poster_url': movie.get('poster', movie.get('Poster', '')),
            'source': 'free_imdb'
        }
    
    def _normalize_free_imdb_search_result(self, movie: Dict) -> Dict:
        """Normalize Free IMDb search result"""
        return {
            'title': movie.get('title', ''),
            'year': self._safe_int(movie.get('year', 0)),
            'imdb_id': movie.get('id', ''),
            'poster_url': movie.get('poster', ''),
            'source': 'free_imdb'
        }
    
    def _find_best_match(self, results: List[Dict], title: str, year: int = None) -> Dict:
        """Find best matching movie from search results"""
        title_lower = title.lower()
        
        for movie in results:
            movie_title = movie.get('title', movie.get('Title', '')).lower()
            movie_year = self._safe_int(movie.get('year', movie.get('Year', 0)))
            
            # Exact title match
            if movie_title == title_lower:
                if not year or movie_year == year:
                    return movie
            
            # Partial title match
            if title_lower in movie_title or movie_title in title_lower:
                if not year or abs(movie_year - year) <= 1:  # Allow 1 year difference
                    return movie
        
        # Return first result if no good match
        return results[0] if results else {}
    
    def _parse_ratings(self, ratings: List[Dict]) -> Dict:
        """Parse ratings array from OMDb"""
        parsed = {}
        for rating in ratings:
            source = rating.get('Source', '')
            value = rating.get('Value', '')
            
            if 'Internet Movie Database' in source:
                parsed['imdb'] = value
            elif 'Rotten Tomatoes' in source:
                parsed['rotten_tomatoes'] = value
            elif 'Metacritic' in source:
                parsed['metacritic'] = value
        
        return parsed
    
    def _parse_genres(self, genres_str: str) -> List[str]:
        """Parse genres string into list"""
        if not genres_str or genres_str == 'N/A':
            return ['Drama']  # Default genre
        
        return [g.strip() for g in genres_str.split(',') if g.strip()]
    
    def _parse_cast(self, cast_str: str) -> List[str]:
        """Parse cast string into list"""
        if not cast_str or cast_str == 'N/A':
            return []
        
        return [a.strip() for a in cast_str.split(',') if a.strip()][:5]
    
    def _safe_int(self, value: Any) -> int:
        """Safely convert value to int"""
        try:
            if isinstance(value, str):
                # Extract first number from string
                import re
                match = re.search(r'\d+', value)
                return int(match.group()) if match else 0
            return int(value) if value else 0
        except (ValueError, TypeError):
            return 0
    
    def _create_slug(self, title: str) -> str:
        """Create URL-friendly slug from title"""
        import re
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug.strip('-')
    
    def get_popular_movies_sample(self, count: int = 10) -> List[Dict]:
        """Generate a sample dataset of popular movies"""
        popular_titles = [
            ('The Dark Knight', 2008),
            ('Pulp Fiction', 1994),
            ('The Shawshank Redemption', 1994),
            ('Inception', 2010),
            ('The Godfather', 1972),
            ('Forrest Gump', 1994),
            ('The Matrix', 1999),
            ('Goodfellas', 1990),
            ('The Lord of the Rings: The Return of the King', 2003),
            ('Fight Club', 1999),
            ('Interstellar', 2014),
            ('The Silence of the Lambs', 1991),
            ('Saving Private Ryan', 1998),
            ('Schindler\'s List', 1993),
            ('Se7en', 1995)
        ]
        
        movies = []
        for title, year in popular_titles[:count]:
            print(f"Fetching data for: {title} ({year})")
            movie_data = self.get_movie_data(title, year)
            if movie_data:
                movies.append(movie_data)
                time.sleep(0.5)  # Rate limiting
        
        return movies

if __name__ == "__main__":
    # Test the service
    service = MultiAPIMovieService()
    
    print("🎬 Multi-API Movie Service Test")
    print("=" * 40)
    
    # Test single movie lookup
    print("1. Testing single movie lookup:")
    movie = service.get_movie_data("The Dark Knight", 2008)
    if movie:
        print(f"✅ Found: {movie.get('title')} ({movie.get('year')})")
        print(f"   Director: {movie.get('director')}")
        print(f"   IMDb Rating: {movie.get('imdb_rating')}")
        print(f"   Source: {movie.get('primary_source')}")
        print(f"   Similar movies: {len(movie.get('similar_movies', []))}")
        if movie.get('streaming'):
            print(f"   Streaming sources: {movie['streaming'].get('total_sources', 0)}")
    
    # Test search functionality
    print("\n2. Testing movie search:")
    results = service.search_movies("Batman", 5)
    print(f"✅ Found {len(results)} Batman movies")
    
    # Test sample dataset
    print("\n3. Creating sample dataset:")
    sample_movies = service.get_popular_movies_sample(5)
    print(f"✅ Generated {len(sample_movies)} sample movies")
    
    # Save sample data
    os.makedirs('data', exist_ok=True)
    with open('data/multi_api_movies.json', 'w') as f:
        json.dump(sample_movies, f, indent=2)
    
    print(f"\n💾 Sample data saved to data/multi_api_movies.json")
    print("🚀 Ready for AI analysis!")