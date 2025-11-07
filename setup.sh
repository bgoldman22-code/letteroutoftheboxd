#!/bin/bash

# LetterOutOfTheBoxd - Setup Script
echo "🎬 Setting up LetterOutOfTheBoxd - Elite Movie Recommendation Tool"

# Check if .env.local exists
if [ ! -f .env.local ]; then
    echo "📄 Creating .env.local file..."
    cp .env.example .env.local
    echo "✅ Created .env.local - Please add your API keys!"
    echo ""
    echo "Required API keys:"
    echo "- OPENAI_API_KEY (get from https://platform.openai.com/api-keys)"
    echo "- TMDB_API_KEY (get from https://www.themoviedb.org/settings/api)" 
    echo "- OMDB_API_KEY (get from http://www.omdbapi.com/apikey.aspx)"
    echo ""
fi

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data
mkdir -p data/chroma_db
mkdir -p analysis

# Install Python dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    echo "🐍 Installing Python dependencies..."
    pip3 install -r requirements.txt
fi

# Check if this is a git repo
if [ ! -d .git ]; then
    echo "🔧 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - LetterOutOfTheBoxd setup"
    
    echo ""
    echo "🚀 Ready to connect to GitHub!"
    echo "Run these commands:"
    echo "git remote add origin https://github.com/bgoldman22-code/letteroutoftheboxd.git"
    echo "git branch -M main"  
    echo "git push -u origin main"
else
    echo "✅ Git repository already initialized"
fi

echo ""
echo "🎯 Next steps:"
echo "1. Add your API keys to .env.local"
echo "2. Push to GitHub: git push origin main"
echo "3. Deploy to Vercel: connect your GitHub repo"
echo "4. Test the scraper: npm run scrape"
echo "5. Try AI analysis: npm run ai-analyze"
echo ""
echo "🎬 Your elite movie recommendation tool is ready!"