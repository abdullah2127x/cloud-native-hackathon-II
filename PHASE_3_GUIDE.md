# Phase 3: AI-Powered Todo Chatbot - Implementation Guide

This guide provides a step-by-step roadmap for building Phase 3. You already have a working Next.js frontend and FastAPI backend from Phase 2. Now we're adding an AI chatbot layer that lets users manage tasks through natural language conversation.

---

## Overview: What Phase 3 Adds

**Phase 2 (What you have):** User clicks buttons → API calls → Database updates
**Phase 3 (What we're building):** User types messages → AI interprets intent → Calls tools → Database updates → AI responds

The key difference: instead of a traditional UI, users have a conversation with an AI assistant that understands task-related commands.

---

## The 3 Reusable Skills to Create

Creating these skills now sets you up for bonus points and future projects.

### Skill 1: openai-chatkit
**Purpose:** Best practices for integrating OpenAI's ChatKit UI library into Next.js applications.

**What it does:**
- Scaffolds ChatKit setup with proper authentication
- Manages domain allowlist configuration for production deployment
- Handles conversation state between frontend and backend
- Provides TypeScript patterns for ChatKit integration
- Manages message history UI and loading states

**When you use it:** Frontend setup, ChatKit component integration

**Reusability:** High - Any Next.js project needing ChatKit can use this

**Bonus points:** Yes, part of "Reusable Intelligence"

### Skill 2: openai-agents-sdk
**Purpose:** Best practices for integrating OpenAI's Agents SDK with OpenRouter support (for cost-effective API calls).

**What it does:**
- Initializes OpenAI Agents SDK with OpenRouter provider configuration
- Defines agent system prompts and tool registration patterns
- Implements stateless agent execution (no memory between requests)
- Handles natural language intent mapping to MCP tools
- Error handling and graceful fallbacks for failed tool calls
- Token counting and cost optimization with OpenRouter

**When you use it:** Backend AI logic, agent configuration

**Reusability:** High - Pattern works for any task automation with OpenAI agents

**Bonus points:** Yes, part of "Reusable Intelligence"

### Skill 3: mcp-tool-builder
**Purpose:** Best practices for building and testing MCP servers that expose application operations as tools for AI agents.

**What it does:**
- Scaffolds MCP server structure with Official MCP SDK
- Generates tool definitions from function signatures
- Implements request/response validation
- Testing patterns for MCP tools
- Tool composition patterns (tools that call other tools)
- Error handling within MCP tools

**When you use it:** MCP server setup, tool creation

**Reusability:** Very High - MCP is becoming standard for AI integration

**Bonus points:** Yes, part of "Reusable Intelligence"

---

## Implementation Workflow: Step-by-Step

This is the order you should follow. Each step depends on the previous ones.

### Phase 3A: Foundation (Database & Backend Setup)
These are the prerequisite steps before building any specs.

**Step 1: Extend Database Schema**
- Add two new tables to your Neon PostgreSQL database
- Create `Conversation` table to store chat sessions
- Create `Message` table to store chat history
- Set up proper indexes for user filtering
- Run migrations on your database
- Update your SQLModel models in FastAPI

**Why first?** Everything else depends on storing conversation data. Without this, you have nowhere to persist chat history.

**What you're doing:**
- Writing migration files
- Creating SQLModel table definitions
- Testing database connectivity

---

### Phase 3B: Build the MCP Server (Backend Core)
This is the brain of your chatbot. The MCP server exposes your task operations as tools.

**Step 2: Create MCP Server Structure**
- Set up a new MCP server using Official MCP SDK
- Create the entry point and initialization
- Define the 5 core tools
- Set up environment configuration

**Step 3: Implement the 5 MCP Tools**
These tools are how the AI agent interacts with your todo system:

1. **add_task tool**
   - Takes: user_id, title, description (optional)
   - Returns: task_id, status, title
   - Database operation: INSERT into tasks table
   - Error handling: Validate title length, user exists

2. **list_tasks tool**
   - Takes: user_id, status filter (all/pending/completed)
   - Returns: Array of task objects
   - Database operation: SELECT from tasks WHERE user_id = ? AND status matches filter
   - Error handling: Handle empty results gracefully

3. **complete_task tool**
   - Takes: user_id, task_id
   - Returns: task_id, status, title
   - Database operation: UPDATE tasks SET completed = true
   - Error handling: Task must exist and belong to user

4. **delete_task tool**
   - Takes: user_id, task_id
   - Returns: task_id, status, title
   - Database operation: DELETE from tasks
   - Error handling: Task must exist and belong to user

5. **update_task tool**
   - Takes: user_id, task_id, title (optional), description (optional)
   - Returns: task_id, status, title
   - Database operation: UPDATE tasks SET title/description
   - Error handling: At least one field must be provided

**Step 4: Test MCP Tools Independently**
- Create test cases for each tool
- Test with different user_ids to ensure isolation
- Test error cases (missing tasks, wrong users)
- Verify tool responses match expected format

**Why this order?** MCP tools are stateless and directly access the database. By building these before the agent, you ensure the tools work correctly before the agent depends on them.

---

### Phase 3C: Integrate AI Agent (Backend Logic)
Now the AI learns to use the MCP tools.

**Step 5: Set Up OpenAI Agents SDK**
- Install OpenAI Agents SDK dependencies
- Configure OpenRouter provider (for cost-effective API calls)
- Set up environment variables for API keys
- Create agent initialization code

**Step 6: Configure Agent Behavior**
- Define system prompt: "You are a helpful todo assistant. Help users manage their tasks..."
- Register the 5 MCP tools with the agent
- Set up tool calling rules (when to call which tool)
- Configure error handling for failed tool calls

**Step 7: Implement Chat Endpoint**
This is the single entry point for conversations:
- Endpoint: POST /api/{user_id}/chat
- Receives: conversation_id (optional), message (required)
- Process:
  1. Fetch conversation history from database
  2. Build message array (history + new message)
  3. Store user message in database
  4. Run agent with MCP tools
  5. Agent calls appropriate tools
  6. Store assistant response in database
  7. Return response to client
  8. Forget everything (stateless = ready for next request)

**Step 8: Test Agent with MCP Tools**
- Test natural language commands like "add a task to buy groceries"
- Test tool calling: verify agent calls correct tool
- Test error handling: what happens when task not found
- Test conversation context: does it remember previous messages

**Why this order?** The agent needs working MCP tools before it can do anything. Database stores conversation history. Chat endpoint orchestrates everything.

---

### Phase 3D: Build Conversational Frontend
Now users see the beautiful interface.

**Step 9: Set Up OpenAI ChatKit**
- Install ChatKit dependencies
- Configure domain allowlist on OpenAI platform
- Set up ChatKit component in Next.js
- Handle authentication token passing

**Step 10: Connect ChatKit to Backend**
- ChatKit sends messages to /api/{user_id}/chat endpoint
- Attach JWT token from Better Auth to requests
- Display AI responses in chat bubbles
- Show loading state while agent is thinking
- Handle conversation continuation (passing conversation_id)

**Step 11: Style and Polish**
- Add loading indicators
- Show error messages gracefully
- Auto-scroll to latest message
- Add message timestamps
- Test on mobile

**Why last?** Frontend is just the presentation layer. Everything happens in the backend. Once backend is solid, frontend is straightforward.

---

## The 4 Specifications: What Goes in Each

These specs are your detailed blueprints. Each one guides the implementation of its section.

### Specification 1: Chat Persistence
**Focus:** Database design and chat endpoint implementation

**What's defined:**
- Database table schemas:
  - Conversation table (id, user_id, created_at, updated_at)
  - Message table (id, conversation_id, user_id, role, content, created_at)
  - Relationships and indexes
- Chat endpoint specification:
  - POST /api/{user_id}/chat
  - Request body: {conversation_id?, message}
  - Response body: {conversation_id, response, tool_calls}
  - Error responses (401, 400, 500)
- State management:
  - How conversation history is fetched
  - How messages are stored
  - User isolation logic (user_id filtering)
- Stateless principles:
  - Why server doesn't cache conversations
  - How each request is independent
  - How horizontal scaling works

**Implementation steps from this spec:**
1. Create migration files for new tables
2. Define SQLModel classes
3. Create database connection/session logic
4. Implement chat endpoint handler
5. Write query functions for conversation retrieval

**Testing covered:**
- Database table creation
- Message storage and retrieval
- User isolation (user A can't see user B's messages)
- Conversation creation and continuation
- Error cases (invalid user_id, missing conversation)

---

### Specification 2: MCP Tools
**Focus:** Tool definitions and implementation

**What's defined:**
- Tool schema for each of the 5 tools:
  - Input parameters and types
  - Output format
  - Error cases
  - Example inputs and outputs
- Tool implementation details:
  - Which database operations each tool performs
  - Validation rules (e.g., title max 200 chars)
  - User isolation enforcement
  - Error messages
- Tool composition patterns:
  - When tools call each other (e.g., delete task requires finding task first)
  - Tool ordering and dependencies

**Example: Add Task tool specification**
```
Name: add_task
Input: {user_id: string, title: string, description?: string}
Output: {task_id: int, status: "created", title: string}
Database: INSERT INTO tasks (user_id, title, description, created_at, updated_at, completed)
Validation: title must be 1-200 chars, user_id must exist
Error cases:
  - Empty title: "Task title cannot be empty"
  - User not found: "Invalid user"
  - Database error: "Failed to create task, try again"
```

**Implementation steps from this spec:**
1. Create MCP server file structure
2. Define tool schemas using MCP SDK
3. Implement each tool function
4. Add database queries for each tool
5. Implement error handling and validation
6. Create tool tests

**Testing covered:**
- Each tool in isolation
- Tool parameter validation
- Database operations
- User isolation
- Error handling

---

### Specification 3: AI Agent
**Focus:** Agent behavior and natural language understanding

**What's defined:**
- Agent system prompt:
  - How agent should introduce itself
  - Personality and tone
  - When to use which tool
  - How to handle errors
- Tool mapping rules:
  - User says "add a task" → use add_task tool
  - User says "show me tasks" → use list_tasks tool
  - User says "mark done" → use complete_task tool
  - User says "delete" → use delete_task tool
  - User says "change" → use update_task tool
- Conversation flow:
  - How agent confirms actions
  - How agent handles ambiguous requests
  - How agent recovers from tool errors
  - How agent maintains conversation context
- Natural language examples:
  - Various ways users might phrase requests
  - How agent should interpret them
  - Expected tool calls for each

**Example mappings:**
```
User: "I need to buy groceries"
Agent interpretation: Add new task
Tool call: add_task(user_id=?, title="Buy groceries")

User: "What's pending?"
Agent interpretation: List incomplete tasks
Tool call: list_tasks(user_id=?, status="pending")

User: "Done with the meeting"
Agent interpretation: Complete task (but which one?)
Tool call: First list_tasks to find "meeting" task, then complete_task
```

**Implementation steps from this spec:**
1. Install OpenAI Agents SDK
2. Configure OpenRouter provider
3. Write system prompt
4. Register MCP tools with agent
5. Implement chat endpoint agent logic
6. Add response post-processing (formatting agent output)
7. Implement error recovery

**Testing covered:**
- Agent understanding of natural language
- Correct tool calling
- Error handling when tool fails
- Conversation context preservation
- Token usage and costs

---

### Specification 4: Chat Interface
**Focus:** User-facing conversational UI

**What's defined:**
- ChatKit integration:
  - Component placement in Next.js
  - Props and configuration
  - Domain allowlist requirements
- Message display:
  - User message bubbles (on right, blue)
  - Assistant message bubbles (on left, gray)
  - System message handling
  - Timestamps and metadata
- Interaction flows:
  - User types message → sends to backend
  - Shows loading state while waiting
  - Receives response → displays in chat
  - Auto-scroll to latest
  - Option to continue conversation
- Error handling UI:
  - Network errors: "Connection failed, try again"
  - Server errors: "Something went wrong"
  - Empty response: "I didn't understand, could you rephrase?"
- Authentication:
  - Pass JWT token from Better Auth
  - Handle unauthorized (redirect to login)
  - New conversation vs. continuing conversation

**Implementation steps from this spec:**
1. Install ChatKit dependencies
2. Create ChatKit component
3. Connect to chat endpoint
4. Handle authentication (JWT token)
5. Manage conversation state (conversation_id)
6. Style message bubbles
7. Add loading indicators
8. Test on mobile

**Testing covered:**
- ChatKit renders correctly
- Messages send and receive
- Error messages display
- Conversation continues across page reloads
- Authentication works

---

## Putting It All Together: The Complete Flow

Here's what happens when a user says "Add a task to buy groceries":

1. **Frontend (Step 1):** User types "Add a task to buy groceries" and clicks send
2. **Frontend (Step 2):** ChatKit sends message to backend: `POST /api/{user_id}/chat` with message and JWT token
3. **Backend (Step 1):** Chat endpoint receives request, extracts user_id from token
4. **Backend (Step 2):** Fetch conversation history from database (Conversation and Message tables)
5. **Backend (Step 3):** Build message array: [...past messages, {role: "user", content: "Add a task..."}]
6. **Backend (Step 4):** Store user message in database
7. **Backend (Step 5):** Run OpenAI Agent with message array and MCP tools registered
8. **Backend (Step 6):** Agent analyzes message: "This is a task creation request"
9. **Backend (Step 7):** Agent calls add_task MCP tool with title="Buy groceries"
10. **Backend (Step 8):** MCP tool executes: `INSERT INTO tasks (user_id, title, completed, created_at) VALUES (...)`
11. **Backend (Step 9):** Tool returns: `{task_id: 42, status: "created", title: "Buy groceries"}`
12. **Backend (Step 10):** Agent formats response: "I've added 'Buy groceries' to your task list"
13. **Backend (Step 11):** Store assistant response in database
14. **Backend (Step 12):** Return response to frontend: `{conversation_id: 5, response: "I've added...", tool_calls: ["add_task"]}`
15. **Frontend (Step 3):** ChatKit displays agent response in conversation
16. **Frontend (Step 4):** User sees the confirmation and can continue chatting

All conversation data is in the database. Server holds no state. Ready for next request.

---

## Getting Started: Immediate Next Steps

### Before you write any code:

1. **Read the 4 specifications carefully** (we'll create them next)
   - Understand the database schema
   - Know what MCP tools need to do
   - Understand agent behavior expectations
   - See what ChatKit integration looks like

2. **Set up the 3 skills** (we'll create these as templates)
   - Study openai-chatkit best practices
   - Learn openai-agents-sdk patterns with OpenRouter
   - Understand mcp-tool-builder workflow

3. **Verify your Phase 2 setup**
   - Next.js frontend is running
   - FastAPI backend is running
   - Better Auth is working
   - Database is accessible

### Then follow the implementation workflow:
1. Extend database (Chat Persistence spec)
2. Build MCP tools (MCP Tools spec)
3. Create chat endpoint and agent (AI Agent spec)
4. Add ChatKit UI (Chat Interface spec)

---

## Dependencies & Ordering

Some things must happen before others:

```
Database Schema
    ↓
MCP Tools (depend on database)
    ↓
Chat Endpoint + Agent (depend on MCP tools)
    ↓
ChatKit Frontend (depends on chat endpoint)
```

**Do NOT do this:**
- ❌ Build ChatKit before backend is ready (no endpoint to call)
- ❌ Build agent before MCP tools exist (nothing to call)
- ❌ Build MCP tools before database schema (nowhere to store data)

**Do this:**
- ✅ Database first
- ✅ MCP tools second
- ✅ Agent and endpoint third
- ✅ Frontend last

---

## Success Criteria

You'll know Phase 3 is complete when:

✅ Users can open ChatKit conversation
✅ Users can type "Add a task to buy groceries"
✅ AI responds: "I've added 'Buy groceries' to your list"
✅ Task appears in the database
✅ Users can continue conversation in same chat
✅ If they reload, conversation history is still there
✅ Each user only sees their own tasks
✅ Natural language variations work ("add a task", "remember to...", "create todo")
✅ Errors handled gracefully ("Task not found", "Invalid request")

---

## Key Principles to Remember

### Stateless is King
Your server should have **no memory** between requests. Every request fetches everything it needs from the database and returns everything the client needs. This makes it infinitely scalable.

### MCP Tools are the Boundary
All database access should go through MCP tools. The agent never directly touches the database. This keeps concerns separated and makes testing easier.

### User Isolation is Security
Every tool call includes user_id. Every database query filters by user_id. User A can never see User B's data.

### Natural Language is Fuzzy
Users will say things in unexpected ways. Your system prompt should be flexible about interpretation. When unsure, ask for clarification.

---

## Resources

- OpenAI ChatKit docs: https://platform.openai.com/docs/guides/chatkit
- OpenAI Agents SDK: https://github.com/openai/agents-sdk
- MCP Official SDK: https://github.com/modelcontextprotocol/python-sdk
- OpenRouter (cheaper API): https://openrouter.ai
- Better Auth: Your Phase 2 implementation reference

---

## Questions to Ask Yourself Before Starting

1. Do I have a working database with tasks table? ✅
2. Do I understand how JWT token flows work? ✅
3. Have I read the 4 specs carefully? (Do this before coding)
4. Do I have OpenAI API keys set up? (Use OpenRouter instead of direct API)
5. Is my Phase 2 code ready to extend?

If all are ✅, you're ready to start.

Good luck! The hardest part is understanding the architecture. The coding is straightforward once you know what to build.
