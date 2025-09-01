// frontend/src/apiClient.js

// The public HTTPS URL of your backend server, provided by ngrok.
const API_BASE_URL = "https://fbfff81cc4de.ngrok-free.app"; // Your backend's ngrok URL

/**
 * A wrapper around the native fetch API to automatically add the
 * Telegram Mini App authentication header and ngrok bypass header.
 */
export const fetchApi = async (path, options = {}) => {
    const tg = window.Telegram?.WebApp;
    if (!tg || !tg.initData) {
        throw new Error("Telegram authentication data (initData) is not available. App must be run inside Telegram.");
    }

    const defaultHeaders = {
        'Content-Type': 'application/json',
        'X-Telegram-Init-Data': tg.initData,
        // THIS IS THE CRITICAL FIX:
        // This header tells ngrok to skip its interstitial warning page.
        'ngrok-skip-browser-warning': 'true',
    };

    const config = { ...options, headers: { ...defaultHeaders, ...options.headers } };

    const response = await fetch(`${API_BASE_URL}${path}`, config);

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.detail || `Load failed (Status: ${response.status})`;
        throw new Error(errorMessage);
    }

    if (response.status === 204) return null;

    return response.json();
};

// --- API Functions for our Dashboard ---
export const getMyPlans = () => fetchApi('/dashboard/plans');
export const getMyChannels = () => fetchApi('/dashboard/channels');