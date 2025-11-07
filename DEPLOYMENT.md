# LetterOutOfTheBoxd Deployment Guide

## 🚀 Quick Deploy to Vercel

### 1. Sign Up for Vercel
Go to: **https://vercel.com** and sign up with your GitHub account

### 2. Push to GitHub
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Elite Movie Recommendation Tool"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/YOUR_USERNAME/LetterOutOfTheBoxd.git

# Push
git push -u origin main
```

### 3. Deploy on Vercel
1. Go to https://vercel.com/new
2. Import your GitHub repository
3. Select "LetterOutOfTheBoxd"
4. Add Environment Variables:
   - `OPENAI_API_KEY` = your_openai_api_key
   - `OMDB_API_KEY` = trilogy (or get your own at omdbapi.com)
   - `WATCHMODE_API_KEY` = your_watchmode_api_key
   - `OPENAI_MODEL` = gpt-4o
   - `OPENAI_EMBEDDING_MODEL` = text-embedding-3-large
   - `NODE_ENV` = production
5. Click "Deploy"

### 4. Your App Will Be Live! 🎉
Vercel will give you a URL like: `https://letter-out-of-the-boxd.vercel.app`

---

## 📋 Environment Variables Needed

```bash
# Required
OPENAI_API_KEY=sk-proj-...your-key...

# Optional (have fallbacks)
OMDB_API_KEY=trilogy
WATCHMODE_API_KEY=your-key

# Configuration
OPENAI_MODEL=gpt-4o
OPENAI_EMBEDDING_MODEL=text-embedding-3-large
NODE_ENV=production
```

---

## 🔧 Local Development

```bash
# Install dependencies
npm install
pip3 install -r requirements.txt

# Run development server
npm run dev

# Test Python scripts
python3 scripts/multi_api_movie_service.py
python3 scripts/ai_movie_analyzer.py
python3 scripts/recommendation_engine.py
```

---

## 📦 What's Included

- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS
- **Backend**: Python AI analysis scripts
- **Database**: ChromaDB (vector database for similarity search)
- **APIs**: 
  - OpenAI (GPT-4o for analysis, embeddings for similarity)
  - OMDb (movie data)
  - Watchmode (streaming availability)
  - TasteDive (recommendations)
- **Visualization**: D3.js for interactive recommendation maps

---

## 🎯 Features

1. **Letterboxd Profile Scraping**: Extract user ratings and profiles
2. **AI Movie Analysis**: Deep analysis of themes, moods, visual styles
3. **Vector Similarity**: Find movies similar to user's favorites
4. **Elite Recommendations**: Personalized suggestions based on taste profile
5. **Interactive Map**: Visualize movie relationships and recommendations
6. **Export Capabilities**: Save recommendation lists

---

## 💰 Cost Breakdown (Monthly)

- **Vercel Hosting**: FREE (Hobby plan)
- **OpenAI API**: ~$5-20 depending on usage
- **ChromaDB**: FREE (local storage)
- **Movie APIs**: FREE (within limits)
- **Total**: ~$5-20/month

---

## 🐛 Troubleshooting

### Python scripts not working on Vercel
Vercel has limited Python support in serverless functions. For heavy Python processing:
1. Use Vercel for frontend only
2. Deploy Python backend to Railway.app or Heroku (free tiers available)
3. Or keep Python processing client-side (run locally, upload results)

### ChromaDB persistence
- ChromaDB data is stored locally in `data/chroma_db/`
- For production, consider:
  - Pinecone (free tier: 1 index, 100K vectors)
  - Weaviate Cloud (free tier available)
  - Or commit ChromaDB data to git (not recommended for large datasets)

---

## 📚 API Documentation

### `/api/scrape` - Scrape Letterboxd Profile
```typescript
POST /api/scrape
{
  "username": "letterboxd_username"
}
```

### `/api/analyze` - Analyze Movies with AI
```typescript
POST /api/analyze
{
  "movies": [{ title, year, director, ... }]
}
```

### `/api/ai-recommendations` - Get Recommendations
```typescript
POST /api/ai-recommendations
{
  "movies": [/* user's loved movies */],
  "username": "user"
}
```

---

## 🎬 Next Steps After Deployment

1. Test Letterboxd scraper with real profiles
2. Build more movie data (run analysis scripts)
3. Fine-tune recommendation algorithm
4. Add user authentication (optional)
5. Create shareable recommendation maps
6. Add export to PDF/image features

---

## 📄 License

MIT - Feel free to modify and use!

---

## 🙏 Credits

Built with:
- Next.js by Vercel
- OpenAI GPT-4
- ChromaDB
- D3.js
- Multiple free movie APIs
