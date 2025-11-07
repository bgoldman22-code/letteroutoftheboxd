'use client';

import { useState } from 'react';
// import RecommendationMap from '@/components/RecommendationMap';

interface Movie {
  title: string;
  year?: string;
  rating?: number;
  similarity_score?: number;
}

interface RecommendationData {
  recommendations: Movie[];
  taste_profile?: any;
  recommendation_map?: any;
}

export default function Home() {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
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
      // Step 1: Analyze profile
      console.log('🎬 Analyzing profile...');
      const analyzeResponse = await fetch('/api/analyze-profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username }),
      });

      if (!analyzeResponse.ok) {
        throw new Error('Failed to analyze profile');
      }

      const profileData = await analyzeResponse.json();
      console.log('✅ Profile analyzed:', profileData);

      // Step 2: Get recommendations
      console.log('🎯 Generating recommendations...');
      const recsResponse = await fetch('/api/get-recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          username,
          numRecommendations: 20,
          diversityFactor: 0.3,
        }),
      });

      if (!recsResponse.ok) {
        throw new Error('Failed to generate recommendations');
      }

      const recsData = await recsResponse.json();
      console.log('✅ Recommendations generated:', recsData);

      setRecommendations(recsData.data);

    } catch (err: any) {
      console.error('Error:', err);
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
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
            
            {error && (
              <div className="mt-4 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
                ❌ {error}
              </div>
            )}

            {loading && (
              <div className="mt-4 text-center">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-purple-500"></div>
                <p className="mt-2 text-gray-300">
                  Analyzing your cinematic taste profile...
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
                    <h3 className="font-semibold text-gray-300 mb-2">Top Genres</h3>
                    <ul className="space-y-1">
                      {recommendations.taste_profile.top_genres?.slice(0, 5).map((genre: string, i: number) => (
                        <li key={i} className="text-purple-200">• {genre}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-300 mb-2">Key Themes</h3>
                    <ul className="space-y-1">
                      {recommendations.taste_profile.top_themes?.slice(0, 5).map((theme: string, i: number) => (
                        <li key={i} className="text-pink-200">• {theme}</li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-300 mb-2">Favorite Directors</h3>
                    <ul className="space-y-1">
                      {recommendations.taste_profile.top_directors?.slice(0, 5).map((director: string, i: number) => (
                        <li key={i} className="text-blue-200">• {director}</li>
                      ))}
                    </ul>
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
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {recommendations.recommendations?.map((movie: Movie, i: number) => (
                  <div
                    key={i}
                    className="bg-white/5 rounded-lg p-4 border border-white/10 hover:border-purple-500/50 transition-all"
                  >
                    <h3 className="font-semibold text-lg mb-1">{movie.title}</h3>
                    {movie.year && <p className="text-sm text-gray-400 mb-2">{movie.year}</p>}
                    {movie.similarity_score && (
                      <div className="flex items-center gap-2">
                        <div className="flex-1 bg-gray-700 rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full"
                            style={{ width: `${movie.similarity_score * 100}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-400">
                          {Math.round(movie.similarity_score * 100)}%
                        </span>
                      </div>
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
