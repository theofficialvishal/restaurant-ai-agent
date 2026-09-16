import React, { useState } from 'react';
import { Send, Sparkles, SlidersHorizontal, AlertCircle } from 'lucide-react';

const QUICK_SUGGESTIONS = [
  '1 Butter Chicken',
  '2 Paneer Tikka',
  '1 Hyderabadi Biryani',
  '2 Garlic Naan',
  'What is available on the menu?',
];

export default function ChatComposer({
  onSendMessage,
  disabled = false,
  isTerminated = false,
  forceCookingFail,
  setForceCookingFail,
  forceServingFail,
  setForceServingFail,
}) {
  const [inputText, setInputText] = useState('');
  const [showSimControls, setShowSimControls] = useState(false);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!inputText.trim() || disabled) return;
    onSendMessage(inputText.trim());
    setInputText('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleChipClick = (suggestion) => {
    if (disabled) return;
    setInputText((prev) => {
      // Do not append if current text is the menu inquiry, or if the clicked suggestion is the menu inquiry
      if (
        suggestion === 'What is available on the menu?' ||
        prev.trim() === 'What is available on the menu?'
      ) {
        return suggestion;
      }
      return prev ? `${prev} ${suggestion}` : suggestion;
    });
  };

  return (
    <div className="border-t border-dhaba-border bg-dhaba-surface p-4 sm:p-5 rounded-b-3xl">
      {/* Quick Suggestion Chips */}
      {!isTerminated && (
        <div className="flex items-center gap-1.5 overflow-x-auto pb-3 mb-2 scrollbar-none">
          <span className="text-[11px] font-bold text-dhaba-muted uppercase tracking-wider whitespace-nowrap flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-dhaba-accent" />
            Quick:
          </span>
          {QUICK_SUGGESTIONS.map((chip, idx) => (
            <button
              key={idx}
              onClick={() => handleChipClick(chip)}
              disabled={disabled}
              className="px-3 py-1 rounded-xl bg-dhaba-card hover:bg-dhaba-border border border-dhaba-border text-[11px] font-medium text-dhaba-cream whitespace-nowrap transition-all hover:border-dhaba-accent/50 disabled:opacity-50 shadow-sm"
            >
              {chip}
            </button>
          ))}
        </div>
      )}

      {/* Simulation Controls Toggle for Dev/Testing */}
      <div className="flex items-center justify-between mb-2 text-xs">
        <button
          type="button"
          onClick={() => setShowSimControls(!showSimControls)}
          className="inline-flex items-center gap-1 text-[11px] font-semibold text-dhaba-muted hover:text-dhaba-accent transition-colors"
        >
          <SlidersHorizontal className="w-3 h-3" />
          <span>{showSimControls ? 'Hide Test Simulation Flags' : 'Dev: Test Failure Simulations'}</span>
        </button>

        {(forceCookingFail || forceServingFail) && (
          <span className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-amber-500/15 text-amber-400 border border-amber-500/30 animate-pulse">
            Simulated Failure Active
          </span>
        )}
      </div>

      {showSimControls && (
        <div className="p-3 mb-3 rounded-2xl bg-dhaba-card/80 border border-dhaba-border flex flex-wrap gap-4 text-xs">
          <label className="flex items-center gap-2 cursor-pointer text-dhaba-cream">
            <input
              type="checkbox"
              checked={forceCookingFail}
              onChange={(e) => setForceCookingFail(e.target.checked)}
              className="w-4 h-4 rounded text-dhaba-accent bg-dhaba-bg border-dhaba-border focus:ring-dhaba-accent"
            />
            <span className="text-xs">Force Cooking Failure (loops to re-select)</span>
          </label>

          <label className="flex items-center gap-2 cursor-pointer text-dhaba-cream">
            <input
              type="checkbox"
              checked={forceServingFail}
              onChange={(e) => setForceServingFail(e.target.checked)}
              className="w-4 h-4 rounded text-dhaba-accent bg-dhaba-bg border-dhaba-border focus:ring-dhaba-accent"
            />
            <span className="text-xs">Force Serving Failure (loops to re-cook)</span>
          </label>
        </div>
      )}

      {/* Main Composer Input */}
      {isTerminated ? (
        <div className="p-4 rounded-2xl bg-dhaba-card border border-dhaba-border text-center text-dhaba-muted text-xs flex items-center justify-center gap-2">
          <AlertCircle className="w-4 h-4 text-dhaba-accent" />
          <span>Ordering session has ended. Click 'New Order' in the header to place a new order.</span>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="flex items-center gap-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            placeholder="Tell our AI Chef your order (e.g. '2 Butter Chicken and 1 Garlic Naan')..."
            className="flex-1 px-4 py-3.5 bg-dhaba-bg border border-dhaba-border rounded-2xl text-xs sm:text-sm text-dhaba-cream placeholder-dhaba-muted focus:outline-none focus:border-dhaba-accent/60 transition-all shadow-inner disabled:opacity-50"
          />

          <button
            type="submit"
            disabled={!inputText.trim() || disabled}
            className="p-3.5 rounded-2xl bg-gradient-to-r from-dhaba-accent to-amber-600 hover:from-dhaba-accentHover hover:to-orange-700 text-white font-semibold transition-all shadow-lg shadow-dhaba-accent/25 hover:shadow-dhaba-accent/40 disabled:opacity-40 disabled:cursor-not-allowed disabled:shadow-none flex-shrink-0"
            title="Send Message"
          >
            <Send className="w-4 h-4 sm:w-5 sm:h-5" />
          </button>
        </form>
      )}
    </div>
  );
}
