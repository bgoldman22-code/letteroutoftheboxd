import { Handler } from '@netlify/functions';
import axios from 'axios';

interface Movie {
  title: string;
  year: string;
  rating?: number;
  letterboxd_url?: string;
  loved?: boolean;
}

interface EnrichedMovie extends Movie {
  omdb_data?: any;
  genres?: string[];
  director?: string;
  actors?: string[];
  plot?: string;
  poster?: string;
  runtime?: string;
  imdb_rating?: string;
  imdb_id?: string;
}

async function enrichMovieWithOMDb(movie: Movie, apiKey: string): Promise<EnrichedMovie> {
  try {
    const response = await axios.get('http://www.omdbapi.com/', {
      params: {
        apikey: apiKey,
        t: movie.title,
        y: movie.year,
        type: 'movie',
      },
    });

    const data = response.data;

    if (data.Response === 'True') {
      return {
        ...movie,
        omdb_data: data,
        genres: data.Genre ? data.Genre.split(', ') : [],
        director: data.Director,
        actors: data.Actors ? data.Actors.split(', ') : [],
        plot: data.Plot,
        poster: data.Poster !== 'N/A' ? data.Poster : undefined,
        runtime: data.Runtime,
        imdb_rating: data.imdbRating,
        imdb_id: data.imdbID,
      };
    } else {
      console.log(`OMDb: Movie not found - ${movie.title} (${movie.year})`);
      return {
        ...movie,
        genres: [],
      };
    }
  } catch (error: any) {
    console.error(`Error enriching ${movie.title}:`, error.message);
    return {
      ...movie,
      genres: [],
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
    const { movies } = JSON.parse(event.body || '{}');
    const omdbApiKey = process.env.OMDB_API_KEY;

    if (!omdbApiKey) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'OMDb API key not configured' }),
      };
    }

    if (!movies || !Array.isArray(movies)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Movies array is required' }),
      };
    }

    console.log(`🎬 Enriching ${movies.length} movies...`);

    // Enrich movies with delays to respect API rate limits
    const enrichedMovies: EnrichedMovie[] = [];
    
    // Process up to 100 movies to stay within timeout
    for (let i = 0; i < Math.min(movies.length, 100); i++) {
      const movie = movies[i];
      const enriched = await enrichMovieWithOMDb(movie, omdbApiKey);
      enrichedMovies.push(enriched);
      
      // Small delay to respect API rate limits
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    console.log(`✅ Enriched ${enrichedMovies.length} movies`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: enrichedMovies,
      }),
    };

  } catch (error: any) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to enrich movies',
      }),
    };
  }
};
