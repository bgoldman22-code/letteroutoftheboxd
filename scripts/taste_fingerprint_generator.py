"""
TASTE FINGERPRINT GENERATOR
═══════════════════════════════════════════════════════════════════

Converts deep cinematic analysis into personalized aesthetic profiles
and vector embeddings for similarity matching.

This system:
1. Scores films on all 58 dimensions (1-7 scale)
2. Generates human-readable taste fingerprints
3. Creates vector embeddings for mathematical similarity
4. Enables matching between films and user taste profiles
"""

import numpy as np
from typing import Dict, List, Any, Tuple
import json


class TasteFingerprintGenerator:
    """Generate personalized cinematic taste fingerprints"""
    
    def __init__(self):
        # 62 dimensions for complete taste model (added Quality Profile category)
        self.dimension_count = 62
        self.dimension_names = self._get_all_dimension_names()
    
    def _get_all_dimension_names(self) -> List[str]:
        """Return all 58 dimension names in order"""
        return [
            # Visual Language (15)
            "color_palette_psychology",
            "lighting_philosophy",
            "camera_movement_personality",
            "shot_composition_philosophy",
            "depth_of_field_psychology",
            "texture_and_grain",
            "aspect_ratio_emotional_frame",
            "spatial_density",
            "cinematic_realism_spectrum",
            "blocking_and_performance_space",
            "color_temperature",
            "lens_distortion_and_perspective",
            "shadow_ratio",
            "frame_rate_and_motion",
            "visual_motif_repetition",
            
            # Editing & Rhythm (8)
            "editing_tempo",
            "narrative_rhythm",
            "temporal_structure",
            "montage_philosophy",
            "scene_length_variance",
            "ellipsis_and_gaps",
            "transition_style",
            "rhythm_acceleration",
            
            # Sound & Score (9)
            "score_emotional_temperature",
            "score_density",
            "music_function",
            "soundscape_texture",
            "diegetic_vs_nondiegetic_ratio",
            "sonic_interiority",
            "silence_as_tool",
            "vocal_treatment",
            "rhythmic_percussion",
            
            # Narrative Psychology (15)
            "philosophical_stance",
            "narrative_tension_source",
            "moral_complexity",
            "ending_resolution",
            "power_dynamics",
            "intimacy_scale",
            "dialogue_philosophy",
            "relationship_to_class",
            "body_and_physicality",
            "time_relationship",
            "hope_quotient",
            "political_consciousness",
            
            # Quality Profile (8)
            "craft_precision_vs_rawness",
            "art_cinema_vs_pop_cinema_mode",
            "narrative_ambition_level",
            "irony_sincerity_register",
            "emotional_weight_tolerance",
            "performance_style_preference",
            "script_construction_visibility",
            "auteur_intentionality_desire",
            
            # Emotional Resonance (11)
            "emotional_temperature",
            "catharsis_availability",
            "tonal_consistency",
            "empathy_requirement",
            "beauty_priority",
            "sensory_immersion",
            "vulnerability_exposure",
            "mystery_comfort",
            "artifice_awareness",
            "suffering_tolerance"
        ]
    
    def generate_taste_fingerprint(
        self, 
        loved_movies_scores: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a complete taste fingerprint from user's loved movies
        
        Args:
            loved_movies_scores: List of movies with their dimensional scores
        
        Returns:
            Complete taste fingerprint with averages, patterns, and narrative
        """
        
        # Calculate average scores across all dimensions
        avg_scores = self._calculate_average_scores(loved_movies_scores)
        
        # Identify strongest preferences
        strong_preferences = self._identify_strong_preferences(avg_scores)
        
        # Generate human-readable narrative
        narrative = self._generate_narrative_fingerprint(avg_scores, strong_preferences)
        
        # Create vector embedding
        taste_vector = self._create_taste_vector(avg_scores)
        
        return {
            "dimensional_scores": avg_scores,
            "strong_preferences": strong_preferences,
            "narrative": narrative,
            "taste_vector": taste_vector.tolist(),
            "vector_dimension": len(taste_vector)
        }
    
    def _calculate_average_scores(
        self, 
        loved_movies_scores: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Calculate average score for each dimension across loved movies"""
        
        dimension_sums = {dim: 0.0 for dim in self.dimension_names}
        dimension_counts = {dim: 0 for dim in self.dimension_names}
        
        for movie in loved_movies_scores:
            scores = movie.get('dimensional_scores', {})
            for dim, score in scores.items():
                if dim in dimension_sums and score is not None:
                    dimension_sums[dim] += score
                    dimension_counts[dim] += 1
        
        # Calculate averages
        avg_scores = {}
        for dim in self.dimension_names:
            if dimension_counts[dim] > 0:
                avg_scores[dim] = dimension_sums[dim] / dimension_counts[dim]
            else:
                avg_scores[dim] = 4.0  # Neutral midpoint
        
        return avg_scores
    
    def _identify_strong_preferences(
        self, 
        avg_scores: Dict[str, float]
    ) -> Dict[str, List[Tuple[str, float]]]:
        """Identify dimensions with strong preferences (extreme scores)"""
        
        strong_low = []  # Scores 1-2.5
        strong_high = []  # Scores 5.5-7
        
        for dim, score in avg_scores.items():
            if score <= 2.5:
                strong_low.append((dim, score))
            elif score >= 5.5:
                strong_high.append((dim, score))
        
        # Sort by extremity
        strong_low.sort(key=lambda x: x[1])
        strong_high.sort(key=lambda x: x[1], reverse=True)
        
        return {
            "low_end_preferences": strong_low[:10],  # Top 10 most extreme
            "high_end_preferences": strong_high[:10]
        }
    
    def _generate_narrative_fingerprint(
        self, 
        avg_scores: Dict[str, float],
        strong_preferences: Dict[str, List[Tuple[str, float]]]
    ) -> str:
        """Generate human-readable taste narrative"""
        
        narrative_parts = []
        
        # Visual Language Summary
        visual_narrative = self._narrate_visual_taste(avg_scores)
        if visual_narrative:
            narrative_parts.append(visual_narrative)
        
        # Rhythm & Pacing Summary
        rhythm_narrative = self._narrate_rhythm_taste(avg_scores)
        if rhythm_narrative:
            narrative_parts.append(rhythm_narrative)
        
        # Sound & Score Summary
        sound_narrative = self._narrate_sound_taste(avg_scores)
        if sound_narrative:
            narrative_parts.append(sound_narrative)
        
        # Quality Profile Summary (NEW)
        quality_narrative = self._narrate_quality_taste(avg_scores)
        if quality_narrative:
            narrative_parts.append(quality_narrative)
        
        # Narrative Psychology Summary
        story_narrative = self._narrate_story_taste(avg_scores)
        if story_narrative:
            narrative_parts.append(story_narrative)
        
        # Emotional Resonance Summary
        emotional_narrative = self._narrate_emotional_taste(avg_scores)
        if emotional_narrative:
            narrative_parts.append(emotional_narrative)
        
        return " ".join(narrative_parts)
    
    def _narrate_visual_taste(self, scores: Dict[str, float]) -> str:
        """Narrate visual language preferences"""
        parts = []
        
        color_score = scores.get('color_palette_psychology', 4)
        if color_score < 3:
            parts.append("You gravitate toward muted, desaturated color palettes that evoke melancholy and earthbound realism.")
        elif color_score > 5:
            parts.append("You respond to saturated, neon-drenched visuals that create heightened, dreamlike intensity.")
        
        lighting_score = scores.get('lighting_philosophy', 4)
        if lighting_score < 3:
            parts.append("You prefer naturalistic lighting that captures the world as it is, unmanipulated.")
        elif lighting_score > 5:
            parts.append("You're drawn to expressionistic chiaroscuro lighting that sculpts psychological landscapes.")
        
        camera_score = scores.get('camera_movement_personality', 4)
        if camera_score < 3:
            parts.append("You value static, contemplative camera work that observes from respectful distance.")
        elif camera_score > 5:
            parts.append("You connect with kinetic, handheld cinematography that puts you inside the nervous system of the story.")
        
        realism_score = scores.get('cinematic_realism_spectrum', 4)
        if realism_score < 3:
            parts.append("You trust observational realism over stylization.")
        elif realism_score > 5:
            parts.append("You embrace surreal dreamscapes where subconscious truth supersedes literal reality.")
        
        return " ".join(parts)
    
    def _narrate_rhythm_taste(self, scores: Dict[str, float]) -> str:
        """Narrate editing and rhythm preferences"""
        parts = []
        
        tempo_score = scores.get('editing_tempo', 4)
        if tempo_score < 3:
            parts.append("You have patience for long takes and meditative pacing that allows you to sit with images.")
        elif tempo_score > 5:
            parts.append("You respond to rapid montage and kinetic editing that creates visceral momentum.")
        
        temporal_score = scores.get('temporal_structure', 4)
        if temporal_score > 5:
            parts.append("You embrace nonlinear narrative structures that mirror how memory actually works.")
        
        return " ".join(parts)
    
    def _narrate_sound_taste(self, scores: Dict[str, float]) -> str:
        """Narrate sound design preferences"""
        parts = []
        
        score_temp = scores.get('score_emotional_temperature', 4)
        if score_temp < 3:
            parts.append("You're drawn to melancholic, minor-key scores that amplify sorrow and loss.")
        elif score_temp > 5:
            parts.append("You connect with triumphant, soaring music that offers emotional uplift.")
        
        silence_score = scores.get('silence_as_tool', 4)
        if silence_score > 5:
            parts.append("You value radical use of silence as space for contemplation and discomfort.")
        
        soundscape_score = scores.get('soundscape_texture', 4)
        if soundscape_score < 3:
            parts.append("You prefer quiet, intimate soundscapes that capture interior emotional space.")
        elif soundscape_score > 5:
            parts.append("You respond to overwhelming sensory saturation in sound design.")
        
        return " ".join(parts)
    
    def _narrate_quality_taste(self, scores: Dict[str, float]) -> str:
        """Narrate quality profile and cinematic craft preferences"""
        parts = []
        
        craft_score = scores.get('craft_precision_vs_rawness', 4)
        if craft_score < 3:
            parts.append("You value raw expressiveness and emotional immediacy over polished perfection—craft can get in the way of truth.")
        elif craft_score > 5:
            parts.append("You find deep satisfaction in meticulous formal mastery where every frame is composed with visual intelligence.")
        
        art_pop_score = scores.get('art_cinema_vs_pop_cinema_mode', 4)
        if art_pop_score < 3:
            parts.append("You prefer art-cinema mode: ambiguity, slowness, existential inquiry that rewards patience.")
        elif art_pop_score > 5:
            parts.append("You prefer pop-cinema mode: clarity, momentum, satisfying plot escalation and kinetic pleasure.")
        
        ambition_score = scores.get('narrative_ambition_level', 4)
        if ambition_score < 2.5:
            parts.append("You seek pure sensory thrill and spectacle over thematic density.")
        elif ambition_score > 5.5:
            parts.append("You want cinema to wrestle with mythic themes—existence, mortality, the human condition writ large.")
        
        irony_score = scores.get('irony_sincerity_register', 4)
        if irony_score < 3:
            parts.append("You need films to take emotion seriously without ironic distance—full sincerity is essential.")
        elif irony_score > 5:
            parts.append("You prefer self-aware, meta-textual cinema that maintains ironic distance from pure emotion.")
        
        weight_score = scores.get('emotional_weight_tolerance', 4)
        if weight_score < 2.5:
            parts.append("You use cinema for restoration and comfort—emotional heaviness feels overwhelming.")
        elif weight_score > 5.5:
            parts.append("You seek devastating emotional weight and unrelenting intensity—light films feel trivial.")
        
        performance_score = scores.get('performance_style_preference', 4)
        if performance_score < 3:
            parts.append("You want acting to disappear into naturalistic behavioral truth.")
        elif performance_score > 5:
            parts.append("You love watching visible craft in heightened theatrical performances.")
        
        script_score = scores.get('script_construction_visibility', 4)
        if script_score > 5:
            parts.append("You find pleasure in intricate narrative architecture and visible structural intelligence.")
        
        auteur_score = scores.get('auteur_intentionality_desire', 4)
        if auteur_score > 5:
            parts.append("You respond to singular directorial vision and total artistic control.")
        
        return " ".join(parts)
    
    def _narrate_story_taste(self, scores: Dict[str, float]) -> str:
        """Narrate narrative psychology preferences"""
        parts = []
        
        philosophy_score = scores.get('philosophical_stance', 4)
        if philosophy_score < 3:
            parts.append("You connect with humanist narratives that maintain hope in human goodness and meaningful connection.")
        elif philosophy_score > 5:
            parts.append("You're drawn to cynical or nihilistic worldviews that refuse easy comfort.")
        
        resolution_score = scores.get('ending_resolution', 4)
        if resolution_score > 5:
            parts.append("You prefer films that end in radical ambiguity, trusting you to live with unanswered questions.")
        
        moral_score = scores.get('moral_complexity', 4)
        if moral_score > 5:
            parts.append("You value moral ambiguity where every character is compromised and human.")
        
        class_score = scores.get('relationship_to_class', 4)
        if class_score > 5:
            parts.append("You notice when economic reality shapes everything, seeing class as central to human experience.")
        
        return " ".join(parts)
    
    def _narrate_emotional_taste(self, scores: Dict[str, float]) -> str:
        """Narrate emotional resonance preferences"""
        parts = []
        
        temp_score = scores.get('emotional_temperature', 4)
        if temp_score < 3:
            parts.append("You process emotion through distance and observation, intellectualizing feeling.")
        elif temp_score > 5:
            parts.append("You need raw, unfiltered emotional intensity and aren't afraid of messiness.")
        
        vulnerability_score = scores.get('vulnerability_exposure', 4)
        if vulnerability_score > 5:
            parts.append("You crave total emotional exposure, needing to see people break completely.")
        
        mystery_score = scores.get('mystery_comfort', 4)
        if mystery_score > 5:
            parts.append("You're comfortable with radical inexplicability, embracing films that never explain themselves.")
        
        beauty_score = scores.get('beauty_priority', 4)
        if beauty_score < 3:
            parts.append("Every frame must be aesthetically composed—you need beauty as refuge.")
        elif beauty_score > 5:
            parts.append("You distrust beauty as lie, preferring deliberate ugliness as honesty.")
        
        return " ".join(parts)
    
    def _create_taste_vector(self, avg_scores: Dict[str, float]) -> np.ndarray:
        """Create normalized vector embedding from dimensional scores"""
        
        # Create vector in consistent dimension order
        vector = np.array([
            avg_scores.get(dim, 4.0) for dim in self.dimension_names
        ])
        
        # Normalize to 0-1 range (from 1-7 scale)
        normalized = (vector - 1) / 6
        
        return normalized
    
    def calculate_similarity(
        self, 
        vector1: np.ndarray, 
        vector2: np.ndarray
    ) -> float:
        """Calculate cosine similarity between two taste vectors"""
        
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)
    
    def match_film_to_taste(
        self, 
        film_vector: np.ndarray,
        user_taste_vector: np.ndarray
    ) -> Dict[str, Any]:
        """Match a film's aesthetic to user's taste profile"""
        
        similarity_score = self.calculate_similarity(film_vector, user_taste_vector)
        
        # Calculate dimensional alignment (which dimensions match strongest)
        dimension_alignment = {}
        for i, dim_name in enumerate(self.dimension_names):
            film_score = film_vector[i]
            user_pref = user_taste_vector[i]
            alignment = 1 - abs(film_score - user_pref)  # Higher = better match
            dimension_alignment[dim_name] = float(alignment)
        
        # Get top matching dimensions
        sorted_alignment = sorted(
            dimension_alignment.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        return {
            "overall_similarity": similarity_score,
            "top_matching_dimensions": sorted_alignment[:10],
            "bottom_matching_dimensions": sorted_alignment[-5:],
            "match_explanation": self._explain_match(sorted_alignment[:5])
        }
    
    def _explain_match(self, top_matches: List[Tuple[str, float]]) -> str:
        """Generate human-readable match explanation"""
        
        explanations = {
            "color_palette_psychology": "shares your color palette sensibility",
            "lighting_philosophy": "uses light the way you respond to",
            "camera_movement_personality": "moves the camera in ways you find natural",
            "editing_tempo": "breathes at your preferred rhythm",
            "score_emotional_temperature": "uses music to evoke emotion the way you like",
            "philosophical_stance": "shares your worldview about human nature",
            "emotional_temperature": "matches your emotional processing style",
            "mystery_comfort": "handles ambiguity the way you prefer",
            "cinematic_realism_spectrum": "balances realism and stylization as you like",
            "vulnerability_exposure": "reveals interiority at your comfort level"
        }
        
        parts = ["This film matches your taste because it"]
        for dim, score in top_matches[:3]:
            if dim in explanations:
                parts.append(explanations[dim])
        
        return " " + ", ".join(parts) + "."


# Example usage and template
TASTE_FINGERPRINT_EXAMPLE = """
EXAMPLE TASTE FINGERPRINT
═══════════════════════════════════════════════════════════════════

You gravitate toward films that use quiet soundscapes, long dissolves, 
and naturalistic lighting to evoke interior emotional space. You respond 
to narratives of longing and identity reconstruction, framed through poetic 
realism. You prefer melancholic humanism over cynicism, and you connect 
with stories where the world is not explained, but felt.

Your visual taste favors muted earth tones and shallow depth of field that 
isolates subjects in emotional loneliness. You have patience for meditative 
long takes and embrace nonlinear temporal structures that mirror memory's 
actual texture. You're drawn to films that end in radical ambiguity, 
trusting you to live with unanswered questions.

You value total emotional exposure—you need to see people break completely. 
You're comfortable with inexplicability and distrust neat resolutions. You 
see beauty in restraint rather than saturated intensity. Your worldview 
aligns with humanist hope while acknowledging moral complexity.

Films that speak to you: In the Mood for Love, Moonlight, The Tree of Life, 
Portrait of a Lady on Fire, First Reformed, The Rider, Paterson.

Films that miss your taste: Mad Max Fury Road (too kinetic), The Grand 
Budapest Hotel (too symmetrical), Whiplash (too aggressive), most superhero 
films (moral clarity vs ambiguity).

Your taste fingerprint: 
Visual → Naturalistic, muted, intimate
Rhythm → Slow, contemplative, nonlinear  
Sound → Quiet, melancholic, silence-positive
Story → Humanist, ambiguous, interior-focused
Emotion → Vulnerable, patient, mystery-comfortable
"""


def create_sample_film_profile() -> Dict[str, float]:
    """Create sample dimensional scores for a film"""
    return {
        "color_palette_psychology": 2.0,  # Muted
        "lighting_philosophy": 2.5,  # Naturalistic
        "camera_movement_personality": 2.0,  # Static, contemplative
        "shot_composition_philosophy": 3.0,  # Balanced
        "depth_of_field_psychology": 6.0,  # Shallow, isolated
        "texture_and_grain": 5.0,  # Film grain, tactile
        "aspect_ratio_emotional_frame": 5.0,  # Intimate 4:3
        "spatial_density": 2.0,  # Minimalist
        "cinematic_realism_spectrum": 4.0,  # Poetic realism
        "blocking_and_performance_space": 2.0,  # Naturalistic
        "color_temperature": 3.0,  # Slightly cool
        "lens_distortion_and_perspective": 2.0,  # Natural perspective
        "shadow_ratio": 3.0,  # Low contrast
        "frame_rate_and_motion": 2.0,  # 24fps dream
        "visual_motif_repetition": 3.0,  # Some recurring imagery
        
        "editing_tempo": 2.0,  # Meditative long takes
        "narrative_rhythm": 2.0,  # Even, flowing
        "temporal_structure": 6.0,  # Nonlinear memory
        "montage_philosophy": 2.0,  # Invisible editing
        "scene_length_variance": 4.0,  # Moderate variation
        "ellipsis_and_gaps": 5.0,  # Significant gaps
        "transition_style": 6.0,  # Slow dissolves
        "rhythm_acceleration": 2.0,  # Steady pace
        
        "score_emotional_temperature": 2.0,  # Melancholic
        "score_density": 3.0,  # Sparse
        "music_function": 2.0,  # Emotional amplification
        "soundscape_texture": 2.0,  # Quiet intimate
        "diegetic_vs_nondiegetic_ratio": 4.0,  # Mix
        "sonic_interiority": 5.0,  # Subjective soundscape
        "silence_as_tool": 6.0,  # Radical silence
        "vocal_treatment": 2.0,  # Clear dialogue
        "rhythmic_percussion": 2.0,  # No percussion
        
        "philosophical_stance": 3.0,  # Humanist with complexity
        "narrative_tension_source": 2.0,  # Internal psychological
        "moral_complexity": 6.0,  # Everyone compromised
        "ending_resolution": 6.0,  # Radical ambiguity
        "power_dynamics": 4.0,  # Mix of agency and determinism
        "intimacy_scale": 6.0,  # Domestic intimate
        "dialogue_philosophy": 2.0,  # Naturalistic
        "relationship_to_class": 4.0,  # Present but not central
        "body_and_physicality": 3.0,  # Mix
        "time_relationship": 6.0,  # Memory-heavy
        "hope_quotient": 3.0,  # Melancholic hope
        "political_consciousness": 4.0,  # Moderate
        
        "emotional_temperature": 5.0,  # Warm but controlled
        "catharsis_availability": 3.0,  # Limited release
        "tonal_consistency": 3.0,  # Mostly consistent
        "empathy_requirement": 3.0,  # Likable but complex
        "beauty_priority": 2.0,  # Beauty essential
        "sensory_immersion": 4.0,  # Moderate
        "vulnerability_exposure": 6.0,  # Raw exposed
        "mystery_comfort": 6.0,  # Radical inexplicability
        "artifice_awareness": 3.0,  # Some meta moments
        "suffering_tolerance": 5.0  # Can witness pain
    }


if __name__ == "__main__":
    # Test the system
    generator = TasteFingerprintGenerator()
    
    # Create sample film
    sample_film = {
        "title": "Moonlight",
        "dimensional_scores": create_sample_film_profile()
    }
    
    # Generate fingerprint
    fingerprint = generator.generate_taste_fingerprint([sample_film])
    
    print("TASTE FINGERPRINT GENERATED")
    print("=" * 70)
    print(f"\nNarrative:\n{fingerprint['narrative']}")
    print(f"\nVector Dimensions: {fingerprint['vector_dimension']}")
    print(f"\nStrong Low Preferences: {fingerprint['strong_preferences']['low_end_preferences'][:3]}")
    print(f"\nStrong High Preferences: {fingerprint['strong_preferences']['high_end_preferences'][:3]}")
