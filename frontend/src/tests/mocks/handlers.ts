// MSW request handlers for API mocking
import { http, HttpResponse } from 'msw';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const handlers = [
  // Health check
  http.get(`${API_URL}/health`, () => {
    return HttpResponse.json({ status: 'ok' });
  }),

  // Get all tasks
  http.get(`${API_URL}/api/todos`, () => {
    return HttpResponse.json([
      {
        id: 'task-1',
        user_id: 'test-user-id',
        title: 'Test Task 1',
        description: 'Description 1',
        completed: false,
        created_at: new Date().toISOString(),
      },
      {
        id: 'task-2',
        user_id: 'test-user-id',
        title: 'Test Task 2',
        description: null,
        completed: true,
        created_at: new Date().toISOString(),
      },
    ]);
  }),

  // Get task by ID
  http.get(`${API_URL}/api/todos/:id`, ({ params }) => {
    const { id } = params;
    return HttpResponse.json({
      id,
      user_id: 'test-user-id',
      title: 'Test Task',
      description: 'Test Description',
      completed: false,
      created_at: new Date().toISOString(),
    });
  }),

  // Create task
  http.post(`${API_URL}/api/todos`, async ({ request }) => {
    const body = await request.json();
    return HttpResponse.json(
      {
        id: 'new-task-id',
        user_id: 'test-user-id',
        ...(body as object),
        completed: false,
        created_at: new Date().toISOString(),
      },
      { status: 201 }
    );
  }),

  // Update task
  http.patch(`${API_URL}/api/todos/:id`, async ({ params, request }) => {
    const { id } = params;
    const body = await request.json();
    return HttpResponse.json({
      id,
      user_id: 'test-user-id',
      title: 'Test Task',
      description: 'Test Description',
      completed: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ...(body as object),
    });
  }),

  // Toggle task completion
  http.post(`${API_URL}/api/todos/:id/toggle`, ({ params }) => {
    const { id } = params;
    return HttpResponse.json({
      id,
      user_id: 'test-user-id',
      title: 'Test Task',
      description: 'Test Description',
      completed: true,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    });
  }),

  // Delete task
  http.delete(`${API_URL}/api/todos/:id`, () => {
    return new HttpResponse(null, { status: 204 });
  }),
];
