# Already-Seen Movie Filtering

## Problem
Recommendation systems that suggest movies users have already watched create poor user experience and waste API calls.

## Solution
The recommendation engine now accepts an optional `user_rated_movies` parameter that excludes all previously seen films from recommendations.

## Implementation

### Updated Function Signature
```python
def generate_recommendations(
    self, 
    user_loved_movies: List[Dict[str, Any]], 
    user_rated_movies: List[Dict[str, Any]] = None,  # NEW PARAMETER
    num_recommendations: int = 20,
    diversity_factor: float = 0.3
) -> Dict[str, Any]:
```

### How It Works

1. **Create Exclusion Set**: Generate slugs (normalized titles) for all rated movies
```python
excluded_slugs = {self._create_slug(m.get('title', '')) for m in user_rated_movies}
print(f"   Excluding {len(excluded_slugs)} already-seen movies")
```

2. **Filter During Candidate Generation**: Skip any candidate that matches exclusion set
```python
for candidate in similar:
    candidate_slug = self._create_slug(candidate.get('title', ''))
    if candidate_slug in excluded_slugs:
        continue  # Skip this movie
    all_candidates.append(candidate)
```

3. **Default Behavior**: If no `user_rated_movies` provided, defaults to `user_loved_movies`
```python
if user_rated_movies is None:
    user_rated_movies = user_loved_movies
```

## Usage Examples

### Example 1: Basic Usage (Only Exclude Loved Movies)
```python
engine = RecommendationEngine()

loved_movies = [
    {'title': 'The Dark Knight', 'rating': 5},
    {'title': 'Inception', 'rating': 5}
]

# Only loved movies are excluded
recommendations = engine.generate_recommendations(loved_movies)
```

### Example 2: Full Letterboxd Profile (Exclude Everything)
```python
# User has rated 500 movies total, loved 50
all_rated_movies = letterboxd_scraper.get_user_ratings(username='johndoe')
loved_movies = [m for m in all_rated_movies if m['rating'] >= 4]

# Exclude all 500 from recommendations
recommendations = engine.generate_recommendations(
    user_loved_movies=loved_movies,
    user_rated_movies=all_rated_movies  # Exclude everything they've seen
)
```

### Example 3: Strategic Exclusion
```python
# Only exclude movies rated 3+ stars (they've "seen enough" of these)
all_rated = get_all_ratings(user)
exclude_list = [m for m in all_rated if m['rating'] >= 3]

recommendations = engine.generate_recommendations(
    user_loved_movies=[m for m in all_rated if m['rating'] >= 4.5],
    user_rated_movies=exclude_list
)
```

## Benefits

✅ **No Duplicate Recommendations**: Never suggest movies user has already rated
✅ **Efficient**: Uses slug-based set lookups (O(1) performance)
✅ **Flexible**: Can exclude just loved movies or entire rating history
✅ **Better UX**: Users only see genuinely new recommendations

## Implementation Details

### Slug Creation
Normalizes titles for matching:
```python
def _create_slug(self, title: str) -> str:
    """Create normalized slug for title matching"""
    import re
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')
```

**Examples:**
- "The Dark Knight" → "the-dark-knight"
- "2001: A Space Odyssey" → "2001-a-space-odyssey"
- "Everything Everywhere All at Once" → "everything-everywhere-all-at-once"

### Console Output
```
🎯 Generating 20 elite recommendations...
   Based on 15 loved movies
   Excluding 287 already-seen movies

📊 Taste Profile:
   Top genres: ['Drama', 'Thriller', 'Sci-Fi']
   Top themes: ['identity', 'mortality', 'isolation']
   Favorite directors: ['Christopher Nolan', 'Denis Villeneuve', 'David Fincher']
```

## Edge Cases Handled

1. **No exclusion list**: Defaults to excluding loved movies only
2. **Empty exclusion list**: Works normally, no filtering applied
3. **Title variations**: Slug matching handles punctuation/spacing differences
4. **Duplicate titles**: Only one exclusion per slug (set deduplication)

## Performance Impact

- **Slug creation**: O(n) where n = number of rated movies
- **Lookup**: O(1) per candidate via set membership
- **Overall**: Negligible impact even with 1000+ rated movies

## Future Enhancements

Potential additions:
- [ ] Exclude by IMDb ID for perfect matching
- [ ] Partial exclusion (exclude 5-star but allow 2-star reconsideration)
- [ ] Time-based exclusion (only exclude movies watched in last N years)
- [ ] Director/actor exclusion lists
- [ ] Genre exclusion preferences

---

**Status**: ✅ Implemented and ready for use
**Version**: 1.0
**Date**: November 7, 2025
