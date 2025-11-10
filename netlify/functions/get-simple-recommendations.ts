import { Handler } from '@netlify/functions';

interface Movie {
  title: string;
  year: string;
  director?: string;
  actors?: string[];
  genres?: string[];
  plot?: string;
  rating?: number;
  loved?: boolean;
  imdb_rating?: string;
  runtime?: string;
  poster?: string;
}

interface AnalyzedMovie extends Movie {
  elite_analysis: {
    dimensional_scores: any;
    human_condition_themes: string[];
    core_essence: string;
    viewer_resonance: string;
    aesthetic_signature: string;
  };
}

interface Recommendation extends Movie {
  match_score: number;
  match_reasons: string[];
}

function extractTasteProfile(analyzedMovies: AnalyzedMovie[]) {
  const genres = new Map<string, number>();
  const directors = new Set<string>();
  const actors = new Set<string>();
  const themes = new Map<string, number>();
  const decades = new Map<string, number>();
  
  let totalRating = 0;
  let ratingCount = 0;

  analyzedMovies.forEach(movie => {
    // Extract genres
    movie.genres?.forEach(genre => {
      const weight = movie.loved ? 2 : (movie.rating || 4) / 5;
      genres.set(genre, (genres.get(genre) || 0) + weight);
    });

    // Extract directors
    if (movie.director) {
      directors.add(movie.director);
    }

    // Extract top actors
    movie.actors?.slice(0, 3).forEach(actor => {
      actors.add(actor);
    });

    // Extract themes
    movie.elite_analysis?.human_condition_themes?.forEach(theme => {
      const weight = movie.loved ? 2 : (movie.rating || 4) / 5;
      themes.set(theme, (themes.get(theme) || 0) + weight);
    });

    // Extract decade
    const year = parseInt(movie.year);
    if (!isNaN(year)) {
      const decade = `${Math.floor(year / 10) * 10}s`;
      decades.set(decade, (decades.get(decade) || 0) + 1);
    }

    // Average rating
    if (movie.rating) {
      totalRating += movie.rating;
      ratingCount++;
    }
  });

  return {
    topGenres: Array.from(genres.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([genre]) => genre),
    favoriteDirectors: Array.from(directors),
    favoriteActors: Array.from(actors),
    topThemes: Array.from(themes.entries())
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([theme]) => theme),
    preferredDecades: Array.from(decades.keys()),
    avgRating: ratingCount > 0 ? totalRating / ratingCount : 4.0,
  };
}

function calculateMatch(candidate: Movie, profile: ReturnType<typeof extractTasteProfile>, userMovieIds: Set<string>): { score: number; reasons: string[] } {
  // Skip if already in user's analyzed movies
  const candidateId = `${candidate.title}_${candidate.year}`;
  if (userMovieIds.has(candidateId)) {
    return { score: 0, reasons: [] };
  }

  let score = 0;
  const reasons: string[] = [];

  // Genre matching (40% weight)
  const candidateGenres = candidate.genres || [];
  const genreMatches = candidateGenres.filter(g => profile.topGenres.includes(g));
  if (genreMatches.length > 0) {
    const genreScore = (genreMatches.length / profile.topGenres.length) * 0.4;
    score += genreScore;
    reasons.push(`Matches your favorite genres: ${genreMatches.join(', ')}`);
  }

  // Director matching (30% weight)
  if (candidate.director && profile.favoriteDirectors.includes(candidate.director)) {
    score += 0.3;
    reasons.push(`Directed by ${candidate.director} - a filmmaker you love`);
  }

  // Actor matching (15% weight)
  const actorMatches = (candidate.actors || []).filter(a => profile.favoriteActors.includes(a));
  if (actorMatches.length > 0) {
    const actorScore = Math.min(actorMatches.length * 0.05, 0.15);
    score += actorScore;
    reasons.push(`Stars ${actorMatches.slice(0, 2).join(', ')}`);
  }

  // Decade matching (10% weight)
  const candidateYear = parseInt(candidate.year);
  if (!isNaN(candidateYear)) {
    const decade = `${Math.floor(candidateYear / 10) * 10}s`;
    if (profile.preferredDecades.includes(decade)) {
      score += 0.1;
      reasons.push(`From the ${decade} - an era you appreciate`);
    }
  }

  // Quality filter (IMDb rating boost)
  if (candidate.imdb_rating) {
    const imdbScore = parseFloat(candidate.imdb_rating);
    if (imdbScore >= 7.5) {
      score += 0.05;
      reasons.push(`Highly rated (${imdbScore}/10 on IMDb)`);
    }
  }

  return { score, reasons };
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

    console.log(`🎯 Generating simple recommendations from ${user_movies.length} user movies and ${candidate_movies.length} candidates`);

    // Extract taste profile from analyzed movies
    const profile = extractTasteProfile(user_movies);
    console.log(`✅ Taste profile: ${profile.topGenres.join(', ')} | ${profile.favoriteDirectors.length} directors`);

    // Create set of user movie IDs for filtering
    const userMovieIds = new Set(
      user_movies.map(m => `${m.title}_${m.year}`)
    );

    // Calculate matches
    const recommendations: Recommendation[] = [];
    
    for (const candidate of candidate_movies) {
      const match = calculateMatch(candidate, profile, userMovieIds);
      
      if (match.score > 0.2) { // Minimum threshold
        recommendations.push({
          ...candidate,
          match_score: match.score,
          match_reasons: match.reasons,
        });
      }
    }

    // Sort by match score
    recommendations.sort((a, b) => b.match_score - a.match_score);
    const topRecommendations = recommendations.slice(0, 15);

    console.log(`✅ Generated ${topRecommendations.length} recommendations`);

    // Format response
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: {
          recommendations: topRecommendations,
          taste_fingerprint: {
            top_genres: profile.topGenres,
            favorite_directors: profile.favoriteDirectors,
            top_themes: profile.topThemes,
            preferred_decades: profile.preferredDecades,
            loved_movies_count: user_movies.filter(m => m.loved).length,
            avg_rating: profile.avgRating,
          },
        },
      }),
    };

  } catch (error: any) {
    console.error('Recommendation error:', error);
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
