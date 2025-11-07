# Vercel Python API Configuration

Your current architecture uses Node.js API routes that call Python scripts via `exec()`. 
This won't work in Vercel's serverless environment.

## Solution: Convert API Routes to Python

Vercel supports Python serverless functions. Here's the migration plan:

### Step 1: Create `/api` folder with Python files

Move your Python scripts to work as Vercel functions:

```
/api/
  analyze_profile.py       (instead of src/app/api/analyze-profile/route.ts)
  get_recommendations.py   (instead of src/app/api/get-recommendations/route.ts)
  movie_details.py         (instead of src/app/api/movie-details/route.ts)
```

### Step 2: Update vercel.json

```json
{
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.9",
      "maxDuration": 60
    }
  },
  "env": {
    "OPENAI_API_KEY": "@openai-api-key",
    "OMDB_API_KEY": "@omdb-api-key",
    "WATCHMODE_API_KEY": "@watchmode-api-key"
  }
}
```

### Step 3: Python Requirements for Vercel

Create `/api/requirements.txt`:
```
openai==1.3.0
chromadb==0.4.18
requests==2.31.0
beautifulsoup4==4.12.2
numpy==1.24.3
python-dotenv==1.0.0
```

## Alternative: Hybrid Approach (Current Architecture)

If you want to keep TypeScript API routes calling Python:

### Option B: Deploy Python Backend Separately

1. Deploy Python scripts to a separate service (Railway, Render, Fly.io)
2. Keep Next.js frontend on Vercel
3. Frontend calls Python backend via HTTP

### Option C: Use Vercel Edge Functions + External Python API

1. Convert critical Python logic to JavaScript/TypeScript
2. Use external API for AI analysis (direct OpenAI calls from TypeScript)
3. Simplify architecture

## Recommendation for Right Now

**Quick MVP Deployment:**

1. Click "Deploy" as-is (it will build the frontend)
2. Frontend will be live at https://letteroutoftheboxd.vercel.app
3. API routes will fail initially (Python not available)
4. We'll fix API routes in post-deployment step

**Then:**
- Convert to Python API routes (Option A) - 30 mins
- OR deploy Python backend separately (Option B) - 1 hour
- OR simplify to pure TypeScript (Option C) - 2 hours

## What to Do Right Now

1. ✅ Set Environment Variables in Vercel UI
2. ✅ Click "Deploy" to get frontend live
3. ✅ We'll fix API integration after initial deployment

The frontend will be beautiful and functional (UI/UX), just without backend connectivity until we implement one of the solutions above.
