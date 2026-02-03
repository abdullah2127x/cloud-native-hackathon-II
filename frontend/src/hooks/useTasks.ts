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

interface FetchTasksParams {
  search?: string;
  status?: "all" | "pending" | "completed";
  priority?: "all" | "high" | "medium" | "low" | "none";
  tags?: string[];
  noTags?: boolean;
  sort?: "priority" | "title" | "created_at";
  order?: "asc" | "desc";
}

interface TaskListResponse {
  tasks: Task[];
  total: number;
  filtered: number;
}

interface UseTasksReturn {
  tasks: Task[];
  total: number;
  filtered: number;
  isLoading: boolean;
  error: Error | null;
  fetchTasks: (params?: FetchTasksParams) => Promise<void>;
  createTask: (data: TaskCreateInput) => Promise<Task>;
  updateTask: (id: string, data: TaskUpdateInput) => Promise<Task>;
  deleteTask: (id: string) => Promise<void>;
  toggleTask: (id: string) => Promise<Task>;
}

export function useTasks(): UseTasksReturn {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [total, setTotal] = useState(0);
  const [filtered, setFiltered] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchTasks = useCallback(async (params?: FetchTasksParams) => {
    try {
      setIsLoading(true);
      setError(null);

      // Build query string from params
      const queryParams = new URLSearchParams();
      if (params?.search) queryParams.append("search", params.search);
      if (params?.status && params.status !== "all") queryParams.append("status", params.status);
      if (params?.priority && params.priority !== "all") queryParams.append("priority", params.priority);
      if (params?.tags && params.tags.length > 0) {
        params.tags.forEach(tag => queryParams.append("tags", tag));
      }
      if (params?.noTags) queryParams.append("no_tags", "true");
      if (params?.sort) queryParams.append("sort", params.sort);
      if (params?.order) queryParams.append("order", params.order);

      const queryString = queryParams.toString();
      const url = `/api/todos${queryString ? '?' + queryString : ''}`;

      const response = await api.get<TaskListResponse>(url);
      setTasks(response.data.tasks);
      setTotal(response.data.total);
      setFiltered(response.data.filtered);
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
    total,
    filtered,
    isLoading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleTask,
  };
}
