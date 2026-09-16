import React, { useState } from 'react';
import { Flame, Search, Plus, Sparkles, AlertCircle } from 'lucide-react';

const CATEGORIES = ['All', 'Curry', 'Starter', 'Rice', 'Bread', 'Dessert'];

export default function MenuSidebar({ menuItems = [], onSelectDish }) {
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [quantities, setQuantities] = useState({});

  const handleQtyChange = (id, delta, max) => {
    setQuantities(prev => {
      const current = prev[id] || 1;
      const next = Math.max(1, Math.min(max, current + delta));
      return { ...prev, [id]: next };
    });
  };

  const filteredItems = menuItems.filter((item) => {
    const matchesCategory = selectedCategory === 'All' || item.category === selectedCategory;
    const matchesSearch =
      item.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      item.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const getSpiceBadge = (level) => {
    if (level === 'Spicy') {
      return (
        <span className="inline-flex items-center gap-0.5 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-red-500/15 text-red-400 border border-red-500/30">
          <Flame className="w-3 h-3 fill-red-400 text-red-400" />
          Spicy
        </span>
      );
    }
    if (level === 'Medium') {
      return (
        <span className="inline-flex items-center gap-0.5 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 border border-amber-500/30">
          <Flame className="w-3 h-3 fill-amber-400 text-amber-400" />
          Medium
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-0.5 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
        Mild
      </span>
    );
  };

  return (
    <aside className="w-full lg:w-96 flex flex-col bg-dhaba-surface border border-dhaba-border rounded-3xl overflow-hidden shadow-xl">
      {/* Sidebar Header */}
      <div className="p-5 border-b border-dhaba-border bg-dhaba-card/40">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h2 className="text-lg font-bold text-dhaba-cream flex items-center gap-2">
              <span>Authentic Dhaba Menu</span>
            </h2>
            <p className="text-xs text-dhaba-muted">Real-time inventory from Dhaba kitchen</p>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-dhaba-card text-dhaba-accent border border-dhaba-border font-mono font-semibold">
            {menuItems.length} Dishes
          </span>
        </div>

        {/* Search input */}
        <div className="relative mb-3">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-dhaba-muted" />
          <input
            type="text"
            placeholder="Search dishes or flavors..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-2 bg-dhaba-bg/80 border border-dhaba-border rounded-xl text-xs text-dhaba-cream placeholder-dhaba-muted focus:outline-none focus:border-dhaba-accent/60 transition-colors"
          />
        </div>

        {/* Category Pills */}
        <div className="flex gap-1.5 overflow-x-auto pb-1 scrollbar-none">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                selectedCategory === cat
                  ? 'bg-dhaba-accent text-white shadow-sm shadow-dhaba-accent/20'
                  : 'bg-dhaba-card text-dhaba-muted hover:text-dhaba-cream hover:bg-dhaba-border border border-dhaba-border/60'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Dish List */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 max-h-[calc(100vh-280px)] min-h-[400px]">
        {filteredItems.length === 0 ? (
          <div className="text-center py-12 text-dhaba-muted">
            <AlertCircle className="w-8 h-8 mx-auto mb-2 opacity-50 text-dhaba-accent" />
            <p className="text-xs">No dishes match your filter.</p>
          </div>
        ) : (
          filteredItems.map((dish) => {
            const isSoldOut = dish.available_qty <= 0;
            return (
              <div
                key={dish.id}
                className={`p-4 rounded-2xl border transition-all duration-200 group ${
                  isSoldOut
                    ? 'bg-dhaba-bg/40 border-dhaba-border/50 opacity-60'
                    : 'bg-dhaba-card/60 hover:bg-dhaba-card border-dhaba-border hover:border-dhaba-accent/40 shadow-sm hover:shadow-md'
                }`}
              >
                <div className="flex items-start justify-between gap-2 mb-1.5">
                  <div>
                    <h3 className="text-sm font-bold text-dhaba-cream group-hover:text-dhaba-accent transition-colors">
                      {dish.name}
                    </h3>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="text-xs font-mono font-bold text-amber-400">
                        ₹{dish.price}
                      </span>
                      {getSpiceBadge(dish.spice_level)}
                    </div>
                  </div>

                  {/* Stock pill */}
                  <div>
                    {isSoldOut ? (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-dhaba-danger/15 text-dhaba-danger border border-dhaba-danger/30">
                        Sold Out
                      </span>
                    ) : (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-dhaba-accent/15 text-dhaba-accent border border-dhaba-accent/30 font-mono">
                        {dish.available_qty} left
                      </span>
                    )}
                  </div>
                </div>

                <p className="text-xs text-dhaba-muted line-clamp-2 leading-relaxed mb-3">
                  {dish.description}
                </p>

                {/* Quick Add Button */}
                <div className="flex justify-end items-center gap-3">
                  <div className="flex items-center gap-2 bg-dhaba-surface border border-dhaba-border rounded-xl p-1">
                    <button
                      onClick={() => handleQtyChange(dish.id, -1, dish.available_qty)}
                      disabled={isSoldOut || (quantities[dish.id] || 1) <= 1}
                      className="w-6 h-6 flex items-center justify-center rounded-lg hover:bg-dhaba-card text-dhaba-muted hover:text-dhaba-cream disabled:opacity-50"
                    >-</button>
                    <span className="text-xs font-mono font-bold w-4 text-center">{quantities[dish.id] || 1}</span>
                    <button
                      onClick={() => handleQtyChange(dish.id, 1, dish.available_qty)}
                      disabled={isSoldOut || (quantities[dish.id] || 1) >= dish.available_qty}
                      className="w-6 h-6 flex items-center justify-center rounded-lg hover:bg-dhaba-card text-dhaba-muted hover:text-dhaba-cream disabled:opacity-50"
                    >+</button>
                  </div>
                  <button
                    onClick={() => {
                        if (onSelectDish) onSelectDish(dish, quantities[dish.id] || 1);
                        setQuantities(prev => ({ ...prev, [dish.id]: 1 }));
                    }}
                    disabled={isSoldOut}
                    className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                      isSoldOut
                        ? 'bg-dhaba-card text-dhaba-muted cursor-not-allowed border border-dhaba-border'
                        : 'bg-dhaba-surface hover:bg-dhaba-accent hover:text-white text-dhaba-cream border border-dhaba-border hover:border-dhaba-accent shadow-sm'
                    }`}
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>Order</span>
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
}
