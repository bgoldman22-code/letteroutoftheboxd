#!/usr/bin/env python3
"""
AI Movie Analyzer
Uses OpenAI GPT-4o for deep movie analysis and ChromaDB for embeddings
"""

import os
from openai import OpenAI
import chromadb
from chromadb.config import Settings
import json
from pathlib import Path
from elite_ai_prompts import generate_elite_analysis_prompt
from dotenv import load_dotenv
from datetime import datetime
import logging
from typing import List, Dict, Any

# Load environment variables
load_dotenv('.env.local')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIMovieAnalyzer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Initialize ChromaDB (free local vector storage)
        chroma_path = os.getenv('CHROMA_DB_PATH', './data/chroma_db')
        os.makedirs(chroma_path, exist_ok=True)
        
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        
        # Create collections
        self.movies_collection = self.chroma_client.get_or_create_collection(
            name="movies",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.users_collection = self.chroma_client.get_or_create_collection(
            name="users", 
            metadata={"hnsw:space": "cosine"}
        )
    
    def analyze_movie_with_ai(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use OpenAI GPT-4o with ELITE 58-DIMENSION TASTE MODEL"""
        
        # Generate the elite analysis prompt with 58 dimensions
        prompt = generate_elite_analysis_prompt(movie_data)
        
        print(f"\n🎬 Analyzing {movie_data.get('title')} with elite 58-dimension taste model...")
        
        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-4o'),
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an elite film phenomenologist who analyzes cinema at the deepest perceptual, aesthetic, and psychological level. You understand visual language, editing rhythm, sound design, philosophical depth, and emotional resonance. You score films on 62 precise dimensions that capture WHY people connect with certain films beyond genre and plot."
                    },
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=int(os.getenv('OPENAI_MAX_TOKENS', 4000)),
                temperature=0.3  # Lower temperature for consistent dimensional scoring
            )
            
            # Parse the JSON response
            analysis_text = response.choices[0].message.content
            
            # Try to extract JSON from the response
            try:
                analysis = json.loads(analysis_text)
                
                # Validate that we got dimensional scores
                if 'dimensional_scores' not in analysis:
                    logger.warning(f"No dimensional scores returned for {movie_data.get('title')}")
                    return self._get_default_analysis()
                
                num_dimensions = len(analysis.get('dimensional_scores', {}))
                print(f"✅ Elite analysis complete: {num_dimensions} dimensions scored")
                
                # Also generate legacy analysis for backwards compatibility
                analysis['legacy_analysis'] = self._convert_to_legacy_format(analysis)
                
                return analysis
                
            except (json.JSONDecodeError, ValueError) as e:
                # Fallback: create structured analysis
                logger.warning(f"Could not parse JSON from AI response: {e}")
                return self._get_default_analysis()
            
        except Exception as e:
            logger.error(f"Error analyzing movie with AI: {e}")
            return self._get_default_analysis()
    
    def _convert_to_legacy_format(self, elite_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Convert elite dimensional analysis to legacy format for backwards compatibility"""
        return {
            "visual_style": [elite_analysis.get('aesthetic_signature', 'cinematic')],
            "themes": elite_analysis.get('human_condition_themes', []),
            "mood": elite_analysis.get('core_essence', 'contemplative')[:50],
            "pacing": "measured",
            "influences": [],
            "innovation": elite_analysis.get('aesthetic_signature', 'unique'),
            "emotional_tone": elite_analysis.get('viewer_resonance', 'engaging')[:50],
            "viewer_experience": elite_analysis.get('viewer_resonance', 'engaging'),
            "curatorial_notes": elite_analysis.get('core_essence', '')
        }
    
    def _parse_analysis_fallback(self, text: str) -> Dict[str, Any]:
        """Fallback parser if JSON extraction fails"""
        return {
            "visual_style": ["cinematic", "atmospheric"],
            "themes": ["human experience"],
            "mood": "contemplative", 
            "pacing": "measured",
            "influences": [],
            "innovation": "unique storytelling",
            "emotional_tone": "reflective",
            "viewer_experience": "engaging",
            "curatorial_notes": text[:200] + "..." if len(text) > 200 else text
        }
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Default analysis if AI fails"""
        return {
            "visual_style": ["standard"],
            "themes": ["general"],
            "mood": "neutral",
            "pacing": "standard", 
            "influences": [],
            "innovation": "traditional approach",
            "emotional_tone": "balanced",
            "viewer_experience": "mainstream",
            "curatorial_notes": "Analysis unavailable"
        }
    
    def create_movie_embedding(self, movie_data: Dict[str, Any], ai_analysis: Dict[str, Any]) -> List[float]:
        """Create embedding for a movie using OpenAI embeddings"""
        
        # Combine movie data and AI analysis into rich text representation
        embedding_text = f"""
        Title: {movie_data.get('title', '')}
        Director: {movie_data.get('director', '')}
        Year: {movie_data.get('year', '')}
        Genres: {' '.join(movie_data.get('genres', []))}
        Plot: {movie_data.get('plot_summary', '')}
        
        Visual Style: {' '.join(ai_analysis.get('visual_style', []))}
        Themes: {' '.join(ai_analysis.get('themes', []))}
        Mood: {ai_analysis.get('mood', '')}
        Pacing: {ai_analysis.get('pacing', '')}
        Emotional Tone: {ai_analysis.get('emotional_tone', '')}
        Influences: {' '.join(ai_analysis.get('influences', []))}
        Innovation: {ai_analysis.get('innovation', '')}
        Curatorial Notes: {ai_analysis.get('curatorial_notes', '')}
        """
        
        try:
            response = self.openai_client.embeddings.create(
                model=os.getenv('OPENAI_EMBEDDING_MODEL', 'text-embedding-3-large'),
                input=embedding_text.strip()
            )
            
            return response.data[0].embedding
            
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            # Return a default embedding vector
            return [0.0] * 3072  # text-embedding-3-large dimension
    
    def store_movie_in_vectordb(self, movie_data: Dict[str, Any], ai_analysis: Dict[str, Any], embedding: List[float]):
        """Store movie in ChromaDB with metadata"""
        
        movie_id = movie_data.get('slug') or movie_data.get('title', '').lower().replace(' ', '-')
        
        # Prepare metadata
        metadata = {
            "title": movie_data.get('title', ''),
            "director": movie_data.get('director', ''),
            "year": str(movie_data.get('year', '')),
            "genres": '|'.join(movie_data.get('genres', [])),
            "mood": ai_analysis.get('mood', ''),
            "emotional_tone": ai_analysis.get('emotional_tone', ''),
            "pacing": ai_analysis.get('pacing', ''),
            "visual_style": '|'.join(ai_analysis.get('visual_style', [])),
            "themes": '|'.join(ai_analysis.get('themes', [])),
            "analyzed_at": datetime.now().isoformat()
        }
        
        # Store in ChromaDB
        self.movies_collection.add(
            embeddings=[embedding],
            documents=[json.dumps({**movie_data, **ai_analysis})],
            metadatas=[metadata],
            ids=[movie_id]
        )
        
        logger.info(f"Stored movie '{movie_data.get('title')}' in vector database")
    
    def analyze_and_store_movie(self, movie_data: Dict[str, Any]) -> bool:
        """Complete workflow: analyze movie with AI and store in vector database"""
        try:
            # Generate slug for ID
            movie_slug = movie_data.get('slug') or movie_data.get('title', '').lower().replace(' ', '-').replace("'", '')
            
            # Check if already exists
            existing = self.movies_collection.get(ids=[movie_slug])
            if existing and len(existing.get('ids', [])) > 0:
                logger.info(f"Movie '{movie_data.get('title')}' already exists in database")
                return False
            
            # Analyze with AI
            ai_analysis = self.analyze_movie_with_ai(movie_data)
            if not ai_analysis:
                logger.error(f"Failed to analyze movie '{movie_data.get('title')}'")
                return False
            
            # Create embedding
            embedding = self.create_movie_embedding(movie_data, ai_analysis)
            
            # Store in database
            self.store_movie_in_vectordb(movie_data, ai_analysis, embedding)
            
            return True
            
        except Exception as e:
            logger.error(f"Error in analyze_and_store_movie: {e}")
            return False
    
    def find_similar_movies(self, movie_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find movies similar to a given movie using vector similarity"""
        
        try:
            # Get the target movie
            results = self.movies_collection.get(ids=[movie_id], include=['embeddings'])
            
            embeddings_list = results.get('embeddings', [])
            if len(embeddings_list) == 0:
                logger.error(f"Movie {movie_id} not found in database")
                return []
            
            target_embedding = embeddings_list[0]
            
            # Query for similar movies
            similar_results = self.movies_collection.query(
                query_embeddings=[target_embedding],
                n_results=limit + 1,  # +1 to exclude the original movie
                include=['documents', 'metadatas', 'distances']
            )
            
            similar_movies = []
            for i, (doc, metadata, distance) in enumerate(zip(
                similar_results['documents'][0],
                similar_results['metadatas'][0], 
                similar_results['distances'][0]
            )):
                # Skip the original movie (distance will be 0 or very small)
                if i == 0 and distance < 0.01:
                    continue
                    
                movie_data = json.loads(doc)
                movie_data['similarity_score'] = 1 - distance  # Convert distance to similarity
                movie_data['metadata'] = metadata
                similar_movies.append(movie_data)
            
            return similar_movies[:limit]
            
        except Exception as e:
            logger.error(f"Error finding similar movies: {e}")
            return []
    
    def generate_recommendations(self, user_profile: Dict[str, Any], num_recommendations: int = 10) -> List[Dict[str, Any]]:
        """Generate personalized recommendations using AI analysis"""
        
        # Get user's favorite movies
        loved_movies = [movie for movie in user_profile.get('ratings', []) 
                       if movie.get('rating', 0) >= 4.0]
        
        if not loved_movies:
            logger.warning("No highly rated movies found for user")
            return []
        
        # Find similar movies for each loved movie
        all_recommendations = []
        
        for movie in loved_movies[:5]:  # Limit to top 5 to control API costs
            movie_slug = movie.get('movie_slug')
            if movie_slug:
                similar = self.find_similar_movies(movie_slug, limit=5)
                for sim_movie in similar:
                    sim_movie['source_movie'] = movie.get('movie_title')
                    sim_movie['source_rating'] = movie.get('rating')
                    all_recommendations.append(sim_movie)
        
        # Remove duplicates and sort by similarity
        seen_ids = set()
        unique_recommendations = []
        
        for rec in sorted(all_recommendations, key=lambda x: x.get('similarity_score', 0), reverse=True):
            movie_id = rec.get('slug') or rec.get('title', '').lower().replace(' ', '-')
            if movie_id not in seen_ids:
                seen_ids.add(movie_id)
                unique_recommendations.append(rec)
        
        return unique_recommendations[:num_recommendations]
    
    def explain_recommendation(self, recommended_movie: Dict[str, Any], user_context: Dict[str, Any]) -> str:
        """Generate AI explanation for why a movie is recommended"""
        
        prompt = f"""
        You are an expert film curator explaining a movie recommendation.
        
        Recommended Movie: {recommended_movie.get('title')} ({recommended_movie.get('year')})
        Director: {recommended_movie.get('director')}
        Similarity Score: {recommended_movie.get('similarity_score', 0):.2f}
        
        User Context:
        - Source Movie: {recommended_movie.get('source_movie')} (rated {recommended_movie.get('source_rating')}/5)
        - User's preferred genres: {', '.join(user_context.get('favorite_genres', [])[:3])}
        
        Movie Analysis:
        - Themes: {', '.join(recommended_movie.get('themes', []))}
        - Mood: {recommended_movie.get('mood')}
        - Visual Style: {', '.join(recommended_movie.get('visual_style', []))}
        
        Provide a 2-3 sentence curator-quality explanation of why this movie is recommended.
        Focus on specific cinematic elements that connect it to their preferences.
        Be insightful and avoid generic language.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model=os.getenv('OPENAI_MODEL', 'gpt-4o'),
                messages=[
                    {"role": "system", "content": "You are a film curator providing personalized recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.4
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return f"Recommended based on similarity to {recommended_movie.get('source_movie')} with {recommended_movie.get('similarity_score', 0):.0%} similarity."

def main():
    """Example usage of the AI Movie Analyzer"""
    analyzer = AIMovieAnalyzer()
    
    # Example movie data
    sample_movie = {
        "title": "The Godfather",
        "year": 1972,
        "director": "Francis Ford Coppola", 
        "genres": ["Crime", "Drama"],
        "plot_summary": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "cast": ["Marlon Brando", "Al Pacino", "James Caan"],
        "slug": "the-godfather"
    }
    
    print("Analyzing movie with AI...")
    analysis = analyzer.analyze_movie_with_ai(sample_movie)
    print("AI Analysis:", json.dumps(analysis, indent=2))
    
    print("\nCreating embedding...")
    embedding = analyzer.create_movie_embedding(sample_movie, analysis)
    print(f"Embedding created with {len(embedding)} dimensions")
    
    print("\nStoring in vector database...")
    analyzer.store_movie_in_vectordb(sample_movie, analysis, embedding)
    print("Movie stored successfully!")

if __name__ == "__main__":
    main()