/**
 * Dashboard Page - Task management interface
 * Spec: 001-todo-web-crud
 * Task: T082, T083, T110-T128
 */

"use client";

import { useEffect, useState } from "react";
import { TaskForm } from "@/components/tasks/TaskForm";
import { TaskList } from "@/components/tasks/TaskList";
import { useTasks } from "@/hooks/useTasks";
import type { TaskCreateInput } from "@/lib/validations/task";

export default function DashboardPage() {
  const { tasks, isLoading, error, fetchTasks, createTask, updateTask, deleteTask, toggleTask } = useTasks();
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [formKey, setFormKey] = useState(0);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (data: TaskCreateInput) => {
    await createTask(data);
    // Force form to remount with fresh state
    setFormKey(prev => prev + 1);
  };

  const handleEditTask = (taskId: string) => {
    setEditingTaskId(taskId);
  };

  const handleUpdateTask = async (data: TaskCreateInput) => {
    if (editingTaskId) {
      await updateTask(editingTaskId, data);
      setEditingTaskId(null);
    }
  };

  const handleCancelEdit = () => {
    setEditingTaskId(null);
  };

  const handleToggleTask = async (taskId: string) => {
    await toggleTask(taskId);
  };

  const handleDeleteTask = async (taskId: string) => {
    await deleteTask(taskId);
  };

  const editingTask = editingTaskId ? tasks.find((t) => t.id === editingTaskId) : null;

  return (
    <div className="px-4 sm:px-0">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">My Tasks</h2>

      {/* Edit task modal */}
      {editingTask && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Edit Task</h3>
            <TaskForm
              mode="edit"
              onSubmit={handleUpdateTask}
              onCancel={handleCancelEdit}
              isLoading={isLoading}
              defaultValues={{
                title: editingTask.title,
                description: editingTask.description || undefined,
              }}
            />
          </div>
        </div>
      )}

      {/* Task creation form */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Create New Task</h3>
        <TaskForm
          key={formKey}
          onSubmit={handleCreateTask}
          isLoading={isLoading}
          defaultValues={{ title: "", description: "" }}
        />
      </div>

      {/* Tasks list */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Tasks</h3>

        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p className="text-sm text-red-600">{error.message}</p>
          </div>
        )}

        <TaskList
          tasks={tasks}
          isLoading={isLoading}
          onToggle={handleToggleTask}
          onEdit={handleEditTask}
          onDelete={handleDeleteTask}
        />
      </div>
    </div>
  );
}
