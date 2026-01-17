// Test setup and configuration
import '@testing-library/jest-dom';
import { server } from './mocks/server';

// Establish API mocking before all tests
beforeAll(() => {
  server.listen({
    onUnhandledRequest: 'warn',
  });
});

// Reset any request handlers that we may add during the tests,
// so they don't affect other tests
afterEach(() => {
  server.resetHandlers();
});

// Clean up after the tests are finished
afterAll(() => {
  server.close();
});

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter() {
    return {
      push: jest.fn(),
      replace: jest.fn(),
      prefetch: jest.fn(),
      back: jest.fn(),
      pathname: '/',
      query: {},
      asPath: '/',
    };
  },
  usePathname() {
    return '/';
  },
  useSearchParams() {
    return new URLSearchParams();
  },
}));

// Mock Better Auth client
jest.mock('@/lib/auth-client', () => ({
  authClient: {
    getSession: jest.fn(() =>
      Promise.resolve({
        user: { id: 'test-user-id', email: 'test@example.com', name: 'Test User' },
        accessToken: 'mock-access-token',
      })
    ),
    signIn: jest.fn(),
    signOut: jest.fn(),
    signUp: jest.fn(),
  },
}));
