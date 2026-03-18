type Props = {
  sourceLang: string;
  targetLang: string;
  onSourceChange: (value: string) => void;
  onTargetChange: (value: string) => void;
};

const options = [
  { value: "en", label: "English" },
  { value: "km", label: "Khmer" },
];

export function LanguageSelector({ sourceLang, targetLang, onSourceChange, onTargetChange }: Props) {
  return (
    <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
      <div>
        <label htmlFor="sourceLang" className="mb-2 block text-sm font-medium">
          Source Language
        </label>
        <select
          id="sourceLang"
          value={sourceLang}
          onChange={(event) => onSourceChange(event.target.value)}
          className="w-full rounded-md border border-slate-300 px-3 py-2"
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="targetLang" className="mb-2 block text-sm font-medium">
          Target Language
        </label>
        <select
          id="targetLang"
          value={targetLang}
          onChange={(event) => onTargetChange(event.target.value)}
          className="w-full rounded-md border border-slate-300 px-3 py-2"
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
