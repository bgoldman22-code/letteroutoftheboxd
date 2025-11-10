# NEW AI-POWERED RECOMMENDATION FLOW

Replace Steps 4-5 in page.tsx with this:

```typescript
      console.log(`📊 Formatted ${analyzedMoviesArray.length} movies for recommendations`);

      // Extract taste profile from analyzed movies
      const tasteProfile = {
        top_genres: Array.from(new Set(analyzedMoviesArray.flatMap(m => m.genres || []))).slice(0, 5),
        favorite_directors: Array.from(new Set(analyzedMoviesArray.map(m => m.director).filter(Boolean))),
        top_themes: Array.from(new Set(analyzedMoviesArray.flatMap(m => 
          m.elite_analysis?.human_condition_themes || []
        ))).slice(0, 5),
        preferred_decades: Array.from(new Set(analyzedMoviesArray.map(m => {
          const year = parseInt(m.year);
          return isNaN(year) ? null : `${Math.floor(year / 10) * 10}s`;
        }).filter(Boolean))),
        avg_rating: analyzedMoviesArray.reduce((sum, m) => sum + (m.rating || 4), 0) / analyzedMoviesArray.length,
        loved_movies_count: analyzedMoviesArray.filter(m => m.loved).length,
      };

      console.log(`🎯 Taste Profile: ${tasteProfile.top_genres.join(', ')} | ${tasteProfile.favorite_directors.length} directors`);

      // Step 4: Build smart exclusion list
      setLoadingStep('Analyzing your viewing history...');
      console.log('🎬 Step 4/6: Building smart exclusion list...');
      
      const exclusionResponse = await fetch('/.netlify/functions/build-exclusion-list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_movies: enrichedMovies, // All scraped movies
          taste_profile: tasteProfile,
        }),
      });

      if (!exclusionResponse.ok) {
        throw new Error('Failed to build exclusion list');
      }

      const exclusionData = await exclusionResponse.json();
      const exclusions = exclusionData.data.exclusions;
      console.log(`🚫 Excluding ${exclusions.length} films (${exclusionData.data.stats.expansion_ratio}x user's rated movies)`);

      // Step 5: Get AI-powered recommendations
      setLoadingStep('Discovering perfect films for you with AI...');
      console.log('🎬 Step 5/6: Getting AI recommendations...');
      
      const aiRecsResponse = await fetch('/.netlify/functions/fetch-ai-recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          taste_profile: tasteProfile,
          exclusions: exclusions,
          count: 50, // Request 50 to ensure variety
        }),
      });

      if (!aiRecsResponse.ok) {
        throw new Error('Failed to get AI recommendations');
      }

      const aiRecsData = await aiRecsResponse.json();
      const aiRecommendations = aiRecsData.data.recommendations;
      console.log(`🤖 AI suggested ${aiRecommendations.length} films`);

      // Step 6: Enrich AI recommendations with OMDb metadata
      setLoadingStep('Enriching recommendations with details...');
      console.log('🎬 Step 6/6: Enriching with OMDb...');

      // Enrich first 30 for initial display
      const enrichResponse = await fetch('/.netlify/functions/enrich-movies', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          movies: aiRecommendations.slice(0, 30),
        }),
      });

      if (!enrichResponse.ok) {
        throw new Error('Failed to enrich recommendations');
      }

      const enrichData = await enrichResponse.json();
      const enrichedCandidates = enrichData.data;
      console.log(`✅ Enriched ${enrichedCandidates.length} recommendations`);

      // Step 7: Match enriched candidates to taste profile
      setLoadingStep('Generating your personalized recommendations...');
      console.log('🎬 Step 7/7: Matching to your taste profile...');
      
      const recsResponse = await fetch('/.netlify/functions/get-simple-recommendations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_movies: analyzedMoviesArray,
          candidate_movies: enrichedCandidates, // AI-recommended, OMDb-enriched films!
        }),
      });
```

## What This Does

1. **Builds Taste Profile** from 6 analyzed movies (genres, directors, themes, decades, rating)
2. **Smart Exclusions** - Expands ~34 rated movies to ~100-150 likely-seen films
3. **AI Recommendations** - GPT-4o-mini suggests 50 films matching taste profile
4. **OMDb Enrichment** - First 30 get posters, plots, ratings, directors, actors
5. **Final Matching** - Scores enriched candidates against taste profile
6. **Display Top 15** with match scores and reasons

## Benefits

✅ **Intelligent Discovery** - AI understands nuance, not just genre matching
✅ **Smart Exclusions** - Won't recommend obvious films user has likely seen
✅ **Variety** - Different recommendations each time (temp=0.8)
✅ **Quality** - AI filters for critically acclaimed films
✅ **Fast** - GPT-4o-mini is 10x faster, 60x cheaper than GPT-4o
✅ **No External APIs** - Just OpenAI (already configured) + OMDb (already configured)

Ready to implement this in page.tsx?
