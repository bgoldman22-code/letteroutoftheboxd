'use client';

import { useState } from 'react';
// import RecommendationMap from '@/components/RecommendationMap';

interface Movie {
  title: string;
  year?: string;
  rating?: number;
  similarity_score?: number;
  dimensional_match?: number;
  thematic_match?: number;
  match_reasons?: string[];
  core_essence?: string;
  aesthetic_signature?: string;
}

interface RecommendationData {
  recommendations: Movie[];
  taste_profile?: any;
  recommendation_map?: any;
}

export default function Home() {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState('');
  const [error, setError] = useState('');
  const [recommendations, setRecommendations] = useState<RecommendationData | null>(null);

  const handleAnalyze = async () => {
    if (!username.trim()) {
      setError('Please enter a Letterboxd username');
      return;
    }

    setLoading(true);
    setError('');
    setRecommendations(null);

    try {
      // Step 1: Scrape Letterboxd profile
      setLoadingStep('Scraping Letterboxd profile...');
      console.log('🎬 Step 1/4: Scraping Letterboxd profile...');
      const profileResponse = await fetch('/.netlify/functions/analyze-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });

      if (!profileResponse.ok) {
        let errorMessage = 'Failed to scrape profile';
        try {
          const errorData = await profileResponse.json();
          errorMessage = errorData.error || errorMessage;
        } catch (e) {
          errorMessage = `HTTP ${profileResponse.status}: ${profileResponse.statusText}`;
        }
        throw new Error(errorMessage);
      }

      let profileData;
      try {
        const responseData = await profileResponse.json();
        profileData = responseData.data;
      } catch (e) {
        throw new Error('Invalid response from profile scraper. The response may be too large or incomplete.');
      }
      console.log(`✅ Profile scraped: ${profileData.all_rated_movies.length} rated movies, ${profileData.loved_movies.length} loved`);

      // Step 2: Enrich movies with OMDb data
      setLoadingStep(`Enriching ${profileData.all_rated_movies.length} movies with OMDb data...`);
      console.log('🎬 Step 2/4: Enriching movies with OMDb data...');
      const enrichResponse = await fetch('/.netlify/functions/enrich-movies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movies: profileData.all_rated_movies }),
      });

      if (!enrichResponse.ok) {
        let errorMessage = 'Failed to enrich movies';
        try {
          const errorData = await enrichResponse.json();
          errorMessage = errorData.error || errorMessage;
        } catch (e) {
          errorMessage = `HTTP ${enrichResponse.status}: ${enrichResponse.statusText}`;
        }
        throw new Error(errorMessage);
      }

      let enrichedMovies;
      try {
        const responseData = await enrichResponse.json();
        enrichedMovies = responseData.data;
      } catch (e) {
        throw new Error('Invalid response from movie enrichment. The response may be too large or incomplete.');
      }
      console.log(`✅ Enriched ${enrichedMovies.length} movies`);

      // Step 3: Analyze movies with 62-dimension AI model in batches
      console.log('🎬 Step 3/4: Analyzing with Elite 62-Dimension Model (processing in batches)...');
      const allAnalyzedMovies = [];
      const batchSize = 10; // Process 10 movies per batch (fits in 26s timeout on paid plan)
      const totalBatches = Math.ceil(enrichedMovies.length / batchSize);
      
      for (let batch = 0; batch < totalBatches; batch++) {
        const start = batch * batchSize;
        const end = Math.min(start + batchSize, enrichedMovies.length);
        const batchMovies = enrichedMovies.slice(start, end);
        
        setLoadingStep(`Analyzing movies ${start + 1}-${end} of ${enrichedMovies.length} (batch ${batch + 1}/${totalBatches})...`);
        console.log(`📦 Batch ${batch + 1}/${totalBatches}: Analyzing movies ${start + 1}-${end}`);
        
        const analyzeResponse = await fetch('/.netlify/functions/analyze-movie', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ movies: batchMovies }),
        });

        if (!analyzeResponse.ok) {
          let errorMessage = 'Failed to analyze movies';
          try {
            const errorData = await analyzeResponse.json();
            errorMessage = errorData.error || errorMessage;
          } catch (e) {
            errorMessage = `HTTP ${analyzeResponse.status}: ${analyzeResponse.statusText}`;
          }
          throw new Error(errorMessage);
        }

        let batchResult;
        try {
          const responseData = await analyzeResponse.json();
          batchResult = responseData.data;
        } catch (e) {
          throw new Error('Invalid response from AI analysis. The response may be too large or incomplete.');
        }
        
        allAnalyzedMovies.push(...batchResult);
        console.log(`✅ Batch ${batch + 1}/${totalBatches} complete: ${batchResult.length} movies analyzed`);
        
        // Small delay between batches to be respectful to APIs
        if (batch < totalBatches - 1) {
          await new Promise(resolve => setTimeout(resolve, 1000));
        }
      }
      
      console.log(`✅ Analyzed ${allAnalyzedMovies.length} movies with 62 dimensions`);
      const analyzedMovies = allAnalyzedMovies;

      // Step 4: Generate recommendations
      setLoadingStep('Generating personalized recommendations...');
      console.log('🎬 Step 4/4: Generating personalized recommendations...');
      
      // For now, use the same movies as candidates (in production, fetch a larger candidate pool)
      const recsResponse = await fetch('/.netlify/functions/get-recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_movies: analyzedMovies,
          candidate_movies: analyzedMovies, // TODO: Use larger pool in production
        }),
      });

      if (!recsResponse.ok) {
        let errorMessage = 'Failed to generate recommendations';
        try {
          const errorData = await recsResponse.json();
          errorMessage = errorData.error || errorMessage;
        } catch (e) {
          errorMessage = `HTTP ${recsResponse.status}: ${recsResponse.statusText}`;
        }
        throw new Error(errorMessage);
      }

      let recsData;
      try {
        const responseData = await recsResponse.json();
        recsData = responseData.data;
      } catch (e) {
        throw new Error('Invalid response from recommendation engine. The response may be too large or incomplete.');
      }
      console.log(`✅ Generated ${recsData.recommendations.length} recommendations`);

      // Format data for display
      setRecommendations({
        recommendations: recsData.recommendations.map((rec: any) => ({
          title: rec.title,
          year: rec.year,
          similarity_score: rec.similarity_score,
          dimensional_match: rec.dimensional_match,
          thematic_match: rec.thematic_match,
          match_reasons: rec.match_reasons,
          core_essence: rec.elite_analysis.core_essence,
          aesthetic_signature: rec.elite_analysis.aesthetic_signature,
        })),
        taste_profile: {
          top_themes: recsData.taste_fingerprint.top_themes,
          avg_rating: recsData.taste_fingerprint.avg_rating,
          loved_movies_count: recsData.taste_fingerprint.loved_movies_count,
        },
      });

    } catch (err: any) {
      console.error('Error:', err);
      setError(err.message || 'An error occurred while analyzing your profile.');
    } finally {
      setLoading(false);
      setLoadingStep('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900 text-white">
      <div className="container mx-auto px-4 py-16">
        {/* Hero Section */}
        <div className="text-center mb-16">
          <h1 className="text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">
            LetterOutOfTheBoxd
          </h1>
          <p className="text-2xl text-gray-300 mb-2">
            Elite Movie Recommendations
          </p>
          <p className="text-lg text-gray-400">
            Powered by 62-Dimension Cinematic Taste Model
          </p>
        </div>

        {/* Input Section */}
        <div className="max-w-2xl mx-auto mb-12">
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
            <label className="block text-sm font-medium mb-3 text-gray-300">
              Enter Your Letterboxd Username
            </label>
            <div className="flex gap-3">
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAnalyze()}
                placeholder="e.g., username"
                className="flex-1 px-4 py-3 rounded-lg bg-white/5 border border-white/20 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
                disabled={loading}
              />
              <button
                onClick={handleAnalyze}
                disabled={loading}
                className="px-8 py-3 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg font-semibold hover:from-purple-600 hover:to-pink-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
              >
                {loading ? '🎬 Analyzing...' : '🎯 Analyze'}
              </button>
            </div>
            
            {/* Status Note */}
            <div className="mt-4 p-4 bg-green-500/20 border border-green-500/30 rounded-lg">
              <p className="text-sm text-green-200">
                <strong>✅ Fully Operational:</strong> All systems running! The 62-dimension Elite Cinematic Taste Model is analyzing movies in real-time using OpenAI GPT-4o.
              </p>
            </div>

            {error && (
              <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
                ❌ {error}
              </div>
            )}

            {loading && (
              <div className="mt-4 text-center">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
                <p className="mt-2 text-gray-300">
                  {loadingStep || 'Analyzing your cinematic taste profile...'}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Results Section */}
        {recommendations && (
          <div className="space-y-8">
            {/* Taste Profile Summary */}
            {recommendations.taste_profile && (
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
                <h2 className="text-3xl font-bold mb-6 text-purple-300">
                  🎨 Your Cinematic Taste Profile
                </h2>
                <div className="grid md:grid-cols-3 gap-6">
                  <div>
                    <h3 className="font-semibold text-gray-300 mb-2">Top Themes</h3>
                    <ul className="space-y-1">
                      {recommendations.taste_profile.top_themes?.slice(0, 5).map((theme: string, i: number) => (
                        <li key={i} className="text-purple-200">• {theme}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-300 mb-2">Average Rating</h3>
                    <p className="text-2xl font-bold text-pink-300">
                      {recommendations.taste_profile.avg_rating?.toFixed(1)} / 5.0
                    </p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-300 mb-2">Loved Movies</h3>
                    <p className="text-2xl font-bold text-blue-300">
                      {recommendations.taste_profile.loved_movies_count}
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Recommendation Visualization */}
            {/* Temporarily disabled for deployment */}
            {/* {recommendations.recommendation_map && (
              <RecommendationMap 
                movies={recommendations.recommendation_map.nodes || []}
                connections={recommendations.recommendation_map.links || []}
                centerMovie={username}
              />
            )} */}

            {/* Recommendation List */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl">
              <h2 className="text-3xl font-bold mb-6 text-purple-300">
                🎯 Your Elite Recommendations
              </h2>
              <div className="space-y-4">
                {recommendations.recommendations?.map((movie: Movie, i: number) => (
                  <div
                    key={i}
                    className="bg-white/5 rounded-lg p-6 border border-white/10 hover:border-purple-500/50 transition-all"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-xl mb-1">{movie.title}</h3>
                        {movie.year && <p className="text-sm text-gray-400">{movie.year}</p>}
                      </div>
                      {movie.similarity_score && (
                        <div className="text-right">
                          <div className="text-2xl font-bold text-purple-400">
                            {Math.round(movie.similarity_score * 100)}%
                          </div>
                          <div className="text-xs text-gray-400">Match</div>
                        </div>
                      )}
                    </div>

                    {/* Match breakdown */}
                    {(movie.dimensional_match || movie.thematic_match) && (
                      <div className="flex gap-4 mb-3">
                        {movie.dimensional_match && (
                          <div className="flex-1">
                            <div className="text-xs text-gray-400 mb-1">Dimensional</div>
                            <div className="bg-gray-700 rounded-full h-2">
                              <div
                                className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full"
                                style={{ width: `${movie.dimensional_match * 100}%` }}
                              />
                            </div>
                          </div>
                        )}
                        {movie.thematic_match && (
                          <div className="flex-1">
                            <div className="text-xs text-gray-400 mb-1">Thematic</div>
                            <div className="bg-gray-700 rounded-full h-2">
                              <div
                                className="bg-gradient-to-r from-pink-500 to-purple-500 h-2 rounded-full"
                                style={{ width: `${movie.thematic_match * 100}%` }}
                              />
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Match reasons */}
                    {movie.match_reasons && movie.match_reasons.length > 0 && (
                      <div className="mb-3">
                        <div className="text-xs text-gray-400 mb-2">Why this matches:</div>
                        <ul className="space-y-1">
                          {movie.match_reasons.map((reason, idx) => (
                            <li key={idx} className="text-sm text-purple-200">
                              • {reason}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Core essence */}
                    {movie.core_essence && (
                      <p className="text-sm text-gray-300 italic border-l-2 border-purple-500/30 pl-3">
                        {movie.core_essence}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
