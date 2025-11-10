import { Handler } from '@netlify/functions';

interface DimensionalScores {
  [key: string]: number;
}

interface EliteAnalysis {
  dimensional_scores: DimensionalScores;
  human_condition_themes: string[];
  core_essence: string;
  viewer_resonance: string;
  aesthetic_signature: string;
}

interface AnalyzedMovie {
  title: string;
  year: string;
  rating?: number;
  loved?: boolean;
  elite_analysis: EliteAnalysis;
}

interface TasteFingerprint {
  dimensional_preferences: DimensionalScores;
  thematic_interests: { [theme: string]: number };
  loved_movies_count: number;
  avg_rating: number;
}

interface Recommendation {
  title: string;
  year: string;
  similarity_score: number;
  dimensional_match: number;
  thematic_match: number;
  elite_analysis: EliteAnalysis;
  match_reasons: string[];
}

// All 62 dimension keys
const ALL_DIMENSIONS = [
  'color_palette_psychology', 'lighting_philosophy', 'camera_movement_personality',
  'shot_composition_philosophy', 'depth_of_field_psychology', 'texture_and_grain',
  'aspect_ratio_emotional_frame', 'spatial_density', 'cinematic_realism_spectrum',
  'blocking_and_performance_space', 'color_temperature', 'lens_distortion_and_perspective',
  'shadow_ratio', 'frame_rate_and_motion', 'visual_motif_repetition',
  'editing_tempo', 'narrative_rhythm', 'temporal_structure', 'montage_philosophy',
  'scene_length_variance', 'ellipsis_and_gaps', 'transition_style', 'rhythm_acceleration',
  'score_emotional_temperature', 'score_density', 'music_function', 'soundscape_texture',
  'diegetic_vs_nondiegetic_ratio', 'sonic_interiority', 'silence_as_tool',
  'vocal_treatment', 'rhythmic_percussion',
  'philosophical_stance', 'narrative_tension_source', 'moral_complexity',
  'ending_resolution', 'power_dynamics', 'intimacy_scale', 'dialogue_philosophy',
  'relationship_to_class', 'body_and_physicality', 'time_relationship',
  'hope_quotient', 'political_consciousness',
  'craft_precision_vs_rawness', 'art_cinema_vs_pop_cinema_mode', 'narrative_ambition_level',
  'irony_sincerity_register', 'emotional_weight_tolerance', 'performance_style_preference',
  'script_construction_visibility', 'auteur_intentionality_desire',
  'emotional_temperature', 'catharsis_availability', 'tonal_consistency',
  'empathy_requirement', 'beauty_priority', 'sensory_immersion',
  'vulnerability_exposure', 'mystery_comfort', 'artifice_awareness', 'suffering_tolerance'
];

function generateTasteFingerprint(userMovies: AnalyzedMovie[]): TasteFingerprint {
  const dimensionalPreferences: DimensionalScores = {};
  const thematicInterests: { [theme: string]: number } = {};
  
  let totalRating = 0;
  let ratingCount = 0;
  let lovedCount = 0;

  // Weight movies by rating and loved status
  userMovies.forEach(movie => {
    const weight = movie.loved ? 2.0 : (movie.rating ? movie.rating / 5 : 1.0);
    
    // Accumulate dimensional preferences
    const scores = movie.elite_analysis.dimensional_scores;
    for (const dim of ALL_DIMENSIONS) {
      if (scores[dim] !== undefined) {
        dimensionalPreferences[dim] = (dimensionalPreferences[dim] || 0) + scores[dim] * weight;
      }
    }

    // Accumulate thematic interests
    const themes = movie.elite_analysis.human_condition_themes || [];
    themes.forEach(theme => {
      thematicInterests[theme] = (thematicInterests[theme] || 0) + weight;
    });

    if (movie.rating) {
      totalRating += movie.rating;
      ratingCount++;
    }
    if (movie.loved) lovedCount++;
  });

  // Normalize dimensional preferences
  const totalWeight = userMovies.reduce((sum, m) => 
    sum + (m.loved ? 2.0 : (m.rating ? m.rating / 5 : 1.0)), 0
  );
  
  for (const dim of ALL_DIMENSIONS) {
    if (dimensionalPreferences[dim]) {
      dimensionalPreferences[dim] /= totalWeight;
    }
  }

  return {
    dimensional_preferences: dimensionalPreferences,
    thematic_interests: thematicInterests,
    loved_movies_count: lovedCount,
    avg_rating: ratingCount > 0 ? totalRating / ratingCount : 0,
  };
}

