"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { LanguageSelector } from "./language-selector";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export function UrlForm() {
  const router = useRouter();
  const [url, setUrl] = useState("");
  const [sourceLang, setSourceLang] = useState("en");
  const [targetLang, setTargetLang] = useState("km");
  const [generateMp3, setGenerateMp3] = useState(false);
  const [reencodeMp4, setReencodeMp4] = useState(false);
  const [generateTts, setGenerateTts] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/api/job`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url,
          source_lang: sourceLang,
          target_lang: targetLang,
          generate_mp3: generateMp3,
          reencode_mp4: reencodeMp4,
          generate_tts: generateTts,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create job");
      }

      const data = await response.json();
      router.push(`/job/${data.id}`);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={onSubmit} className="space-y-4 rounded-lg bg-white p-6 shadow-sm">
      <div>
        <label htmlFor="url" className="mb-2 block text-sm font-medium">
          Video URL
        </label>
        <input
          id="url"
          type="url"
          required
          value={url}
          onChange={(event) => setUrl(event.target.value)}
          placeholder="https://youtube.com/watch?v=..."
          className="w-full rounded-md border border-slate-300 px-3 py-2"
        />
      </div>

      <LanguageSelector
        sourceLang={sourceLang}
        targetLang={targetLang}
        onSourceChange={setSourceLang}
        onTargetChange={setTargetLang}
      />

      <div className="grid grid-cols-1 gap-2 text-sm md:grid-cols-3">
        <label className="flex items-center gap-2">
          <input type="checkbox" checked={generateMp3} onChange={(e) => setGenerateMp3(e.target.checked)} />
          Generate MP3
        </label>
        <label className="flex items-center gap-2">
          <input type="checkbox" checked={reencodeMp4} onChange={(e) => setReencodeMp4(e.target.checked)} />
          Export MP4
        </label>
        <label className="flex items-center gap-2">
          <input type="checkbox" checked={generateTts} onChange={(e) => setGenerateTts(e.target.checked)} />
          Generate TTS
        </label>
      </div>

      {error ? <p className="text-sm text-red-600">{error}</p> : null}

      <button
        type="submit"
        disabled={loading}
        className="rounded-md bg-slate-900 px-4 py-2 text-white disabled:opacity-70"
      >
        {loading ? "Submitting..." : "Start Processing"}
      </button>
    </form>
  );
}
