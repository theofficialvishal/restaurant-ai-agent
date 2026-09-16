const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Fetch authoritative menu with real-time available stock
 */
export async function fetchMenu() {
  const res = await fetch(`${API_BASE}/api/menu`);
  if (!res.ok) {
    throw new Error(`Failed to load menu: ${res.status}`);
  }
  const data = await res.json();
  return data.items || [];
}

/**
 * Submit customer utterance to LangGraph backend agent
 */
export async function sendChatMessage({
  sessionId,
  message,
  forceCookingFail = false,
  forceServingFail = false,
}) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId || null,
      message,
      force_cooking_fail: Boolean(forceCookingFail),
      force_serving_fail: Boolean(forceServingFail),
    }),
  });

  if (!res.ok) {
    const errText = await res.text();
    throw new Error(`Chat error (${res.status}): ${errText}`);
  }

  return await res.json();
}

/**
 * Reset conversation and session state on server
 */
export async function resetSession(sessionId) {
  const res = await fetch(`${API_BASE}/api/reset`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId || null,
    }),
  });

  if (!res.ok) {
    throw new Error(`Reset error (${res.status})`);
  }

  return await res.json();
}

/**
 * Check health of backend server
 */
export async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/api/health`);
    if (!res.ok) return false;
    return await res.json();
  } catch {
    return false;
  }
}
