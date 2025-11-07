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

export function generateJobId(): string {
  return `job_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

export async function createJob(jobId: string, total: number): Promise<JobStatus> {
  const store = getStore('jobs');
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
  await store.setJSON(jobId, job);
  return job;
}

export async function getJob(jobId: string): Promise<JobStatus | null> {
  try {
    const store = getStore('jobs');
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
    const store = getStore('jobs');
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
    const store = getStore('jobs');
    await store.setJSON(jobId, job);
  }
}

export async function failJob(jobId: string, error: string): Promise<void> {
  const job = await getJob(jobId);
  if (job) {
    job.status = 'error';
    job.error = error;
    job.updatedAt = new Date().toISOString();
    const store = getStore('jobs');
    await store.setJSON(jobId, job);
  }
}
