/**
 * SearchBar component - Search input with debounce
 * Spec: 002-todo-organization-features
 * Task: T067, T109
 */

import { Search, X } from "lucide-react";
import { useDebounce } from "@/hooks/useDebounce";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

export function SearchBar({ value, onChange }: SearchBarProps) {
  const debouncedValue = useDebounce(value, 300);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange(e.target.value);
  };

  const handleClear = () => {
    onChange("");
  };

  return (
    <div className="relative">
      {/* T061: Replace hardcoded colors with theme variables */}
      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none" style={{ color: "var(--muted-foreground)" }}>
        <Search className="h-5 w-5" />
      </div>
      <input
        type="text"
        value={value}
        onChange={handleChange}
        placeholder="Search tasks..."
        className="block w-full pl-10 pr-10 py-2 border rounded-md leading-5 focus:outline-none focus:ring-1 transition sm:text-sm"
        style={{
          backgroundColor: "var(--input-bg)",
          borderColor: "var(--input-border)",
          color: "var(--input-text)",
        }}
        onFocus={(e) => {
          e.currentTarget.style.borderColor = "var(--primary)";
          e.currentTarget.style.boxShadow = "0 0 0 1px var(--primary)";
        }}
        onBlur={(e) => {
          e.currentTarget.style.borderColor = "var(--input-border)";
          e.currentTarget.style.boxShadow = "none";
        }}
      />
      {value && (
        <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
          <button
            type="button"
            onClick={handleClear}
            className="focus:outline-none transition hover:opacity-70"
            style={{ color: "var(--muted-foreground)" }}
            aria-label="Clear search"
          >
            <X className="h-5 w-5" />
          </button>
        </div>
      )}
    </div>
  );
}
