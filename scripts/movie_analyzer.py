#!/usr/bin/env python3
"""
Movie Analysis Engine
Analyzes movie data for themes, moods, visual styles, and relationships
"""

import json
import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import nltk
from textblob import TextBlob
from collections import Counter, defaultdict
import re

class MovieAnalyzer:
    def __init__(self):
        self.movies_data = {}
        self.user_ratings = {}
        self.similarity_matrix = None
        self.movie_features = {}
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def load_data(self, data_dir='data'):
        """Load scraped movie and user data"""
        for filename in os.listdir(data_dir):
            if filename.endswith('_ratings.json'):
                username = filename.replace('_ratings.json', '')
                with open(os.path.join(data_dir, filename), 'r') as f:
                    self.user_ratings[username] = json.load(f)
            
            elif filename.endswith('_movies.json'):
                with open(os.path.join(data_dir, filename), 'r') as f:
                    movies = json.load(f)
                    for movie in movies:
                        self.movies_data[movie['slug']] = movie
    
    def analyze_themes(self, movie_data):
        """Analyze thematic elements of movies"""
        themes = {
            'existential': ['meaning', 'purpose', 'existence', 'death', 'life', 'philosophy'],
            'coming_of_age': ['growing up', 'adolescence', 'teenager', 'youth', 'childhood'],
            'love_romance': ['love', 'romance', 'relationship', 'marriage', 'dating'],
            'family': ['family', 'parent', 'child', 'sibling', 'home', 'tradition'],
            'war_conflict': ['war', 'battle', 'conflict', 'military', 'soldier', 'violence'],
            'social_justice': ['justice', 'inequality', 'racism', 'discrimination', 'rights'],
            'technology': ['technology', 'ai', 'robot', 'future', 'cyber', 'digital'],
            'crime': ['crime', 'murder', 'theft', 'police', 'detective', 'criminal'],
            'supernatural': ['ghost', 'magic', 'supernatural', 'fantasy', 'mystical'],
            'survival': ['survival', 'disaster', 'apocalypse', 'rescue', 'escape']
        }
        
        movie_themes = {}
        
        for slug, movie in movie_data.items():
            detected_themes = []
            
            # Analyze plot, genres, and tags
            text_content = ' '.join([
                movie.get('genres', []),
                movie.get('themes', []),
                movie.get('plot_summary', ''),
                ' '.join(movie.get('reviews', []))
            ]).lower()
            
            for theme, keywords in themes.items():
                score = sum(text_content.count(keyword) for keyword in keywords)
                if score > 0:
                    detected_themes.append({'theme': theme, 'score': score})
            
            movie_themes[slug] = sorted(detected_themes, key=lambda x: x['score'], reverse=True)
        
        return movie_themes
    
    def analyze_moods(self, movie_data):
        """Analyze emotional mood and tone of movies"""
        mood_categories = {
            'dark': ['dark', 'grim', 'bleak', 'somber', 'melancholy', 'noir'],
            'uplifting': ['uplifting', 'inspiring', 'hopeful', 'positive', 'cheerful'],
            'intense': ['intense', 'gripping', 'suspenseful', 'thrilling', 'tense'],
            'contemplative': ['thoughtful', 'reflective', 'meditative', 'introspective'],
            'surreal': ['surreal', 'bizarre', 'strange', 'weird', 'abstract'],
            'realistic': ['realistic', 'gritty', 'authentic', 'raw', 'naturalistic'],
            'comedic': ['funny', 'humorous', 'comedy', 'witty', 'satirical'],
            'romantic': ['romantic', 'tender', 'passionate', 'intimate', 'sweet']
        }
        
        movie_moods = {}
        
        for slug, movie in movie_data.items():
            # Analyze reviews and descriptions for mood indicators
            reviews_text = ' '.join(movie.get('reviews', [])).lower()
            
            mood_scores = {}
            for mood, keywords in mood_categories.items():
                score = sum(reviews_text.count(keyword) for keyword in keywords)
                if score > 0:
                    mood_scores[mood] = score
            
            # Use TextBlob for sentiment analysis
            if reviews_text:
                blob = TextBlob(reviews_text)
                sentiment = blob.sentiment
                
                # Map sentiment to mood categories
                if sentiment.polarity > 0.3:
                    mood_scores['uplifting'] = mood_scores.get('uplifting', 0) + 2
                elif sentiment.polarity < -0.3:
                    mood_scores['dark'] = mood_scores.get('dark', 0) + 2
                
                if sentiment.subjectivity > 0.7:
                    mood_scores['contemplative'] = mood_scores.get('contemplative', 0) + 1
            
            movie_moods[slug] = mood_scores
        
        return movie_moods
    
    def analyze_visual_style(self, movie_data):
        """Analyze visual and cinematographic style"""
        visual_elements = {
            'cinematography': {
                'handheld': ['handheld', 'shaky cam', 'documentary style'],
                'static': ['static shots', 'composed', 'formal framing'],
                'dynamic': ['dynamic camera', 'movement', 'kinetic'],
                'intimate': ['close-ups', 'intimate framing', 'character study'],
                'expansive': ['wide shots', 'landscape', 'epic scope', 'vast']
            },
            'color_palette': {
                'monochrome': ['black and white', 'monochrome', 'noir'],
                'vibrant': ['colorful', 'vibrant', 'saturated'],
                'muted': ['muted colors', 'desaturated', 'pale'],
                'warm': ['warm tones', 'golden', 'amber'],
                'cool': ['cool tones', 'blue', 'cyan', 'cold']
            },
            'lighting': {
                'natural': ['natural lighting', 'daylight', 'sun'],
                'dramatic': ['dramatic lighting', 'chiaroscuro', 'contrasted'],
                'soft': ['soft lighting', 'diffused', 'gentle'],
                'harsh': ['harsh lighting', 'stark', 'fluorescent']
            }
        }
        
        movie_styles = {}
        
        for slug, movie in movie_data.items():
            style_analysis = {}
            
            # Analyze reviews and descriptions for visual style mentions
            text_content = ' '.join([
                movie.get('plot_summary', ''),
                ' '.join(movie.get('reviews', []))
            ]).lower()
            
            for category, elements in visual_elements.items():
                category_scores = {}
                for element, keywords in elements.items():
                    score = sum(text_content.count(keyword) for keyword in keywords)
                    if score > 0:
                        category_scores[element] = score
                
                if category_scores:
                    style_analysis[category] = category_scores
            
            movie_styles[slug] = style_analysis
        
        return movie_styles
    
    def calculate_movie_similarity(self, movies_data):
        """Calculate similarity between movies based on multiple factors"""
        movie_slugs = list(movies_data.keys())
        
        if len(movie_slugs) < 2:
            return {}
        
        # Create feature vectors for each movie
        features = []
        for slug in movie_slugs:
            movie = movies_data[slug]
            
            # Combine various features into a single text representation
            feature_text = ' '.join([
                ' '.join(movie.get('genres', [])),
                ' '.join(movie.get('themes', [])),
                movie.get('director', ''),
                ' '.join(movie.get('cast', [])[:5]),  # Top 5 cast members
                str(movie.get('year', '')),
                movie.get('runtime', ''),
            ])
            
            features.append(feature_text)
        
        # Calculate TF-IDF similarity
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        tfidf_matrix = vectorizer.fit_transform(features)
        
        # Calculate cosine similarity
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Create similarity dictionary
        similarities = {}
        for i, slug1 in enumerate(movie_slugs):
            similarities[slug1] = {}
            for j, slug2 in enumerate(movie_slugs):
                if i != j:
                    similarities[slug1][slug2] = float(similarity_matrix[i][j])
        
        return similarities
    
    def find_user_preferences(self, username):
        """Analyze user's preferences based on their ratings"""
        if username not in self.user_ratings:
            return None
        
        user_data = self.user_ratings[username]
        
        # Separate high and low rated movies
        high_rated = [r for r in user_data if r.get('rating', 0) >= 4.0]
        low_rated = [r for r in user_data if r.get('rating', 0) <= 2.0]
        
        preferences = {
            'favorite_genres': self._analyze_genre_preferences(high_rated),
            'favorite_directors': self._analyze_director_preferences(high_rated),
            'favorite_actors': self._analyze_actor_preferences(high_rated),
            'preferred_themes': self._analyze_theme_preferences(high_rated),
            'preferred_moods': self._analyze_mood_preferences(high_rated),
            'disliked_elements': {
                'genres': self._analyze_genre_preferences(low_rated),
                'themes': self._analyze_theme_preferences(low_rated)
            },
            'rating_patterns': self._analyze_rating_patterns(user_data)
        }
        
        return preferences
    
    def _analyze_genre_preferences(self, rated_movies):
        """Analyze genre preferences from rated movies"""
        genres = []
        for movie_rating in rated_movies:
            slug = movie_rating.get('movie_slug')
            if slug in self.movies_data:
                movie_genres = self.movies_data[slug].get('genres', [])
                genres.extend(movie_genres)
        
        return Counter(genres).most_common(10)
    
    def _analyze_director_preferences(self, rated_movies):
        """Analyze director preferences"""
        directors = []
        for movie_rating in rated_movies:
            slug = movie_rating.get('movie_slug')
            if slug in self.movies_data:
                director = self.movies_data[slug].get('director')
                if director:
                    directors.append(director)
        
        return Counter(directors).most_common(10)
    
    def _analyze_actor_preferences(self, rated_movies):
        """Analyze actor preferences"""
        actors = []
        for movie_rating in rated_movies:
            slug = movie_rating.get('movie_slug')
            if slug in self.movies_data:
                cast = self.movies_data[slug].get('cast', [])
                actors.extend(cast[:3])  # Top 3 actors per movie
        
        return Counter(actors).most_common(15)
    
    def _analyze_theme_preferences(self, rated_movies):
        """Analyze thematic preferences"""
        # This would use the theme analysis results
        themes = []
        for movie_rating in rated_movies:
            slug = movie_rating.get('movie_slug')
            if slug in self.movies_data:
                movie_themes = self.movies_data[slug].get('themes', [])
                themes.extend(movie_themes)
        
        return Counter(themes).most_common(10)
    
    def _analyze_mood_preferences(self, rated_movies):
        """Analyze mood preferences"""
        # This would use the mood analysis results
        moods = []
        # Implementation would depend on mood analysis data structure
        return Counter(moods).most_common(10)
    
    def _analyze_rating_patterns(self, user_ratings):
        """Analyze user's rating patterns"""
        ratings = [r.get('rating', 0) for r in user_ratings if r.get('rating')]
        
        if not ratings:
            return {}
        
        return {
            'average_rating': np.mean(ratings),
            'rating_std': np.std(ratings),
            'total_ratings': len(ratings),
            'rating_distribution': dict(Counter([str(r) for r in ratings])),
            'generous_rater': np.mean(ratings) > 3.5,  # Above average ratings
            'critical_rater': np.mean(ratings) < 2.5   # Below average ratings
        }
    
    def generate_recommendations(self, username, num_recommendations=20):
        """Generate movie recommendations based on user preferences"""
        user_prefs = self.find_user_preferences(username)
        if not user_prefs:
            return []
        
        # Get movies the user hasn't seen
        user_watched = {r['movie_slug'] for r in self.user_ratings.get(username, [])}
        unwatched_movies = {slug: movie for slug, movie in self.movies_data.items() 
                           if slug not in user_watched}
        
        # Score unwatched movies based on preferences
        scored_movies = []
        
        for slug, movie in unwatched_movies.items():
            score = self._calculate_recommendation_score(movie, user_prefs)
            scored_movies.append({
                'slug': slug,
                'movie': movie,
                'score': score,
                'reasons': self._get_recommendation_reasons(movie, user_prefs)
            })
        
        # Sort by score and return top recommendations
        scored_movies.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_movies[:num_recommendations]
    
    def _calculate_recommendation_score(self, movie, user_prefs):
        """Calculate recommendation score for a movie"""
        score = 0.0
        
        # Genre matching
        movie_genres = set(movie.get('genres', []))
        preferred_genres = {genre for genre, count in user_prefs['favorite_genres']}
        genre_overlap = len(movie_genres.intersection(preferred_genres))
        score += genre_overlap * 2.0
        
        # Director matching
        if movie.get('director') in [d for d, c in user_prefs['favorite_directors']]:
            score += 3.0
        
        # Actor matching
        movie_cast = set(movie.get('cast', []))
        preferred_actors = {actor for actor, count in user_prefs['favorite_actors']}
        actor_overlap = len(movie_cast.intersection(preferred_actors))
        score += actor_overlap * 1.5
        
        # Theme matching (if available)
        movie_themes = set(movie.get('themes', []))
        preferred_themes = {theme for theme, count in user_prefs['preferred_themes']}
        theme_overlap = len(movie_themes.intersection(preferred_themes))
        score += theme_overlap * 1.0
        
        # Avoid disliked elements
        disliked_genres = {genre for genre, count in user_prefs['disliked_elements']['genres']}
        if movie_genres.intersection(disliked_genres):
            score -= 2.0
        
        return max(0.0, score)  # Ensure non-negative score
    
    def _get_recommendation_reasons(self, movie, user_prefs):
        """Get reasons why a movie is recommended"""
        reasons = []
        
        # Genre matches
        movie_genres = set(movie.get('genres', []))
        preferred_genres = {genre for genre, count in user_prefs['favorite_genres']}
        genre_matches = movie_genres.intersection(preferred_genres)
        if genre_matches:
            reasons.append(f"Genres you like: {', '.join(list(genre_matches)[:3])}")
        
        # Director match
        if movie.get('director') in [d for d, c in user_prefs['favorite_directors']]:
            reasons.append(f"Directed by {movie.get('director')} (a director you enjoy)")
        
        # Actor matches
        movie_cast = set(movie.get('cast', []))
        preferred_actors = {actor for actor, count in user_prefs['favorite_actors']}
        actor_matches = movie_cast.intersection(preferred_actors)
        if actor_matches:
            reasons.append(f"Stars {', '.join(list(actor_matches)[:2])} (actors you like)")
        
        return reasons

