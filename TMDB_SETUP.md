# TMDb API Setup Guide

## Why TMDb?
The system was recommending your OWN movies back to you (movies from your Letterboxd profile). This is pointless! 

Now we fetch **external candidates from TMDb** - popular movies you likely haven't seen yet - and recommend those based on your taste profile.

## Get a FREE TMDb API Key

1. **Go to TMDb**: https://www.themoviedb.org/signup
2. **Create a free account**
3. **Go to Settings** → **API**: https://www.themoviedb.org/settings/api
4. **Request an API key** (choose "Developer" type)
5. **Copy your API Key** (v3 auth)

## Add to Netlify Environment

1. Go to: https://app.netlify.com/sites/letteroutoftheboxd/configuration/env
2. Click **"Add a variable"**
3. Key: `TMDB_API_KEY`
4. Value: `[paste your TMDb API key here]`
5. Click **"Save"**

## Deploy

Once the key is added, push and deploy:

```bash
git push
npx netlify deploy --prod
```

## What Will Happen

**OLD FLOW (BROKEN):**
1. Scrape your Letterboxd (~34 movies YOU rated)
2. Pick 6 movies
3. Recommend the other 28 BACK to you ❌ (pointless!)

**NEW FLOW (FIXED):**
1. Scrape your Letterboxd (~34 movies YOU rated)
2. Pick 6 movies
3. Analyze those 6 to build your taste profile ✅
4. Fetch 200+ popular movies from TMDb in your favorite genres ✅
5. Filter out movies you've already seen ✅
6. Recommend from EXTERNAL pool 🎉

This is the actual promise: **discover NEW movies you'll love based on your taste!**
