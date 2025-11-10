import { Handler } from '@netlify/functions';
import axios from 'axios';

interface TMDbMovie {
  id: number;
  title: string;
  release_date: string;
  genre_ids: number[];
  vote_average: number;
  overview: string;
  poster_path: string;
}

interface EnrichedCandidate {
  title: string;
  year: string;
  genres: string[];
  poster?: string;
  plot?: string;
  imdb_rating?: string;
  tmdb_id: number;
}

// TMDb genre mapping
const GENRE_MAP: { [key: number]: string } = {
  28: 'Action',
  12: 'Adventure',
  16: 'Animation',
  35: 'Comedy',
  80: 'Crime',
  99: 'Documentary',
  18: 'Drama',
  10751: 'Family',
  14: 'Fantasy',
  36: 'History',
  27: 'Horror',
  10402: 'Music',
  9648: 'Mystery',
  10749: 'Romance',
  878: 'Sci-Fi',
  10770: 'TV Movie',
  53: 'Thriller',
  10752: 'War',
  37: 'Western',
};

async function fetchTMDbMovies(
  genres: string[],
  page: number = 1
): Promise<TMDbMovie[]> {
  const tmdbApiKey = process.env.TMDB_API_KEY;
  
  if (!tmdbApiKey) {
    throw new Error('TMDb API key not configured');
  }

  try {
    // Convert genre names to TMDb IDs
    const genreIds = genres
      .map(genre => {
        const entry = Object.entries(GENRE_MAP).find(
          ([_, name]) => name.toLowerCase() === genre.toLowerCase()
        );
        return entry ? entry[0] : null;
      })
      .filter(Boolean)
      .join(',');

    const response = await axios.get(
      'https://api.themoviedb.org/3/discover/movie',
      {
        params: {
          api_key: tmdbApiKey,
          language: 'en-US',
          sort_by: 'popularity.desc',
          include_adult: false,
          include_video: false,
          page,
          with_genres: genreIds || undefined,
          'vote_count.gte': 100, // Minimum votes for quality filter
          'vote_average.gte': 6.0, // Minimum rating
        },
      }
    );

    return response.data.results || [];
  } catch (error: any) {
    console.error('TMDb API error:', error.message);
    return [];
  }
}

async function enrichWithOMDb(
  tmdbMovie: TMDbMovie,
  omdbApiKey: string
): Promise<EnrichedCandidate | null> {
  try {
    const year = tmdbMovie.release_date?.split('-')[0] || '';
    
    // Try to find on OMDb for additional metadata
    const response = await axios.get('http://www.omdbapi.com/', {
      params: {
        apikey: omdbApiKey,
        t: tmdbMovie.title,
        y: year,
        type: 'movie',
      },
    });

    const omdbData = response.data;
    
    if (omdbData.Response === 'True') {
      return {
        title: tmdbMovie.title,
        year,
        genres: omdbData.Genre ? omdbData.Genre.split(', ') : tmdbMovie.genre_ids.map(id => GENRE_MAP[id]).filter(Boolean),
        poster: omdbData.Poster !== 'N/A' ? omdbData.Poster : `https://image.tmdb.org/t/p/w500${tmdbMovie.poster_path}`,
        plot: omdbData.Plot || tmdbMovie.overview,
        imdb_rating: omdbData.imdbRating,
        tmdb_id: tmdbMovie.id,
      };
    } else {
      // Use TMDb data only
      return {
        title: tmdbMovie.title,
        year,
        genres: tmdbMovie.genre_ids.map(id => GENRE_MAP[id]).filter(Boolean),
        poster: tmdbMovie.poster_path ? `https://image.tmdb.org/t/p/w500${tmdbMovie.poster_path}` : undefined,
        plot: tmdbMovie.overview,
        imdb_rating: tmdbMovie.vote_average.toString(),
        tmdb_id: tmdbMovie.id,
      };
    }
  } catch (error) {
    // Fallback to TMDb data only
    const year = tmdbMovie.release_date?.split('-')[0] || '';
    return {
      title: tmdbMovie.title,
      year,
      genres: tmdbMovie.genre_ids.map(id => GENRE_MAP[id]).filter(Boolean),
      poster: tmdbMovie.poster_path ? `https://image.tmdb.org/t/p/w500${tmdbMovie.poster_path}` : undefined,
      plot: tmdbMovie.overview,
      imdb_rating: tmdbMovie.vote_average.toString(),
      tmdb_id: tmdbMovie.id,
    };
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
    const { favorite_genres, user_movies } = JSON.parse(event.body || '{}');
    const omdbApiKey = process.env.OMDB_API_KEY;

    if (!omdbApiKey) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'OMDb API key not configured' }),
      };
    }

    console.log(`🎬 Fetching TMDb candidates for genres: ${favorite_genres?.join(', ')}`);

    // Create set of user's movie titles for filtering
    const userMovieTitles = new Set(
      (user_movies || []).map((m: any) => m.title.toLowerCase())
    );

    // Fetch movies from TMDb (multiple pages for variety)
    const allTMDbMovies: TMDbMovie[] = [];
    const pages = favorite_genres?.length > 0 ? [1, 2, 3] : [1, 2]; // Fetch 2-3 pages
    
    for (const page of pages) {
      const movies = await fetchTMDbMovies(favorite_genres || ['Drama', 'Thriller'], page);
      allTMDbMovies.push(...movies);
      await new Promise(resolve => setTimeout(resolve, 250)); // Rate limiting
    }

    console.log(`✅ Fetched ${allTMDbMovies.length} movies from TMDb`);

    // Filter out movies the user has already rated
    const unseenMovies = allTMDbMovies.filter(
      movie => !userMovieTitles.has(movie.title.toLowerCase())
    );

    console.log(`🔍 After filtering user's movies: ${unseenMovies.length} unseen candidates`);

    // Take top 200 popular unseen movies
    const candidates = unseenMovies.slice(0, 200);

    // Enrich a subset with OMDb data (50 movies to stay within timeout)
    const toEnrich = candidates.slice(0, 50);
    console.log(`📦 Enriching ${toEnrich.length} candidates with OMDb...`);

    const enrichedCandidates: EnrichedCandidate[] = [];
    
    // Process in batches to respect API limits
    const BATCH_SIZE = 10;
    for (let i = 0; i < toEnrich.length; i += BATCH_SIZE) {
      const batch = toEnrich.slice(i, i + BATCH_SIZE);
      const batchResults = await Promise.all(
        batch.map(movie => enrichWithOMDb(movie, omdbApiKey))
      );
      enrichedCandidates.push(...batchResults.filter(Boolean) as EnrichedCandidate[]);
      
      if (i + BATCH_SIZE < toEnrich.length) {
        await new Promise(resolve => setTimeout(resolve, 200));
      }
    }

    console.log(`✅ Enriched ${enrichedCandidates.length} candidates`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: enrichedCandidates,
      }),
    };

  } catch (error: any) {
    console.error('TMDb fetch error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to fetch candidate movies',
      }),
    };
  }
};
