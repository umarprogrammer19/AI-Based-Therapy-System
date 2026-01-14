# Quickstart Guide: Chat Interface (Home Page)

## Overview
Quickstart guide for implementing and testing the chat interface with streaming responses.

## Prerequisites
- Node.js 18+
- npm or yarn package manager
- Backend server running on http://localhost:8000
- Next.js 16 development environment

## Setup
1. Navigate to the frontend directory: `cd frontend`
2. Install dependencies: `npm install` (includes Next.js, Vercel AI SDK, Tailwind CSS, Lucide React)
3. Ensure backend API is running at http://localhost:8000/api/chat
4. Verify API connectivity by testing the endpoint directly

## Implementation Steps

### Step 1: Create Chat Page Component
1. Create `src/app/page.tsx` with the main chat interface
2. Implement the useChat hook from Vercel AI SDK
3. Add proper styling for message bubbles (blue for user, gray for AI)
4. Implement auto-scrolling to the latest message

### Step 2: Add Streaming Response Logic
1. Configure the useChat hook to connect to /api/chat
2. Implement character-by-character streaming display
3. Add loading indicators during API requests
4. Handle error states gracefully

### Step 3: Implement UI Elements
1. Create header with "Ketamine Therapy AI" and admin link
2. Design fixed input area at the bottom with text input and send button
3. Add medical disclaimer footer
4. Implement responsive design for all screen sizes

### Step 4: Create API Route
1. Create `src/app/api/chat/route.ts` to proxy requests to backend
2. Handle CORS and authentication if needed
3. Implement proper error handling and response formatting

### Step 5: Add Admin Interface
1. Create `src/app/admin/page.tsx` for admin functionality
2. Implement navigation between chat and admin interfaces
3. Add basic admin dashboard layout

## Testing
1. Test chat functionality with various ketamine therapy questions
2. Verify streaming responses work correctly
3. Test loading states and error handling
4. Verify medical disclaimer is visible
5. Test navigation between chat and admin interfaces
6. Validate responsive design on mobile devices

## Example Usage
1. Start the development server: `npm run dev`
2. Open http://localhost:3000
3. Type a question about ketamine therapy in the input field
4. Submit and observe the streaming response from the AI
5. Verify message bubbles display with correct colors

## Expected Behavior
- Messages appear in blue bubbles for user input
- AI responses appear in gray bubbles with streaming effect
- Loading indicators show when AI is processing
- Medical disclaimer is visible at the bottom
- Header includes link to admin interface
- Input area remains fixed at the bottom of the screen

## Troubleshooting
- Verify backend API is running and accessible
- Check network tab for API request/response details
- Ensure all required dependencies are installed
- Verify environment configurations
- Confirm proper CORS settings if running in production