def main():
    analyzer = MovieAnalyzer()
    
    print("Loading data...")
    analyzer.load_data()
    
    if not analyzer.movies_data:
        print("No movie data found. Run the scraper first.")
        return
    
    print("Analyzing themes...")
    themes = analyzer.analyze_themes(analyzer.movies_data)
    
    print("Analyzing moods...")
    moods = analyzer.analyze_moods(analyzer.movies_data)
    
    print("Analyzing visual styles...")
    styles = analyzer.analyze_visual_style(analyzer.movies_data)
    
    print("Calculating movie similarities...")
    similarities = analyzer.calculate_movie_similarity(analyzer.movies_data)
    
    # Save analysis results
    os.makedirs('analysis', exist_ok=True)
    
    with open('analysis/themes.json', 'w') as f:
        json.dump(themes, f, indent=2)
    
    with open('analysis/moods.json', 'w') as f:
        json.dump(moods, f, indent=2)
    
    with open('analysis/styles.json', 'w') as f:
        json.dump(styles, f, indent=2)
    
    with open('analysis/similarities.json', 'w') as f:
        json.dump(similarities, f, indent=2)
    
    print("Analysis complete! Results saved to analysis/ directory")
    
    # Generate recommendations if user data exists
    if analyzer.user_ratings:
        username = list(analyzer.user_ratings.keys())[0]
        print(f"Generating recommendations for {username}...")
        
        recommendations = analyzer.generate_recommendations(username)
        
        with open(f'analysis/{username}_recommendations.json', 'w') as f:
            json.dump(recommendations, f, indent=2)
        
        print(f"Recommendations saved to analysis/{username}_recommendations.json")

if __name__ == "__main__":
    main()