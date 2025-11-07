import { Handler } from '@netlify/functions';
import OpenAI from 'openai';

interface EnrichedMovie {
  title: string;
  year: string;
  director?: string;
  actors?: string[];
  genres?: string[];
  plot?: string;
  runtime?: string;
  rating?: number;
  loved?: boolean;
}

interface DimensionalScores {
  [key: string]: number;
}

interface AnalysisResult {
  dimensional_scores: DimensionalScores;
  human_condition_themes: string[];
  core_essence: string;
  viewer_resonance: string;
  aesthetic_signature: string;
}

const ELITE_ANALYSIS_PROMPT_TEMPLATE = `You are an elite film phenomenologist analyzing cinema at the deepest perceptual level.

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
62 DIMENSIONS TO SCORE (1-7 scale):
═══════════════════════════════════════════════════════════════════

A. VISUAL LANGUAGE (15):
1. color_palette_psychology: muted earth tones (1) → saturated neon (7)
2. lighting_philosophy: naturalistic (1) → expressionistic chiaroscuro (7)
3. camera_movement_personality: static (1) → kinetic handheld (7)
4. shot_composition_philosophy: symmetrical (1) → off-balance tension (7)
5. depth_of_field_psychology: deep focus (1) → shallow isolated (7)
6. texture_and_grain: digital pristine (1) → heavy analog grain (7)
7. aspect_ratio_emotional_frame: widescreen epic (1) → boxy intimate 4:3 (7)
8. spatial_density: minimalist empty (1) → maximal dense (7)
9. cinematic_realism_spectrum: documentary vérité (1) → surreal dreamspace (7)
10. blocking_and_performance_space: naturalistic (1) → choreographed theatrical (7)
11. color_temperature: cold blue clinical (1) → warm amber intimate (7)
12. lens_distortion_and_perspective: natural eye (1) → extreme wide distortion (7)
13. shadow_ratio: low contrast even (1) → high contrast deep shadows (7)
14. frame_rate_and_motion: 24fps cinematic (1) → high frame rate hyper-real (7)
15. visual_motif_repetition: varied no recurring (1) → obsessive visual themes (7)

B. EDITING & RHYTHM (8):
16. editing_tempo: meditative long takes (1) → jagged hyper-montage (7)
17. narrative_rhythm: even flowing (1) → staccato episodic (7)
18. temporal_structure: chronological linear (1) → nonlinear dream logic (7)
19. montage_philosophy: invisible continuity (1) → Eisensteinian collision (7)
20. scene_length_variance: uniform (1) → radical variation (7)
21. ellipsis_and_gaps: everything shown (1) → radical ellipsis (7)
22. transition_style: hard cuts (1) → slow dissolves (7)
23. rhythm_acceleration: steady pace (1) → builds to frenetic (7)

C. SOUND DESIGN & SCORE (9):
24. score_emotional_temperature: melancholic minor (1) → triumphant major (7)
25. score_density: minimalist sparse (1) → maximalist orchestral (7)
26. music_function: emotional amplification (1) → ironic counterpoint (7)
27. soundscape_texture: quiet intimate (1) → overwhelming saturation (7)
28. diegetic_vs_nondiegetic_ratio: all diegetic (1) → pure score (7)
29. sonic_interiority: external world (1) → subjective inner (7)
30. silence_as_tool: constant sound (1) → radical silence (7)
31. vocal_treatment: crisp clear (1) → obscured murmured (7)
32. rhythmic_percussion: no percussion (1) → driving drums (7)

D. NARRATIVE & PHILOSOPHY (13):
33. philosophical_stance: humanist hope (1) → nihilist void (7)
34. narrative_tension_source: internal psychological (1) → external systemic (7)
35. moral_complexity: clear good vs evil (1) → everyone compromised (7)
36. ending_resolution: complete closure (1) → radical ambiguity (7)
37. power_dynamics: individual agency (1) → structural determinism (7)
38. intimacy_scale: epic historical (1) → domestic intimate (7)
39. dialogue_philosophy: naturalistic (1) → heightened poetic (7)
40. relationship_to_class: class invisible (1) → class as central (7)
41. body_and_physicality: disembodied cerebral (1) → visceral bodily (7)
42. time_relationship: present moment (1) → historical memory (7)
43. hope_quotient: optimistic (1) → despair entropy (7)
44. political_consciousness: apolitical (1) → overtly political (7)

E. QUALITY PROFILE (8):
45. craft_precision_vs_rawness: raw expressiveness (1) → craft precision (7)
46. art_cinema_vs_pop_cinema_mode: art-cinema ambiguity (1) → pop-cinema clarity (7)
47. narrative_ambition_level: sensory thrill (1) → mythic statement (7)
48. irony_sincerity_register: sincere earnest (1) → ironic self-aware (7)
49. emotional_weight_tolerance: light comfort (1) → devastating weight (7)
50. performance_style_preference: naturalistic (1) → heightened theatrical (7)
51. script_construction_visibility: invisible organic (1) → visible architecture (7)
52. auteur_intentionality_desire: collaborative (1) → singular vision (7)

F. EMOTIONAL RESONANCE (11):
53. emotional_temperature: cold distant (1) → hot raw (7)
54. catharsis_availability: no release (1) → explosive climax (7)
55. tonal_consistency: genre pure (1) → radical collision (7)
56. empathy_requirement: likable protagonists (1) → repellent characters (7)
57. beauty_priority: beauty essential (1) → ugliness as honesty (7)
58. sensory_immersion: cerebral distant (1) → fully immersive (7)
59. vulnerability_exposure: protected defended (1) → raw exposed (7)
60. mystery_comfort: all explained (1) → radical inexplicability (7)
61. artifice_awareness: invisible craft (1) → self-conscious meta (7)
62. suffering_tolerance: suffering avoided (1) → suffering unrelenting (7)

═══════════════════════════════════════════════════════════════════
OUTPUT FORMAT:
═══════════════════════════════════════════════════════════════════

Return ONLY valid JSON:

{
  "dimensional_scores": {
    "color_palette_psychology": 3.5,
    "lighting_philosophy": 2.0,
    ... (all 62 dimensions)
  },
  "human_condition_themes": ["loneliness", "identity", "grief"],
  "core_essence": "Brief 2-3 sentence capture of film's deepest nature",
  "viewer_resonance": "What kind of viewer connects with this film and why",
  "aesthetic_signature": "The film's unique visual/sonic/emotional fingerprint"
}

Focus on HOW the film makes you feel and perceive, not plot summary.`;

