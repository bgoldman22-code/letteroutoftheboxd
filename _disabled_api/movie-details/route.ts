import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const { title, year } = await request.json();

    if (!title) {
      return NextResponse.json(
        { error: 'Movie title is required' },
        { status: 400 }
      );
    }

    console.log(`🎬 Fetching 62-dimension analysis for: ${title} ${year ? `(${year})` : ''}`);

    // Execute Python script to get movie details with 62-dimension analysis
    const scriptPath = path.join(process.cwd(), 'scripts', 'ai_movie_analyzer.py');
    
    // Create a simple Python command that calls the analyzer
    const pythonCode = `
import sys
sys.path.append('${process.cwd()}/scripts')
from ai_movie_analyzer import AIMovieAnalyzer
from multi_api_movie_service import MultiAPIMovieService
import json

movie_service = MultiAPIMovieService()
analyzer = AIMovieAnalyzer()

# Get movie data
movie_data = movie_service.get_movie_data("${title.replace(/"/g, '\\"')}")
if not movie_data:
    print(json.dumps({"error": "Movie not found"}))
    sys.exit(1)

# Analyze with 62-dimension model
analysis = analyzer.analyze_and_store_movie(
    title=movie_data.get('title'),
    movie_data=movie_data
)

# Output results
result = {
    "movie": movie_data,
    "analysis": analysis,
    "dimensional_scores": analysis.get('dimensional_scores', {}),
    "core_essence": analysis.get('core_essence', ''),
    "viewer_resonance": analysis.get('viewer_resonance', ''),
    "aesthetic_signature": analysis.get('aesthetic_signature', ''),
    "human_condition_themes": analysis.get('human_condition_themes', [])
}
print(json.dumps(result))
`;

    const { stdout, stderr } = await execAsync(`python3 -c ${JSON.stringify(pythonCode)}`, {
      cwd: process.cwd(),
      env: { ...process.env },
      maxBuffer: 10 * 1024 * 1024,
      timeout: 60000, // 60 second timeout
    });

    if (stderr && !stderr.includes('INFO:')) {
      console.error('Python stderr:', stderr);
    }

    // Parse the JSON output
    let movieDetails;
    try {
      const jsonMatch = stdout.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        movieDetails = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('No valid JSON found in script output');
      }
    } catch (parseError) {
      console.error('Failed to parse Python output:', stdout);
      throw parseError;
    }

    if (movieDetails.error) {
      return NextResponse.json(
        { error: movieDetails.error },
        { status: 404 }
      );
    }

    return NextResponse.json({
      success: true,
      data: movieDetails,
      message: `Successfully analyzed ${title}`,
    });

  } catch (error: any) {
    console.error('Error fetching movie details:', error);
    return NextResponse.json(
      {
        error: 'Failed to fetch movie details',
        details: error.message,
      },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title');
  const year = searchParams.get('year');

  if (!title) {
    return NextResponse.json({
      message: 'Use GET with ?title=MovieTitle or POST with { "title": "MovieTitle" }',
      endpoint: '/api/movie-details',
      methods: ['GET', 'POST'],
    });
  }

  // Forward to POST handler
  return POST(
    new NextRequest(request.url, {
      method: 'POST',
      body: JSON.stringify({ title, year }),
    })
  );
}
