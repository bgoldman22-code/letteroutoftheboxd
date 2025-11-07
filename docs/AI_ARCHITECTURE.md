# Cost-Optimized AI Architecture

## **OpenAI + Free Resources Strategy**

### **Core Components (Cost-Effective)**

1. **Primary LLM**: OpenAI GPT-4o 
   - You already have credits ✅
   - ~$0.03 per 1K tokens (input), $0.06 per 1K tokens (output)
   - Estimated cost: $0.10-0.50 per recommendation session

2. **Embeddings**: OpenAI text-embedding-3-large
   - $0.00013 per 1K tokens
   - 3072 dimensions for rich similarity
   - Estimated cost: $0.01-0.05 per movie analysis

3. **Vector Database**: ChromaDB (100% Free)
   - Local storage - no monthly fees
   - Persistent storage in `./data/chroma_db`
   - Scales to millions of movies locally

4. **Movie Metadata**: Free APIs
   - **TMDB**: 1000 requests/day free
   - **OMDB**: 1000 requests/day free
   - **Letterboxd**: Public scraping (rate-limited)

### **Monthly Cost Estimate**

For moderate usage (100 users, 1000 movie analyses):
- **OpenAI GPT-4o**: $50-150/month
- **OpenAI Embeddings**: $10-30/month  
- **Vector Storage**: $0 (local ChromaDB)
- **Movie APIs**: $0 (free tiers)
- **Total**: $60-180/month

### **Scaling Strategy**

**Phase 1 (MVP)**: 
- Local ChromaDB
- 10K movie corpus
- Basic OpenAI integration

**Phase 2 (Growth)**:
- Upgrade to Weaviate Cloud (free tier)
- 100K movie corpus  
- Batch processing optimizations

**Phase 3 (Scale)**:
- Consider Qdrant Cloud ($20/month) 
- 1M+ movie corpus
- Advanced caching strategies

### **Free Alternatives If Needed**

- **LLM**: Ollama (local Llama models) - 100% free but lower quality
- **Embeddings**: HuggingFace sentence-transformers - free but less accurate
- **Vector DB**: ChromaDB local - always free

### **Implementation Files Created**

1. `scripts/ai_movie_analyzer.py` - Main AI analysis engine
2. `src/app/api/ai-recommendations/route.ts` - Next.js API integration
3. `.env.example` - Environment configuration
4. `setup.sh` - Automated setup script

### **Usage**

```bash
# Install dependencies
./setup.sh

# Add API keys to .env.local
OPENAI_API_KEY=your_key_here

# Test AI analysis
npm run ai-analyze

# Start development
npm run dev
```

This architecture gives you **elite-level movie curation** using primarily your existing OpenAI credits plus free resources. The total monthly cost scales with usage but remains very reasonable compared to enterprise solutions like Pinecone ($70+/month).