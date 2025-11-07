import { Handler } from '@netlify/functions';
import { getJob, cleanupOldJobs } from './lib/jobTracker';

export const handler: Handler = async (event) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json',
  };

  // Handle CORS
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    const jobId = event.queryStringParameters?.jobId;

    if (!jobId) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Missing jobId parameter' }),
      };
    }

    // Clean up old jobs periodically
    cleanupOldJobs();

    // Get job status
    const job = getJob(jobId);

    if (!job) {
      return {
        statusCode: 404,
        headers,
        body: JSON.stringify({ error: 'Job not found' }),
      };
    }

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify(job),
    };
  } catch (error: any) {
    console.error('Error checking job status:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Failed to check job status',
        details: error.message,
      }),
    };
  }
};
