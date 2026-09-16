import React from 'react';
import { X, Receipt, ChefHat, CheckCircle2, RotateCcw } from 'lucide-react';

export default function BillModal({ isOpen, onClose, bill, onNewOrder }) {
  if (!isOpen || !bill) return null;

  const items = bill.items || [];
  const subtotal = bill.subtotal || 0;
  const tax = bill.tax || 0;
  const grandTotal = bill.grand_total || 0;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-md bg-dhaba-card border border-dhaba-border rounded-3xl p-6 sm:p-8 shadow-2xl overflow-hidden ring-1 ring-white/10">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 p-2 rounded-xl bg-dhaba-surface hover:bg-dhaba-border border border-dhaba-border text-dhaba-muted hover:text-dhaba-cream transition-colors"
          title="Close Receipt"
        >
          <X className="w-4 h-4" />
        </button>

        {/* Receipt Header */}
        <div className="text-center pb-6 border-b border-dhaba-border/60">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-dhaba-accent to-amber-600 mx-auto flex items-center justify-center mb-3 shadow-lg shadow-dhaba-accent/20">
            <ChefHat className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-xl font-extrabold text-dhaba-cream tracking-tight">Desi Dhaba</h2>
          <p className="text-xs text-dhaba-muted mt-0.5">Authentic Flavors • Tax Invoice</p>
          <div className="mt-2 inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30 text-[11px] font-semibold">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Order Completed & Served</span>
          </div>
        </div>

        {/* Itemized Items */}
        <div className="py-5 space-y-3 max-h-60 overflow-y-auto">
          <div className="text-[11px] font-bold text-dhaba-muted uppercase tracking-wider grid grid-cols-12 pb-1 border-b border-dhaba-border/40">
            <span className="col-span-6">Item</span>
            <span className="col-span-2 text-center">Qty</span>
            <span className="col-span-2 text-right">Price</span>
            <span className="col-span-2 text-right">Total</span>
          </div>

          {items.map((item, idx) => (
            <div key={idx} className="grid grid-cols-12 text-xs items-center py-1 font-mono">
              <span className="col-span-6 font-sans font-semibold text-dhaba-cream truncate pr-2">
                {item.dish_name}
              </span>
              <span className="col-span-2 text-center text-dhaba-muted">{item.quantity}</span>
              <span className="col-span-2 text-right text-dhaba-muted">₹{item.unit_price}</span>
              <span className="col-span-2 text-right font-bold text-dhaba-cream">₹{item.item_total}</span>
            </div>
          ))}
        </div>

        {/* Math Breakdown */}
        <div className="pt-4 border-t border-dashed border-dhaba-border/80 space-y-2 text-xs font-mono">
          <div className="flex justify-between text-dhaba-muted">
            <span>Subtotal</span>
            <span>₹{subtotal.toFixed(2)}</span>
          </div>
          <div className="flex justify-between text-dhaba-muted">
            <span>Restaurant GST (5%)</span>
            <span>₹{tax.toFixed(2)}</span>
          </div>
          <div className="pt-2 border-t border-dhaba-border flex justify-between items-center text-base font-bold text-dhaba-cream font-sans">
            <span>Grand Total</span>
            <span className="px-3 py-1 rounded-xl bg-dhaba-accent/20 text-dhaba-accent border border-dhaba-accent/40 font-mono">
              ₹{grandTotal.toFixed(2)}
            </span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-6 flex gap-3">
          <button
            onClick={() => {
              onClose();
              if (onNewOrder) onNewOrder();
            }}
            className="flex-1 inline-flex items-center justify-center gap-2 px-4 py-3 rounded-2xl bg-dhaba-accent hover:bg-dhaba-accentHover text-white font-semibold text-xs sm:text-sm transition-all shadow-lg shadow-dhaba-accent/20 hover:shadow-dhaba-accent/30"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Order Again</span>
          </button>

          <button
            onClick={onClose}
            className="px-5 py-3 rounded-2xl bg-dhaba-surface hover:bg-dhaba-border border border-dhaba-border text-dhaba-cream font-semibold text-xs sm:text-sm transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
