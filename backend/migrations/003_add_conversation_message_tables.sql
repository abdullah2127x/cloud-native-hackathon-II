-- Migration 003: Add conversation and message tables for chat interface
-- Created: 2026-02-04
-- Feature: 001-chat-interface
-- Task IDs: T005, T006

-- Step 1: Create conversation table
CREATE TABLE conversation (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL REFERENCES "user"(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Index on user_id for filtering user's conversations
CREATE INDEX idx_conversation_user_id ON conversation(user_id);

-- Step 2: Create message table
CREATE TABLE message (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    conversation_id VARCHAR(36) NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Indexes for message queries
CREATE INDEX idx_message_user_id ON message(user_id);
CREATE INDEX idx_message_conversation_id ON message(conversation_id);
CREATE INDEX idx_message_created_at ON message(created_at);

-- Rollback Instructions:
-- To rollback this migration, run:
-- DROP TABLE message;
-- DROP TABLE conversation;
