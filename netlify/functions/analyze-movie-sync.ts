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
- Emotional textures and tonal qualities
- Philosophical underpinnings
- Visceral and psychological impact

FILM TO ANALYZE:
{FILM_DATA}

Return ONLY valid JSON with this exact structure:
{
  "dimensional_scores": {
    "visual_poetry": 1-7,
    "narrative_complexity": 1-7,
    "temporal_rhythm": 1-7,
    "emotional_authenticity": 1-7,
    "philosophical_depth": 1-7,
    "visceral_impact": 1-7,
    "tonal_consistency": 1-7,
    "character_interiority": 1-7,
    "world_immersion": 1-7,
    "aesthetic_boldness": 1-7,
    "intellectual_rigor": 1-7,
    "sensory_richness": 1-7,
    "thematic_resonance": 1-7,
    "pacing_mastery": 1-7,
    "symbolic_density": 1-7,
    "emotional_complexity": 1-7,
    "visual_coherence": 1-7,
    "narrative_innovation": 1-7,
    "atmospheric_depth": 1-7,
    "psychological_insight": 1-7,
    "cinematic_language": 1-7,
    "tonal_range": 1-7,
    "existential_weight": 1-7,
    "sensorial_design": 1-7,
    "narrative_clarity": 1-7,
    "visual_ambition": 1-7,
    "emotional_restraint": 1-7,
    "philosophical_ambiguity": 1-7,
    "rhythmic_variation": 1-7,
    "character_authenticity": 1-7,
    "world_building": 1-7,
    "aesthetic_consistency": 1-7,
    "intellectual_accessibility": 1-7,
    "sensory_overload": 1-7,
    "thematic_clarity": 1-7,
    "pacing_variation": 1-7,
    "symbolic_accessibility": 1-7,
    "emotional_directness": 1-7,
    "visual_minimalism": 1-7,
    "narrative_linearity": 1-7,
    "atmospheric_subtlety": 1-7,
    "psychological_complexity": 1-7,
    "cinematic_convention": 1-7,
    "tonal_shifts": 1-7,
    "existential_lightness": 1-7,
    "sensorial_restraint": 1-7,
    "narrative_ambiguity": 1-7,
    "visual_realism": 1-7,
    "emotional_intensity": 1-7,
    "philosophical_clarity": 1-7,
    "rhythmic_consistency": 1-7,
    "character_complexity": 1-7,
    "world_realism": 1-7,
    "aesthetic_experimentation": 1-7,
    "intellectual_challenge": 1-7,
    "sensory_balance": 1-7,
    "thematic_layering": 1-7,
    "pacing_deliberation": 1-7,
    "symbolic_richness": 1-7,
    "emotional_subtlety": 1-7,
    "visual_expressionism": 1-7,
    "narrative_fragmentation": 1-7,
    "atmospheric_intensity": 1-7
  },
  "human_condition_themes": ["theme1", "theme2", "theme3"],
  "core_essence": "one sentence capturing the film's deepest quality",
  "viewer_resonance": "who this film speaks to and why",
  "aesthetic_signature": "the film's unique visual/tonal identity"
}`;

const handler: Handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
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

    console.log(`🎬 Analyzing ${movies.length} movies with optimized batch processing...`);

    const openai = new OpenAI({ apiKey: openaiApiKey });
    const analyzed: { [title: string]: AnalysisResult } = {};
    
    // Process only first 15 movies to stay within 26s timeout
    // This ensures reliable completion without 504 errors
    const MAX_MOVIES = 15;
    const moviesToProcess = movies.slice(0, MAX_MOVIES);
    const CONCURRENT_REQUESTS = 6; // Analyze all 6 movies at once for Phase 1 speed (was 3)
    
    if (movies.length > MAX_MOVIES) {
      console.log(`⚠️  Limiting analysis to ${MAX_MOVIES} movies (found ${movies.length}) to stay within timeout`);
    }
    
    for (let i = 0; i < moviesToProcess.length; i += CONCURRENT_REQUESTS) {
      const batch = moviesToProcess.slice(i, i + CONCURRENT_REQUESTS);
      
      await Promise.all(batch.map(async (movie) => {
        try {
          const filmData = `
Title: ${movie.title} (${movie.year})
Director: ${movie.director || 'Unknown'}
Cast: ${movie.actors?.slice(0, 3).join(', ') || 'Unknown'}
Genres: ${movie.genres?.join(', ') || 'Unknown'}
Plot: ${movie.plot?.substring(0, 200) || 'No plot available'}
Runtime: ${movie.runtime || 'Unknown'}
`;

          console.log(`  📽️  Analyzing: ${movie.title} (${movie.year})`);

          const completion = await openai.chat.completions.create({
            model: 'gpt-4o-mini', // Using mini for 10x faster response + 60x cheaper
            messages: [
              {
                role: 'system',
                content: 'You are an elite film critic. Respond ONLY with valid JSON. Be concise.',
              },
              {
                role: 'user',
                content: ELITE_ANALYSIS_PROMPT_TEMPLATE.replace('{FILM_DATA}', filmData),
              },
            ],
            temperature: 0.5, // Reduced from 0.7 for faster, more focused generation
            max_tokens: 800, // Reduced from 1000 for speed
          });

          const responseText = completion.choices[0]?.message?.content?.trim() || '{}';
          
          // Strip markdown code blocks if present
          let cleanedJson = responseText;
          if (cleanedJson.startsWith('```')) {
            // Remove ```json or ``` at start and ``` at end
            cleanedJson = cleanedJson.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '').trim();
          }
          
          const analysis: AnalysisResult = JSON.parse(cleanedJson);

          analyzed[`${movie.title} (${movie.year})`] = analysis;
          console.log(`  ✅ ${movie.title}: Complete`);

        } catch (error: any) {
          console.error(`  ❌ ${movie.title}: ${error.message}`);
        }
      }));
    }

    console.log(`✅ Analysis complete! Processed ${Object.keys(analyzed).length}/${movies.length} movies`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        analyzed,
        total_movies: movies.length,
        processed: Object.keys(analyzed).length,
      }),
    };

  } catch (error: any) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Analysis failed',
      }),
    };
  }
};

export { handler };
