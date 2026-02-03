/**
 * TagInput component - Tag input with autocomplete
 * Spec: 002-todo-organization-features
 * Task: T056
 */

import { useState, useRef, KeyboardEvent } from "react";
import { X } from "lucide-react";
import { TagChip } from "./TagChip";

interface TagInputProps {
  value: string[];
  onChange: (tags: string[]) => void;
  suggestions: string[];
  placeholder?: string;
  disabled?: boolean;
}

export function TagInput({ value, onChange, suggestions, placeholder = "Add tags...", disabled = false }: TagInputProps) {
  const [inputValue, setInputValue] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const filteredSuggestions = suggestions
    .filter(suggestion =>
      suggestion.toLowerCase().includes(inputValue.toLowerCase()) &&
      !value.some(tag => tag.toLowerCase() === suggestion.toLowerCase())
    )
    .slice(0, 5); // Limit to 5 suggestions

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setInputValue(newValue);

    // Show suggestions when user types
    if (newValue.trim()) {
      setShowSuggestions(true);
      setError(null);
    } else {
      setShowSuggestions(false);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();

      // Add the current input value as a tag
      const trimmedValue = inputValue.trim();

      if (trimmedValue) {
        // Validate the tag
        if (trimmedValue.includes(" ")) {
          setError("Tags must be single words (no spaces)");
          return;
        }

        if (trimmedValue.length > 50) {
          setError("Tag must be 50 characters or less");
          return;
        }

        if (!value.some(tag => tag.toLowerCase() === trimmedValue.toLowerCase())) {
          onChange([...value, trimmedValue]);
          setInputValue("");
          setError(null);
        }
      }
    } else if (e.key === "Backspace" && !inputValue && value.length > 0) {
      // Remove last tag when backspace pressed on empty input
      onChange(value.slice(0, -1));
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    if (!value.some(tag => tag.toLowerCase() === suggestion.toLowerCase())) {
      onChange([...value, suggestion]);
      setInputValue("");
      setShowSuggestions(false);
    }
  };

  const removeTag = (tagToRemove: string) => {
    onChange(value.filter(tag => tag !== tagToRemove));
  };

  const addTagFromInput = () => {
    const trimmedValue = inputValue.trim();

    if (trimmedValue) {
      // Validate the tag
      if (trimmedValue.includes(" ")) {
        setError("Tags must be single words (no spaces)");
        return;
      }

      if (trimmedValue.length > 50) {
        setError("Tag must be 50 characters or less");
        return;
      }

      if (!value.some(tag => tag.toLowerCase() === trimmedValue.toLowerCase())) {
        onChange([...value, trimmedValue]);
        setInputValue("");
        setError(null);
      }
    }
  };

  return (
    <div className="relative">
      <div className="flex flex-wrap gap-2 mb-2">
        {value.map((tag, index) => (
          <TagChip
            key={`${tag}-${index}`} // Using index to handle duplicate tag names
            name={tag}
            onRemove={() => !disabled && removeTag(tag)}
          />
        ))}
      </div>

      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
          onFocus={() => inputValue && setShowSuggestions(true)}
          placeholder={value.length === 0 ? placeholder : ""}
          disabled={disabled}
          className={`w-full rounded-md border ${
            error ? "border-red-500" : "border-gray-300"
          } px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed`}
        />

        {error && (
          <p className="mt-1 text-sm text-red-600">{error}</p>
        )}

        {showSuggestions && filteredSuggestions.length > 0 && (
          <div className="absolute z-10 mt-1 w-full rounded-md bg-white shadow-lg border border-gray-200 max-h-60 overflow-auto">
            <div className="py-1">
              {filteredSuggestions.map((suggestion, index) => (
                <div
                  key={suggestion}
                  className="px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  {suggestion}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
