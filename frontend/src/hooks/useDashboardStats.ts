import { useMemo } from "react";
import { calculateDashboardStats, type DashboardStatistics } from "@/lib/dashboard-stats";
import type { Todo } from "@/types/task";

export function useDashboardStats(todos: Todo[] | undefined): DashboardStatistics {
  return useMemo(() => {
    if (!todos) {
      return {
        total: 0,
        completed: 0,
        pending: 0,
        today: 0,
      };
    }
    return calculateDashboardStats(todos);
  }, [todos]);
}
