import type { Todo } from "@/types/task";

export interface DashboardStatistics {
  total: number;
  completed: number;
  pending: number;
  today: number;
}

export function calculateDashboardStats(
  todos: Todo[]
): DashboardStatistics {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  return {
    total: todos.length,
    completed: todos.filter((t) => t.completed).length,
    pending: todos.filter((t) => !t.completed).length,
    today: todos.filter((t) => {
      const todoDate = new Date(t.created_at);
      todoDate.setHours(0, 0, 0, 0);
      return todoDate.getTime() === today.getTime();
    }).length,
  };
}
