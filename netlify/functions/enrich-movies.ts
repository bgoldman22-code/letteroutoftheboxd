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

    console.log(`🎬 Enriching ${movies.length} movies with parallel processing...`);

    // Process up to 100 movies in parallel batches to stay within timeout
    const moviesToProcess = movies.slice(0, Math.min(movies.length, 100));
    
    // Parallel processing with concurrency limit to respect API rate limits
    const BATCH_SIZE = 10; // Process 10 movies at a time
    const enrichedMovies: EnrichedMovie[] = [];
    
    for (let i = 0; i < moviesToProcess.length; i += BATCH_SIZE) {
      const batch = moviesToProcess.slice(i, i + BATCH_SIZE);
      console.log(`📦 Processing batch ${Math.floor(i / BATCH_SIZE) + 1}/${Math.ceil(moviesToProcess.length / BATCH_SIZE)}: ${batch.length} movies`);
      
      const batchResults = await Promise.all(
        batch.map(movie => enrichMovieWithOMDb(movie, omdbApiKey))
      );
      
      enrichedMovies.push(...batchResults);
      
      // Small delay between batches to respect API rate limits
      if (i + BATCH_SIZE < moviesToProcess.length) {
        await new Promise(resolve => setTimeout(resolve, 200));
      }
    }

    console.log(`✅ Enriched ${enrichedMovies.length} movies in parallel`);

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
