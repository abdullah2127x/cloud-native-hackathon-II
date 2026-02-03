/**
 * TaskForm - Form component for creating and editing tasks
 * Spec: 001-todo-web-crud, 002-todo-organization-features
 * Task: T079, T112, T037, T057
 */

"use client";

import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { taskCreateSchema, type TaskCreateInput, priorityValues, PRIORITY_CONFIG } from "@/lib/validations/task";
import { Button } from "@/components/ui/Button";
import { TagInput } from "./TagInput";
import { useTags } from "@/hooks/useTags";

interface TaskFormProps {
  onSubmit: (data: TaskCreateInput) => Promise<void>;
  onCancel?: () => void;
  isLoading?: boolean;
  defaultValues?: Partial<TaskCreateInput>;
  mode?: "create" | "edit";
}

export function TaskForm({
  onSubmit,
  onCancel,
  isLoading = false,
  defaultValues,
  mode = "create"
}: TaskFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    setValue,
    watch,
  } = useForm<TaskCreateInput>({
    resolver: zodResolver(taskCreateSchema),
    defaultValues,
  });

  const { tags, isLoading: tagsLoading, fetchTags } = useTags();
  const watchedTags = watch("tags", defaultValues?.tags || []);

  useEffect(() => {
    fetchTags();
  }, [fetchTags]);

  const handleFormSubmit = async (data: TaskCreateInput) => {
    await onSubmit(data);
    // Note: Create form is remounted via key prop in parent component
    // Edit form stays mounted and user can cancel or continue editing
    if (mode === "edit") {
      // Could add success feedback here if needed
    }
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700">
          Title
        </label>
        <input
          {...register("title")}
          id="title"
          type="text"
          disabled={isLoading}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
          placeholder="Enter task title"
        />
        {errors.title && (
          <p className="mt-1 text-sm text-red-600">{errors.title.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700">
          Description (Optional)
        </label>
        <textarea
          {...register("description")}
          id="description"
          rows={3}
          disabled={isLoading}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
          placeholder="Enter task description"
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">{errors.description.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="priority" className="block text-sm font-medium text-gray-700">
          Priority
        </label>
        <select
          {...register("priority")}
          id="priority"
          disabled={isLoading}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        >
          {priorityValues.map((priority) => (
            <option key={priority} value={priority}>
              {PRIORITY_CONFIG[priority].label}
            </option>
          ))}
        </select>
        {errors.priority && (
          <p className="mt-1 text-sm text-red-600">{errors.priority.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="tags" className="block text-sm font-medium text-gray-700">
          Tags (Optional)
        </label>
        <TagInput
          value={watchedTags}
          onChange={(newTags) => setValue("tags", newTags, { shouldValidate: true })}
          suggestions={tags.map(tag => tag.name)}
          disabled={isLoading || tagsLoading}
          placeholder="Add tags (comma or enter to add)..."
        />
        {errors.tags && (
          <p className="mt-1 text-sm text-red-600">{errors.tags.message}</p>
        )}
      </div>

      <div className="flex justify-end gap-2">
        {mode === "edit" && onCancel && (
          <Button
            type="button"
            variant="secondary"
            onClick={onCancel}
            disabled={isLoading}
          >
            Cancel
          </Button>
        )}
        <Button
          type="submit"
          variant="default"
          disabled={isLoading}
        >
          {mode === "edit"
            ? isLoading
              ? "Saving..."
              : "Save Changes"
            : isLoading
            ? "Creating..."
            : "Create Task"}
        </Button>
      </div>
    </form>
  );
}
