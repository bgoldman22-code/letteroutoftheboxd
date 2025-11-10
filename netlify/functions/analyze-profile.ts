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
    
    // SIMPLIFIED MULTI-SOURCE SCRAPING
    // Letterboxd's filtered RSS feeds (by rating/decade) return 404s
    // Instead: Use main RSS feed + films page for broader coverage
    const rssFeeds = [
      { name: 'Recent Activity', url: `${baseUrl}/rss/`, minRating: 3.5 },
      { name: 'All Films Page 1', url: `${baseUrl}/films/page/1/`, minRating: 3.5, isHtml: true },
      { name: 'All Films Page 2', url: `${baseUrl}/films/page/2/`, minRating: 3.5, isHtml: true },
    ];
    
    const seenFilms = new Map<string, Movie>(); // Use Map to deduplicate by filmId
    const lovedMovies: Movie[] = [];
    
    for (const feed of rssFeeds) {
      try {
        console.log(`📡 Fetching ${feed.name}: ${feed.url}`);
        
        const response = await axios.get(feed.url, {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
          },
          timeout: 10000,
        });
        
        let feedCount = 0;
        
        if (feed.isHtml) {
          // Parse HTML film page
          const $html = cheerio.load(response.data);
          $html('li.poster-container').each((_, element) => {
            const filmLink = $html(element).find('div[data-film-slug]');
            const filmSlug = filmLink.attr('data-film-slug');
            const filmName = filmLink.attr('data-film-name');
            const ratingSpan = $html(element).find('span.rating');
            const ratingClass = ratingSpan.attr('class') || '';
            
            // Extract rating from class (e.g., "rated-10" = 5 stars, "rated-8" = 4 stars)
            const ratingMatch = ratingClass.match(/rated-(\d+)/);
            const memberRating = ratingMatch ? parseFloat(ratingMatch[1]) / 2 : 0;
            
            if (filmName && filmSlug && memberRating >= feed.minRating) {
              // Extract year from slug or film name
              const yearMatch = filmSlug.match(/-(\d{4})$/);
              const filmYear = yearMatch ? yearMatch[1] : '';
              
              const filmId = `${filmName}_${filmYear}`;
              
              if (!seenFilms.has(filmId)) {
                const movie: Movie = {
                  title: filmName,
                  year: filmYear,
                  rating: memberRating,
                  letterboxd_url: `https://letterboxd.com/film/${filmSlug}/`,
                };
                
                seenFilms.set(filmId, movie);
                feedCount++;
                
                if (memberRating === 5.0) {
                  lovedMovies.push({ ...movie, loved: true });
                }
              }
            }
          });
        } else {
          // Parse RSS feed
          const $rss = cheerio.load(response.data, { xmlMode: true });
          
          $rss('item').each((_, element) => {
            const filmTitle = $rss(element).find('letterboxd\\:filmTitle, filmTitle').text();
            const filmYear = $rss(element).find('letterboxd\\:filmYear, filmYear').text();
            const memberRating = parseFloat($rss(element).find('letterboxd\\:memberRating, memberRating').text() || '0');
            const link = $rss(element).find('link').text();
            
            if (filmTitle && filmYear && memberRating >= feed.minRating) {
              const filmId = `${filmTitle}_${filmYear}`;
              
              if (!seenFilms.has(filmId)) {
                const movie: Movie = {
                  title: filmTitle,
                  year: filmYear,
                  rating: memberRating,
                  letterboxd_url: link,
                };
                
                seenFilms.set(filmId, movie);
                feedCount++;
                
                if (memberRating === 5.0) {
                  lovedMovies.push({ ...movie, loved: true });
                }
              }
            }
          });
        }
        
        console.log(`   ✅ ${feed.name}: +${feedCount} unique films`);
        
        // Small delay between requests
        await new Promise(resolve => setTimeout(resolve, 300));
        
      } catch (error) {
        console.error(`   ❌ ${feed.name} failed:`, error instanceof Error ? error.message : 'Unknown error');
        // Continue with other feeds
      }
    }
    
    // Convert Map to sorted array (highest rated first)
    const allRatedMovies = Array.from(seenFilms.values()).sort((a, b) => b.rating - a.rating);
    
    console.log(`\n🎬 TOTAL SCRAPED: ${allRatedMovies.length} unique films (${lovedMovies.length} loved)`);

    
    return {
      username,
      total_films: totalFilms,
      films_this_year: filmsThisYear,
      loved_movies: lovedMovies,
      all_rated_movies: allRatedMovies,
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
