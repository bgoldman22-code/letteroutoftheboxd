import { Handler } from '@netlify/functions';

interface Movie {
  title: string;
  year?: string;
  director?: string;
  genres?: string[];
  poster?: string;
  rating?: number;
}

// Shuffle array utility
function shuffle<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

// Calculate diversity score between two movies
function diversityScore(movie1: Movie, movie2: Movie): number {
  let score = 0;
  
  // Different decade
  const year1 = parseInt(movie1.year || '2000');
  const year2 = parseInt(movie2.year || '2000');
  const decadeDiff = Math.abs(Math.floor(year1 / 10) - Math.floor(year2 / 10));
  score += Math.min(decadeDiff * 10, 50);
  
  // Different genres
  const genres1 = new Set(movie1.genres || []);
  const genres2 = new Set(movie2.genres || []);
  const genreOverlap = [...genres1].filter(g => genres2.has(g)).length;
  score += (Math.max(genres1.size, genres2.size) - genreOverlap) * 15;
  
  // Different director
  if (movie1.director !== movie2.director) {
    score += 20;
  }
  
  return score;
}

// Select diverse movies from pool that are different from selected movies
function selectDiverseMovies(pool: Movie[], selectedMovies: Movie[], count: number): Movie[] {
  const scored = pool.map(movie => {
    // Calculate average diversity from all selected movies
    const avgDiversity = selectedMovies.reduce((sum, selected) => 
      sum + diversityScore(movie, selected), 0) / selectedMovies.length;
    
    return { movie, score: avgDiversity };
  });
  
  // Sort by diversity score (highest first) and take top N
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, count).map(s => s.movie);
}

// Select edge case movies that fill taste gaps
function selectEdgeCaseMovies(
  pool: Movie[], 
  round1: Movie[], 
  round2: Movie[], 
  count: number
): Movie[] {
  const allSelected = [...round1, ...round2];
  
  // Calculate characteristics of selected movies
  const avgYear = allSelected.reduce((sum, m) => sum + parseInt(m.year || '2000'), 0) / allSelected.length;
  const allGenres = new Set(allSelected.flatMap(m => m.genres || []));
  
  // Score movies based on how they fill gaps
  const scored = pool.map(movie => {
    let score = 0;
    const movieYear = parseInt(movie.year || '2000');
    
    // Prefer movies from different eras
    const yearDiff = Math.abs(movieYear - avgYear);
    score += yearDiff / 2;
    
    // Prefer movies with genres not yet seen
    const movieGenres = new Set(movie.genres || []);
    const newGenres = [...movieGenres].filter(g => !allGenres.has(g));
    score += newGenres.length * 30;
    
    // Add randomness to avoid always picking the same edge cases
    score += Math.random() * 20;
    
    return { movie, score };
  });
  
  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, count).map(s => s.movie);
}

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
    const {
      movies,
      round1Selections = [],
      round2Selections = [],
      round3Selections = [],
      round4Selections = [],
      round1Shown = [],
      round2Shown = [],
      round3Shown = [],
      round4Shown = []
    } = JSON.parse(event.body || '{}');

    if (!movies || !Array.isArray(movies) || movies.length === 0) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Movies array is required' }),
      };
    }

    // Helper to get excluded movies
    const getExcludedTitles = (...shownArrays: Movie[][]) => {
      const excluded = new Set<string>();
      shownArrays.forEach(arr => {
        arr.forEach(m => excluded.add(`${m.title}-${m.year}`));
      });
      return excluded;
    };

    // Helper to filter remaining pool
    const getRemainingPool = (excludedTitles: Set<string>) => {
      return movies.filter((m: Movie) => !excludedTitles.has(`${m.title}-${m.year}`));
    };

    // ROUND 1: Random diverse sample
    if (round1Selections.length === 0) {
      const shuffled = shuffle(movies);
      const round1 = shuffled.slice(0, 10);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          round: 1,
          movies: round1,
          instruction: 'Pick your 3 absolute favorites from these films',
        }),
      };
    }

    // ROUND 2: Diverse from Round 1
    if (round2Selections.length === 0) {
      const excluded = getExcludedTitles(round1Shown);
      const remainingPool = getRemainingPool(excluded);
      const round2 = selectDiverseMovies(remainingPool, round1Selections, 10);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          round: 2,
          movies: round2,
          instruction: 'Now pick 3 from this diverse set - explore different styles!',
        }),
      };
    }

    // ROUND 3: Diverse from Rounds 1 & 2
    if (round3Selections.length === 0) {
      const excluded = getExcludedTitles(round1Shown, round2Shown);
      const remainingPool = getRemainingPool(excluded);
      const allSelections = [...round1Selections, ...round2Selections];
      const round3 = selectDiverseMovies(remainingPool, allSelections, 10);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          round: 3,
          movies: round3,
          instruction: 'Keep going - 3 more films that speak to you!',
        }),
      };
    }

    // ROUND 4: Diverse from Rounds 1, 2 & 3
    if (round4Selections.length === 0) {
      const excluded = getExcludedTitles(round1Shown, round2Shown, round3Shown);
      const remainingPool = getRemainingPool(excluded);
      const allSelections = [...round1Selections, ...round2Selections, ...round3Selections];
      const round4 = selectDiverseMovies(remainingPool, allSelections, 10);
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          round: 4,
          movies: round4,
          instruction: 'Almost there - pick 3 more to refine your taste profile!',
        }),
      };
    }

    // ROUND 5: Final round - edge cases and gap-filling
    const excluded = getExcludedTitles(round1Shown, round2Shown, round3Shown, round4Shown);
    const remainingPool = getRemainingPool(excluded);
    const allPreviousSelections = [
      ...round1Selections,
      ...round2Selections,
      ...round3Selections,
      ...round4Selections
    ];
    const round5 = selectEdgeCaseMovies(
      remainingPool,
      round1Selections,
      [...round2Selections, ...round3Selections, ...round4Selections],
      10
    );
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        round: 5,
        movies: round5,
        instruction: 'Final round - pick your last 3 to complete your cinematic DNA!',
      }),
    };

  } catch (error: any) {
    console.error('Selection rounds error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to generate selection rounds',
      }),
    };
  }
};

export { handler };
