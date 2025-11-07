import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import fs from 'fs/promises';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const { 
      username, 
      lovedMovies, 
      allRatedMovies,
      numRecommendations = 20,
      diversityFactor = 0.3 
    } = await request.json();

    if (!username && (!lovedMovies || lovedMovies.length === 0)) {
      return NextResponse.json(
        { error: 'Either username or lovedMovies array is required' },
        { status: 400 }
      );
    }

    console.log(`🎯 Generating recommendations for ${username || 'user'}`);

    // Create temporary input file for Python script
    const tempInputPath = path.join(process.cwd(), 'data', 'temp_recommendation_input.json');
    const inputData = {
      username,
      loved_movies: lovedMovies,
      all_rated_movies: allRatedMovies,
      num_recommendations: numRecommendations,
      diversity_factor: diversityFactor,
    };

    await fs.writeFile(tempInputPath, JSON.stringify(inputData, null, 2));

    // Execute Python recommendation engine via CLI wrapper
    const scriptPath = path.join(process.cwd(), 'scripts', 'cli_recommendation_engine.py');
    const pythonCommand = `python3 ${scriptPath} ${tempInputPath}`;

    const { stdout, stderr } = await execAsync(pythonCommand, {
      cwd: process.cwd(),
      env: { ...process.env },
      maxBuffer: 20 * 1024 * 1024, // 20MB buffer
      timeout: 120000, // 2 minute timeout
    });

    if (stderr && !stderr.includes('INFO:')) {
      console.error('Python stderr:', stderr);
    }

    // Parse the JSON output
    let recommendations;
    try {
      const jsonMatch = stdout.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        recommendations = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('No valid JSON found in script output');
      }
    } catch (parseError) {
      console.error('Failed to parse Python output:', stdout);
      throw parseError;
    }

    // Clean up temp file
    await fs.unlink(tempInputPath).catch(() => {});

    return NextResponse.json({
      success: true,
      data: recommendations,
      message: `Generated ${recommendations.recommendations?.length || 0} recommendations`,
    });

  } catch (error: any) {
    console.error('Error generating recommendations:', error);
    return NextResponse.json(
      {
        error: 'Failed to generate recommendations',
        details: error.message,
      },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  return NextResponse.json({
    message: 'Use POST method with recommendation parameters',
    endpoint: '/api/get-recommendations',
    method: 'POST',
    parameters: {
      username: 'string (optional if lovedMovies provided)',
      lovedMovies: 'array of movie objects (optional if username provided)',
      allRatedMovies: 'array of all rated movies for filtering (optional)',
      numRecommendations: 'number (default: 20)',
      diversityFactor: 'number 0-1 (default: 0.3)',
    },
  });
}
