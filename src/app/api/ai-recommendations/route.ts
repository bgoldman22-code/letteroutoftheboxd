import { NextRequest, NextResponse } from 'next/server'
import { spawn } from 'child_process'
import path from 'path'

export async function POST(request: NextRequest) {
  try {
    const { movies, username, lovedMoviesOnly = true } = await request.json()
    
    if (!movies || !Array.isArray(movies)) {
      return NextResponse.json({ error: 'Movies array is required' }, { status: 400 })
    }

    // Call Python recommendation engine
    const recommendations = await callPythonRecommendationEngine(movies)
    
    return NextResponse.json({
      recommendations: recommendations.recommendations || [],
      taste_profile: recommendations.taste_profile || {},
      recommendation_map: recommendations.recommendation_map || {},
      insights: recommendations.insights || [],
      analysis: {
        total_analyzed: movies.length,
        ai_enhanced: true,
        generated_at: recommendations.generated_at || new Date().toISOString()
      }
    })

  } catch (error) {
    console.error('AI recommendation error:', error)
    
    return NextResponse.json({
      error: 'Failed to generate recommendations',
      message: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 })
  }
}

async function callPythonRecommendationEngine(movies: any[]): Promise<any> {
  return new Promise((resolve, reject) => {
    const scriptPath = path.join(process.cwd(), 'scripts', 'recommendation_engine.py')
    const inputData = JSON.stringify({ movies })
    
    // Spawn Python process
    const python = spawn('python3', [scriptPath, '--json'])
    
    let stdout = ''
    let stderr = ''
    
    python.stdout.on('data', (data) => {
      stdout += data.toString()
    })
    
    python.stderr.on('data', (data) => {
      stderr += data.toString()
    })
    
    // Send movie data to Python script via stdin
    python.stdin.write(inputData)
    python.stdin.end()
    
    python.on('close', (code) => {
      if (code !== 0) {
        console.error('Python script error:', stderr)
        reject(new Error(`Python script exited with code ${code}`))
        return
      }
      
      try {
        // Extract JSON from output (may have other log messages)
        const jsonMatch = stdout.match(/\{[\s\S]*\}/)
        if (jsonMatch) {
          const result = JSON.parse(jsonMatch[0])
          resolve(result)
        } else {
          reject(new Error('No JSON output from Python script'))
        }
      } catch (parseError) {
        console.error('Failed to parse Python output:', parseError)
        reject(parseError)
      }
    })
  })
}