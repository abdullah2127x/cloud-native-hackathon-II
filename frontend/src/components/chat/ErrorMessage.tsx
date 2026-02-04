/**
 * ErrorMessage component for displaying chat errors with retry.
 *
 * Task IDs: T421, T427, T429
 * Spec: specs/001-chat-interface/spec.md
 */

'use client';

import { Button } from '@/components/ui/Button';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface ErrorMessageProps {
  message: string;
  onRetry: () => void;
  isRetrying?: boolean;
}

/**
 * T421: Display error with icon, empathetic message, and retry button.
 */
export default function ErrorMessage({
  message,
  onRetry,
  isRetrying = false,
}: ErrorMessageProps) {
  return (
    <div className="rounded-lg border border-destructive bg-destructive/5 p-4">
      <div className="flex items-start gap-3">
        <AlertCircle className="mt-0.5 h-5 w-5 flex-shrink-0 text-destructive" />

        <div className="flex-1">
          <p className="text-sm text-destructive">{message}</p>

          {/* T421: Retry button */}
          <Button
            onClick={onRetry}
            disabled={isRetrying}
            size="sm"
            variant="outline"
            className="mt-2"
          >
            {isRetrying ? (
              <>
                <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                Retrying...
              </>
            ) : (
              <>
                <RefreshCw className="mr-2 h-4 w-4" />
                Try Again
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}
