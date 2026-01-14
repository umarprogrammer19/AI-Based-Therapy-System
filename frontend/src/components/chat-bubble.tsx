'use client';

import { cn } from '@/lib/utils';
import { Bot, User } from 'lucide-react';
import { ReactNode } from 'react';

interface ChatBubbleProps {
  children: ReactNode;
  variant?: 'user' | 'ai';
  className?: string;
}

export function ChatBubble({ children, variant = 'ai', className }: ChatBubbleProps) {
  const isUser = variant === 'user';

  return (
    <div className={cn(
      'flex',
      isUser ? 'justify-end' : 'justify-start',
      className
    )}>
      <div
        className={cn(
          'max-w-[80%] rounded-2xl px-4 py-3',
          isUser
            ? 'bg-blue-500 text-white rounded-tr-none'
            : 'bg-gray-200 text-gray-800 rounded-tl-none'
        )}
      >
        <div className="flex items-start gap-2">
          {!isUser && <Bot className="h-5 w-5 mt-0.5 flex-shrink-0" />}
          <div className="whitespace-pre-wrap break-words">
            {children}
          </div>
          {isUser && <User className="h-5 w-5 mt-0.5 flex-shrink-0 text-blue-100" />}
        </div>
      </div>
    </div>
  );
}

interface ChatBubbleWrapperProps {
  children: ReactNode;
  variant?: 'user' | 'ai';
  className?: string;
}

export function ChatBubbleWrapper({ children, variant, className }: ChatBubbleWrapperProps) {
  return (
    <div className={cn(
      'flex',
      variant === 'user' ? 'justify-end' : 'justify-start',
      className
    )}>
      {children}
    </div>
  );
}