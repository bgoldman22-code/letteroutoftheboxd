import { Handler } from '@netlify/functions';

interface Movie {
  title: string;
  year: string;
  rating?: number;
  genres?: string[];
  director?: string;
  imdb_rating?: string;
}

interface TasteProfile {
  top_genres: string[];
  favorite_directors: string[];
  top_themes: string[];
  preferred_decades: string[];
  avg_rating: number;
}

// Top 100 most-watched classics (assume cinephiles have seen these)
const ESSENTIAL_CLASSICS = [
  "The Shawshank Redemption", "The Godfather", "The Dark Knight", "Pulp Fiction",
  "Forrest Gump", "Inception", "Fight Club", "The Matrix", "Goodfellas",
  "The Silence of the Lambs", "Schindler's List", "The Lord of the Rings: The Return of the King",
  "Se7en", "The Usual Suspects", "Léon: The Professional", "The Prestige",
  "Memento", "Casablanca", "Citizen Kane", "Psycho", "Vertigo", "Rear Window",
  "12 Angry Men", "Apocalypse Now", "A Clockwork Orange", "Taxi Driver",
  "Blade Runner", "2001: A Space Odyssey", "Alien", "The Shining"
];

// Recent cultural phenomena (most film fans have seen)
const RECENT_ZEITGEIST = [
  "Everything Everywhere All at Once", "Oppenheimer", "Barbie", "Parasite",
  "Get Out", "Joker", "Knives Out", "Dune", "Dune: Part Two", "Spider-Man: No Way Home",
  "Top Gun: Maverick", "Avatar: The Way of Water", "No Time to Die"
];

// Director filmographies (if user likes a director, they've likely seen their major works)
const DIRECTOR_FILMOGRAPHIES: { [key: string]: string[] } = {
  "Christopher Nolan": ["The Dark Knight", "Inception", "Interstellar", "Dunkirk", "Tenet", "Oppenheimer", "The Prestige", "Memento"],
  "Denis Villeneuve": ["Blade Runner 2049", "Arrival", "Dune", "Dune: Part Two", "Sicario", "Prisoners", "Enemy"],
  "David Fincher": ["Se7en", "Fight Club", "Gone Girl", "The Social Network", "Zodiac", "The Girl with the Dragon Tattoo"],
  "Quentin Tarantino": ["Pulp Fiction", "Kill Bill", "Inglourious Basterds", "Django Unchained", "Once Upon a Time in Hollywood"],
  "Martin Scorsese": ["Goodfellas", "Taxi Driver", "The Departed", "The Wolf of Wall Street", "The Irishman", "Killers of the Flower Moon"],
  "Paul Thomas Anderson": ["There Will Be Blood", "The Master", "Phantom Thread", "Boogie Nights", "Magnolia"],
  "Bong Joon Ho": ["Parasite", "Memories of Murder", "The Host", "Snowpiercer", "Okja"],
  "Yorgos Lanthimos": ["The Favourite", "Poor Things", "The Lobster", "The Killing of a Sacred Deer"],
  "Wes Anderson": ["The Grand Budapest Hotel", "Moonrise Kingdom", "The Royal Tenenbaums", "Fantastic Mr. Fox"],
  "Coen Brothers": ["No Country for Old Men", "Fargo", "The Big Lebowski", "True Grit", "Inside Llewyn Davis"],
};

// Franchise logic (if seen later, seen earlier)
const FRANCHISES: { [key: string]: string[] } = {
  "Dune: Part Two": ["Dune"],
  "The Lord of the Rings: The Return of the King": ["The Lord of the Rings: The Fellowship of the Ring", "The Lord of the Rings: The Two Towers"],
  "Blade Runner 2049": ["Blade Runner"],
  "Toy Story 3": ["Toy Story", "Toy Story 2"],
  "The Dark Knight": ["Batman Begins"],
  "The Dark Knight Rises": ["Batman Begins", "The Dark Knight"],
};

function buildExpandedExclusionList(
  userMovies: Movie[],
  tasteProfile: TasteProfile
): string[] {
  const exclusions = new Set<string>();

  // 1. Add all user's rated movies (exact matches)
  userMovies.forEach(m => {
    exclusions.add(m.title.toLowerCase());
  });

  // 2. Check if user is a cinephile (high avg rating, diverse classics)
  const isCinephile = tasteProfile.avg_rating >= 4.0 && userMovies.length >= 20;
  
  if (isCinephile) {
    // Assume they've seen essential classics
    ESSENTIAL_CLASSICS.forEach(title => exclusions.add(title.toLowerCase()));
    console.log(`📚 Cinephile detected (${tasteProfile.avg_rating}/5) - excluding ${ESSENTIAL_CLASSICS.length} essential classics`);
  }

  // 3. Recent cultural zeitgeist (if user is active, they've likely seen these)
  const hasRecentMovies = userMovies.some(m => {
    const year = parseInt(m.year);
    return year >= 2022;
  });
  
  if (hasRecentMovies) {
    RECENT_ZEITGEIST.forEach(title => exclusions.add(title.toLowerCase()));
    console.log(`🎬 Active filmgoer - excluding ${RECENT_ZEITGEIST.length} recent zeitgeist films`);
  }

  // 4. Director filmographies (if user likes a director, exclude their major works)
  tasteProfile.favorite_directors.forEach(director => {
    const filmography = DIRECTOR_FILMOGRAPHIES[director];
    if (filmography) {
      filmography.forEach(title => exclusions.add(title.toLowerCase()));
      console.log(`🎥 Favorite director: ${director} - excluding ${filmography.length} films`);
    }
  });

  // 5. Franchise logic (if seen sequel, exclude prequels)
  userMovies.forEach(m => {
    const prequels = FRANCHISES[m.title];
    if (prequels) {
      prequels.forEach(title => exclusions.add(title.toLowerCase()));
      console.log(`🎞️ Franchise detected: ${m.title} - excluding ${prequels.length} earlier films`);
    }
  });

  // 6. Genre-specific popular films
  tasteProfile.top_genres.forEach(genre => {
    const genreCount = userMovies.filter(m => 
      m.genres?.some(g => g.toLowerCase() === genre.toLowerCase())
    ).length;
    
    // If user has rated 10+ films in a genre, they're deep into it
    if (genreCount >= 10) {
      console.log(`🎭 Deep into ${genre} (${genreCount} films) - will request obscure recommendations`);
      // Note: We'll tell GPT about this in the prompt, not exclude specific titles
    }
  });

  const exclusionArray = Array.from(exclusions);
  console.log(`🚫 Total exclusions: ${exclusionArray.length} films`);
  
  return exclusionArray;
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
    const { user_movies, taste_profile } = JSON.parse(event.body || '{}');

    if (!user_movies || !taste_profile) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'user_movies and taste_profile required' }),
      };
    }

    console.log(`🧠 Building smart exclusion list for user with ${user_movies.length} rated movies`);
    
    const exclusionList = buildExpandedExclusionList(user_movies, taste_profile);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: {
          exclusions: exclusionList,
          stats: {
            user_rated: user_movies.length,
            total_excluded: exclusionList.length,
            expansion_ratio: (exclusionList.length / user_movies.length).toFixed(1),
          },
        },
      }),
    };

  } catch (error: any) {
    console.error('Exclusion builder error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to build exclusion list',
      }),
    };
  }
};
