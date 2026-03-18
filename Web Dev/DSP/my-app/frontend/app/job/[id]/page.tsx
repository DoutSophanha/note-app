"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

type JobStatus = {
  id: string;
  status: string;
  progress: number;
  step: string;
  error?: string;
};

export default function JobStatusPage() {
  const params = useParams<{ id: string }>();
  const [job, setJob] = useState<JobStatus | null>(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      const response = await fetch(`${API_BASE_URL}/api/job/${params.id}`);
      if (response.ok) {
        const data = await response.json();
        setJob(data);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [params.id]);

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold">Job Status</h1>
      <div className="rounded-lg bg-white p-6 shadow-sm">
        <p className="text-sm">Job ID: {params.id}</p>
        <p className="mt-2 text-sm">Status: {job?.status ?? "loading"}</p>
        <p className="text-sm">Step: {job?.step ?? "-"}</p>
        <div className="mt-4 h-3 w-full rounded bg-slate-200">
          <div
            className="h-3 rounded bg-slate-900 transition-all"
            style={{ width: `${job?.progress ?? 0}%` }}
          />
        </div>
        <p className="mt-2 text-sm">Progress: {job?.progress ?? 0}%</p>
        {job?.error ? <p className="mt-2 text-sm text-red-600">{job.error}</p> : null}
      </div>

      {job?.status === "completed" ? (
        <Link href={`/job/${params.id}/result`} className="rounded-md bg-slate-900 px-4 py-2 text-white">
          View Result
        </Link>
      ) : null}
    </div>
  );
}
