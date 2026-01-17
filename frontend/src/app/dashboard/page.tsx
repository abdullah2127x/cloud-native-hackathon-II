/**
 * Dashboard Page - Task management interface
 * Spec: 001-todo-web-crud
 * Task: T082, T083
 */

"use client";

import { useEffect } from "react";
import { TaskForm } from "@/components/tasks/TaskForm";
import { EmptyState } from "@/components/tasks/EmptyState";
import { useTasks } from "@/hooks/useTasks";
import type { TaskCreateInput } from "@/lib/validations/task";

export default function DashboardPage() {
  const { tasks, isLoading, error, fetchTasks, createTask } = useTasks();

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (data: TaskCreateInput) => {
    await createTask(data);
  };

  return (
    <div className="px-4 sm:px-0">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">My Tasks</h2>

      {/* Task creation form */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Create New Task</h3>
        <TaskForm onSubmit={handleCreateTask} isLoading={isLoading} />
      </div>

      {/* Tasks list */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Tasks</h3>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-600">{error.message}</p>
          </div>
        )}

        {isLoading && tasks.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-gray-500">Loading tasks...</p>
          </div>
        ) : tasks.length === 0 ? (
          <EmptyState />
        ) : (
          <div className="space-y-3">
            {tasks.map((task) => (
              <div
                key={task.id}
                className="p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h4 className="text-base font-medium text-gray-900">
                      {task.title}
                    </h4>
                    {task.description && (
                      <p className="mt-1 text-sm text-gray-600">{task.description}</p>
                    )}
                    <p className="mt-2 text-xs text-gray-500">
                      Created: {new Date(task.created_at).toLocaleDateString()}
                    </p>
                  </div>
                  <div className="ml-4">
                    <input
                      type="checkbox"
                      checked={task.completed}
                      readOnly
                      className="h-5 w-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
