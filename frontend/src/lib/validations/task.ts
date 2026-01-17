// Task validation schemas using Zod
import { z } from "zod";

export const taskCreateSchema = z.object({
  title: z.string()
    .min(1, "Title is required")
    .max(200, "Title must be less than 200 characters"),
  description: z.string()
    .max(2000, "Description must be less than 2000 characters")
    .optional()
    .nullable(),
});

export const taskUpdateSchema = z.object({
  title: z.string()
    .min(1, "Title is required")
    .max(200, "Title must be less than 200 characters")
    .optional(),
  description: z.string()
    .max(2000, "Description must be less than 2000 characters")
    .optional()
    .nullable(),
});

export type TaskCreateInput = z.infer<typeof taskCreateSchema>;
export type TaskUpdateInput = z.infer<typeof taskUpdateSchema>;
