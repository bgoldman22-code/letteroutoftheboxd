#!/usr/bin/env node

/**
 * Test script for Netlify functions
 * Tests each function independently with sample data
 */

const axios = require('axios');

// For local testing, we'll invoke the functions directly
const analyzeProfile = require('../netlify/functions/analyze-profile');
const enrichMovies = require('../netlify/functions/enrich-movies');

async function testAnalyzeProfile() {
  console.log('\n🧪 Testing analyze-profile function...');
  
  const event = {
    httpMethod: 'POST',
    body: JSON.stringify({ username: 'bgoldman22' }),
  };

  try {
    const response = await analyzeProfile.handler(event);
    const data = JSON.parse(response.body);
    
    if (response.statusCode === 200) {
      console.log('✅ analyze-profile PASSED');
      console.log(`   Found ${data.data.all_rated_movies.length} rated movies`);
      console.log(`   Found ${data.data.loved_movies.length} loved movies`);
      return data.data;
    } else {
      console.error('❌ analyze-profile FAILED:', data.error);
      return null;
    }
  } catch (error) {
    console.error('❌ analyze-profile ERROR:', error.message);
    return null;
  }
}

async function testEnrichMovies(movies) {
  console.log('\n🧪 Testing enrich-movies function...');
  
  const event = {
    httpMethod: 'POST',
    body: JSON.stringify({ movies: movies.slice(0, 5) }), // Test with 5 movies
  };

  try {
    const response = await enrichMovies.handler(event);
    const data = JSON.parse(response.body);
    
    if (response.statusCode === 200) {
      console.log('✅ enrich-movies PASSED');
      console.log(`   Enriched ${data.data.length} movies`);
      return data.data;
    } else {
      console.error('❌ enrich-movies FAILED:', data.error);
      return null;
    }
  } catch (error) {
    console.error('❌ enrich-movies ERROR:', error.message);
    return null;
  }
}

async function runTests() {
  console.log('🎬 Starting Netlify Functions Test Suite\n');
  console.log('════════════════════════════════════════════════════════════');
  
  // Load environment variables
  require('dotenv').config();
  
  // Check for required API keys
  if (!process.env.OMDB_API_KEY) {
    console.error('❌ OMDB_API_KEY not found in environment variables');
    process.exit(1);
  }
  
  if (!process.env.OPENAI_API_KEY) {
    console.error('❌ OPENAI_API_KEY not found in environment variables');
    process.exit(1);
  }
  
  console.log('✅ Environment variables loaded');
  
  // Test 1: Analyze profile
  const profileData = await testAnalyzeProfile();
  if (!profileData) {
    console.error('\n❌ Test suite failed at analyze-profile');
    process.exit(1);
  }
  
  // Test 2: Enrich movies
  const enrichedMovies = await testEnrichMovies(profileData.all_rated_movies);
  if (!enrichedMovies) {
    console.error('\n❌ Test suite failed at enrich-movies');
    process.exit(1);
  }
  
  console.log('\n════════════════════════════════════════════════════════════');
  console.log('✅ All tests passed!\n');
}

runTests().catch(error => {
  console.error('\n❌ Test suite error:', error);
  process.exit(1);
});
