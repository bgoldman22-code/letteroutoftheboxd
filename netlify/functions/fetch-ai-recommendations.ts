import { Handler } from '@netlify/functions';
import OpenAI from 'openai';

interface TasteProfile {
  top_genres: string[];
  favorite_directors: string[];
  top_themes: string[];
  preferred_decades: string[];
  avg_rating: number;
  loved_movies_count: number;
}

interface RecommendedMovie {
  title: string;
  year: string;
}

async function getAIRecommendations(
  tasteProfile: TasteProfile,
  exclusions: string[],
  count: number = 50
): Promise<RecommendedMovie[]> {
  const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });

  const prompt = `You are an elite film curator with deep knowledge of cinema across all eras and genres.

Based on this user's cinematic taste profile:
- **Top Genres**: ${tasteProfile.top_genres.join(', ')}
- **Favorite Directors**: ${tasteProfile.favorite_directors.join(', ')}
- **Core Themes**: ${tasteProfile.top_themes.join(', ')}
- **Preferred Decades**: ${tasteProfile.preferred_decades.join(', ')}
- **Average Rating**: ${tasteProfile.avg_rating}/5.0 (${tasteProfile.avg_rating >= 4.3 ? 'highly selective' : tasteProfile.avg_rating >= 4.0 ? 'discerning' : 'open-minded'})

**Your Task**: Recommend exactly ${count} films that match this taste profile.

**Requirements**:
1. **EXCLUDE these films** (user has seen or likely seen): ${exclusions.slice(0, 50).join(', ')}${exclusions.length > 50 ? ` and ${exclusions.length - 50} more` : ''}
2. **Diversity**: Mix acclaimed classics (30%), recent gems (40%), and hidden masterpieces (30%)
3. **Quality**: Only films with critical acclaim or strong artistic merit
4. **Variety**: Different directors, eras, styles - not just variations of the same film
5. **Thematic alignment**: Match their core themes (${tasteProfile.top_themes.slice(0, 3).join(', ')})
6. **Smart depth**: If user loves a specific director, suggest their lesser-known works OR similar filmmakers

**Output Format** (JSON only, no markdown):
[
  {"title": "Exact Movie Title", "year": "YYYY"},
  ...
]

Return ONLY the JSON array, nothing else.`;

  console.log(`🤖 Asking GPT-4o-mini for ${count} recommendations...`);
  console.log(`🚫 Excluding ${exclusions.length} films`);

  const response = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      {
        role: 'system',
        content: 'You are an expert film curator. Always respond with valid JSON arrays only.',
      },
      {
        role: 'user',
        content: prompt,
      },
    ],
    temperature: 0.8, // Higher creativity for variety
    max_tokens: 2000,
  });

  const content = response.choices[0].message.content || '';
  
  // Strip markdown code blocks if present
  let jsonStr = content.trim();
  if (jsonStr.startsWith('```')) {
    jsonStr = jsonStr.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
  }

  try {
    const recommendations = JSON.parse(jsonStr);
    console.log(`✅ GPT returned ${recommendations.length} recommendations`);
    return recommendations;
  } catch (parseError) {
    console.error('JSON parse error:', parseError);
    console.error('Response content:', content);
    throw new Error('Failed to parse AI recommendations');
  }
}

export const handler: Handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json',
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  try {
    const { taste_profile, exclusions, count } = JSON.parse(event.body || '{}');

    if (!taste_profile) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'taste_profile is required' }),
      };
    }

    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({ error: 'OpenAI API key not configured' }),
      };
    }

    console.log(`🎬 Generating AI recommendations for user with taste profile:`);
    console.log(`   Genres: ${taste_profile.top_genres.join(', ')}`);
    console.log(`   Directors: ${taste_profile.favorite_directors.slice(0, 3).join(', ')}`);
    console.log(`   Avg Rating: ${taste_profile.avg_rating}/5`);

    const recommendations = await getAIRecommendations(
      taste_profile,
      exclusions || [],
      count || 50
    );

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: {
          recommendations,
          count: recommendations.length,
        },
      }),
    };

  } catch (error: any) {
    console.error('AI recommendation error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to generate AI recommendations',
      }),
    };
  }
};
