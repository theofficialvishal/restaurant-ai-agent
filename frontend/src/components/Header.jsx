import React from 'react';
import { Utensils, RotateCcw, Sparkles, ChefHat, Receipt } from 'lucide-react';

export default function Header({ onReset, onToggleBill, hasBill, isConnected = true }) {
  return (
    <header className="sticky top-0 z-40 border-b border-dhaba-border bg-dhaba-surface/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-20 flex items-center justify-between gap-4">
        {/* Logo and Dhaba Branding */}
        <div className="flex items-center gap-3.5">
          <div className="relative">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-dhaba-accent via-orange-600 to-amber-600 flex items-center justify-center shadow-lg shadow-dhaba-accent/20 ring-1 ring-white/10">
              <ChefHat className="w-6 h-6 text-white" />
            </div>
            <span className="absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-dhaba-surface flex items-center justify-center border border-dhaba-border">
              <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-dhaba-success animate-pulse' : 'bg-dhaba-danger'}`} />
            </span>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-extrabold tracking-tight text-dhaba-cream">
                Desi Dhaba
              </h1>
              <span className="text-[11px] uppercase tracking-wider px-2.5 py-0.5 rounded-full bg-dhaba-accent/15 text-dhaba-accent font-bold border border-dhaba-accent/30 shadow-sm">
                AI Restaurant
              </span>
            </div>
            <p className="text-xs text-dhaba-muted flex items-center gap-1.5 mt-0.5">
              <span>Authentic Indian Dining</span>
              <span className="text-dhaba-border">•</span>
              <span className="text-amber-400/90 flex items-center gap-1">
                <Sparkles className="w-3 h-3 inline" />
                LangGraph Powered
              </span>
            </p>
          </div>
        </div>

        {/* Right Actions: Bill Preview & Reset */}
        <div className="flex items-center gap-2.5">
          {hasBill && (
            <button
              onClick={onToggleBill}
              className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-dhaba-card hover:bg-dhaba-border border border-dhaba-border text-xs font-semibold text-dhaba-cream transition-all shadow-sm hover:border-dhaba-accent/40"
              title="View Itemized Receipt"
            >
              <Receipt className="w-4 h-4 text-dhaba-accent" />
              <span className="hidden sm:inline">View Bill</span>
            </button>
          )}

          <button
            onClick={onReset}
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-dhaba-card hover:bg-dhaba-border border border-dhaba-border text-xs font-semibold text-dhaba-muted hover:text-dhaba-cream transition-all hover:border-dhaba-accent/40"
            title="Start New Order / Reset State"
          >
            <RotateCcw className="w-3.5 h-3.5 text-dhaba-accent" />
            <span className="hidden sm:inline">New Order</span>
          </button>
        </div>
      </div>
    </header>
  );
}
