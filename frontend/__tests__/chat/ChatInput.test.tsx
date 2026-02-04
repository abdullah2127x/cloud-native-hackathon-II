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

  it('disables submission when disabled prop is true', async () => {
    const user = userEvent.setup();
    const mockOnSend = jest.fn();

    render(<ChatInput onSend={mockOnSend} disabled={true} />);

    const input = screen.getByPlaceholderText(/type your message/i);
    const button = screen.getByRole('button', { name: /send/i });

    expect(input).toBeDisabled();
    expect(button).toBeDisabled();

    await user.type(input, 'Test');
    expect(mockOnSend).not.toHaveBeenCalled();
  });
});
