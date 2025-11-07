import { Handler } from '@netlify/functions';
import axios from 'axios';
import {
  generateJobId,
  createJob,
  updateJobProgress,
  completeJob,
  failJob,
} from './lib/jobTracker';

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

    // Generate job ID and return immediately
    const jobId = generateJobId();
    createJob(jobId, movies.length);

    console.log(`🎬 Starting enrichment job ${jobId} for ${movies.length} movies...`);

    // Start background processing (don't await)
    processEnrichment(jobId, movies, omdbApiKey).catch((error) => {
      console.error('Background enrichment error:', error);
      failJob(jobId, error.message);
    });

    // Return job ID immediately
    return {
      statusCode: 202, // Accepted
      headers,
      body: JSON.stringify({
        success: true,
        jobId,
        message: `Enrichment job started for ${movies.length} movies`,
      }),
    };

  } catch (error: any) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to start enrichment',
      }),
    };
  }
};

// Background processing function
async function processEnrichment(
  jobId: string,
  movies: Movie[],
  omdbApiKey: string
): Promise<void> {
  const enrichedMovies: EnrichedMovie[] = [];

  for (let i = 0; i < movies.length; i++) {
    const movie = movies[i];
    
    updateJobProgress(jobId, i, `Enriching ${movie.title} (${movie.year})`);
    
    const enriched = await enrichMovieWithOMDb(movie, omdbApiKey);
    enrichedMovies.push(enriched);

    // Small delay to respect API rate limits
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  console.log(`✅ Enrichment job ${jobId} completed: ${enrichedMovies.length} movies`);
  completeJob(jobId, enrichedMovies);
}
