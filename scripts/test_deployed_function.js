const axios = require('axios');

async function testAnalyzeProfile() {
  console.log('Testing analyze-profile function on Netlify...\n');
  
  try {
    const response = await axios.post(
      'https://letteroutoftheboxd.netlify.app/.netlify/functions/analyze-profile',
      { username: 'bgoldman22' },
      {
        headers: { 'Content-Type': 'application/json' },
        timeout: 30000, // 30 second timeout
      }
    );
    
    console.log('✅ Response status:', response.status);
    console.log('✅ Response data:', JSON.stringify(response.data, null, 2));
    
  } catch (error) {
    if (error.response) {
      console.error('❌ HTTP Error:', error.response.status);
      console.error('❌ Error data:', error.response.data);
    } else if (error.request) {
      console.error('❌ No response received');
      console.error('❌ Request:', error.message);
    } else {
      console.error('❌ Error:', error.message);
    }
  }
}

testAnalyzeProfile();
