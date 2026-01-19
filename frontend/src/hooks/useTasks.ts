/**
 * useTasks - Custom hook for task management
 * Spec: 001-todo-web-crud
 * Task: T081
 */

"use client";

import { useState, useCallback } from "react";
 
import type { Task } from "@/types/task";
import type { TaskCreateInput, TaskUpdateInput } from "@/lib/validations/task";
import api from "@/middleware/api-interceptor";

interface UseTasksReturn {
  tasks: Task[];
  isLoading: boolean;
  error: Error | null;
  fetchTasks: () => Promise<void>;
  createTask: (data: TaskCreateInput) => Promise<Task>;
  updateTask: (id: string, data: TaskUpdateInput) => Promise<Task>;
  deleteTask: (id: string) => Promise<void>;
  toggleTask: (id: string) => Promise<Task>;
}

export function useTasks(): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchTasks = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await api.get<Task[]>("/api/todos");
      setTasks(response.data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to fetch tasks"));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createTask = useCallback(async (data: TaskCreateInput): Promise<Task> => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await api.post<Task>("/api/todos", data);
      setTasks((prev) => [response.data, ...prev]); // Add to beginning
      return response.data;
    } catch (err) {
      const error = err instanceof Error ? err : new Error("Failed to create task");
      setError(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateTask = useCallback(async (id: string, data: TaskUpdateInput): Promise<Task> => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await api.patch<Task>(`/api/todos/${id}`, data);
      setTasks((prev) =>
        prev.map((task) => (task.id === id ? response.data : task))
      );
      return response.data;
    } catch (err) {
      const error = err instanceof Error ? err : new Error("Failed to update task");
      setError(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const deleteTask = useCallback(async (id: string): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      await api.delete(`/api/todos/${id}`);
      setTasks((prev) => prev.filter((task) => task.id !== id));
    } catch (err) {
      const error = err instanceof Error ? err : new Error("Failed to delete task");
      setError(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const toggleTask = useCallback(async (id: string): Promise<Task> => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await api.post<Task>(`/api/todos/${id}/toggle`);
      setTasks((prev) =>
        prev.map((task) => (task.id === id ? response.data : task))
      );
      return response.data;
    } catch (err) {
      const error = err instanceof Error ? err : new Error("Failed to toggle task");
      setError(error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    tasks,
    isLoading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTask,
  };
}
