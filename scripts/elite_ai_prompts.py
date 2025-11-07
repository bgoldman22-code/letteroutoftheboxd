"""
ELITE AI MOVIE ANALYZER - DEEP TASTE MODEL VERSION
═══════════════════════════════════════════════════════════════════

Analyzes films across 62 deep cinematic dimensions using AI.
Goes far beyond genre and plot to understand WHY people connect with films.
"""

ELITE_ANALYSIS_PROMPT = """
You are an elite film phenomenologist analyzing cinema at the deepest perceptual level.

Your task: Score this film on 62 cinematic taste dimensions (1-7 scale).

This is NOT about plot, genre, or ratings. This is about:
- Visual language and aesthetic choices
- Rhythmic and temporal experience  
- Sound design and musical architecture
- Psychological and philosophical depth
- Emotional resonance and viewer experience

═══════════════════════════════════════════════════════════════════
FILM TO ANALYZE:
═══════════════════════════════════════════════════════════════════

Title: {title}
Year: {year}
Director: {director}
Cast: {cast}
Genres: {genres}
Plot: {plot}
Runtime: {runtime}

═══════════════════════════════════════════════════════════════════
SCORING INSTRUCTIONS:
═══════════════════════════════════════════════════════════════════

For EACH dimension below, provide:
1. A score from 1-7
2. A brief evidence-based explanation

Use this scale:
1-2 = Strongly exhibits left pole characteristic
3-4 = Moderately exhibits left pole or neutral
5-6 = Moderately exhibits right pole
7 = Strongly exhibits right pole characteristic

═══════════════════════════════════════════════════════════════════
A. VISUAL LANGUAGE (15 dimensions)
═══════════════════════════════════════════════════════════════════

1. color_palette_psychology
   Scale: 1 (muted earth tones, desaturated) → 7 (saturated neon intensity)
   Evidence: [Describe color choices and their emotional impact]
   Score: 

2. lighting_philosophy
   Scale: 1 (naturalistic available light) → 7 (expressionistic chiaroscuro)
   Evidence: [Describe lighting approach and mood creation]
   Score: 

3. camera_movement_personality
   Scale: 1 (locked down static observation) → 7 (kinetic handheld chaos)
   Evidence: [Describe camera's relationship to subject]
   Score: 

4. shot_composition_philosophy
   Scale: 1 (symmetrical centered balanced) → 7 (off-balance diagonal tension)
   Evidence: [Describe compositional choices]
   Score: 

5. depth_of_field_psychology
   Scale: 1 (deep focus everything visible) → 7 (shallow isolated subject)
   Evidence: [Describe focus choices and their meaning]
   Score: 

6. texture_and_grain
   Scale: 1 (digital pristine) → 7 (heavy grain analog texture)
   Evidence: [Describe material quality of image]
   Score: 

7. aspect_ratio_emotional_frame
   Scale: 1 (widescreen epic space) → 7 (boxy intimate 4:3 portrait)
   Evidence: [Describe aspect ratio and its emotional impact]
   Score: 

8. spatial_density
   Scale: 1 (minimalist empty space) → 7 (maximal visual density)
   Evidence: [Describe use of space and visual information]
   Score: 

9. cinematic_realism_spectrum
   Scale: 1 (documentary vérité) → 7 (surreal dreamspace)
   Evidence: [Describe relationship to reality]
   Score: 

10. blocking_and_performance_space
    Scale: 1 (naturalistic actor movement) → 7 (choreographed theatrical)
    Evidence: [Describe performance style]
    Score: 

11. color_temperature
    Scale: 1 (cold blue clinical) → 7 (warm amber intimate)
    Evidence: [Describe emotional warmth of color]
    Score: 

12. lens_distortion_and_perspective
    Scale: 1 (natural human eye) → 7 (extreme wide angle distortion)
    Evidence: [Describe perceptual stability]
    Score: 

13. shadow_ratio
    Scale: 1 (low contrast even lighting) → 7 (high contrast deep shadows)
    Evidence: [Describe use of shadow and mystery]
    Score: 

14. frame_rate_and_motion
    Scale: 1 (24fps cinematic dreamstate) → 7 (high frame rate hyper-real)
    Evidence: [Describe temporal texture]
    Score: 

15. visual_motif_repetition
    Scale: 1 (varied no recurring imagery) → 7 (obsessive visual themes)
    Evidence: [Describe self-conscious style]
    Score: 

═══════════════════════════════════════════════════════════════════
B. EDITING & RHYTHM (8 dimensions)
═══════════════════════════════════════════════════════════════════

16. editing_tempo
    Scale: 1 (meditative long takes) → 7 (jagged hyper-montage)
    Evidence: [Describe how film breathes]
    Score: 

17. narrative_rhythm
    Scale: 1 (even flowing linear) → 7 (staccato episodic chaos)
    Evidence: [Describe story tempo]
    Score: 

18. temporal_structure
    Scale: 1 (chronological linear time) → 7 (nonlinear dream logic)
    Evidence: [Describe time structure]
    Score: 

19. montage_philosophy
    Scale: 1 (invisible continuity editing) → 7 (Eisensteinian collision)
    Evidence: [Describe editing visibility]
    Score: 

20. scene_length_variance
    Scale: 1 (uniform scene length) → 7 (radical length variation)
    Evidence: [Describe rhythm predictability]
    Score: 

21. ellipsis_and_gaps
    Scale: 1 (everything shown) → 7 (radical ellipsis huge gaps)
    Evidence: [Describe narrative completeness]
    Score: 

22. transition_style
    Scale: 1 (hard cuts) → 7 (slow dissolves fades)
    Evidence: [Describe temporal movement sharpness]
    Score: 

23. rhythm_acceleration
    Scale: 1 (steady pace throughout) → 7 (builds to frenetic climax)
    Evidence: [Describe emotional architecture]
    Score: 

═══════════════════════════════════════════════════════════════════
C. SOUND DESIGN & SCORE (9 dimensions)
═══════════════════════════════════════════════════════════════════

24. score_emotional_temperature
    Scale: 1 (melancholic strings minor key) → 7 (triumphant brass major)
    Evidence: [Describe musical mood]
    Score: 

25. score_density
    Scale: 1 (minimalist sparse) → 7 (maximalist orchestral saturation)
    Evidence: [Describe musical presence]
    Score: 

26. music_function
    Scale: 1 (emotional amplification) → 7 (ironic counterpoint)
    Evidence: [Describe music-image relationship]
    Score: 

27. soundscape_texture
    Scale: 1 (quiet intimate ambience) → 7 (overwhelming sensory saturation)
    Evidence: [Describe sound volume and density]
    Score: 

28. diegetic_vs_nondiegetic_ratio
    Scale: 1 (all diegetic source music) → 7 (pure score orchestral omniscience)
    Evidence: [Describe music realism]
    Score: 

29. sonic_interiority
    Scale: 1 (external world sounds) → 7 (subjective inner soundscape)
    Evidence: [Describe sound subjectivity]
    Score: 

30. silence_as_tool
    Scale: 1 (constant sound/score) → 7 (radical use of silence)
    Evidence: [Describe use of absence]
    Score: 

31. vocal_treatment
    Scale: 1 (crisp clear dialogue) → 7 (obscured murmured layered)
    Evidence: [Describe speech clarity]
    Score: 

32. rhythmic_percussion
    Scale: 1 (no percussion strings/piano) → 7 (driving drums anxiety pulse)
    Evidence: [Describe rhythmic urgency]
    Score: 

═══════════════════════════════════════════════════════════════════
E. QUALITY PROFILE - Cinematic Craft & Intention (8 dimensions)
═══════════════════════════════════════════════════════════════════

What the viewer perceives as meaningful, satisfying, impressive, or worthwhile.
NOT about "good vs bad" — about what KIND of cinematic intention resonates.

45. craft_precision_vs_rawness
   Scale: 1 (raw expressiveness) → 7 (craft precision)
   Evidence: [Polished formal mastery vs emotional immediacy]
   Score: 

46. art_cinema_vs_pop_cinema_mode
   Scale: 1 (art-cinema: ambiguity/slowness) → 7 (pop-cinema: clarity/pace)
   Evidence: [Neither is better, just different value systems]
   Score: 

47. narrative_ambition_level
   Scale: 1 (purely sensory thrill) → 4 (grounded realism) → 7 (mythic statement)
   Evidence: [How much meaning density the viewer wants]
   Score: 

48. irony_sincerity_register
   Scale: 1 (sincere earnest) → 7 (ironic self-aware)
   Evidence: [Emotional directness vs self-aware distance]
   Score: 

49. emotional_weight_tolerance
   Scale: 1 (light comfort) → 4 (mid-range) → 7 (devastating weight)
   Evidence: [How heavy can it be before it stops being enjoyable]
   Score: 

50. performance_style_preference
   Scale: 1 (naturalistic behavioral) → 7 (heightened theatrical)
   Evidence: [Should acting disappear or be visibly performed]
   Score: 

51. script_construction_visibility
   Scale: 1 (invisible organic) → 7 (visible architecture)
   Evidence: [Want to see screenplay bones or structure hidden]
   Score: 

52. auteur_intentionality_desire
   Scale: 1 (collaborative process) → 7 (singular vision)
   Evidence: [Value directorial control and artistic ego]
   Score: 

═══════════════════════════════════════════════════════════════════
F. EMOTIONAL RESONANCE (11 dimensions)
═══════════════════════════════════════════════════════════════════

33. philosophical_stance
    Scale: 1 (humanist hope) → 7 (nihilist void)
    Evidence: [Describe worldview about human nature]
    Score: 

34. narrative_tension_source
    Scale: 1 (internal psychological) → 7 (external systemic)
    Evidence: [Describe where conflict lives]
    Score: 

35. moral_complexity
    Scale: 1 (clear good vs evil) → 7 (everyone compromised)
    Evidence: [Describe moral clarity or ambiguity]
    Score: 

36. ending_resolution
    Scale: 1 (complete closure) → 7 (radical ambiguity)
    Evidence: [Describe how much is explained]
    Score: 

37. power_dynamics
    Scale: 1 (individual agency) → 7 (structural determinism)
    Evidence: [Describe belief in free will]
    Score: 

38. intimacy_scale
    Scale: 1 (epic historical scope) → 7 (domestic intimate portrait)
    Evidence: [Describe zoom level of human experience]
    Score: 

39. dialogue_philosophy
    Scale: 1 (naturalistic conversation) → 7 (heightened poetic language)
    Evidence: [Describe speech realism]
    Score: 

40. relationship_to_class
    Scale: 1 (class invisible) → 7 (class as central)
    Evidence: [Describe economic reality awareness]
    Score: 

41. body_and_physicality
    Scale: 1 (disembodied cerebral) → 7 (visceral bodily experience)
    Evidence: [Describe mind vs flesh emphasis]
    Score: 

42. time_relationship
    Scale: 1 (present moment urgency) → 7 (historical memory weight)
    Evidence: [Describe temporal focus]
    Score: 

43. hope_quotient
    Scale: 1 (optimistic change possible) → 7 (despair stasis entropy)
    Evidence: [Describe belief in improvement]
    Score: 

44. political_consciousness
    Scale: 1 (apolitical individual) → 7 (overtly political systemic)
    Evidence: [Describe power structure awareness]
    Score: 

═══════════════════════════════════════════════════════════════════
E. EMOTIONAL RESONANCE (11 dimensions)
═══════════════════════════════════════════════════════════════════

45. emotional_temperature
    Scale: 1 (cold distant clinical) → 7 (hot raw overwhelming)
    Evidence: [Describe emotional intensity permission]
    Score: 

46. catharsis_availability
    Scale: 1 (no release sustained tension) → 7 (explosive emotional climax)
    Evidence: [Describe release potential]
    Score: 

47. tonal_consistency
    Scale: 1 (genre pure consistent) → 7 (radical genre collision)
    Evidence: [Describe tonal stability]
    Score: 

48. empathy_requirement
    Scale: 1 (likable protagonists) → 7 (repellent difficult characters)
    Evidence: [Describe character likability]
    Score: 

49. beauty_priority
    Scale: 1 (beauty essential) → 7 (ugliness as honesty)
    Evidence: [Describe aesthetic necessity]
    Score: 

50. sensory_immersion
    Scale: 1 (cerebral distant) → 7 (fully immersive sensory)
    Evidence: [Describe embodied experience]
    Score: 

51. vulnerability_exposure
    Scale: 1 (protected defended) → 7 (raw exposed interiority)
    Evidence: [Describe emotional nakedness]
    Score: 

52. mystery_comfort
    Scale: 1 (all explained) → 7 (radical inexplicability)
    Evidence: [Describe tolerance for unknowing]
    Score: 

53. artifice_awareness
    Scale: 1 (invisible craft immersion) → 7 (self-conscious meta-cinema)
    Evidence: [Describe awareness of construction]
    Score: 

52. auteur_intentionality_desire
   Scale: 1 (collaborative process) → 7 (singular vision)
   Evidence: [Value directorial control and artistic ego]
   Score: 

═══════════════════════════════════════════════════════════════════
F. EMOTIONAL RESONANCE (11 dimensions)
═══════════════════════════════════════════════════════════════════

53. emotional_temperature
   Scale: 1 (cold distant clinical) → 7 (hot raw overwhelming)
   Evidence: [Emotional intensity permission]
   Score: 

54. catharsis_availability
   Scale: 1 (no release sustained tension) → 7 (explosive emotional climax)
   Evidence: [Do we get to release or sit in discomfort]
   Score: 

55. tonal_consistency
   Scale: 1 (genre pure consistent) → 7 (radical genre collision)
   Evidence: [Does tone stay stable or lurch between modes]
   Score: 

56. empathy_requirement
   Scale: 1 (likable protagonists) → 7 (repellent difficult characters)
   Evidence: [Character likability requirement]
   Score: 

57. beauty_priority
   Scale: 1 (beauty essential) → 7 (ugliness as honesty)
   Evidence: [Aesthetic necessity]
   Score: 

58. sensory_immersion
   Scale: 1 (cerebral distant) → 7 (fully immersive sensory)
   Evidence: [Embodied experience level]
   Score: 

59. vulnerability_exposure
   Scale: 1 (protected defended) → 7 (raw exposed interiority)
   Evidence: [Emotional nakedness tolerance]
   Score: 

60. mystery_comfort
   Scale: 1 (all explained) → 7 (radical inexplicability)
   Evidence: [Tolerance for unknowing]
   Score: 

61. artifice_awareness
   Scale: 1 (invisible craft immersion) → 7 (self-conscious meta-cinema)
   Evidence: [Awareness of construction]
   Score: 

62. suffering_tolerance
   Scale: 1 (suffering avoided) → 7 (suffering unrelenting)
   Evidence: [Pain endurance requirement]
   Score: 

═══════════════════════════════════════════════════════════════════
OUTPUT FORMAT:
═══════════════════════════════════════════════════════════════════

Return ONLY valid JSON in this exact format:

{{
  "dimensional_scores": {{
    "color_palette_psychology": 3.5,
    "lighting_philosophy": 2.0,
    ... (all 62 dimensions with scores 1-7)
  }},
  "human_condition_themes": ["loneliness", "identity", "grief"],
  "core_essence": "A brief 2-3 sentence capture of the film's deepest nature",
  "viewer_resonance": "What kind of viewer connects with this film and why",
  "aesthetic_signature": "The film's unique visual/sonic/emotional fingerprint"
}}Remember: 
- This is NOT plot summary
- This is phenomenological analysis
- Focus on HOW the film makes you feel and perceive
- Every score needs specific evidence from the film
- Think like a film theorist, not a reviewer
"""


def generate_elite_analysis_prompt(movie_data: dict) -> str:
    """Generate the complete analysis prompt for a specific film"""
    return ELITE_ANALYSIS_PROMPT.format(
        title=movie_data.get('title', 'Unknown'),
        year=movie_data.get('year', 'Unknown'),
        director=movie_data.get('director', 'Unknown'),
        cast=', '.join(movie_data.get('cast', [])[:5]),
        genres=', '.join(movie_data.get('genres', [])),
        plot=movie_data.get('plot_summary', 'No plot available'),
        runtime=movie_data.get('runtime', 'Unknown')
    )
