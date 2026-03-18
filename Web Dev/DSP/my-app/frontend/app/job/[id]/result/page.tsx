"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import { DownloadButtons } from "../../../../components/download-buttons";
import { SubtitleEditor } from "../../../../components/subtitle-editor";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

type JobResult = {
  id: string;
  status: string;
  files: Record<string, string>;
  available_subtitle_languages: string[];
};

export default function JobResultPage() {
  const params = useParams<{ id: string }>();
  const [result, setResult] = useState<JobResult | null>(null);
  const [txtData, setTxtData] = useState("");

  useEffect(() => {
    const fetchResult = async () => {
      const response = await fetch(`${API_BASE_URL}/api/job/${params.id}/result`);
      if (!response.ok) {
        return;
      }
      const data = await response.json();
      setResult(data);

      if (data.files?.txt) {
        const txtResponse = await fetch(
          `${API_BASE_URL}/static-file?path=${encodeURIComponent(data.files.txt)}`,
        );
        if (txtResponse.ok) {
          setTxtData(await txtResponse.text());
        }
      }
    };

    fetchResult();
  }, [params.id]);

  if (!result) {
    return <p>Loading result...</p>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-semibold">Job Result</h1>
      <div className="rounded-lg bg-white p-4 shadow-sm text-sm">
        <p>Status: {result.status}</p>
        <p className="mt-2">Available subtitle languages: {result.available_subtitle_languages.join(", ") || "N/A"}</p>
      </div>
      <DownloadButtons files={result.files} />
      <SubtitleEditor initialTxt={txtData} />
    </div>
  );
}
