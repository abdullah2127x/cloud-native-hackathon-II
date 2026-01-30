"use client";

import { useMemo } from "react";
import { Badge } from "@/components/ui/badge";
import type { Todo } from "@/types/task";

interface TagsListProps {
  todos: Todo[] | undefined;
  selectedTag: string | null;
  onSelectTag: (tag: string) => void;
}

export function TagsList({
  todos = [],
  selectedTag,
  onSelectTag,
}: TagsListProps) {
  // Extract unique tags and their counts
  const tagCounts = useMemo(() => {
    const counts: { [key: string]: number } = {};

    todos.forEach((todo) => {
      if (todo.tags && Array.isArray(todo.tags)) {
        todo.tags.forEach((tag) => {
          counts[tag] = (counts[tag] || 0) + 1;
        });
      }
    });

    return Object.entries(counts)
      .map(([tag, count]) => ({ tag, count }))
      .sort((a, b) => b.count - a.count);
  }, [todos]);

  if (tagCounts.length === 0) {
    return (
      <div className="text-center py-8 bg-slate-50 dark:bg-slate-900 rounded-lg">
        <p className="text-slate-600 dark:text-slate-400">
          No tags found. Add tags to your tasks to organize them.
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
      {tagCounts.map(({ tag, count }) => (
        <button
          key={tag}
          onClick={() => onSelectTag(selectedTag === tag ? "" : tag)}
          className={`p-4 text-center rounded-lg border-2 transition ${
            selectedTag === tag
              ? "border-purple-600 dark:border-purple-400 bg-purple-50 dark:bg-purple-900/30"
              : "border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600"
          }`}
        >
          <div className="font-semibold text-slate-900 dark:text-white truncate">
            {tag}
          </div>
          <div className="text-xs text-slate-600 dark:text-slate-400 mt-1">
            {count} task{count !== 1 ? "s" : ""}
          </div>
        </button>
      ))}
    </div>
  );
}
