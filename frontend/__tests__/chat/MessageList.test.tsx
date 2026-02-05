/**
 * MessageList component tests.
 *
 * Task ID: T131
 * Spec: specs/001-chat-interface/spec.md
 */

import { render, screen } from '@testing-library/react';
import MessageList from '@/components/chat/MessageList';

// Mock Virtuoso
jest.mock('react-virtuoso', () => ({
  Virtuoso: ({ data, itemContent, footer }: any) => (
    <div data-testid="virtuoso-list">
      {data.map((item: any, index: number) => (
        <div key={item.id}>{itemContent(index, item)}</div>
      ))}
      {footer && footer()}
    </div>
  ),
}));

describe('MessageList', () => {
  const mockMessages = [
    { id: '1', role: 'user', content: 'Hello' },
    { id: '2', role: 'assistant', content: 'Hi there!' },
    { id: '3', role: 'user', content: 'How are you?' },
  ];

  it('renders messages in correct order', () => {
    render(<MessageList messages={mockMessages} />);

    const messages = screen.getAllByText(/hello|hi there|how are you/i);
    expect(messages).toHaveLength(3);
    expect(messages[0]).toHaveTextContent('Hello');
    expect(messages[1]).toHaveTextContent('Hi there!');
    expect(messages[2]).toHaveTextContent('How are you?');
  });

  it('displays empty state when no messages', () => {
    render(<MessageList messages={[]} />);

    expect(screen.getByText(/start a conversation/i)).toBeInTheDocument();
  });

  it('renders user messages right-aligned', () => {
    render(<MessageList messages={[mockMessages[0]]} />);

    const messageContainer = screen.getByText('Hello').closest('div');
    expect(messageContainer?.parentElement).toHaveClass('justify-end');
  });

  it('renders assistant messages left-aligned', () => {
    render(<MessageList messages={[mockMessages[1]]} />);

    const messageContainer = screen.getByText('Hi there!').closest('div');
    expect(messageContainer?.parentElement).toHaveClass('justify-start');
  });

  it('displays typing indicator when isLoading is true', () => {
    render(<MessageList messages={mockMessages} isLoading={true} />);

    expect(screen.getByText(/ai is typing/i)).toBeInTheDocument();
  });

  it('hides typing indicator when isLoading is false', () => {
    render(<MessageList messages={mockMessages} isLoading={false} />);

    expect(screen.queryByText(/ai is typing/i)).not.toBeInTheDocument();
  });
});
