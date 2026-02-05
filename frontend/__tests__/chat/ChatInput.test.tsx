/**
 * ChatInput component tests.
 *
 * Task ID: T132
 * Spec: specs/001-chat-interface/spec.md
 */

import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ChatInput from '@/components/chat/ChatInput';

describe('ChatInput', () => {
  it('accepts text input', async () => {
    const user = userEvent.setup();
    const mockOnSend = jest.fn();

    render(<ChatInput onSend={mockOnSend} />);

    const input = screen.getByPlaceholderText(/type your message/i);
    await user.type(input, 'Hello world');

    expect(input).toHaveValue('Hello world');
  });

  it('submits on button click', async () => {
    const user = userEvent.setup();
    const mockOnSend = jest.fn();

    render(<ChatInput onSend={mockOnSend} />);

    const input = screen.getByPlaceholderText(/type your message/i);
    const button = screen.getByRole('button', { name: /send/i });

    await user.type(input, 'Test message');
    await user.click(button);

    expect(mockOnSend).toHaveBeenCalledWith('Test message');
  });

  it('submits on Enter key', async () => {
    const user = userEvent.setup();
    const mockOnSend = jest.fn();

    render(<ChatInput onSend={mockOnSend} />);

    const input = screen.getByPlaceholderText(/type your message/i);

    await user.type(input, 'Test message{Enter}');

    expect(mockOnSend).toHaveBeenCalledWith('Test message');
  });

  it('clears input after submit', async () => {
    const user = userEvent.setup();
    const mockOnSend = jest.fn();

    render(<ChatInput onSend={mockOnSend} />);

    const input = screen.getByPlaceholderText(/type your message/i);

    await user.type(input, 'Test message');
    await user.click(screen.getByRole('button', { name: /send/i }));

    expect(input).toHaveValue('');
  });

  it('disables send button but keeps input enabled when isLoading is true', async () => {
    const user = userEvent.setup();
    const mockOnSend = jest.fn();

    render(<ChatInput onSend={mockOnSend} isLoading={true} />);

    const input = screen.getByPlaceholderText(/waiting for response/i);
    const button = screen.getByRole('button');

    // Input should NOT be disabled - user can still type (FR-017)
    expect(input).not.toBeDisabled();
    // But button should be disabled
    expect(button).toBeDisabled();

    // User can type while loading
    await user.type(input, 'Test');
    expect(mockOnSend).not.toHaveBeenCalled();
  });
});
