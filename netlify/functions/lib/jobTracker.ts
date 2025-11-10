import { getStore } from '@netlify/blobs';

export interface JobStatus {
  jobId: string;
  status: 'pending' | 'processing' | 'completed' | 'error';
  progress: {
    current: number;
    total: number;
    currentItem?: string;
  };
  result?: any;
  error?: string;
  createdAt: string;
  updatedAt: string;
}

function getJobStore() {
  // Use explicit site ID and token from environment
  const siteID = process.env.NETLIFY_SITE_ID || '58b620ff-bd3c-44c0-8f6f-0ab0ce8f724d';
  // Use NETLIFY_FUNCTIONS_TOKEN (automatic, has correct permissions) instead of personal token
  const token = process.env.NETLIFY_FUNCTIONS_TOKEN || process.env.NETLIFY_AUTH_TOKEN;
  
  console.log('🔍 DEBUG - Netlify Blobs Config:');
  console.log('  - NETLIFY_SITE_ID:', siteID ? `${siteID.substring(0, 8)}...` : 'MISSING');
  console.log('  - Token type:', token === process.env.NETLIFY_FUNCTIONS_TOKEN ? 'NETLIFY_FUNCTIONS_TOKEN (automatic)' : 'NETLIFY_AUTH_TOKEN (personal)');
  console.log('  - Token value:', token ? `${token.substring(0, 6)}... (length: ${token.length})` : 'MISSING');
  console.log('  - All env vars available:', Object.keys(process.env).filter(k => k.includes('NETLIFY')));
  
  if (token) {
    console.log('✅ Creating store with siteID and token');
    try {
      const store = getStore({
        name: 'jobs',
        siteID,
        token,
      });
      console.log('✅ Store created successfully');
      return store;
    } catch (error: any) {
      console.error('❌ Error creating store:', error.message);
      throw error;
    }
  }
  
  // Fallback to simple name (shouldn't happen in production)
  console.warn('⚠️  No token found, using default store config');
  return getStore('jobs');
}

export function generateJobId(): string {
  return `job_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

export async function createJob(jobId: string, total: number): Promise<JobStatus> {
  console.log(`📋 Creating job: ${jobId} for ${total} items`);
  
  try {
    const store = getJobStore();
    console.log('✅ Got store instance');
    
    const job: JobStatus = {
      jobId,
      status: 'pending',
      progress: {
        current: 0,
        total,
      },
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    
    console.log('📝 Attempting to write job to Netlify Blobs...');
    await store.setJSON(jobId, job);
    console.log('✅ Job created successfully in Netlify Blobs');
    
    return job;
  } catch (error: any) {
    console.error('❌ Error creating job in Netlify Blobs:');
    console.error('  - Error message:', error.message);
    console.error('  - Error name:', error.name);
    console.error('  - Error stack:', error.stack);
    throw error;
  }
}

export async function getJob(jobId: string): Promise<JobStatus | null> {
  try {
    const store = getJobStore();
    const job = await store.get(jobId, { type: 'json' });
    return job as JobStatus | null;
  } catch (error) {
    console.error('Error reading job:', error);
    return null;
  }
}

export async function updateJobProgress(
  jobId: string,
  current: number,
  currentItem?: string
): Promise<void> {
  const job = await getJob(jobId);
  if (job) {
    job.status = 'processing';
    job.progress.current = current;
    if (currentItem) {
      job.progress.currentItem = currentItem;
    }
    job.updatedAt = new Date().toISOString();
    const store = getJobStore();
    await store.setJSON(jobId, job);
  }
}

export async function completeJob(jobId: string, result: any): Promise<void> {
  const job = await getJob(jobId);
  if (job) {
    job.status = 'completed';
    job.result = result;
    job.progress.current = job.progress.total;
    job.updatedAt = new Date().toISOString();
    const store = getJobStore();
    await store.setJSON(jobId, job);
  }
}

export async function failJob(jobId: string, error: string): Promise<void> {
  const job = await getJob(jobId);
  if (job) {
    job.status = 'error';
    job.error = error;
    job.updatedAt = new Date().toISOString();
    const store = getJobStore();
    await store.setJSON(jobId, job);
  }
}