function generatePrompt(movie: EnrichedMovie): string {
  return ELITE_ANALYSIS_PROMPT_TEMPLATE
    .replace('{title}', movie.title)
    .replace('{year}', movie.year)
    .replace('{director}', movie.director || 'Unknown')
    .replace('{cast}', movie.actors?.slice(0, 5).join(', ') || 'Unknown')
    .replace('{genres}', movie.genres?.join(', ') || 'Unknown')
    .replace('{plot}', movie.plot || 'No plot available')
    .replace('{runtime}', movie.runtime || 'Unknown');
}

async function analyzeMovieWithAI(movie: EnrichedMovie, openai: OpenAI): Promise<AnalysisResult> {
  try {
    const prompt = generatePrompt(movie);

    const response = await openai.chat.completions.create({
      model: process.env.OPENAI_MODEL || 'gpt-4o',
      messages: [
        {
          role: 'system',
          content: 'You are an elite film phenomenologist. Return ONLY valid JSON.'
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      response_format: { type: 'json_object' },
      temperature: 0.7,
    });

    const content = response.choices[0].message.content;
    if (!content) {
      throw new Error('No response from OpenAI');
    }

    const analysis = JSON.parse(content);
    return analysis;

  } catch (error: any) {
    console.error(`Error analyzing ${movie.title}:`, error.message);
    throw error;
  }
}

export const handler: Handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  try {
    const { movies } = JSON.parse(event.body || '{}');
    const openaiApiKey = process.env.OPENAI_API_KEY;

    if (!openaiApiKey) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'OpenAI API key not configured' }),
      };
    }

    if (!movies || !Array.isArray(movies)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Movies array is required' }),
      };
    }

    const openai = new OpenAI({ apiKey: openaiApiKey });

    console.log(`🎬 Analyzing ${movies.length} movies with Elite 62-Dimension Model...`);

    // Analyze movies with delays to avoid rate limits
    const analyzedMovies = [];
    
    for (const movie of movies.slice(0, 20)) { // Limit to 20 for serverless timeout
      try {
        const analysis = await analyzeMovieWithAI(movie, openai);
        analyzedMovies.push({
          ...movie,
          elite_analysis: analysis,
        });
        console.log(`✅ Analyzed: ${movie.title}`);
        
        // Delay to respect rate limits
        await new Promise(resolve => setTimeout(resolve, 1000));
      } catch (error: any) {
        console.error(`❌ Failed to analyze ${movie.title}:`, error.message);
        // Continue with other movies
      }
    }

    console.log(`✅ Successfully analyzed ${analyzedMovies.length}/${movies.length} movies`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: analyzedMovies,
      }),
    };

  } catch (error: any) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to analyze movies',
      }),
    };
  }
};
