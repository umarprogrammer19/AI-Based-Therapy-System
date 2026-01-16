'use client';

import { useRef, useEffect, useState } from 'react';
import { Send, Upload, FileText, User } from 'lucide-react';
import { ChatBubble } from '../components/chat-bubble';
import { useAuth } from '../contexts/AuthContext';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const { user, isAuthenticated, isLoading: isAuthLoading } = useAuth();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    // Add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Send message directly to backend API
      const backendBaseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

      // For anonymous users, use a simpler request without auth
      let response;
      if (isAuthenticated) {
        const token = localStorage.getItem('token');
        response = await fetch(`${backendBaseUrl}/api/chat/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,
          },
          body: JSON.stringify({
            query: content,
          }),
        });
      } else {
        // Anonymous chat request (this will work if the backend allows it)
        response = await fetch(`${backendBaseUrl}/api/chat/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            query: content,
            user_id: 'anonymous'
          }),
        });
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Add AI response
      const aiMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.message || data.response || 'No response from AI',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Chat error:', error);
      alert('An error occurred while processing your request.');

      // Add error message
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setUploadStatus(null);
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile || !isAuthenticated) return;

    setUploadStatus('Uploading...');
    const token = localStorage.getItem('token');

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const backendBaseUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${backendBaseUrl}/api/user-docs/upload`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setUploadStatus('Upload successful!');
        // Reset selected file
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = '';
        }
      } else {
        setUploadStatus(`Error: ${result.detail || 'Upload failed'}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('Error: Failed to upload file');
    }
  };

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      sendMessage(input);
    }
  };

  if (isAuthLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm py-4 px-6 flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">Ketamine Therapy AI</h1>
        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
            <>
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-gray-600" />
                <span className="text-sm text-gray-600">{user?.username}</span>
              </div>
              <a
                href="/admin"
                className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
              >
                Admin
              </a>
            </>
          ) : (
            <div className="flex space-x-2">
              <a
                href="/login"
                className="text-blue-600 hover:text-blue-800 text-sm font-medium transition-colors"
              >
                Login
              </a>
              <a
                href="/register"
                className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-md text-sm font-medium transition-colors"
              >
                Register
              </a>
            </div>
          )}
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 overflow-y-auto p-4 pb-32">
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

      {/* File Upload Section - Above Input Area */}
      {isAuthenticated && (
        <div className="fixed bottom-20 left-0 right-0 bg-white border-t border-gray-200 py-4 px-4">
          <div className="max-w-3xl mx-auto">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
              <Upload className="mx-auto h-8 w-8 text-gray-400" />
              <p className="mt-2 text-sm text-gray-600">
                {selectedFile ? selectedFile.name : 'Upload documents related to ketamine therapy'}
              </p>

              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                accept=".pdf,.docx,.txt,.md"
                className="hidden"
              />

              <div className="mt-3 flex flex-col sm:flex-row sm:items-center sm:justify-center gap-2">
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200 transition-colors text-sm"
                >
                  Choose File
                </button>

                {selectedFile && (
                  <button
                    onClick={handleFileUpload}
                    disabled={uploadStatus?.includes('Uploading')}
                    className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors text-sm disabled:opacity-50"
                  >
                    Upload Document
                  </button>
                )}
              </div>

              {selectedFile && (
                <div className="mt-2 flex items-center justify-center">
                  <FileText className="h-4 w-4 text-blue-500 mr-1" />
                  <span className="text-xs text-gray-500">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </span>
                </div>
              )}

              {uploadStatus && (
                <div className={`mt-2 p-2 rounded text-xs ${
                  uploadStatus.includes('successful')
                    ? 'bg-green-100 text-green-800'
                    : uploadStatus.includes('Error')
                      ? 'bg-red-100 text-red-800'
                      : 'bg-blue-100 text-blue-800'
                }`}>
                  {uploadStatus}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Input Area - Fixed at the bottom */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 py-4 px-4">
        <form
          onSubmit={onSubmit}
          className="max-w-3xl mx-auto flex gap-2"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about ketamine therapy..."
            className="flex-1 border border-gray-300 rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white placeholder-gray-500"
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
