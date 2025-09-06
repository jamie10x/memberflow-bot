// frontend/src/apiClient.js

// This is the key line to add. It exports the Telegram Web App object
// so it can be safely imported and used by any component.
export const tg = window.Telegram?.WebApp;

// This is the variable for your backend URL. It uses the Vercel env var
// in production and falls back to localhost for local development.
const API_BASE_URL = import.meta.env.VITE_BACKEND_API_URL || 'http://localhost:8000';

// A helper function to add the required auth header to authenticated requests.
const getAuthHeaders = () => {
    return {
        'Content-Type': 'application/json',
        // The backend expects the raw initData string in this header for validation.
        'X-Telegram-Init-Data': tg?.initData || '',
    };
};

// --- API Functions ---

// Example of an authenticated request (for the dashboard)
export const getMyAnalytics = async () => {
    if (!tg?.initData) throw new Error("Telegram authentication data (initData) is not available.");

    const response = await fetch(`${API_BASE_URL}/dashboard/analytics`, {
        headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch analytics');
    return response.json();
};

export const getMyPlans = async () => {
    if (!tg?.initData) throw new Error("Telegram authentication data (initData) is not available.");

    const response = await fetch(`${API_BASE_URL}/dashboard/plans`, {
        headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch plans');
    return response.json();
};

export const getMyChannels = async () => {
    if (!tg?.initData) throw new Error("Telegram authentication data (initData) is not available.");

    const response = await fetch(`${API_BASE_URL}/dashboard/channels`, {
        headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch channels');
    return response.json();
};

export const createMyPlan = async (planData) => {
    if (!tg?.initData) throw new Error("Telegram authentication data (initData) is not available.");

    const response = await fetch(`${API_BASE_URL}/dashboard/plans`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(planData),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to create plan');
    return response.json();
};

export const deleteMyPlan = async (planId) => {
    if (!tg?.initData) throw new Error("Telegram authentication data (initData) is not available.");

    const response = await fetch(`${API_BASE_URL}/dashboard/plans/${planId}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to delete plan');
    // DELETE requests often return no content, so we don't call .json()
    return true;
};

export const getMyPaymentSettings = async () => {
    if (!tg?.initData) throw new Error("Telegram authentication data (initData) is not available.");

    const response = await fetch(`${API_BASE_URL}/dashboard/payment-settings`, {
        headers: getAuthHeaders(),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch payment settings');
    // It's possible for settings to be null, so we handle that.
    if (response.status === 204 || response.headers.get('content-length') === '0') {
        return null;
    }
    return response.json();
};

export const saveMyPaymentSettings = async (settingsData) => {
    if (!tg?.initData) throw new Error("Telegram authentication data (initData) is not available.");

    const response = await fetch(`${API_BASE_URL}/dashboard/payment-settings`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(settingsData),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to save payment settings');
    return response.json();
};


// Example of a public request (for the checkout page)
export const getPublicPlanDetails = async (planId) => {
    const response = await fetch(`${API_BASE_URL}/public/plans/${planId}`);
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to fetch plan details');
    return response.json();
};

export const initTonPayment = async (initData) => {
    const response = await fetch(`${API_BASE_URL}/checkout/init-ton-payment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(initData),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to initialize payment');
    return response.json();
};

export const verifyTonPayment = async (verifyData) => {
    const response = await fetch(`${API_BASE_URL}/checkout/verify-ton-payment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(verifyData),
    });
    if (!response.ok) throw new Error((await response.json()).detail || 'Failed to verify payment');
    return response.json();
};