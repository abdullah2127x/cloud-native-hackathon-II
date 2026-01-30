"use client";

import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { CheckCircle2, Circle, MoreVertical, Trash2, Edit } from "lucide-react";
import { getPriorityConfig } from "@/lib/priority-colors";
import type { Todo } from "@/types/task";

interface TodoCardProps {
  todo: Todo;
  onToggle: () => void;
  onEdit: (todo: Todo) => void;
  onDelete: () => void;
}

export function TodoCard({ todo, onToggle, onEdit, onDelete }: TodoCardProps) {
  const priorityConfig = getPriorityConfig(todo.priority);

  return (
    <Card
      className={`border-slate-200 dark:border-slate-700 transition ${
        todo.completed
          ? "bg-slate-100 dark:bg-slate-800/50"
          : "hover:shadow-md"
      }`}
    >
      <CardContent className="pt-6">
        <div className="flex gap-4">
          {/* Checkbox */}
          <button onClick={onToggle} className="mt-1 flex-shrink-0">
            {todo.completed ? (
              <CheckCircle2 className="w-6 h-6 text-green-600 dark:text-green-500" />
            ) : (
              <Circle className="w-6 h-6 text-slate-300 dark:text-slate-600 hover:text-slate-400" />
            )}
          </button>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1">
                <h3
                  className={`font-semibold text-slate-900 dark:text-white transition ${
                    todo.completed
                      ? "line-through text-slate-500 dark:text-slate-400"
                      : ""
                  }`}
                >
                  {todo.title}
                </h3>
                {todo.description && (
                  <p
                    className={`text-sm text-slate-600 dark:text-slate-400 mt-1 ${
                      todo.completed ? "line-through" : ""
                    }`}
                  >
                    {todo.description}
                  </p>
                )}
              </div>

              {/* Action Menu */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" size="sm" className="flex-shrink-0">
                    <MoreVertical className="w-4 h-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem onClick={() => onEdit(todo)}>
                    <Edit className="w-4 h-4 mr-2" />
                    Edit
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    onClick={onDelete}
                    className="text-red-600 dark:text-red-400"
                  >
                    <Trash2 className="w-4 h-4 mr-2" />
                    Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>

            {/* Badges */}
            <div className="flex flex-wrap gap-2 mt-3">
              <Badge
                className={`${priorityConfig.bgColor} ${priorityConfig.textColor} border-0`}
              >
                {priorityConfig.label}
              </Badge>
              {todo.tags && todo.tags.length > 0 && (
                <>
                  {todo.tags.map((tag) => (
                    <Badge
                      key={tag}
                      variant="outline"
                      className="border-slate-300 dark:border-slate-600"
                    >
                      {tag}
                    </Badge>
                  ))}
                </>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
