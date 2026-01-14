# Feature Specification: Chat Endpoint with RAG

**Feature Branch**: `003-chat-rag`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "@.claude/agents/rag-engineer.md I want to build the Chat Endpoint with RAG.

**Requirements**:
1. **Endpoint**: `POST /api/chat`.
2. **Logic**:
   - [cite_start]**Guardrail**: Check if user query is off-topic[cite: 17].
   - **Retrieval**: Convert query to vector. Search `VectorChunk` for top 3 matches using `pgvector` distance.
   - **Generation**: Send System Prompt + Context + Query to Mistral.
   - [cite_start]**System Prompt**: \"You are a Ketamine Assistant. Use ONLY the provided context. If context is missing, say you don't know.\"[cite: 88]. use mistral larger model (branch name starts with 003)"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.

  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Chat with Knowledge Base (Priority: P1)

End users need to interact with a chatbot that can answer questions based on the ketamine therapy knowledge base. The system receives user queries, retrieves relevant information from the vector database, and generates contextual responses using the Mistral AI model.

**Why this priority**: This is the core functionality that delivers value to users by enabling them to get accurate information about ketamine therapy from the knowledge base.

**Independent Test**: Can be fully tested by sending a query to the chat endpoint and verifying that the response is generated using context from the vector database and follows the system prompt guidelines.

**Acceptance Scenarios**:

1. **Given** user submits a ketamine therapy related query, **When** they call the POST /api/chat endpoint, **Then** the system returns a response based on relevant context from the knowledge base
2. **Given** user submits a query unrelated to ketamine therapy, **When** they call the POST /api/chat endpoint, **Then** the system responds with a guardrail message indicating the topic is off-topic

---

### User Story 2 - Context Retrieval and Ranking (Priority: P2)

For each user query, the system needs to convert the query to a vector representation and retrieve the most relevant information chunks from the vector database using pgvector similarity search.

**Why this priority**: This is essential for the RAG functionality, enabling the system to find and use the most relevant information for generating responses.

**Independent Test**: Can be tested by submitting a query and verifying that the system retrieves the top 3 most relevant context chunks from the vector database.

**Acceptance Scenarios**:

1. **Given** user submits a query, **When** the system processes the request, **Then** it retrieves the top 3 most relevant VectorChunk records using pgvector distance search

---

### User Story 3 - Response Generation with Context (Priority: P3)

The system combines the retrieved context with the user query and system prompt to generate a coherent, informative response using the Mistral AI model.

**Why this priority**: This completes the RAG loop by generating responses that are grounded in the knowledge base while following the specified system prompt.

**Independent Test**: Can be tested by verifying that responses are generated using the retrieved context and adhere to the system prompt guidelines.

**Acceptance Scenarios**:

1. **Given** relevant context chunks are retrieved, **When** the system generates a response, **Then** it uses the Mistral model with the system prompt, context, and user query to produce the response

---

### Edge Cases

- What happens when no relevant context is found in the vector database?
- How does system handle malformed queries or invalid input?
- What occurs if the Mistral API is unavailable or returns an error?
- How does the system handle extremely long queries that exceed model token limits?
- What happens when the vector database is temporarily unavailable?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST provide a POST /api/chat endpoint for user queries
- **FR-002**: System MUST implement guardrail logic to detect off-topic queries about ketamine therapy
- **FR-003**: System MUST convert user queries to vector embeddings for similarity search
- **FR-004**: System MUST retrieve top 3 most relevant VectorChunk records using pgvector distance search
- **FR-005**: System MUST generate responses using Mistral AI model with system prompt, context, and user query
- **FR-006**: System MUST follow the system prompt: "You are a Ketamine Assistant. Use ONLY the provided context. If context is missing, say you don't know."
- **FR-007**: System MUST return appropriate error responses when services are unavailable
- **FR-008**: System MUST handle queries up to 1000 characters in length
- **FR-009**: System MUST respond to queries within 10 seconds under normal load
- **FR-010**: System MUST return responses in JSON format with message and metadata

*Example of marking unclear requirements:*

- **FR-011**: System MUST use Mistral 7B or larger model for response generation

### Key Entities *(include if feature involves data)*

- **ChatQuery**: Represents a user's input query with metadata such as timestamp and user ID
- **ChatResponse**: Contains the generated response with context references and confidence indicators
- **VectorChunk**: Existing entity that contains text content and vector embeddings for similarity search

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can submit queries to the chat endpoint and receive relevant responses within 10 seconds 95% of the time
- **SC-002**: System successfully retrieves relevant context for 90% of ketamine therapy related queries
- **SC-003**: 85% of generated responses are rated as helpful and accurate by users
- **SC-004**: System properly detects and responds to off-topic queries with appropriate guardrail messages 98% of the time
- **SC-005**: System maintains 99% uptime during peak usage hours
