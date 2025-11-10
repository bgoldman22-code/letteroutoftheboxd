# Diversifying Letterboxd Scraping Strategy

## Current Problem
- RSS feed: Only returns ~50-100 most recent entries
- Result: Skewed toward recent watches, misses older favorites

## Letterboxd Data Sources

### 1. **RSS Feeds** (Current - Limited)
- `/{username}/rss/` - Recent activity (50-100 entries)
- ✅ Easy to parse
- ❌ Only recent, not comprehensive

### 2. **Direct Page Scraping** (More comprehensive)
- `/{username}/films/` - All rated films (paginated)
- `/{username}/films/rated/5/` - 5-star films
- `/{username}/films/rated/4.5/` - 4.5-star films
- `/{username}/films/decade/2020s/` - By decade
- `/{username}/films/genre/thriller/` - By genre

### 3. **Multiple RSS Endpoints** (Strategic sampling)
- Main feed: Recent activity
- Loved: `/{username}/films/rated/5/rss/`
- By rating: Different star levels
- Could provide better sampling

## Proposed Strategy: Multi-Source Sampling

```
1. Scrape 5-star films (ALL of them)
   → User's absolute favorites, any era
   
2. Scrape recent RSS (last 50)
   → Recent taste, current preferences
   
3. Scrape by rating tiers:
   - 4.5 stars (top 20)
   - 4 stars (top 20)
   → Mix of very good films across eras

4. Optional: Sample by decade
   - 2020s, 2010s, 2000s, 1990s
   → Ensure temporal diversity
```

## Implementation Options

### Option A: **Smart RSS Sampling** (Fast, Simple)
```
GET /{username}/films/rated/5/rss/     → All 5-star (loved)
GET /{username}/rss/                    → Recent 50
GET /{username}/films/rated/4.5/rss/   → High-rated classics
```
Combine + deduplicate → ~100-150 diverse films

### Option B: **Paginated Scraping** (Comprehensive, Slower)
```
GET /{username}/films/page/1/
GET /{username}/films/page/2/
... continue until have 200+ films
```
Parse HTML for ratings → Full profile

### Option C: **Hybrid** (Recommended)
```
1. GET all 5-star films (RSS or paginated)
2. GET recent 50 from main RSS
3. GET top-rated from each decade
4. Deduplicate → Target: 150-200 diverse films
```

## Quick Win: Use Multiple RSS Feeds

This requires NO HTML parsing (stays within RSS), just hit different endpoints:

```typescript
const rssSources = [
  `/${username}/rss/`,                    // Recent activity
  `/${username}/films/rated/5/rss/`,     // Loved films
  `/${username}/films/rated/4.5/rss/`,   // Near-loved
  `/${username}/films/decade/2020s/rss/`, // Recent favorites
  `/${username}/films/decade/2010s/rss/`, // 2010s favorites
];
```

Each RSS feed returns different slices → Combine for diversity!

**Should I implement Option C (Hybrid) for maximum diversity?**
