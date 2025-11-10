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
  // Try simple store name first - Netlify automatically handles auth in function context
  console.log('🔍 Creating Netlify Blobs store with automatic authentication...');
  console.log('  - Running in Netlify Functions context');
  console.log('  - Available NETLIFY vars:', Object.keys(process.env).filter(k => k.includes('NETLIFY')));
  
  try {
    // In Netlify Functions, getStore() automatically uses the correct context
    const store = getStore('jobs');
    console.log('✅ Store created successfully with automatic authentication');
    return store;
  } catch (error: any) {
    console.error('❌ Error creating Netlify Blobs store:', error.message);
    console.error('   This might mean Netlify Blobs is not enabled on this site.');
    throw error;
  }
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
