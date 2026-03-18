type Props = {
  files: Record<string, string>;
};

const labelByFormat: Record<string, string> = {
  srt: "Download SRT",
  vtt: "Download VTT",
  txt: "Download TXT",
  mp3: "Download MP3",
  mp4: "Download MP4",
  tts: "Download TTS",
};

export function DownloadButtons({ files }: Props) {
  const entries = Object.entries(files);

  if (!entries.length) {
    return null;
  }

  return (
    <div className="rounded-lg bg-white p-4 shadow-sm">
      <h2 className="mb-3 text-sm font-semibold">Downloads</h2>
      <div className="flex flex-wrap gap-2">
        {entries.map(([key, value]) => (
          <a
            key={key}
            href={`http://localhost:8000/static-file?path=${encodeURIComponent(value)}`}
            className="rounded-md bg-slate-900 px-4 py-2 text-sm text-white"
            target="_blank"
            rel="noreferrer"
          >
            {labelByFormat[key] ?? `Download ${key.toUpperCase()}`}
          </a>
        ))}
      </div>
    </div>
  );
}
