# LetterOutOfTheBoxd 🎬

**Elite Movie Recommendation Tool** - Advanced analysis of Letterboxd user ratings with sophisticated recommendation mapping based on movie themes, moods, visual styles, directors, actors, and deep content analysis.

## 🌟 Features

- **Letterboxd Profile Analysis**: Scrape and analyze user ratings, reviews, and preferences
- **AI-Powered Movie Analysis**: Deep analysis of themes, moods, visual styles using LLMs
- **Interactive Recommendation Maps**: D3.js visualizations showing movie connections and relationships
- **Smart Filtering**: Recommendations based on cinematic style, narrative structure, and emotional resonance
- **Export Capabilities**: Export recommendation lists and analysis data

## 🚀 Tech Stack

- **Frontend**: Next.js 15 with TypeScript and Tailwind CSS
- **Visualization**: D3.js for interactive recommendation maps
- **Backend**: Node.js API routes for data processing
- **Data Analysis**: Python scripts for scraping and analysis
- **AI Integration**: OpenAI/Anthropic APIs for movie analysis and recommendations
- **Vector Storage**: Pinecone for similarity search and embeddings
- **Hosting**: Vercel (frontend), Railway/Render (API)

## 🛠️ Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd LetterOutOfTheBoxd
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   # Add your API keys for OpenAI, Anthropic, Pinecone, etc.
   ```

5. **Start the development server**
   ```bash
   npm run dev
   ```

6. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📊 AI Architecture

### Core Components

1. **Data Pipeline**
   - Letterboxd profile scraping
   - TMDb/OMDb API integration for movie metadata
   - AI-enhanced style and theme extraction

2. **Recommendation Engine**
   - Vector embeddings using OpenAI text-embedding-3-large
   - Semantic similarity search with Pinecone
   - LLM-powered curation with Claude Sonnet 3.5

3. **Visualization**
   - Interactive D3.js maps showing movie relationships
   - AI-assisted layout optimization
   - Real-time filtering and exploration

### LLM Integration

- **Movie Analysis**: Claude Sonnet for deep thematic and stylistic analysis
- **Recommendations**: GPT-4o for generating personalized suggestions
- **Explanations**: AI-generated reasoning for each recommendation
- **Visualization**: AI-optimized layouts and color schemes

## 🎯 Usage

1. **Enter a Letterboxd username** to analyze their movie preferences
2. **View the recommendation map** showing connections between movies
3. **Explore recommendations** with detailed explanations
4. **Filter by themes, moods, or styles** to find specific types of films
5. **Export your recommendations** for future reference

## 🔧 Scripts

### Development
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Data Processing
```bash
python scripts/letterboxd_scraper.py    # Scrape user profiles
python scripts/movie_analyzer.py        # Analyze movie data
```

## 🚀 Deployment

### Vercel (Recommended for Frontend)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Railway/Render (For API/Backend)
1. Create new service connected to GitHub
2. Configure environment variables
3. Set up automatic deployments

## 🤖 AI Integration Setup

### Required API Keys
- **OpenAI**: For embeddings and GPT-4o analysis
- **Anthropic**: For Claude Sonnet movie curation  
- **Pinecone**: For vector similarity search
- **TMDb**: For movie metadata

### Environment Variables
```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key  
PINECONE_API_KEY=your_pinecone_key
TMDB_API_KEY=your_tmdb_key
```

## 📈 Roadmap

### Phase 1: Core Features ✅
- [x] Basic Next.js setup with TypeScript
- [x] Letterboxd scraping infrastructure  
- [x] D3.js recommendation visualization
- [x] API routes for data processing

### Phase 2: AI Integration 🚧
- [ ] OpenAI embeddings integration
- [ ] Claude Sonnet analysis pipeline
- [ ] Pinecone vector storage setup
- [ ] LLM-powered recommendations

### Phase 3: Advanced Features 🎯
- [ ] Mood and style filters
- [ ] Cross-movie relationship analysis  
- [ ] Director/actor influence mapping
- [ ] Temporal trend analysis
- [ ] Social recommendation sharing

### Phase 4: Scale & Polish 🌟
- [ ] Performance optimization
- [ ] Mobile-responsive design
- [ ] User accounts and saved lists
- [ ] API rate limiting and caching
- [ ] Advanced visualization features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Letterboxd for the amazing platform and community
- The Movie Database (TMDb) for comprehensive movie data
- D3.js community for visualization inspiration
- OpenAI and Anthropic for AI capabilities

---

**Built with ❤️ for film enthusiasts who want recommendations that understand the art of cinema.**