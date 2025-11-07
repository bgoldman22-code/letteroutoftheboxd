#!/usr/bin/env python3
"""
Letterboxd Profile Scraper
Scrapes user profiles, ratings, and movie data from Letterboxd
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urljoin, urlparse
import os
from datetime import datetime

class LetterboxdScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.base_url = 'https://letterboxd.com'
        
    def get_user_profile(self, username):
        """Get basic user profile information"""
        url = f"{self.base_url}/{username}/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            profile_data = {
                'username': username,
                'display_name': self._extract_display_name(soup),
                'bio': self._extract_bio(soup),
                'followers': self._extract_followers(soup),
                'following': self._extract_following(soup),
                'films_watched': self._extract_films_watched(soup),
                'scraped_at': datetime.now().isoformat()
            }
            
            return profile_data
        
        except requests.RequestException as e:
            print(f"Error fetching profile for {username}: {e}")
            return None
    
    def get_user_ratings(self, username, limit=None):
        """Get user's movie ratings and reviews"""
        ratings = []
        page = 1
        
        while True:
            url = f"{self.base_url}/{username}/films/by/date/page/{page}/"
            
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                film_items = soup.find_all('li', class_='poster-container')
                
                if not film_items:
                    break
                
                for item in film_items:
                    rating_data = self._extract_rating_data(item, username)
                    if rating_data:
                        ratings.append(rating_data)
                        
                        if limit and len(ratings) >= limit:
                            return ratings
                
                page += 1
                time.sleep(random.uniform(1, 3))  # Rate limiting
                
            except requests.RequestException as e:
                print(f"Error fetching ratings page {page} for {username}: {e}")
                break
        
        return ratings
    
    def get_movie_details(self, movie_slug):
        """Get detailed information about a specific movie"""
        url = f"{self.base_url}/film/{movie_slug}/"
        
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            movie_data = {
                'slug': movie_slug,
                'title': self._extract_movie_title(soup),
                'year': self._extract_movie_year(soup),
                'director': self._extract_director(soup),
                'cast': self._extract_cast(soup),
                'genres': self._extract_genres(soup),
                'runtime': self._extract_runtime(soup),
                'average_rating': self._extract_average_rating(soup),
                'total_ratings': self._extract_total_ratings(soup),
                'themes': self._extract_themes(soup),
                'mood': self._extract_mood_tags(soup),
                'visual_style': self._extract_visual_style(soup),
                'scraped_at': datetime.now().isoformat()
            }
            
            return movie_data
            
        except requests.RequestException as e:
            print(f"Error fetching movie details for {movie_slug}: {e}")
            return None
    
    def _extract_display_name(self, soup):
        name_elem = soup.find('h1', class_='title-1')
        return name_elem.text.strip() if name_elem else None
    
    def _extract_bio(self, soup):
        bio_elem = soup.find('div', class_='profile-text')
        return bio_elem.text.strip() if bio_elem else None
    
    def _extract_followers(self, soup):
        followers_elem = soup.find('a', href=lambda x: x and '/followers/' in x)
        if followers_elem:
            count_elem = followers_elem.find('span', class_='value')
            return count_elem.text.strip() if count_elem else None
        return None
    
    def _extract_following(self, soup):
        following_elem = soup.find('a', href=lambda x: x and '/following/' in x)
        if following_elem:
            count_elem = following_elem.find('span', class_='value')
            return count_elem.text.strip() if count_elem else None
        return None
    
    def _extract_films_watched(self, soup):
        films_elem = soup.find('a', href=lambda x: x and '/films/' in x)
        if films_elem:
            count_elem = films_elem.find('span', class_='value')
            return count_elem.text.strip() if count_elem else None
        return None
    
    def _extract_rating_data(self, item, username):
        """Extract rating data from a film item"""
        try:
            # Get movie slug from poster link
            poster_link = item.find('div', class_='film-poster')
            if not poster_link:
                return None
            
            # Get movie slug from data-film-slug attribute or construct from link
            movie_slug = poster_link.get('data-film-slug')
            if not movie_slug:
                link = poster_link.find('a')
                if link and link.get('href'):
                    movie_slug = link.get('href').strip('/').replace('film/', '')
            
            # Get movie title
            img = poster_link.find('img')
            movie_title = img.get('alt') if img else None
            
            # Get rating
            rating_elem = item.find('span', class_='rating')
            rating = None
            if rating_elem:
                # Count filled stars
                filled_stars = rating_elem.find_all('span', class_='rated-')
                rating = len(filled_stars) * 0.5  # Each star is 0.5
            
            # Get watch date
            date_elem = item.find('time')
            watch_date = date_elem.get('datetime') if date_elem else None
            
            # Get like status
            liked = item.find('span', class_='like') is not None
            
            # Get review if exists
            review_elem = item.find('div', class_='film-detail-content')
            review = review_elem.text.strip() if review_elem else None
            
            return {
                'username': username,
                'movie_slug': movie_slug,
                'movie_title': movie_title,
                'rating': rating,
                'liked': liked,
                'watch_date': watch_date,
                'review': review,
                'scraped_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error extracting rating data: {e}")
            return None
    
    def _extract_movie_title(self, soup):
        title_elem = soup.find('h1', class_='headline-1')
        return title_elem.text.strip() if title_elem else None
    
    def _extract_movie_year(self, soup):
        year_elem = soup.find('div', class_='releaseyear')
        if year_elem:
            year_link = year_elem.find('a')
            return year_link.text.strip() if year_link else None
        return None
    
    def _extract_director(self, soup):
        director_elem = soup.find('span', class_='director')
        if director_elem:
            director_link = director_elem.find('a')
            return director_link.text.strip() if director_link else None
        return None
    
    def _extract_cast(self, soup):
        cast_section = soup.find('div', class_='cast-list')
        cast = []
        if cast_section:
            cast_links = cast_section.find_all('a', class_='text-slug')
            cast = [link.text.strip() for link in cast_links[:10]]  # Top 10 cast members
        return cast
    
    def _extract_genres(self, soup):
        genre_links = soup.find_all('a', href=lambda x: x and '/films/genre/' in x)
        return [link.text.strip() for link in genre_links]
    
    def _extract_runtime(self, soup):
        runtime_elem = soup.find('p', class_='text-link')
        if runtime_elem and 'mins' in runtime_elem.text:
            return runtime_elem.text.strip()
        return None
    
    def _extract_average_rating(self, soup):
        rating_elem = soup.find('section', class_='film-stats')
        if rating_elem:
            avg_elem = rating_elem.find('span', class_='average-rating')
            if avg_elem:
                rating_link = avg_elem.find('a')
                return rating_link.text.strip() if rating_link else None
        return None
    
    def _extract_total_ratings(self, soup):
        rating_elem = soup.find('section', class_='film-stats')
        if rating_elem:
            count_elem = rating_elem.find('a', class_='has-icon')
            return count_elem.text.strip() if count_elem else None
        return None
    
    def _extract_themes(self, soup):
        """Extract thematic elements and tags"""
        # This would need to be enhanced with ML/NLP analysis
        # For now, we'll look for genre and tag information
        themes = []
        
        # Get genres as basic themes
        genre_links = soup.find_all('a', href=lambda x: x and '/films/genre/' in x)
        themes.extend([link.text.strip() for link in genre_links])
        
        return themes
    
    def _extract_mood_tags(self, soup):
        """Extract mood-related tags and themes"""
        # This would be enhanced with sentiment analysis
        moods = []
        
        # Look for common mood descriptors in reviews or tags
        mood_keywords = ['dark', 'light', 'comedic', 'serious', 'surreal', 'realistic', 
                        'uplifting', 'depressing', 'intense', 'calm', 'chaotic', 'peaceful']
        
        # This is a placeholder - real implementation would analyze reviews
        return moods
    
    def _extract_visual_style(self, soup):
        """Extract visual style information"""
        # This would be enhanced with computer vision analysis
        styles = []
        
        # Look for cinematography-related tags or descriptions
        style_keywords = ['black and white', 'color', 'wide shots', 'close-ups', 
                         'handheld', 'steady cam', 'animation', 'documentary style']
        
        # This is a placeholder - real implementation would analyze visual elements
        return styles
    
    def enrich_ratings_with_movie_data(self, ratings, movie_service):
        """Enrich user ratings with comprehensive movie data from APIs"""
        enriched_ratings = []
        
        for rating in ratings:
            print(f"Enriching: {rating.get('movie_title')} ({rating.get('movie_slug')})")
            
            # Get movie data from multi-API service
            movie_data = movie_service.get_movie_data(
                title=rating.get('movie_title'),
                year=None  # Could parse from Letterboxd if available
            )
            
            if movie_data:
                # Merge rating data with movie data
                enriched = {
                    **movie_data,
                    'user_rating': rating.get('rating'),
                    'user_liked': rating.get('liked'),
                    'user_watch_date': rating.get('watch_date'),
                    'user_review': rating.get('review'),
                    'letterboxd_slug': rating.get('movie_slug')
                }
                enriched_ratings.append(enriched)
                time.sleep(0.5)  # Rate limiting
            else:
                print(f"  ⚠️  Could not find movie data")
        
        return enriched_ratings

def main():
    from multi_api_movie_service import MultiAPIMovieService
    
    scraper = LetterboxdScraper()
    movie_service = MultiAPIMovieService()
    
    # Example usage
    username = input("Enter Letterboxd username: ").strip()
    
    if not username:
        print("No username provided")
        return
    
    print(f"\n🎬 Scraping Letterboxd profile for: {username}")
    print("=" * 50)
    
    # Get profile data
    print("\n1️⃣ Fetching profile data...")
    profile = scraper.get_user_profile(username)
    if profile:
        print(f"   ✅ Found: {profile.get('display_name')}")
        print(f"   Films watched: {profile.get('films_watched')}")
    
    # Get ratings (limit to 50 for testing)
    print(f"\n2️⃣ Scraping movie ratings...")
    ratings = scraper.get_user_ratings(username, limit=50)
    print(f"   ✅ Found {len(ratings)} ratings")
    
    # Filter for highly rated movies (4+ stars)
    loved_movies = [r for r in ratings if r.get('rating') and r.get('rating') >= 4.0]
    print(f"   ❤️  {len(loved_movies)} movies rated 4+ stars")
    
    # Enrich with movie data
    print(f"\n3️⃣ Enriching with movie data from APIs...")
    enriched_ratings = scraper.enrich_ratings_with_movie_data(loved_movies[:10], movie_service)
    print(f"   ✅ Enriched {len(enriched_ratings)} movies")
    
    # Save data
    print(f"\n4️⃣ Saving data...")
    os.makedirs('data', exist_ok=True)
    
    output_data = {
        'profile': profile,
        'total_ratings': len(ratings),
        'loved_movies_count': len(loved_movies),
        'enriched_movies': enriched_ratings,
        'scraped_at': datetime.now().isoformat()
    }
    
    filename = f'data/{username}_complete_profile.json'
    with open(filename, 'w') as f:
        json.dump(output_data, f, indent=2)
    
    print(f"   ✅ Data saved to {filename}")
    print(f"\n🚀 Ready for AI analysis and recommendations!")

if __name__ == "__main__":
    main()