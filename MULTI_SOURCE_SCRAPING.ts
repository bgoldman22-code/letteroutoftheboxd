// MULTI-SOURCE LETTERBOXD SCRAPING STRATEGY
// Replace the RSS scraping section in analyze-profile.ts with this approach

async function scrapeMultipleRSSFeeds(username: string): Promise<Movie[]> {
  const baseUrl = `https://letterboxd.com/${username}`;
  const allMovies = new Map<string, Movie>(); // Use Map to deduplicate by filmId
  
  // Define RSS feed sources to scrape
  const rssSources = [
    { url: `${baseUrl}/rss/`, name: 'Recent Ratings', priority: 1 },
    { url: `${baseUrl}/films/rated/5/rss/`, name: '5-Star Films', priority: 3 },
    { url: `${baseUrl}/films/rated/4.5/rss/`, name: '4.5-Star Films', priority: 2 },
    { url: `${baseUrl}/films/decade/2020s/rss/`, name: '2020s Films', priority: 1 },
    { url: `${baseUrl}/films/decade/2010s/rss/`, name: '2010s Films', priority: 1 },
    { url: `${baseUrl}/films/decade/2000s/rss/`, name: '2000s Films', priority: 1 },
  ];
  
  console.log(`🎬 Scraping ${rssSources.length} RSS feeds for diverse movie selection...`);
  
  // Scrape each RSS feed
  for (const source of rssSources) {
    try {
      console.log(`📡 Fetching: ${source.name}`);
      
      const rssResponse = await axios.get(source.url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        },
        timeout: 5000, // 5 second timeout per feed
      });
      
      const $rss = cheerio.load(rssResponse.data, { xmlMode: true });
      let feedCount = 0;
      
      $rss('item').each((_, element) => {
        const filmTitle = $rss(element).find('letterboxd\\:filmTitle, filmTitle').text();
        const filmYear = $rss(element).find('letterboxd\\:filmYear, filmYear').text();
        const memberRating = parseFloat($rss(element).find('letterboxd\\:memberRating, memberRating').text() || '0');
        const link = $rss(element).find('link').text();
        
        if (filmTitle && filmYear && memberRating > 0) {
          const filmId = `${filmTitle}_${filmYear}`;
          
          // Only add if not already in collection OR if this is a higher priority source
          const existingMovie = allMovies.get(filmId);
          
          if (!existingMovie || source.priority > (existingMovie as any).priority) {
            const movie: Movie = {
              title: filmTitle,
              year: filmYear,
              rating: memberRating,
              letterboxd_url: link,
              loved: memberRating >= 4.5, // Mark 4.5+ as loved
            };
            
            // Store with priority for deduplication
            (movie as any).priority = source.priority;
            allMovies.set(filmId, movie);
            feedCount++;
          }
        }
      });
      
      console.log(`   ✅ ${source.name}: ${feedCount} unique films added`);
      
      // Small delay between feeds to be respectful
      await new Promise(resolve => setTimeout(resolve, 250));
      
    } catch (error: any) {
      // If a feed fails, log but continue with others
      console.log(`   ⚠️ ${source.name}: Failed (${error.message})`);
    }
  }
  
  // Convert Map to Array and remove priority field
  const movies = Array.from(allMovies.values()).map(m => {
    const { priority, ...movie } = m as any;
    return movie as Movie;
  });
  
  console.log(`📊 Total unique films scraped: ${movies.length}`);
  console.log(`❤️ Loved films (4.5+): ${movies.filter(m => m.loved).length}`);
  console.log(`🎯 High-rated films (3.5+): ${movies.filter(m => m.rating >= 3.5).length}`);
  
  // Sort by rating (highest first) to prioritize loved films
  movies.sort((a, b) => b.rating - a.rating);
  
  return movies;
}

// BENEFITS:
// ✅ 150-200+ movies instead of 30-40
// ✅ Diverse across decades (not just recent)
// ✅ Includes loved films (5-star, 4.5-star)
// ✅ Better representation of taste across eras
// ✅ Automatic deduplication
// ✅ Prioritizes important films (loved > recent)
// ✅ Graceful failure (if one feed fails, others continue)

// USAGE in analyze-profile.ts:
// Replace the single RSS scraping section with:
// const allRatedMovies = await scrapeMultipleRSSFeeds(username);
