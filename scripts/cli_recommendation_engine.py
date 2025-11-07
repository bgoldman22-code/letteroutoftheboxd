#!/usr/bin/env python3
"""
CLI Wrapper for Recommendation Engine
Allows API to call the engine via command line
"""

import sys
import json
import os
from pathlib import Path

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent))

from recommendation_engine import RecommendationEngine
from letterboxd_scraper import LetterboxdScraper
from dotenv import load_dotenv

load_dotenv('.env.local')


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Input file path required"}))
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        # Load input data
        with open(input_file, 'r') as f:
            input_data = json.load(f)
        
        username = input_data.get('username')
        loved_movies = input_data.get('loved_movies', [])
        all_rated_movies = input_data.get('all_rated_movies')
        num_recommendations = input_data.get('num_recommendations', 20)
        diversity_factor = input_data.get('diversity_factor', 0.3)
        
        # If username provided, scrape their profile
        if username and not loved_movies:
            print(f"Fetching profile for {username}...", file=sys.stderr)
            scraper = LetterboxdScraper()
            
            profile = scraper.get_user_profile(username)
            if not profile:
                print(json.dumps({"error": f"Could not fetch profile for {username}"}))
                sys.exit(1)
            
            ratings = scraper.get_user_ratings(username, limit=500)
            
            # Get loved movies (4+ stars)
            loved_movies = [r for r in ratings if r.get('rating', 0) >= 4]
            all_rated_movies = ratings
            
            # Enrich with movie data
            loved_movies = scraper.enrich_ratings_with_movie_data(loved_movies[:50])
        
        if not loved_movies:
            print(json.dumps({"error": "No loved movies provided or found"}))
            sys.exit(1)
        
        # Generate recommendations
        print(f"Generating {num_recommendations} recommendations...", file=sys.stderr)
        engine = RecommendationEngine()
        
        recommendations = engine.generate_recommendations(
            user_loved_movies=loved_movies,
            user_rated_movies=all_rated_movies,
            num_recommendations=num_recommendations,
            diversity_factor=diversity_factor
        )
        
        # Output JSON result
        print(json.dumps(recommendations, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
