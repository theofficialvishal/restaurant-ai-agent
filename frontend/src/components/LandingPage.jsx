import React from 'react';
import { MessageSquare, Leaf, Truck, Heart, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function LandingPage() {
  const navigate = useNavigate();
  return (
    <div className="relative min-h-screen bg-dhaba-bg flex flex-col items-center justify-center overflow-hidden">
      {/* Background Image with Overlay */}
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-40"
        style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1585937421612-70a008356fbe?q=80&w=2000&auto=format&fit=crop")' }}
      >
        <div className="absolute inset-0 bg-gradient-to-t from-dhaba-bg via-dhaba-bg/80 to-transparent"></div>
        <div className="absolute inset-0 bg-gradient-to-r from-dhaba-bg via-dhaba-bg/80 to-transparent"></div>
      </div>

      {/* Centered Content */}
      <div className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 w-full flex flex-col items-center justify-center text-center pt-32 pb-20">
        <h1 className="text-6xl md:text-8xl lg:text-[7rem] font-bold font-serif leading-[1.1] text-dhaba-cream mb-6 drop-shadow-2xl">
          Good Food <br />
          <span className="text-dhaba-accent">Better Mood</span>
        </h1>
        <p className="text-xl md:text-2xl text-dhaba-cream/90 max-w-2xl mx-auto mb-12 drop-shadow-lg font-medium">
          Chat with our AI assistant and order your favourite Indian food.
        </p>
        
        <button 
          onClick={() => navigate('/order')}
          className="group relative inline-flex items-center gap-4 bg-dhaba-accent hover:bg-dhaba-accentHover text-white px-10 py-5 rounded-full text-xl font-bold transition-all shadow-xl shadow-dhaba-accent/40 hover:shadow-2xl hover:shadow-dhaba-accent/50 overflow-hidden transform hover:-translate-y-1"
        >
          <span className="relative z-10">Start Ordering</span>
          <ArrowRight className="w-6 h-6 relative z-10 group-hover:translate-x-1.5 transition-transform" />
          <div className="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out"></div>
        </button>
      </div>



      {/* Features Bar */}
      <div className="relative z-10 w-full max-w-5xl mx-auto px-4 pb-12 mt-auto">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <Feature icon={<MessageSquare className="w-6 h-6" />} title="AI Powered" subtitle="Ordering" />
          <Feature icon={<Leaf className="w-6 h-6" />} title="Authentic" subtitle="Indian Menu" />
          <Feature icon={<Truck className="w-6 h-6" />} title="Real-time" subtitle="Order Updates" />
          <Feature icon={<Heart className="w-6 h-6" />} title="Fast & Friendly" subtitle="Service" />
        </div>
      </div>
    </div>
  );
}

function Feature({ icon, title, subtitle }) {
  return (
    <div className="flex flex-col items-center text-center gap-3 group">
      <div className="w-14 h-14 rounded-full bg-dhaba-card border border-dhaba-border flex items-center justify-center text-dhaba-accent group-hover:bg-dhaba-border transition-colors shadow-sm">
        {icon}
      </div>
      <div>
        <h3 className="text-sm font-semibold text-dhaba-cream">{title}</h3>
        <p className="text-xs text-dhaba-muted">{subtitle}</p>
      </div>
    </div>
  );
}
