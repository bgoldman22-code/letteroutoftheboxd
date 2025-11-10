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
    
    // Scrape ratings page to get MORE movies (up to 200)
    // Format: /username/films/by/member-rating/
    const ratingsUrl = `${baseUrl}/films/by/member-rating/`;
    const allRatedMovies: Movie[] = [];
    const lovedMovies: Movie[] = [];
    const seenFilms = new Set<string>();
    
    // Scrape first 3 pages to get ~150-200 movies
    for (let page = 1; page <= 3; page++) {
      const pageUrl = page === 1 ? ratingsUrl : `${ratingsUrl}page/${page}/`;
      console.log(`📄 Scraping page ${page}: ${pageUrl}`);
      
      try {
        const pageResponse = await axios.get(pageUrl, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
          },
        });
        
        const $page = cheerio.load(pageResponse.data);
        let moviesOnPage = 0;
        
        $page('.poster-container').each((_, element) => {
          const filmDiv = $page(element).find('.film-poster');
          const filmTitle = filmDiv.attr('data-film-name') || '';
          const filmSlug = filmDiv.attr('data-film-slug') || '';
          const filmYear = filmDiv.attr('data-film-release-year') || '';
          
          // Get rating from parent element
          const ratingSpan = $page(element).find('.rating');
          const ratingText = ratingSpan.attr('class') || '';
          const ratingMatch = ratingText.match(/rated-(\d+)/);
          const memberRating = ratingMatch ? parseInt(ratingMatch[1]) / 2 : 0; // Convert 1-10 to 0.5-5
          
          if (filmTitle && filmYear && memberRating >= 3.5) {
            const filmId = `${filmTitle}_${filmYear}`;
            
            if (!seenFilms.has(filmId)) {
              seenFilms.add(filmId);
              moviesOnPage++;
              
              const movie: Movie = {
                title: filmTitle,
                year: filmYear,
                rating: memberRating,
                letterboxd_url: `https://letterboxd.com/film/${filmSlug}/`,
              };
              
              allRatedMovies.push(movie);
              
              if (memberRating === 5.0) {
                lovedMovies.push({ ...movie, loved: true });
              }
            }
          }
        });
        
        console.log(`  ✅ Found ${moviesOnPage} rated movies on page ${page}`);
        
        // Stop if we got no movies (reached end of ratings)
        if (moviesOnPage === 0) break;
        
        // Small delay to be nice to Letterboxd servers
        await new Promise(resolve => setTimeout(resolve, 500));
        
      } catch (pageError: any) {
        console.error(`  ❌ Error scraping page ${page}:`, pageError.message);
        break;
      }
    }
    
    console.log(`✅ Total scraped: ${allRatedMovies.length} rated movies (3.5+ stars), ${lovedMovies.length} loved (5 stars)`);
    
    return {
      username,
      total_films: totalFilms,
      films_this_year: filmsThisYear,
      loved_movies: lovedMovies,
      all_rated_movies: allRatedMovies, // Return all for rounds system
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
