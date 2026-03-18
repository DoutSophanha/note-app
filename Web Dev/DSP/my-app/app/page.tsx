import { UrlForm } from "../frontend/components/url-form";

export default function Home() {
  return (
    <div className="mx-auto w-full max-w-4xl p-6 space-y-6">
      <header>
        <h1 className="text-2xl font-bold">Offline Subtitle Extract + Translate</h1>
        <p className="mt-2 text-sm text-slate-600">
          Paste a video URL, extract or generate subtitles, translate EN ↔ KM, and export.
        </p>
      </header>
      <UrlForm />
    </div>
  );
}
