# Feature Specification: Chat Interface (Home Page)

**Feature Branch**: `004-chat-interface`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "@.claude/agents/frontend-lead.md I want to build the **Chat Interface** (The Home Page).

**Requirements**:
1. **Tech Stack**:
   - Next.js 16 (App Router).
   - Vercel AI SDK (`npm install ai`).
   - Tailwind CSS for styling.
   - Lucide React for icons.

2. **UI Layout**:
   - **Header**: "Ketamine Therapy AI" with a link to `/admin`.
   - **Main Chat Area**:
     - Centered chat window.
     - Message bubbles: Blue for User, Gray for AI.
     - **Streaming**: The AI response must type out character-by-character.
   - **Input Area**: Fixed at the bottom. Text input + Send button.
   - [cite_start]**Disclaimer Footer**: "This AI is for educational purposes only. It is not a substitute for professional medical advice."[cite: 95].

3. **Logic**:
   - Use the `useChat` hook from Vercel AI SDK.
   - Connect it to our backend endpoint: `http://localhost:8000/api/chat`.
   - Handle loading states (show a thinking bubble while RAG searches)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Chat Interface (Priority: P1)

A user visits the home page and interacts with the chat interface to ask questions about ketamine therapy. The user enters their question, submits it, and receives a streamed response from the AI that appears character-by-character. The user can see their question in blue bubbles and the AI response in gray bubbles.

**Why this priority**: This is the core functionality that delivers the primary value of the application - allowing users to interact with the AI system about ketamine therapy.

**Independent Test**: Can be fully tested by visiting the home page, entering a question about ketamine therapy, and verifying that the AI responds with a relevant answer in a streaming fashion with proper message bubbles.

**Acceptance Scenarios**:

1. **Given** user is on the home page, **When** user types a question about ketamine therapy and clicks send, **Then** the question appears in a blue bubble and the AI response streams character-by-character in a gray bubble.
2. **Given** user has submitted a question, **When** the AI is processing the request, **Then** a loading indicator appears showing the system is thinking.
3. **Given** user is viewing the chat interface, **When** the page loads, **Then** the header displays "Ketamine Therapy AI" with a link to the admin panel.

---

### User Story 2 - Navigate Between Pages (Priority: P2)

A user wants to access the admin panel from the chat interface. The user clicks the admin link in the header, which navigates them to the admin dashboard. From the admin panel, the user can return to the chat interface.

**Why this priority**: Essential for system administration and maintaining the knowledge base that powers the AI responses.

**Independent Test**: Can be tested by clicking the admin link in the header and verifying navigation to the admin page, then navigating back to the chat interface.

**Acceptance Scenarios**:

1. **Given** user is on the home page, **When** user clicks the admin link in the header, **Then** user is redirected to the admin dashboard.
2. **Given** user is on the admin dashboard, **When** user navigates back to the chat interface, **Then** user returns to the home page with the chat functionality available.

---

### User Story 3 - View Medical Disclaimer (Priority: P3)

A user needs to understand the limitations of the AI system. The user sees a clear disclaimer at the bottom of the chat interface that explains the AI is for educational purposes only and not a substitute for professional medical advice.

**Why this priority**: Critical for legal compliance and user safety regarding medical information.

**Independent Test**: Can be verified by checking that the medical disclaimer is visible and prominently displayed at the bottom of the chat interface.

**Acceptance Scenarios**:

1. **Given** user is on the home page, **When** user scrolls to the bottom of the interface, **Then** the medical disclaimer "This AI is for educational purposes only. It is not a substitute for professional medical advice." is visible.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a chat interface with message bubbles where user messages appear in blue and AI responses appear in gray
- **FR-002**: System MUST stream AI responses character-by-character to simulate typing
- **FR-003**: System MUST provide a text input field fixed at the bottom of the screen with a send button
- **FR-004**: System MUST connect to the backend API endpoint at `http://localhost:8000/api/chat` using the Vercel AI SDK
- **FR-005**: System MUST display loading indicators when the RAG system is searching for relevant information
- **FR-006**: System MUST display a header with "Ketamine Therapy AI" and a link to `/admin`
- **FR-007**: System MUST display a medical disclaimer at the bottom of the interface: "This AI is for educational purposes only. It is not a substitute for professional medical advice."
- **FR-008**: System MUST maintain the chat history in the current session and display messages in chronological order
- **FR-009**: System MUST handle errors gracefully and display appropriate user feedback when the backend is unavailable

### Key Entities *(include if feature involves data)*

- **Chat Messages**: Represent the conversation between user and AI, including content, timestamps, and sender identification
- **Chat Session**: Represents a single interaction session between user and the system, containing the message history

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can successfully submit questions and receive streamed responses in under 10 seconds average response time
- **SC-002**: 95% of user interactions result in successful message exchanges without system errors
- **SC-003**: The chat interface loads completely and is interactive within 3 seconds of page load
- **SC-004**: Users can see the medical disclaimer clearly and understand the limitations of the AI system