#!/usr/bin/env python3
"""
Elite Recommendation Engine
Generates sophisticated movie recommendations based on user preferences and AI analysis
"""

import json
import os
from typing import Dict, List, Any, Tuple
from datetime import datetime
from collections import defaultdict
import numpy as np
from dotenv import load_dotenv

from ai_movie_analyzer import AIMovieAnalyzer
from multi_api_movie_service import MultiAPIMovieService

load_dotenv('.env.local')


class RecommendationEngine:
    """Advanced recommendation system using AI embeddings and preference analysis"""
    
    def __init__(self):
        self.analyzer = AIMovieAnalyzer()
        self.movie_service = MultiAPIMovieService()
    
    def generate_recommendations(
        self, 
        user_loved_movies: List[Dict[str, Any]], 
        user_rated_movies: List[Dict[str, Any]] = None,
        num_recommendations: int = 20,
        diversity_factor: float = 0.3
    ) -> Dict[str, Any]:
        """
        Generate personalized recommendations based on user's loved movies
        
        Args:
            user_loved_movies: List of movies the user rated highly (4+ stars)
            user_rated_movies: ALL movies the user has seen/rated (to exclude from recommendations)
            num_recommendations: Number of recommendations to generate
            diversity_factor: 0-1, higher means more diverse recommendations
        
        Returns:
            Dictionary with recommendations, insights, and metadata
        """
        print(f"\n🎯 Generating {num_recommendations} elite recommendations...")
        print(f"   Based on {len(user_loved_movies)} loved movies")
        
        # Create exclusion set of already-seen movies
        if user_rated_movies is None:
            user_rated_movies = user_loved_movies
        
        excluded_slugs = {self._create_slug(m.get('title', '')) for m in user_rated_movies}
        print(f"   Excluding {len(excluded_slugs)} already-seen movies")
        
        # Step 1: Analyze user's taste profile
        taste_profile = self._analyze_taste_profile(user_loved_movies)
        print(f"\n📊 Taste Profile:")
        print(f"   Top genres: {taste_profile['top_genres'][:3]}")
        print(f"   Top themes: {taste_profile['top_themes'][:3]}")
        print(f"   Favorite directors: {taste_profile['top_directors'][:3]}")
        
        # Step 2: Ensure all loved movies are in vector DB
        self._ensure_movies_analyzed(user_loved_movies)
        
        # Step 3: Find similar movies for each loved movie
        all_candidates = []
        
        for movie in user_loved_movies:
            movie_slug = self._create_slug(movie.get('title', ''))
            similar = self.analyzer.find_similar_movies(movie_slug, limit=10)
            
            for candidate in similar:
                # Skip if user has already seen/rated this movie
                candidate_slug = self._create_slug(candidate.get('title', ''))
                if candidate_slug in excluded_slugs:
                    continue
                
                # Add context about which loved movie it's similar to
                candidate['similar_to'] = movie.get('title')
                candidate['base_similarity'] = candidate.get('similarity_score', 0)
                all_candidates.append(candidate)
        
        # Step 4: Score and rank candidates
        scored_recommendations = self._score_candidates(
            all_candidates, 
            taste_profile, 
            user_loved_movies,
            diversity_factor
        )
        
        # Step 5: Deduplicate and select top recommendations
        final_recommendations = self._select_top_recommendations(
            scored_recommendations,
            num_recommendations
        )
        
        # Step 6: Create recommendation map data
        recommendation_map = self._create_recommendation_map(
            user_loved_movies,
            final_recommendations
        )
        
        return {
            'recommendations': final_recommendations,
            'taste_profile': taste_profile,
            'recommendation_map': recommendation_map,
            'insights': self._generate_insights(taste_profile, final_recommendations),
            'generated_at': datetime.now().isoformat()
        }
    
    def _analyze_taste_profile(self, loved_movies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze user's taste from their loved movies"""
        
        # Count occurrences
        genres = defaultdict(int)
        themes = defaultdict(int)
        directors = defaultdict(int)
        actors = defaultdict(int)
        decades = defaultdict(int)
        moods = defaultdict(int)
        
        for movie in loved_movies:
            # Genres
            for genre in movie.get('genres', []):
                genres[genre] += 1
            
            # Themes (if available from AI analysis)
            for theme in movie.get('themes', []):
                themes[theme] += 1
            
            # Directors
            director = movie.get('director', '')
            if director and director != 'N/A':
                directors[director] += 1
            
            # Cast
            for actor in movie.get('cast', [])[:3]:  # Top 3 actors
                actors[actor] += 1
            
            # Decade
            year = movie.get('year', 0)
            if year:
                decade = (year // 10) * 10
                decades[f"{decade}s"] += 1
            
            # Mood
            mood = movie.get('mood', '')
            if mood:
                moods[mood] += 1
        
        # Sort by frequency
        top_genres = sorted(genres.items(), key=lambda x: x[1], reverse=True)
        top_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)
        top_directors = sorted(directors.items(), key=lambda x: x[1], reverse=True)
        top_actors = sorted(actors.items(), key=lambda x: x[1], reverse=True)
        top_decades = sorted(decades.items(), key=lambda x: x[1], reverse=True)
        top_moods = sorted(moods.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'top_genres': [g[0] for g in top_genres[:5]],
            'top_themes': [t[0] for t in top_themes[:5]],
            'top_directors': [d[0] for d in top_directors[:5]],
            'top_actors': [a[0] for a in top_actors[:5]],
            'top_decades': [d[0] for d in top_decades[:3]],
            'top_moods': [m[0] for m in top_moods[:3]],
            'genre_distribution': dict(genres),
            'total_movies': len(loved_movies),
            'average_year': sum(m.get('year', 0) for m in loved_movies) / len(loved_movies) if loved_movies else 0
        }
    
    def _ensure_movies_analyzed(self, movies: List[Dict[str, Any]]):
        """Ensure all movies are analyzed and stored in vector DB"""
        print(f"\n🔍 Checking vector database...")
        
        for movie in movies:
            movie_slug = self._create_slug(movie.get('title', ''))
            
            # Check if exists
            existing = self.analyzer.movies_collection.get(ids=[movie_slug])
            if not existing or len(existing.get('ids', [])) == 0:
                print(f"   📝 Analyzing: {movie.get('title')}")
                self.analyzer.analyze_and_store_movie(movie)
            else:
                print(f"   ✅ Already analyzed: {movie.get('title')}")
    
    def _score_candidates(
        self, 
        candidates: List[Dict[str, Any]], 
        taste_profile: Dict[str, Any],
        loved_movies: List[Dict[str, Any]],
        diversity_factor: float
    ) -> List[Dict[str, Any]]:
        """Score candidates based on multiple factors"""
        
        loved_titles = {self._create_slug(m.get('title', '')) for m in loved_movies}
        
        for candidate in candidates:
            # Base similarity score (already calculated)
            similarity = candidate.get('base_similarity', 0)
            
            # Genre match bonus
            candidate_genres = set(candidate.get('genres', []))
            profile_genres = set(taste_profile['top_genres'])
            genre_match = len(candidate_genres & profile_genres) / max(len(candidate_genres), 1)
            
            # Director match bonus
            director_bonus = 1.2 if candidate.get('director') in taste_profile['top_directors'] else 1.0
            
            # Theme match bonus (if available)
            candidate_themes = set(candidate.get('themes', []))
            profile_themes = set(taste_profile['top_themes'])
            theme_match = len(candidate_themes & profile_themes) / max(len(candidate_themes), 1) if candidate_themes else 0
            
            # Recency penalty (slightly favor newer movies for diversity)
            year = candidate.get('year', 2000)
            recency_factor = min(year / 2020, 1.0)
            
            # Calculate final score
            base_score = similarity * 0.5  # 50% weight
            genre_score = genre_match * 0.2  # 20% weight
            theme_score = theme_match * 0.15  # 15% weight
            director_score = (director_bonus - 1.0) * 0.15  # 15% weight
            
            # Apply diversity factor (reduces similarity weight)
            final_score = (
                base_score * (1 - diversity_factor * 0.3) +
                genre_score +
                theme_score +
                director_score +
                recency_factor * diversity_factor * 0.1
            )
            
            candidate['recommendation_score'] = final_score
            candidate['score_breakdown'] = {
                'similarity': similarity,
                'genre_match': genre_match,
                'theme_match': theme_match,
                'director_match': director_bonus > 1.0
            }
        
        return sorted(candidates, key=lambda x: x.get('recommendation_score', 0), reverse=True)
    
    def _select_top_recommendations(
        self, 
        scored_candidates: List[Dict[str, Any]], 
        num_recommendations: int
    ) -> List[Dict[str, Any]]:
        """Select top recommendations, avoiding duplicates"""
        
        seen_titles = set()
        recommendations = []
        
        for candidate in scored_candidates:
            title_slug = self._create_slug(candidate.get('title', ''))
            
            # Skip if already seen or is a loved movie
            if title_slug not in seen_titles and candidate.get('type') != 'loved':
                recommendations.append(candidate)
                seen_titles.add(title_slug)
                
                if len(recommendations) >= num_recommendations:
                    break
        
        return recommendations
    
    def _create_recommendation_map(
        self, 
        loved_movies: List[Dict[str, Any]], 
        recommendations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create data structure for visualization map"""
        
        # Create nodes
        nodes = []
        
        # Add loved movies as central nodes
        for movie in loved_movies:
            nodes.append({
                'id': self._create_slug(movie.get('title', '')),
                'title': movie.get('title'),
                'year': movie.get('year'),
                'type': 'loved',
                'rating': movie.get('user_rating', 5.0),
                'genres': movie.get('genres', []),
                'director': movie.get('director', '')
            })
        
        # Add recommendations as peripheral nodes
        for rec in recommendations:
            nodes.append({
                'id': self._create_slug(rec.get('title', '')),
                'title': rec.get('title'),
                'year': rec.get('year'),
                'type': 'recommendation',
                'score': rec.get('recommendation_score', 0),
                'genres': rec.get('genres', []),
                'director': rec.get('director', ''),
                'similar_to': rec.get('similar_to', '')
            })
        
        # Create edges (connections)
        edges = []
        for rec in recommendations:
            # Find the loved movie it's most similar to
            similar_to = rec.get('similar_to', '')
            if similar_to:
                edges.append({
                    'source': self._create_slug(similar_to),
                    'target': self._create_slug(rec.get('title', '')),
                    'weight': rec.get('base_similarity', 0),
                    'type': 'similarity'
                })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'total_nodes': len(nodes),
            'total_edges': len(edges)
        }
    
    def _generate_insights(
        self, 
        taste_profile: Dict[str, Any], 
        recommendations: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate human-readable insights about recommendations"""
        
        insights = []
        
        # Genre insights
        if taste_profile['top_genres']:
            top_genre = taste_profile['top_genres'][0]
            insights.append(f"Your taste strongly favors {top_genre} films")
        
        # Director insights
        if taste_profile['top_directors']:
            top_director = taste_profile['top_directors'][0]
            insights.append(f"You're a fan of {top_director}'s work")
        
        # Era insights
        avg_year = taste_profile.get('average_year', 2000)
        if avg_year < 1990:
            insights.append("You appreciate classic cinema")
        elif avg_year > 2010:
            insights.append("You enjoy contemporary films")
        else:
            insights.append("You have an eclectic taste spanning different eras")
        
        # Recommendation insights
        if recommendations:
            high_score_count = sum(1 for r in recommendations if r.get('recommendation_score', 0) > 0.7)
            if high_score_count > 5:
                insights.append(f"Found {high_score_count} highly matched recommendations for you")
        
        return insights
    
    def _create_slug(self, title: str) -> str:
        """Create URL-friendly slug from title"""
        import re
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug.strip('-')


def main():
    """Test the recommendation engine"""
    engine = RecommendationEngine()
    
    # Load sample user data (would come from Letterboxd scraper)
    try:
        with open('data/multi_api_movies.json', 'r') as f:
            sample_movies = json.load(f)
        
        # Simulate user ratings (4-5 stars for loved movies)
        for i, movie in enumerate(sample_movies):
            movie['user_rating'] = 5.0 if i < 3 else 4.5
        
        print("🎬 Testing Elite Recommendation Engine")
        print("=" * 60)
        
        # Generate recommendations
        results = engine.generate_recommendations(
            user_loved_movies=sample_movies,
            num_recommendations=10,
            diversity_factor=0.3
        )
        
        # Display results
        print(f"\n✨ TOP {len(results['recommendations'])} RECOMMENDATIONS:")
        print("-" * 60)
        
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"\n{i}. {rec.get('title')} ({rec.get('year')})")
            print(f"   Score: {rec.get('recommendation_score', 0):.1%}")
            print(f"   Similar to: {rec.get('similar_to')}")
            print(f"   Genres: {', '.join(rec.get('genres', [])[:3])}")
            if rec.get('score_breakdown'):
                breakdown = rec['score_breakdown']
                print(f"   Match: Similarity {breakdown['similarity']:.1%}, "
                      f"Genre {breakdown['genre_match']:.1%}")
        
        print(f"\n💡 INSIGHTS:")
        for insight in results['insights']:
            print(f"   • {insight}")
        
        # Save results
        output_file = 'data/recommendations_output.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Full results saved to {output_file}")
        print(f"🎯 Recommendation map data ready for visualization!")
        
    except FileNotFoundError:
        print("❌ Sample data not found. Please run multi_api_movie_service.py first")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
