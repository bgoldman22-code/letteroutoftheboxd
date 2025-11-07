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
    // Scrape profile page
    const profileResponse = await axios.get(baseUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
      },
    });
    
    const $ = cheerio.load(profileResponse.data);
    
    // Extract stats
    const stats = $('.profile-stats');
    const totalFilms = parseInt(stats.find('a[href$="/films/"] .value').text().replace(/,/g, '') || '0');
    const filmsThisYear = parseInt(stats.find('a[href$="/films/diary/this-year/"] .value').text().replace(/,/g, '') || '0');
    
    // Scrape loved movies (films they gave heart to)
    const lovedMovies: Movie[] = [];
    const lovedResponse = await axios.get(`${baseUrl}/likes/films/`, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
      },
    });
    
    const $loved = cheerio.load(lovedResponse.data);
    $loved('.poster-container').each((_, element) => {
      const filmSlug = $loved(element).find('div').attr('data-film-slug') || '';
      const filmName = $loved(element).find('img').attr('alt') || '';
      
      // Extract year from film name (usually in format "Title (Year)")
      const yearMatch = filmName.match(/\((\d{4})\)/);
      const year = yearMatch ? yearMatch[1] : '';
      const title = filmName.replace(/\s*\(\d{4}\)$/, '');
      
      lovedMovies.push({
        title,
        year,
        rating: 5, // Loved films are typically highly rated
        letterboxd_url: `https://letterboxd.com/film/${filmSlug}/`,
        loved: true,
      });
    });
    
    // Scrape rated films (more comprehensive list)
    const allRatedMovies: Movie[] = [];
    let page = 1;
    let hasMorePages = true;
    
    while (hasMorePages && page <= 5) { // Limit to 5 pages for performance
      const ratedUrl = `${baseUrl}/films/ratings/page/${page}/`;
      
      try {
        const ratedResponse = await axios.get(ratedUrl, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
          },
        });
        
        const $rated = cheerio.load(ratedResponse.data);
        const filmElements = $rated('.poster-container');
        
        if (filmElements.length === 0) {
          hasMorePages = false;
          break;
        }
        
        $rated('.poster-container').each((_, element) => {
          const filmSlug = $rated(element).find('div').attr('data-film-slug') || '';
          const filmName = $rated(element).find('img').attr('alt') || '';
          const ratingClass = $rated(element).find('.rating').attr('class') || '';
          
          // Extract rating from class (e.g., "rated-10" means 5 stars)
          const ratingMatch = ratingClass.match(/rated-(\d+)/);
          const ratingValue = ratingMatch ? parseInt(ratingMatch[1]) / 2 : 0;
          
          // Extract year
          const yearMatch = filmName.match(/\((\d{4})\)/);
          const year = yearMatch ? yearMatch[1] : '';
          const title = filmName.replace(/\s*\(\d{4}\)$/, '');
          
          if (title && year) {
            allRatedMovies.push({
              title,
              year,
              rating: ratingValue,
              letterboxd_url: `https://letterboxd.com/film/${filmSlug}/`,
              loved: lovedMovies.some(m => m.title === title && m.year === year),
            });
          }
        });
        
        page++;
        
        // Add delay to be respectful to Letterboxd servers
        await new Promise(resolve => setTimeout(resolve, 1000));
        
      } catch (error) {
        console.log(`No more pages at page ${page}`);
        hasMorePages = false;
      }
    }
    
    return {
      username,
      total_films: totalFilms,
      films_this_year: filmsThisYear,
      loved_movies: lovedMovies.slice(0, 50), // Limit to top 50
      all_rated_movies: allRatedMovies.slice(0, 200), // Limit to 200 for analysis
    };
    
  } catch (error: any) {
    console.error('Scraping error:', error.message);
    throw new Error(`Failed to scrape Letterboxd profile: ${error.message}`);
  }
}

export const handler: Handler = async (event) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json',
  };

  // Handle preflight
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

    console.log(`🎬 Scraping profile for: ${username}`);
    const profileData = await scrapeLetterboxdProfile(username);
    
    console.log(`✅ Scraped ${profileData.all_rated_movies.length} rated movies, ${profileData.loved_movies.length} loved`);

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
        error: error.message || 'Failed to analyze profile',
      }),
    };
  }
};
