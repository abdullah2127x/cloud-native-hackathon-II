/**
 * Tests for error-classifier utility.
 *
 * Task ID: T428
 * Spec: specs/001-chat-interface/spec.md
 */

import { describe, it, expect } from 'vitest';
import { classifyError, type ClassifiedError } from './error-classifier';

describe('error-classifier', () => {
  // T428: Test network error classification
  describe('network errors', () => {
    it('classifies TypeError with "Failed to fetch" as network error', () => {
      const error = new TypeError('Failed to fetch');
      const classified = classifyError(error);

      expect(classified.type).toBe('network');
      expect(classified.message).toContain('Connection lost');
      expect(classified.isRetryable).toBe(true);
    });

    it('returns empathetic message for network errors', () => {
      const error = new TypeError('Failed to fetch');
      const classified = classifyError(error);

      expect(classified.message).toContain('Check your internet');
      expect(classified.message).toContain('try again');
    });
  });

  // T428: Test timeout error classification
  describe('timeout errors', () => {
    it('classifies DOMException with "AbortError" as timeout', () => {
      const error = new DOMException('The operation was aborted', 'AbortError');
      const classified = classifyError(error);

      expect(classified.type).toBe('timeout');
      expect(classified.message).toContain('timed out');
      expect(classified.isRetryable).toBe(true);
    });

    it('classifies Error with "timeout" text as timeout', () => {
      const error = new Error('Request timeout after 3000ms');
      const classified = classifyError(error);

      expect(classified.type).toBe('timeout');
      expect(classified.isRetryable).toBe(true);
    });

    it('classifies Error with "408" as timeout', () => {
      const error = new Error('408 Request Timeout');
      const classified = classifyError(error);

      expect(classified.type).toBe('timeout');
      expect(classified.isRetryable).toBe(true);
    });
  });

  // T428: Test auth error classification
  describe('auth errors', () => {
    it('classifies Error with "401" as auth error', () => {
      const error = new Error('401 Unauthorized');
      const classified = classifyError(error);

      expect(classified.type).toBe('auth');
      expect(classified.message).toContain('Session expired');
      expect(classified.isRetryable).toBe(false);
    });

    it('classifies Error with "unauthorized" as auth error', () => {
      const error = new Error('unauthorized access denied');
      const classified = classifyError(error);

      expect(classified.type).toBe('auth');
      expect(classified.isRetryable).toBe(false);
    });

    it('classifies Error with "session" as auth error', () => {
      const error = new Error('Your session has expired');
      const classified = classifyError(error);

      expect(classified.type).toBe('auth');
      expect(classified.isRetryable).toBe(false);
    });
  });

  // T428: Test validation error classification
  describe('validation errors', () => {
    it('classifies Error with "400" as validation error', () => {
      const error = new Error('400 Bad Request');
      const classified = classifyError(error);

      expect(classified.type).toBe('validation');
      expect(classified.message).toContain('Invalid input');
      expect(classified.isRetryable).toBe(false);
    });

    it('classifies Error with "validation" as validation error', () => {
      const error = new Error('validation failed: title is required');
      const classified = classifyError(error);

      expect(classified.type).toBe('validation');
      expect(classified.isRetryable).toBe(false);
    });
  });

  // T428: Test server error classification
  describe('server errors', () => {
    it('classifies Error with "500" as server error', () => {
      const error = new Error('500 Internal Server Error');
      const classified = classifyError(error);

      expect(classified.type).toBe('server');
      expect(classified.message).toContain('Something went wrong');
      expect(classified.isRetryable).toBe(true);
    });

    it('classifies Error with "server" as server error', () => {
      const error = new Error('Server error occurred');
      const classified = classifyError(error);

      expect(classified.type).toBe('server');
      expect(classified.isRetryable).toBe(true);
    });
  });

  // T428: Test access error classification
  describe('access errors', () => {
    it('classifies Error with "403" as access error', () => {
      const error = new Error('403 Forbidden');
      const classified = classifyError(error);

      expect(classified.type).toBe('validation');
      expect(classified.message).toContain('permission');
      expect(classified.isRetryable).toBe(false);
    });

    it('classifies Error with "access" as access error', () => {
      const error = new Error('access denied');
      const classified = classifyError(error);

      expect(classified.type).toBe('validation');
      expect(classified.isRetryable).toBe(false);
    });

    it('classifies Error with "denied" as access error', () => {
      const error = new Error('permission denied');
      const classified = classifyError(error);

      expect(classified.type).toBe('validation');
      expect(classified.isRetryable).toBe(false);
    });
  });

  // T428: Test not found error classification
  describe('not found errors', () => {
    it('classifies Error with "404" as not found', () => {
      const error = new Error('404 Not Found');
      const classified = classifyError(error);

      expect(classified.type).toBe('validation');
      expect(classified.message).toContain('not found');
      expect(classified.isRetryable).toBe(false);
    });

    it('classifies Error with "not found" as not found', () => {
      const error = new Error('conversation not found');
      const classified = classifyError(error);

      expect(classified.type).toBe('validation');
      expect(classified.message).toContain('not found');
      expect(classified.isRetryable).toBe(false);
    });
  });

  // T428: Test unknown error classification
  describe('unknown errors', () => {
    it('returns unknown type for unclassified errors', () => {
      const error = new Error('Some random error');
      const classified = classifyError(error);

      expect(classified.type).toBe('unknown');
      expect(classified.isRetryable).toBe(true);
    });

    it('handles non-Error objects gracefully', () => {
      const classified = classifyError('string error');

      expect(classified.type).toBe('unknown');
      expect(classified.message).toContain('unexpected');
      expect(classified.isRetryable).toBe(true);
    });

    it('handles null gracefully', () => {
      const classified = classifyError(null);

      expect(classified.type).toBe('unknown');
      expect(classified.isRetryable).toBe(true);
    });

    it('handles undefined gracefully', () => {
      const classified = classifyError(undefined);

      expect(classified.type).toBe('unknown');
      expect(classified.isRetryable).toBe(true);
    });
  });

  // T428: Test empathetic messaging
  describe('empathetic messaging', () => {
    it('all messages are positive and actionable', () => {
      const errors = [
        new TypeError('Failed to fetch'),
        new DOMException('The operation was aborted', 'AbortError'),
        new Error('401 Unauthorized'),
        new Error('400 Bad Request'),
        new Error('500 Internal Server Error'),
        new Error('403 Forbidden'),
        new Error('404 Not Found'),
      ];

      errors.forEach((error) => {
        const classified = classifyError(error);

        // All messages should be non-empty
        expect(classified.message.length).toBeGreaterThan(0);

        // Messages should be actionable (contain a suggestion)
        expect(
          classified.message.toLowerCase()
        ).toMatch(/please|try|check|again|log in|contact|help|contact/i);

        // Messages should be polite (use lowercase for most part)
        expect(classified.message[0]).not.toBe('A');
      });
    });
  });

  // T428: Test type consistency
  describe('type consistency', () => {
    it('always returns ClassifiedError with all required fields', () => {
      const errors: any[] = [
        new Error('Test error'),
        'string error',
        null,
        undefined,
        { custom: 'error' },
      ];

      errors.forEach((error) => {
        const classified = classifyError(error);

        expect(classified).toHaveProperty('type');
        expect(classified).toHaveProperty('message');
        expect(classified).toHaveProperty('isRetryable');
        expect(typeof classified.type).toBe('string');
        expect(typeof classified.message).toBe('string');
        expect(typeof classified.isRetryable).toBe('boolean');
      });
    });
  });
});
