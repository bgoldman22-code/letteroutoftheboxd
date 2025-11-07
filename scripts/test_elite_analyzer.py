"""
TEST ELITE AI ANALYZER WITH 58-DIMENSION MODEL
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_movie_analyzer import AIMovieAnalyzer
from multi_api_movie_service import MultiAPIMovieService
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

def test_elite_analyzer():
    """Test the elite analyzer on a sample movie"""
    
    print("=" * 80)
    print("TESTING ELITE 58-DIMENSION AI ANALYZER")
    print("=" * 80)
    
    # Initialize services
    movie_service = MultiAPIMovieService()
    analyzer = AIMovieAnalyzer()
    
    # Test with a visually distinctive film
    test_movie = "Blade Runner 2049"
    
    print(f"\n📡 Fetching movie data for: {test_movie}")
    movie_data = movie_service.get_movie_data(test_movie)
    
    if not movie_data:
        print(f"❌ Could not fetch data for {test_movie}")
        return
    
    print(f"✅ Movie data retrieved")
    print(f"   Title: {movie_data.get('title')}")
    print(f"   Director: {movie_data.get('director')}")
    print(f"   Year: {movie_data.get('year')}")
    
    # Analyze with elite model
    print(f"\n🧠 Running elite 58-dimension analysis...")
    analysis = analyzer.analyze_movie_with_ai(movie_data)
    
    if not analysis:
        print("❌ Analysis failed")
        return
    
    print("\n" + "=" * 80)
    print("ELITE ANALYSIS RESULTS")
    print("=" * 80)
    
    # Display dimensional scores
    if 'dimensional_scores' in analysis:
        scores = analysis['dimensional_scores']
        print(f"\n📊 DIMENSIONAL SCORES ({len(scores)} dimensions):\n")
        
        # Group by category
        visual_dims = [k for k in scores.keys() if any(x in k for x in ['color', 'lighting', 'camera', 'composition', 'depth', 'texture', 'aspect', 'spatial', 'realism', 'blocking', 'temperature', 'lens', 'shadow', 'frame', 'motif'])]
        editing_dims = [k for k in scores.keys() if any(x in k for x in ['editing', 'rhythm', 'temporal', 'montage', 'scene_length', 'ellipsis', 'transition', 'acceleration'])]
        sound_dims = [k for k in scores.keys() if any(x in k for x in ['score', 'soundscape', 'music', 'diegetic', 'sonic', 'silence', 'vocal', 'percussion'])]
        narrative_dims = [k for k in scores.keys() if any(x in k for x in ['philosophical', 'tension', 'moral', 'ending', 'power', 'intimacy', 'dialogue', 'class', 'body', 'time_relationship', 'hope', 'political'])]
        emotional_dims = [k for k in scores.keys() if any(x in k for x in ['emotional', 'catharsis', 'tonal', 'empathy', 'beauty', 'sensory', 'vulnerability', 'mystery', 'artifice', 'suffering'])]
        
        if visual_dims:
            print("🎨 VISUAL LANGUAGE:")
            for dim in sorted(visual_dims):
                score = scores[dim]
                bar = "█" * int(score) + "░" * (7 - int(score))
                print(f"   {dim:40s} [{bar}] {score}")
        
        if editing_dims:
            print("\n✂️ EDITING & RHYTHM:")
            for dim in sorted(editing_dims):
                score = scores[dim]
                bar = "█" * int(score) + "░" * (7 - int(score))
                print(f"   {dim:40s} [{bar}] {score}")
        
        if sound_dims:
            print("\n🎵 SOUND & SCORE:")
            for dim in sorted(sound_dims):
                score = scores[dim]
                bar = "█" * int(score) + "░" * (7 - int(score))
                print(f"   {dim:40s} [{bar}] {score}")
        
        if narrative_dims:
            print("\n📖 NARRATIVE PSYCHOLOGY:")
            for dim in sorted(narrative_dims):
                score = scores[dim]
                bar = "█" * int(score) + "░" * (7 - int(score))
                print(f"   {dim:40s} [{bar}] {score}")
        
        if emotional_dims:
            print("\n💗 EMOTIONAL RESONANCE:")
            for dim in sorted(emotional_dims):
                score = scores[dim]
                bar = "█" * int(score) + "░" * (7 - int(score))
                print(f"   {dim:40s} [{bar}] {score}")
    
    # Display qualitative insights
    print("\n" + "-" * 80)
    print("📝 QUALITATIVE INSIGHTS:\n")
    
    if 'core_essence' in analysis:
        print(f"Core Essence: {analysis['core_essence']}\n")
    
    if 'aesthetic_signature' in analysis:
        print(f"Aesthetic Signature: {analysis['aesthetic_signature']}\n")
    
    if 'viewer_resonance' in analysis:
        print(f"Viewer Resonance: {analysis['viewer_resonance']}\n")
    
    if 'human_condition_themes' in analysis:
        print(f"Human Condition Themes: {', '.join(analysis['human_condition_themes'])}\n")
    
    # Save results
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'elite_analysis_test.json')
    with open(output_file, 'w') as f:
        json.dump({
            'movie': movie_data,
            'elite_analysis': analysis
        }, f, indent=2)
    
    print(f"\n💾 Full analysis saved to: {output_file}")
    print("\n" + "=" * 80)
    print("✅ ELITE ANALYZER TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_elite_analyzer()
