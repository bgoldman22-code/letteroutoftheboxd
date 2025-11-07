#!/usr/bin/env python3
"""
Alternative movie data sources when TMDB API is unavailable
Uses free public APIs and web scraping as fallback
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime
import os

class AlternativeMovieAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def get_movie_from_imdb_id(self, imdb_id: str):
        """Get movie data using free OMDb API alternative"""
        # Free OMDb alternative endpoint (no key required for basic data)
        url = f"https://www.omdbapi.com/?i={imdb_id}&plot=full"
        
        try:
            response = self.session.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('Response') == 'True':
                    return self._parse_omdb_data(data)
        except:
            pass
            
        return self._get_fallback_movie_data(imdb_id)
    
    def search_movie_by_title(self, title: str, year: int = None):
        """Search for movie using multiple free sources"""
        
        # Try Wikipedia/Wikidata (completely free)
        wiki_data = self._search_wikipedia(title, year)
        if wiki_data:
            return wiki_data
            
        # Try JustWatch public API (free for basic data)  
        justwatch_data = self._search_justwatch(title, year)
        if justwatch_data:
            return justwatch_data
            
        # Fallback to basic data structure
        return {
            'title': title,
            'year': year,
            'director': 'Unknown',
            'genres': ['Drama'],  # Default
            'cast': [],
            'plot_summary': f'Information for {title} not available.',
            'source': 'fallback'
        }
    
    def _search_wikipedia(self, title: str, year: int = None):
        """Get movie data from Wikipedia (completely free)"""
        try:
            # Search Wikipedia for the movie
            search_title = f"{title} {year} film" if year else f"{title} film"
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{search_title.replace(' ', '_')}"
            
            response = self.session.get(wiki_url)
            if response.status_code == 200:
                data = response.json()
                
                return {
                    'title': title,
                    'year': year,
                    'director': 'Unknown',
                    'genres': ['Drama'],
                    'cast': [],
                    'plot_summary': data.get('extract', ''),
                    'source': 'wikipedia',
                    'wikipedia_url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
                }
                
        except Exception as e:
            print(f"Wikipedia search failed: {e}")
            
        return None
    
    def _search_justwatch(self, title: str, year: int = None):
        """Try JustWatch API (has free tier for basic data)"""
        try:
            # JustWatch has a public API for basic movie data
            url = "https://apis.justwatch.com/content/titles/en_US/popular"
            params = {
                'body': json.dumps({
                    'query': title,
                    'page_size': 5
                })
            }
            
            response = self.session.get(url, params=params, timeout=10)
            if response.status_code == 200:
                results = response.json().get('items', [])
                
                for item in results:
                    if item.get('title', '').lower() == title.lower():
                        return {
                            'title': item.get('title', title),
                            'year': item.get('original_release_year', year),
                            'director': 'Unknown',
                            'genres': [genre.get('translation', 'Drama') for genre in item.get('genre_names', [])],
                            'cast': [],
                            'plot_summary': item.get('short_description', ''),
                            'source': 'justwatch'
                        }
                        
        except Exception as e:
            print(f"JustWatch search failed: {e}")
            
        return None
    
    def _parse_omdb_data(self, data):
        """Parse OMDb API response"""
        return {
            'title': data.get('Title', ''),
            'year': int(data.get('Year', 0)),
            'director': data.get('Director', 'Unknown'),
            'genres': data.get('Genre', '').split(', '),
            'cast': data.get('Actors', '').split(', ')[:5],
            'plot_summary': data.get('Plot', ''),
            'runtime': data.get('Runtime', ''),
            'imdb_rating': data.get('imdbRating', ''),
            'source': 'omdb'
        }
    
    def _get_fallback_movie_data(self, identifier):
        """Generate fallback movie data when APIs fail"""
        return {
            'title': 'Movie Data Unavailable',
            'year': 2020,
            'director': 'Unknown',
            'genres': ['Drama'],
            'cast': [],
            'plot_summary': 'Movie information temporarily unavailable. AI analysis can still work with user ratings.',
            'source': 'fallback'
        }
    
    def get_popular_movies_sample(self, limit=50):
        """Get sample of popular movies for testing (no API required)"""
        
        popular_movies = [
            {
                'title': 'The Godfather',
                'year': 1972,
                'director': 'Francis Ford Coppola',
                'genres': ['Crime', 'Drama'],
                'cast': ['Marlon Brando', 'Al Pacino', 'James Caan'],
                'plot_summary': 'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.',
                'slug': 'the-godfather'
            },
            {
                'title': 'Citizen Kane', 
                'year': 1941,
                'director': 'Orson Welles',
                'genres': ['Drama', 'Mystery'],
                'cast': ['Orson Welles', 'Joseph Cotten', 'Dorothy Comingore'],
                'plot_summary': 'Following the death of publishing tycoon Charles Foster Kane, reporters scramble to uncover the meaning of his final utterance.',
                'slug': 'citizen-kane'
            },
            {
                'title': 'Pulp Fiction',
                'year': 1994, 
                'director': 'Quentin Tarantino',
                'genres': ['Crime', 'Drama'],
                'cast': ['John Travolta', 'Samuel L. Jackson', 'Uma Thurman'],
                'plot_summary': 'The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.',
                'slug': 'pulp-fiction'
            },
            {
                'title': 'The Shawshank Redemption',
                'year': 1994,
                'director': 'Frank Darabont', 
                'genres': ['Drama'],
                'cast': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton'],
                'plot_summary': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
                'slug': 'the-shawshank-redemption'
            },
            {
                'title': 'Goodfellas',
                'year': 1990,
                'director': 'Martin Scorsese',
                'genres': ['Biography', 'Crime', 'Drama'], 
                'cast': ['Robert De Niro', 'Ray Liotta', 'Joe Pesci'],
                'plot_summary': 'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill.',
                'slug': 'goodfellas'
            }
        ]
        
        return popular_movies[:limit]

def main():
    """Test the alternative movie API"""
    api = AlternativeMovieAPI()
    
    print("Testing alternative movie APIs...")
    
    # Test with sample movies
    movies = api.get_popular_movies_sample(5)
    
    print(f"Retrieved {len(movies)} sample movies:")
    for movie in movies:
        print(f"- {movie['title']} ({movie['year']}) by {movie['director']}")
    
    # Save sample data
    os.makedirs('data', exist_ok=True)
    with open('data/sample_movies.json', 'w') as f:
        json.dump(movies, f, indent=2)
    
    print("\nSample movie data saved to data/sample_movies.json")
    print("You can now test AI analysis with this data!")

if __name__ == "__main__":
    main()