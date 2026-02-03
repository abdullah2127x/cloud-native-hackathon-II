"use client";

import { useEffect } from "react";
import { useTasks } from "@/hooks/useTasks";
import { PriorityTabs } from "../components/PriorityTabs";
import { TodoCard } from "../components/TodoCard";
import { Flag } from "lucide-react";
import type { Todo } from "@/types/task";

export default function PriorityPage() {
  const { tasks, isLoading, fetchTasks, deleteTask, toggleTask } = useTasks();

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // T006: Fixed priority filtering logic to render all priority levels
  const renderPriorityContent = (
    todos: Todo[],
    priority: "high" | "medium" | "low" | "none"
  ) => {
    if (todos.length === 0) {
      return (
        <div className="text-center py-8 bg-slate-50 dark:bg-slate-900 rounded-lg">
          <Flag className="h-12 w-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
          <p className="text-slate-600 dark:text-slate-400">
            No tasks at this priority level
          </p>
        </div>
      );
    }

    return (
      <div className="space-y-3">
        {todos.map((todo) => (
          <TodoCard
            key={todo.id}
            todo={todo}
            onToggle={() => toggleTask(todo.id)}
            onEdit={(t) => {
              // Edit functionality handled in main dashboard
            }}
            onDelete={() => deleteTask(todo.id)}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">
          Tasks by Priority
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2">
          Organize and view tasks by priority level
        </p>
      </div>

      {/* Priority Tabs */}
      <PriorityTabs
        todos={tasks}
        isLoading={isLoading}
        renderContent={renderPriorityContent}
      />
    </div>
  );
}
