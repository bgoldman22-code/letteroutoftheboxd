import * as fs from 'fs';
import * as path from 'path';

const JOB_DIR = '/tmp/letterboxd-jobs';

// Ensure job directory exists
if (!fs.existsSync(JOB_DIR)) {
  fs.mkdirSync(JOB_DIR, { recursive: true });
}

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

export function createJob(jobId: string, total: number): JobStatus {
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
  saveJob(job);
  return job;
}

export function saveJob(job: JobStatus): void {
  job.updatedAt = new Date().toISOString();
  const filePath = path.join(JOB_DIR, `${job.jobId}.json`);
  fs.writeFileSync(filePath, JSON.stringify(job, null, 2));
}

export function getJob(jobId: string): JobStatus | null {
  try {
    const filePath = path.join(JOB_DIR, `${jobId}.json`);
    if (!fs.existsSync(filePath)) {
      return null;
    }
    const data = fs.readFileSync(filePath, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    console.error('Error reading job:', error);
    return null;
  }
}

export function updateJobProgress(
  jobId: string,
  current: number,
  currentItem?: string
): void {
  const job = getJob(jobId);
  if (job) {
    job.status = 'processing';
    job.progress.current = current;
    if (currentItem) {
      job.progress.currentItem = currentItem;
    }
    saveJob(job);
  }
}

export function completeJob(jobId: string, result: any): void {
  const job = getJob(jobId);
  if (job) {
    job.status = 'completed';
    job.result = result;
    job.progress.current = job.progress.total;
    saveJob(job);
  }
}

export function failJob(jobId: string, error: string): void {
  const job = getJob(jobId);
  if (job) {
    job.status = 'error';
    job.error = error;
    saveJob(job);
  }
}

// Clean up old jobs (older than 1 hour)
export function cleanupOldJobs(): void {
  try {
    const files = fs.readdirSync(JOB_DIR);
    const oneHourAgo = Date.now() - 60 * 60 * 1000;
    
    files.forEach((file) => {
      const filePath = path.join(JOB_DIR, file);
      const stats = fs.statSync(filePath);
      if (stats.mtimeMs < oneHourAgo) {
        fs.unlinkSync(filePath);
      }
    });
  } catch (error) {
    console.error('Error cleaning up jobs:', error);
  }
}
