'use client';

import { useChat } from 'ai/react';
import { useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { ChatBubble } from '../components/chat-bubble';

export default function Home() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
    headers: {
      'Content-Type': 'application/json',
    },
    body: {
      user_id: 'web_user',
    },
    onResponse: (response) => {
      // Handle the response if needed
      console.log('Response received:', response);
    },
    onError: (error) => {
      console.error('Chat error:', error);
      alert('An error occurred while processing your request.');
    }
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleSubmit(e);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm py-4 px-6 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">Ketamine Therapy AI</h1>
        <a
          href="/admin"
          className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
        >
          Admin
        </a>
      </header>

      {/* Chat Container */}
      <div className="flex-1 overflow-y-auto p-4 pb-20">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.length === 0 ? (
            <div className="text-center py-10">
              <div className="mx-auto bg-gray-100 rounded-full p-3 w-12 h-12 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-bot-message-square text-gray-400">
                  <path d="M12 6V2H8"/>
                  <path d="m8 18-2 3v1H3v-1l2-3"/>
                  <path d="M16 2h3a1 1 0 0 1 1 1v1l-2 3"/>
                  <rect x="2" y="6" width="20" height="12" rx="2"/>
                  <path d="M8 12h.01"/>
                  <path d="M12 12h.01"/>
                  <path d="M16 12h.01"/>
                </svg>
              </div>
              <h2 className="mt-4 text-lg font-medium text-gray-900">
                Welcome to Ketamine Therapy AI
              </h2>
              <p className="mt-2 text-gray-500">
                Ask me anything about ketamine therapy, its benefits, risks, and applications.
              </p>
            </div>
          ) : (
            messages.map((message) => (
              <ChatBubble
                key={message.id}
                variant={message.role === 'user' ? 'user' : 'ai'}
              >
                {message.content}
              </ChatBubble>
            ))
          )}

          {/* Loading indicator when AI is thinking */}
          {isLoading && (
            <ChatBubble variant="ai">
              <div className="flex items-center gap-2">
                <div className="flex space-x-1">
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce delay-75"></div>
                  <div className="h-2 w-2 bg-gray-500 rounded-full animate-bounce delay-150"></div>
                </div>
              </div>
            </ChatBubble>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area - Fixed at the bottom */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-4 px-4">
        <form
          onSubmit={onSubmit}
          className="max-w-3xl mx-auto flex gap-2"
        >
          <input
            value={input}
            onChange={handleInputChange}
            placeholder="Ask about ketamine therapy..."
            className="flex-1 border border-gray-300 rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-500 text-white rounded-full p-3 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="h-5 w-5" />
          </button>
        </form>

        {/* Disclaimer Footer */}
        <div className="max-w-3xl mx-auto mt-3 text-center text-xs text-gray-500">
          This AI is for educational purposes only. It is not a substitute for professional medical advice.
        </div>
      </div>
    </div>
  );
}
