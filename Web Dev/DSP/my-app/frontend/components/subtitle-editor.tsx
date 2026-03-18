"use client";

import { useMemo, useState } from "react";

type Props = {
  initialTxt: string;
};

export function SubtitleEditor({ initialTxt }: Props) {
  const [value, setValue] = useState(initialTxt);

  const lineCount = useMemo(() => value.split("\n").length, [value]);

  return (
    <div className="rounded-lg bg-white p-4 shadow-sm">
      <div className="mb-2 flex items-center justify-between text-sm text-slate-600">
        <span>Subtitle Preview / Editor</span>
        <span>{lineCount} lines</span>
      </div>
      <textarea
        value={value}
        onChange={(event) => setValue(event.target.value)}
        className="h-80 w-full rounded-md border border-slate-300 p-3 font-mono text-sm"
      />
    </div>
  );
}