function calculateSimilarity(
  fingerprint: TasteFingerprint,
  candidate: AnalyzedMovie,
  userMovieIds: Set<string>
): { score: number; dimensional_match: number; thematic_match: number; reasons: string[] } {
  
  // Skip if already seen
  const candidateId = `${candidate.title}_${candidate.year}`;
  if (userMovieIds.has(candidateId)) {
    return { score: 0, dimensional_match: 0, thematic_match: 0, reasons: [] };
  }

  // Calculate dimensional similarity (cosine similarity)
  let dotProduct = 0;
  let fingerprintMagnitude = 0;
  let candidateMagnitude = 0;
  let dimensionCount = 0;

  for (const dim of ALL_DIMENSIONS) {
    const fpValue = fingerprint.dimensional_preferences[dim];
    const candValue = candidate.elite_analysis.dimensional_scores[dim];
    
    if (fpValue !== undefined && candValue !== undefined) {
      dotProduct += fpValue * candValue;
      fingerprintMagnitude += fpValue * fpValue;
      candidateMagnitude += candValue * candValue;
      dimensionCount++;
    }
  }

  const dimensionalMatch = dimensionCount > 0 
    ? dotProduct / (Math.sqrt(fingerprintMagnitude) * Math.sqrt(candidateMagnitude))
    : 0;

  // Calculate thematic similarity
  const candidateThemes = candidate.elite_analysis.human_condition_themes || [];
  let thematicScore = 0;
  
  candidateThemes.forEach(theme => {
    if (fingerprint.thematic_interests[theme]) {
      thematicScore += fingerprint.thematic_interests[theme];
    }
  });

  const maxThematicScore = Math.max(...Object.values(fingerprint.thematic_interests), 1);
  const thematicMatch = candidateThemes.length > 0 ? thematicScore / maxThematicScore : 0;

  // Combined score (70% dimensional, 30% thematic)
  const combinedScore = (dimensionalMatch * 0.7) + (thematicMatch * 0.3);

  // Generate match reasons
  const reasons: string[] = [];
  
  if (dimensionalMatch > 0.8) {
    reasons.push('Exceptional dimensional alignment with your taste');
  } else if (dimensionalMatch > 0.7) {
    reasons.push('Strong cinematic style match');
  }

  if (thematicMatch > 0.5) {
    const matchedThemes = candidateThemes.filter(t => fingerprint.thematic_interests[t]);
    if (matchedThemes.length > 0) {
      reasons.push(`Explores themes you love: ${matchedThemes.slice(0, 3).join(', ')}`);
    }
  }

  // Find strongest dimensional matches
  const strongDimensions: string[] = [];
  for (const dim of ALL_DIMENSIONS) {
    const fpValue = fingerprint.dimensional_preferences[dim];
    const candValue = candidate.elite_analysis.dimensional_scores[dim];
    
    if (fpValue && candValue && Math.abs(fpValue - candValue) < 0.5) {
      strongDimensions.push(dim.replace(/_/g, ' '));
    }
  }

  if (strongDimensions.length > 5) {
    reasons.push(`Matches your preferences in ${strongDimensions.slice(0, 3).join(', ')}`);
  }

  return {
    score: combinedScore,
    dimensional_match: dimensionalMatch,
    thematic_match: thematicMatch,
    reasons,
  };
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
    const { user_movies, candidate_movies } = JSON.parse(event.body || '{}');

    if (!user_movies || !Array.isArray(user_movies)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'user_movies array is required' }),
      };
    }

    if (!candidate_movies || !Array.isArray(candidate_movies)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'candidate_movies array is required' }),
      };
    }

    console.log(`🎯 Generating recommendations from ${user_movies.length} user movies and ${candidate_movies.length} candidates`);

    // Generate taste fingerprint
    const fingerprint = generateTasteFingerprint(user_movies);
    console.log(`✅ Generated taste fingerprint with ${Object.keys(fingerprint.dimensional_preferences).length} dimensions`);

    // Create set of user movie IDs for filtering
    const userMovieIds = new Set(
      user_movies.map(m => `${m.title}_${m.year}`)
    );

    // Calculate similarities
    const recommendations: Recommendation[] = [];
    
    for (const candidate of candidate_movies) {
      // Skip candidates without elite analysis (only analyzed movies have this)
      if (!candidate.elite_analysis || !candidate.elite_analysis.dimensional_scores) {
        continue;
      }
      
      const similarity = calculateSimilarity(fingerprint, candidate, userMovieIds);
      
      if (similarity.score > 0) {
        recommendations.push({
          title: candidate.title,
          year: candidate.year,
          similarity_score: similarity.score,
          dimensional_match: similarity.dimensional_match,
          thematic_match: similarity.thematic_match,
          elite_analysis: candidate.elite_analysis,
          match_reasons: similarity.reasons,
        });
      }
    }

    // Sort by similarity score and take top 20
    recommendations.sort((a, b) => b.similarity_score - a.similarity_score);
    const topRecommendations = recommendations.slice(0, 20);

    console.log(`✅ Generated ${topRecommendations.length} recommendations`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: {
          recommendations: topRecommendations,
          taste_fingerprint: {
            dimensional_summary: fingerprint.dimensional_preferences,
            top_themes: Object.entries(fingerprint.thematic_interests)
              .sort(([, a], [, b]) => b - a)
              .slice(0, 10)
              .map(([theme]) => theme),
            avg_rating: fingerprint.avg_rating,
            loved_movies_count: fingerprint.loved_movies_count,
          },
        },
      }),
    };

  } catch (error: any) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to generate recommendations',
      }),
    };
  }
};
