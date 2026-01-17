// User-facing messages

export const ERROR_MESSAGES = {
  // Network errors
  NETWORK_ERROR: 'Unable to connect to server. Please check your internet connection.',
  TIMEOUT_ERROR: 'Request timed out. Please try again.',
  SERVER_ERROR: 'Something went wrong on our end. Please try again later.',

  // Authentication errors
  SESSION_EXPIRED: 'Your session has expired. Please sign in again.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  AUTHENTICATION_REQUIRED: 'Please sign in to continue.',

  // Validation errors
  VALIDATION_ERROR: 'Please check your input and try again.',
  REQUIRED_FIELD: 'This field is required.',
  INVALID_EMAIL: 'Please enter a valid email address.',
  PASSWORD_TOO_SHORT: 'Password must be at least 8 characters long.',

  // Task errors
  TASK_NOT_FOUND: 'Task not found.',
  TASK_CREATE_ERROR: 'Failed to create task. Please try again.',
  TASK_UPDATE_ERROR: 'Failed to update task. Please try again.',
  TASK_DELETE_ERROR: 'Failed to delete task. Please try again.',
} as const;

export const SUCCESS_MESSAGES = {
  TASK_CREATED: 'Task created successfully!',
  TASK_UPDATED: 'Task updated successfully!',
  TASK_DELETED: 'Task deleted successfully!',
  SIGN_IN_SUCCESS: 'Welcome back!',
  SIGN_UP_SUCCESS: 'Account created successfully!',
  SIGN_OUT_SUCCESS: 'You have been signed out.',
} as const;

export const CONFIRMATION_MESSAGES = {
  DELETE_TASK: 'Are you sure you want to delete this task? This action cannot be undone.',
  DISCARD_CHANGES: 'Are you sure you want to discard your changes?',
} as const;
