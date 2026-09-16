import React from 'react';
import { Check, Flame, Utensils, Receipt, AlertTriangle, RefreshCw, ChefHat, Sparkles } from 'lucide-react';

const STEPS = [
  { id: 'validated', label: 'Validated', icon: Sparkles },
  { id: 'order_placed', label: 'Order Taken', icon: ChefHat },
  { id: 'cooking', label: 'Kitchen Cooking', icon: Flame },
  { id: 'serving', label: 'Table Serving', icon: Utensils },
  { id: 'completed', label: 'Billed', icon: Receipt },
];

export default function OrderStatus({ workflowStatus = 'IDLE', servingRetries = 0 }) {
  // Determine active step index (0 to 4)
  const getStepIndex = (status) => {
    switch (status) {
      case 'VALIDATING':
        return 0;
      case 'ORDER_PLACED':
        return 1;
      case 'COOKING':
      case 'COOKING_FAILED':
      case 'RESELECT_DISH':
        return 2;
      case 'SERVING':
      case 'SERVING_FAILED':
      case 'RE_COOKING':
        return 3;
      case 'COMPLETED':
        return 4;
      default:
        return -1;
    }
  };

  const currentIndex = getStepIndex(workflowStatus);

  const getStatusBanner = () => {
    if (workflowStatus === 'RE_COOKING') {
      return (
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-amber-500/15 border border-amber-500/30 text-amber-400 text-xs font-semibold animate-pulse">
          <RefreshCw className="w-3.5 h-3.5 animate-spin" />
          <span>Kitchen Rush: Preparing fresh batch after table service mishap (Retry #{servingRetries})</span>
        </div>
      );
    }
    if (workflowStatus === 'RESELECT_DISH' || workflowStatus === 'COOKING_FAILED') {
      return (
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-red-500/15 border border-red-500/30 text-red-400 text-xs font-semibold">
          <AlertTriangle className="w-3.5 h-3.5" />
          <span>Kitchen Mishap: Dish over-simmered. Please pick another dish!</span>
        </div>
      );
    }
    if (workflowStatus === 'TERMINATED') {
      return (
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-dhaba-card border border-dhaba-border text-dhaba-muted text-xs">
          <span>Session concluded after maximum attempts. Click 'New Order' to restart.</span>
        </div>
      );
    }
    if (workflowStatus === 'COMPLETED') {
      return (
        <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 text-xs font-semibold">
          <Check className="w-3.5 h-3.5" />
          <span>Order Complete! Dish served hot & fresh. Check your bill below.</span>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-dhaba-surface border border-dhaba-border rounded-3xl p-5 shadow-lg">
      <div className="text-center mb-8 mt-2">
        <h2 className="text-2xl font-bold font-serif text-dhaba-cream mb-2">
          Your Order is in Progress
        </h2>
        <p className="text-sm text-dhaba-muted">
          Sit back and relax while we prepare your delicious food!
        </p>
      </div>

      {/* Stepper Steps */}
      <div className="grid grid-cols-5 gap-2 relative">
        {/* Connecting Line */}
        <div className="absolute top-5 left-1/10 right-1/10 h-[2px] bg-dhaba-border -z-0">
           <div className="h-full bg-dhaba-accent transition-all duration-500" style={{ width: `${(currentIndex / 4) * 100}%` }}></div>
        </div>
        {STEPS.map((step, idx) => {
          const Icon = step.icon;
          const isDone = currentIndex > idx || (currentIndex === 4 && idx === 4);
          const isCurrent = currentIndex === idx && currentIndex !== 4;
          const isPending = currentIndex < idx;

          return (
            <div key={step.id} className="flex flex-col items-center text-center group">
              <div
                className={`relative z-10 w-9 h-9 sm:w-11 sm:h-11 rounded-full flex items-center justify-center transition-all duration-300 mb-3 ${
                  isDone
                    ? 'bg-dhaba-accent text-white shadow-lg shadow-dhaba-accent/30'
                    : isCurrent
                    ? 'bg-dhaba-card text-dhaba-accent border-2 border-dhaba-accent animate-pulse'
                    : 'bg-dhaba-bg text-dhaba-muted border-2 border-dhaba-border'
                }`}
              >
                {isDone ? (
                  <Check className="w-4 h-4 sm:w-5 sm:h-5 stroke-[3]" />
                ) : (
                  <Icon className="w-4 h-4 sm:w-5 sm:h-5" />
                )}
              </div>

              <span
                className={`text-[11px] sm:text-xs font-medium tracking-tight ${
                  isDone || isCurrent ? 'text-dhaba-cream font-semibold' : 'text-dhaba-muted'
                }`}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>

      {/* Chef Illustration Card for Cooking */}
      {(currentIndex === 2 || currentIndex === 3) && (
        <div className="mt-8 flex items-center gap-6 bg-dhaba-bg/50 rounded-2xl p-4 border border-dhaba-border relative overflow-hidden">
           <img 
              src="https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=400&auto=format&fit=crop" 
              alt="Chef Cooking" 
              className="w-24 h-24 object-cover rounded-xl"
           />
           <div>
              <h4 className="text-lg font-bold font-serif text-dhaba-cream mb-1">Our chef is preparing your meal...</h4>
              <p className="text-sm text-dhaba-muted">This may take a few minutes.<br/>Good food takes time! 😋</p>
           </div>
        </div>
      )}

      {/* Dynamic Status Alert Banner */}
      {getStatusBanner() && <div className="mt-6 pt-4 border-t border-dhaba-border/60">{getStatusBanner()}</div>}
    </div>
  );
}
