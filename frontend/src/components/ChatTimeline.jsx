import React, { useEffect, useRef } from 'react';
import { ChefHat, User, Sparkles } from 'lucide-react';

export default function ChatTimeline({ messages = [], isTyping = false }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 max-h-[calc(100vh-380px)] min-h-[350px]">
      {messages.length === 0 ? (
        <div className="h-full flex flex-col items-center justify-center text-center p-8">
          <div className="w-16 h-16 rounded-3xl bg-dhaba-accent/15 border border-dhaba-accent/30 flex items-center justify-center mb-4 shadow-lg shadow-dhaba-accent/10">
            <ChefHat className="w-8 h-8 text-dhaba-accent" />
          </div>
          <h3 className="text-lg font-bold text-dhaba-cream mb-1">Namaste! Welcome to Desi Dhaba</h3>
          <p className="text-xs sm:text-sm text-dhaba-muted max-w-sm">
            I am your Dhaba ordering assistant. Choose a dish from our menu or type your order below!
          </p>
        </div>
      ) : (
        messages.map((msg, index) => {
          const isAssistant = msg.role === 'assistant';
          return (
            <div
              key={index}
              className={`flex items-start gap-3 ${isAssistant ? 'justify-start' : 'justify-end'}`}
            >
              {/* Chef Avatar */}
              {isAssistant && (
                <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-dhaba-accent to-amber-600 flex-shrink-0 flex items-center justify-center shadow-md shadow-dhaba-accent/20 border border-white/10 mt-1">
                  <ChefHat className="w-5 h-5 text-white" />
                </div>
              )}

              {/* Message Bubble */}
              <div
                className={`max-w-[85%] sm:max-w-[75%] rounded-3xl p-4 sm:p-5 shadow-md ${
                  isAssistant
                    ? 'bg-dhaba-card border border-dhaba-border text-dhaba-cream rounded-tl-sm'
                    : 'bg-gradient-to-r from-dhaba-accent to-amber-600 text-white rounded-tr-sm shadow-dhaba-accent/20'
                }`}
              >
                <div className="flex items-center justify-between gap-3 mb-1.5">
                  <span
                    className={`text-[11px] font-bold uppercase tracking-wider ${
                      isAssistant ? 'text-dhaba-accent' : 'text-white/80'
                    }`}
                  >
                    {isAssistant ? 'Dhaba Chef' : 'You'}
                  </span>
                  {msg.timestamp && (
                    <span className={`text-[10px] ${isAssistant ? 'text-dhaba-muted' : 'text-white/60'}`}>
                      {msg.timestamp}
                    </span>
                  )}
                </div>

                <div className="text-xs sm:text-sm leading-relaxed whitespace-pre-line font-normal">
                  {msg.content}
                </div>
              </div>

              {/* User Avatar */}
              {!isAssistant && (
                <div className="w-9 h-9 rounded-2xl bg-dhaba-surface flex-shrink-0 flex items-center justify-center border border-dhaba-border text-dhaba-muted mt-1">
                  <User className="w-4 h-4 text-dhaba-cream" />
                </div>
              )}
            </div>
          );
        })
      )}

      {/* Animated Typing / Cooking Indicator */}
      {isTyping && (
        <div className="flex items-start gap-3">
          <div className="w-9 h-9 rounded-2xl bg-gradient-to-br from-dhaba-accent to-amber-600 flex-shrink-0 flex items-center justify-center shadow-md shadow-dhaba-accent/20 border border-white/10 mt-1">
            <ChefHat className="w-5 h-5 text-white" />
          </div>
          <div className="bg-dhaba-card border border-dhaba-border rounded-3xl rounded-tl-sm p-4 text-dhaba-muted flex items-center gap-3 shadow-md">
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-dhaba-accent animate-bounce [animation-delay:-0.3s]" />
              <span className="w-2 h-2 rounded-full bg-dhaba-accent animate-bounce [animation-delay:-0.15s]" />
              <span className="w-2 h-2 rounded-full bg-dhaba-accent animate-bounce" />
            </div>
            <span className="text-xs font-medium text-dhaba-cream">Chef is checking the tandoor & menu...</span>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
