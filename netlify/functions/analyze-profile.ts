import { Handler } from '@netlify/functions';
import axios from 'axios';
import * as cheerio from 'cheerio';

interface Movie {
  title: string;
  year: string;
  rating: number;
  letterboxd_url: string;
  loved?: boolean;
}

interface ProfileData {
  username: string;
  total_films: number;
  films_this_year: number;
  loved_movies: Movie[];
  all_rated_movies: Movie[];
}

async function scrapeLetterboxdProfile(username: string): Promise<ProfileData> {
  const baseUrl = `https://letterboxd.com/${username}`;
  
  try {
    // Scrape profile page for stats
    const profileResponse = await axios.get(baseUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
      },
    });
    
    const $ = cheerio.load(profileResponse.data);
    
    // Extract stats
    const stats = $('.profile-stats');
    const totalFilms = parseInt(stats.find('a[href$="/films/"] .value').text().replace(/,/g, '') || '0');
    const filmsThisYear = parseInt(stats.find('a[href$="/films/diary/this-year/"] .value').text().replace(/,/g, '') || '0');
    
    console.log(`📊 Profile stats: ${totalFilms} total films, ${filmsThisYear} this year`);
    
    // Use RSS feed to get rated movies (much more reliable!)
    // RSS typically returns the most recent 50-100 entries
    const rssUrl = `${baseUrl}/rss/`;
    console.log(`� Fetching RSS feed: ${rssUrl}`);
    
    const rssResponse = await axios.get(rssUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
      },
    });
    
    const $rss = cheerio.load(rssResponse.data, { xmlMode: true });
    
    const allRatedMovies: Movie[] = [];
    const lovedMovies: Movie[] = [];
    const seenFilms = new Set<string>(); // Track unique films
    
    $rss('item').each((_, element) => {
      const filmTitle = $rss(element).find('letterboxd\\:filmTitle, filmTitle').text();
      const filmYear = $rss(element).find('letterboxd\\:filmYear, filmYear').text();
      const memberRating = parseFloat($rss(element).find('letterboxd\\:memberRating, memberRating').text() || '0');
      const link = $rss(element).find('link').text();
      
      if (filmTitle && filmYear && memberRating > 0) {
        const filmId = `${filmTitle}_${filmYear}`;
        
        // Skip duplicates (rewatches)
        if (seenFilms.has(filmId)) {
          return;
        }
        seenFilms.add(filmId);
        
        // ONLY include movies rated 3.5 stars (7/10) or higher - focus on what they LOVED
        if (memberRating >= 3.5) {
          const movie: Movie = {
            title: filmTitle,
            year: filmYear,
            rating: memberRating,
            letterboxd_url: link,
          };
          
          allRatedMovies.push(movie);
          
          // Consider 5-star ratings as "loved"
          if (memberRating === 5.0) {
            lovedMovies.push({ ...movie, loved: true });
          }
        }
      }
    });
    
    console.log(`✅ RSS feed scraped: ${allRatedMovies.length} rated movies (3.5+ stars), ${lovedMovies.length} loved (5 stars)`);
    
    return {
      username,
      total_films: totalFilms,
      films_this_year: filmsThisYear,
      loved_movies: lovedMovies,
      all_rated_movies: allRatedMovies, // Return all movies from RSS
    };
    
  } catch (error: any) {
    console.error('Error scraping Letterboxd:', error.message);
    throw new Error(`Failed to scrape Letterboxd profile: ${error.message}`);
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
    const { username } = JSON.parse(event.body || '{}');

    if (!username) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Username is required' }),
      };
    }

    console.log(`🎬 Scraping Letterboxd profile for: ${username}`);

    const profileData = await scrapeLetterboxdProfile(username);

    console.log(`✅ Successfully scraped profile`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: profileData,
      }),
    };

  } catch (error: any) {
    console.error('Function error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to scrape profile',
      }),
    };
  }
};
