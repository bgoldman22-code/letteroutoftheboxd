import { NextRequest, NextResponse } from 'next/server';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

export async function POST(request: NextRequest) {
  try {
    const { username } = await request.json();

    if (!username) {
      return NextResponse.json(
        { error: 'Username is required' },
        { status: 400 }
      );
    }

    console.log(`🎬 Analyzing Letterboxd profile: ${username}`);

    // Execute Python script to analyze Letterboxd profile
    const scriptPath = path.join(process.cwd(), 'scripts', 'letterboxd_scraper.py');
    const pythonCommand = `python3 ${scriptPath} ${username}`;

    const { stdout, stderr } = await execAsync(pythonCommand, {
      cwd: process.cwd(),
      env: { ...process.env },
      maxBuffer: 10 * 1024 * 1024, // 10MB buffer for large outputs
    });

    if (stderr && !stderr.includes('INFO:')) {
      console.error('Python stderr:', stderr);
    }

    // Parse the JSON output from Python script
    let profileData;
    try {
      // Extract JSON from stdout (script should print JSON to stdout)
      const jsonMatch = stdout.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        profileData = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('No valid JSON found in script output');
      }
    } catch (parseError) {
      console.error('Failed to parse Python output:', stdout);
      throw parseError;
    }

    return NextResponse.json({
      success: true,
      data: profileData,
      message: `Successfully analyzed ${username}'s profile`,
    });

  } catch (error: any) {
    console.error('Error analyzing profile:', error);
    return NextResponse.json(
      {
        error: 'Failed to analyze profile',
        details: error.message,
      },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  return NextResponse.json({
    message: 'Use POST method with { "username": "letterboxd_username" }',
    endpoint: '/api/analyze-profile',
    method: 'POST',
  });
}
