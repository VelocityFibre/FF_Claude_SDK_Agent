'use client';

/**
 * Database AI Assistant - Command Palette
 *
 * Press ⌘K (Mac) or Ctrl+K (Windows) to open
 * Ask natural language questions about your database
 *
 * Usage:
 * Import and add to your root layout or specific pages
 */

import { useEffect, useState, useCallback } from 'react';
import { X, Sparkles, Loader2, AlertCircle } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant' | 'error';
  content: string;
  timestamp: Date;
}

interface CommandPaletteProps {
  /** Optional: Page context to make queries more relevant */
  context?: {
    page?: string;
    projectId?: string;
    contractorId?: string;
    [key: string]: any;
  };
  /** Optional: Custom placeholder text */
  placeholder?: string;
  /** Optional: Keyboard shortcut (default: ⌘K / Ctrl+K) */
  shortcut?: string;
}

export function CommandPalette({
  context = {},
  placeholder = "Ask about your database...",
  shortcut = "mod+k"
}: CommandPaletteProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Suggested queries based on context
  const suggestions = getSuggestions(context);

  // Handle keyboard shortcut
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Check for ⌘K (Mac) or Ctrl+K (Windows)
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen(prev => !prev);
      }

      // Close on Escape
      if (e.key === 'Escape') {
        setIsOpen(false);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Send query to agent
  const sendQuery = useCallback(async (query: string) => {
    if (!query.trim()) return;

    // Add user message
    const userMessage: Message = {
      role: 'user',
      content: query,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/agent/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: query,
          context
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();

      // Add assistant message
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response || 'No response received',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Agent error:', error);

      // Add error message
      const errorMessage: Message = {
        role: 'error',
        content: error instanceof Error
          ? `Error: ${error.message}`
          : 'Failed to get response. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [context]);

  // Handle suggestion click
  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    sendQuery(suggestion);
  };

  // Clear conversation
  const clearMessages = () => {
    setMessages([]);
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
        onClick={() => setIsOpen(false)}
      />

      {/* Command Palette */}
      <div className="fixed top-[20%] left-1/2 -translate-x-1/2 w-full max-w-2xl z-50 px-4">
        <div className="bg-white rounded-lg shadow-2xl border border-gray-200 overflow-hidden">

          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b bg-gradient-to-r from-blue-50 to-indigo-50">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-blue-600" />
              <h3 className="font-semibold text-gray-900">Database Assistant</h3>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 hover:bg-white/50 rounded transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>

          {/* Messages */}
          <div className="max-h-96 overflow-y-auto p-4 space-y-3">
            {messages.length === 0 ? (
              <div className="text-center py-8">
                <Sparkles className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-500 text-sm mb-4">
                  Ask me anything about your database
                </p>

                {/* Suggestions */}
                {suggestions.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-xs text-gray-400 uppercase tracking-wider mb-2">
                      Try asking:
                    </p>
                    {suggestions.map((suggestion, i) => (
                      <button
                        key={i}
                        onClick={() => handleSuggestionClick(suggestion)}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 rounded-md transition-colors"
                      >
                        {suggestion}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <>
                {messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`rounded-lg px-4 py-3 max-w-[85%] ${
                        msg.role === 'user'
                          ? 'bg-blue-600 text-white'
                          : msg.role === 'error'
                          ? 'bg-red-50 text-red-900 border border-red-200'
                          : 'bg-gray-100 text-gray-900'
                      }`}
                    >
                      {msg.role === 'error' && (
                        <AlertCircle className="w-4 h-4 inline mr-2" />
                      )}
                      <div className="text-sm whitespace-pre-wrap">
                        {msg.content}
                      </div>
                      <div className="text-xs mt-1 opacity-70">
                        {msg.timestamp.toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                ))}

                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 rounded-lg px-4 py-3">
                      <Loader2 className="w-5 h-5 animate-spin text-gray-500" />
                    </div>
                  </div>
                )}

                {/* Clear button */}
                {messages.length > 0 && (
                  <div className="flex justify-center pt-2">
                    <button
                      onClick={clearMessages}
                      className="text-xs text-gray-500 hover:text-gray-700 underline"
                    >
                      Clear conversation
                    </button>
                  </div>
                )}
              </>
            )}
          </div>

          {/* Input */}
          <div className="border-t p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    sendQuery(input);
                  }
                }}
                placeholder={placeholder}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
                autoFocus
              />
              <button
                onClick={() => sendQuery(input)}
                disabled={!input.trim() || isLoading}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {isLoading ? 'Thinking...' : 'Ask'}
              </button>
            </div>

            {/* Hint */}
            <p className="text-xs text-gray-500 mt-2">
              Press <kbd className="px-1.5 py-0.5 bg-gray-100 border rounded text-xs">⌘K</kbd> to toggle •
              <kbd className="px-1.5 py-0.5 bg-gray-100 border rounded text-xs ml-1">Esc</kbd> to close
            </p>
          </div>
        </div>
      </div>
    </>
  );
}

/**
 * Get contextual suggestions based on current page
 */
function getSuggestions(context: Record<string, any>): string[] {
  const { page, projectId, contractorId } = context;

  // Project page suggestions
  if (page === 'project' || projectId) {
    return [
      'Show me the BOQ status for this project',
      'What contractors are assigned to this project?',
      'Is this project on budget?',
      'Show me recent activity for this project'
    ];
  }

  // Contractor page suggestions
  if (page === 'contractor' || contractorId) {
    return [
      'What is this contractor\'s performance score?',
      'Show me this contractor\'s active projects',
      'What is the safety rating for this contractor?',
      'Show me recent invoices for this contractor'
    ];
  }

  // Dashboard/general suggestions
  return [
    'How many active projects do we have?',
    'Show me top performing contractors',
    'Which projects are over budget?',
    'What BOQs are pending approval?',
    'Show me project statistics'
  ];
}

/**
 * Keyboard shortcut display component
 */
export function CommandPaletteShortcut() {
  return (
    <button
      onClick={() => {
        // Trigger the keyboard event
        const event = new KeyboardEvent('keydown', {
          key: 'k',
          metaKey: true,
          bubbles: true
        });
        window.dispatchEvent(event);
      }}
      className="inline-flex items-center gap-2 px-3 py-1.5 text-sm text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
    >
      <Sparkles className="w-4 h-4" />
      <span>Ask AI</span>
      <kbd className="px-1.5 py-0.5 text-xs bg-white border rounded">⌘K</kbd>
    </button>
  );
}
