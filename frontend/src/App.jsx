import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import MenuSidebar from './components/MenuSidebar';
import OrderStatus from './components/OrderStatus';
import ChatTimeline from './components/ChatTimeline';
import ChatComposer from './components/ChatComposer';
import BillModal from './components/BillModal';
import LandingPage from './components/LandingPage';
import { fetchMenu, sendChatMessage, resetSession, checkHealth } from './services/api';

const DEFAULT_GREETING = {
  role: 'assistant',
  content:
    'Namaste! Welcome to Desi Dhaba. 🍲\nWhat delicious Indian dish would you like to enjoy today? Browse our authentic menu on the left or type your order below!',
  timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
};

export default function App() {
  const [sessionId, setSessionId] = useState(null);
  const [menuItems, setMenuItems] = useState([]);
  const [messages, setMessages] = useState([DEFAULT_GREETING]);
  const [workflowStatus, setWorkflowStatus] = useState('IDLE');
  const [isTyping, setIsTyping] = useState(false);
  const [isTerminated, setIsTerminated] = useState(false);
  const [servingRetries, setServingRetries] = useState(0);
  const [currentOrder, setCurrentOrder] = useState([]);
  const [bill, setBill] = useState(null);
  const [isBillOpen, setIsBillOpen] = useState(false);
  const [isConnected, setIsConnected] = useState(true);

  // Dev simulation failure flags
  const [forceCookingFail, setForceCookingFail] = useState(false);
  const [forceServingFail, setForceServingFail] = useState(false);

  // Load menu and check backend health on mount
  const loadInitialData = async () => {
    try {
      const health = await checkHealth();
      setIsConnected(Boolean(health));

      const items = await fetchMenu();
      setMenuItems(items);
    } catch (err) {
      console.warn('Backend offline or loading fallback:', err.message);
      setIsConnected(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  // Reset entire conversation and session
  const handleReset = async () => {
    setIsTyping(true);
    try {
      const resetData = await resetSession(sessionId);
      setSessionId(resetData.session_id);
    } catch (err) {
      console.warn('Reset error, generating local ID:', err.message);
      setSessionId(null);
    } finally {
      setWorkflowStatus('IDLE');
      setIsTerminated(false);
      setServingRetries(0);
      setCurrentOrder([]);
      setBill(null);
      setIsBillOpen(false);
      setForceCookingFail(false);
      setForceServingFail(false);
      setIsTyping(false);

      const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages([
        {
          ...DEFAULT_GREETING,
          timestamp: time,
        },
      ]);

      // Refresh inventory
      try {
        const freshMenu = await fetchMenu();
        setMenuItems(freshMenu);
      } catch {
        // ignore
      }
    }
  };

  // Submit message to live FastAPI + LangGraph agent
  const handleSendMessage = async (text) => {
    if (isTerminated || !text.trim()) return;

    const userTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setMessages((prev) => [...prev, { role: 'user', content: text, timestamp: userTime }]);
    setIsTyping(true);

    try {
      const response = await sendChatMessage({
        sessionId,
        message: text,
        forceCookingFail,
        forceServingFail,
      });

      // Update session ID if assigned by server
      if (response.session_id) {
        setSessionId(response.session_id);
      }

      // Append assistant reply
      const assistantTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.assistant_message || 'Thank you!',
          timestamp: assistantTime,
        },
      ]);

      // Update agent state
      setWorkflowStatus(response.workflow_status || 'IDLE');
      setIsTerminated(Boolean(response.is_terminal));
      setCurrentOrder(response.current_order || []);
      setServingRetries(response.serving_retries || 0);

      // Refresh menu inventory in real-time
      const updatedMenu = await fetchMenu();
      setMenuItems(updatedMenu);

      // Bill presentation
      if (response.bill && response.workflow_status === 'COMPLETED') {
        setBill(response.bill);
        setTimeout(() => {
          setIsBillOpen(true);
        }, 500);
      }

      // Reset one-shot simulation toggles after trigger
      if (forceCookingFail) setForceCookingFail(false);
      if (forceServingFail) setForceServingFail(false);
    } catch (err) {
      console.error('Chat error:', err);
      const assistantTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Server connection issue: ${err.message}. Please check that the FastAPI server is running.`,
          timestamp: assistantTime,
        },
      ]);
      setIsConnected(false);
    } finally {
      setIsTyping(false);
    }
  };

  // Quick action from dish card in Menu Sidebar
  const handleSelectDish = (dish, qty = 1) => {
    handleSendMessage(`I want ${qty} plate${qty > 1 ? 's' : ''} of ${dish.name}`);
  };

  const OrderInterface = () => (
    <div className="min-h-screen bg-dhaba-bg text-dhaba-cream flex flex-col selection:bg-dhaba-accent selection:text-white font-sans animate-in fade-in duration-300">
      {/* Top Header */}
      <Header
        onReset={handleReset}
        onToggleBill={() => setIsBillOpen(true)}
        hasBill={Boolean(bill)}
        isConnected={isConnected}
      />

      {/* Main Two-Column Layout */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 py-6 w-full flex flex-col lg:flex-row gap-6">
        {/* Left Column: Real-time Menu Sidebar */}
        <MenuSidebar menuItems={menuItems} onSelectDish={handleSelectDish} />

        {/* Right Column: Order Status & Conversational Hub */}
        <div className="flex-1 flex flex-col gap-4 min-w-0">
          {/* Order Lifecycle Stepper */}
          <OrderStatus workflowStatus={workflowStatus} servingRetries={servingRetries} />

          {/* Chat Timeline & Composer Container */}
          <div className="flex-1 flex flex-col bg-dhaba-surface border border-dhaba-border rounded-3xl overflow-hidden shadow-xl">
            <ChatTimeline messages={messages} isTyping={isTyping} />

            <ChatComposer
              onSendMessage={handleSendMessage}
              disabled={isTyping || isTerminated}
              isTerminated={isTerminated}
              forceCookingFail={forceCookingFail}
              setForceCookingFail={setForceCookingFail}
              forceServingFail={forceServingFail}
              setForceServingFail={setForceServingFail}
            />
          </div>
        </div>
      </main>

      {/* Itemized Bill Modal */}
      <BillModal
        isOpen={isBillOpen}
        onClose={() => setIsBillOpen(false)}
        bill={bill}
        onNewOrder={handleReset}
      />

      {/* Footer */}
      <footer className="border-t border-dhaba-border bg-dhaba-surface/50 py-4 text-center text-xs text-dhaba-muted font-serif">
        Desi Dhaba AI Restaurant • Full Stack LangGraph & FastAPI Integration
      </footer>
    </div>
  );

  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/order" element={<OrderInterface />} />
    </Routes>
  );
}
