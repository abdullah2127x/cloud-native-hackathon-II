"use client";

import { useEffect, useState, useMemo } from "react";
import { useTasks } from "@/hooks/useTasks";
import { TagsList } from "../components/TagsList";
import { TodoCard } from "../components/TodoCard";
import { Skeleton } from "@/components/ui/skeleton";
import { Tag } from "lucide-react";
import type { Todo } from "@/types/task";

export default function TagsPage() {
  const { tasks, isLoading, fetchTasks, updateTask, deleteTask, toggleTask } = useTasks();
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Filter todos by selected tag
  const filteredTodos = useMemo(() => {
    if (!selectedTag || !tasks) return [];
    return tasks.filter((t) => t.tags && t.tags.includes(selectedTag));
  }, [tasks, selectedTag]);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
            Tasks by Tags
          </h1>
        </div>
        <Skeleton className="h-40 rounded-lg" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
          Tasks by Tags
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2">
          Filter and organize tasks by custom tags
        </p>
      </div>

      {/* Tags Grid */}
      <div className="bg-white dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 p-6">
        <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
          All Tags
        </h2>
        <TagsList
          todos={tasks}
          selectedTag={selectedTag}
          onSelectTag={setSelectedTag}
        />
      </div>

      {/* Filtered Tasks */}
      {selectedTag && (
        <div className="space-y-4">
          <div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-2">
              Tasks tagged: <span className="text-purple-600 dark:text-purple-400">#{selectedTag}</span>
            </h2>
            <p className="text-sm text-slate-600 dark:text-slate-400">
              {filteredTodos.length} task{filteredTodos.length !== 1 ? "s" : ""} found
            </p>
          </div>

          <div className="space-y-3">
            {filteredTodos.length === 0 ? (
              <div className="text-center py-8 bg-slate-50 dark:bg-slate-900 rounded-lg">
                <Tag className="h-12 w-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
                <p className="text-slate-600 dark:text-slate-400">
                  No tasks with this tag
                </p>
              </div>
            ) : (
              filteredTodos.map((todo) => (
                <TodoCard
                  key={todo.id}
                  todo={todo}
                  onToggle={() => toggleTask(todo.id)}
                  onEdit={(t) => {
                    // Handle edit
                  }}
                  onDelete={() => deleteTask(todo.id)}
                />
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
