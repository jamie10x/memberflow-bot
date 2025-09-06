// frontend/src/apiClient.js

// IMPORTANT: Replace this with your actual public BACKEND ngrok URL.
const API_BASE_URL = "https://fbfff81cc4de.ngrok-free.app";

// JSDoc Type Definitions for IDE autocompletion and error checking.
/**
 * @typedef {Object} Plan
 * @property {number} id
 * @property {string} name
 * @property {string} price
 * @property {string} currency
 * @property {string} interval - 'month' or 'year'
 * @property {number} user_id
 */

/**
 * @typedef {Object} InitPaymentResponse
 * @property {string} boc_hash - A unique identifier for the payment attempt.
 * @property {string} to_wallet - The recipient creator's TON wallet address.
 * @property {string} amount - The transaction amount in nanotons (or nano-USDT).
 * @property {string} memo - The comment to be attached to the blockchain transaction.
 */

/**
 * A wrapper around the native fetch API to automatically add the
 * Telegram Mini App authentication header and ngrok bypass header.
 * @param {string} path - The API endpoint path (e.g., '/dashboard/plans').
 * @param {RequestInit} [options] - Standard fetch() options (method, body, etc.).
 * @returns {Promise<any>} - The JSON response from the API.
 */
export const fetchApi = async (path, options = {}) => {
    const tg = window.Telegram?.WebApp;
    if (!tg || !tg.initData) {
        throw new Error("Telegram authentication data (initData) is not available. App must be run inside Telegram.");
    }

    const defaultHeaders = {
        'Content-Type': 'application/json',
        'X-Telegram-Init-Data': tg.initData,
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

// --- API Functions ---

/**
 * Fetches public details for a single plan.
 * @param {string | number} planId
 * @returns {Promise<Plan>}
 */
export const getPublicPlanDetails = (planId) => fetchApi(`/public/plans/${planId}`);

/**
 * Initiates the payment process on the backend.
 * @param {{plan_id: number, telegram_id: number, username: string|null}} data
 * @returns {Promise<InitPaymentResponse>}
 */
export const initTonPayment = (data) => fetchApi('/checkout/init-ton-payment', { method: 'POST', body: JSON.stringify(data) });

/**
 * Asks the backend to verify a transaction.
 * @param {{boc_hash: string}} data
 * @returns {Promise<any>} // Returns a Subscription object on success
 */
export const verifyTonPayment = (data) => fetchApi('/checkout/verify-ton-payment', { method: 'POST', body: JSON.stringify(data) });

/** @returns {Promise<Plan[]>} */
export const getMyPlans = () => fetchApi('/dashboard/plans');
export const createMyPlan = (planData) => fetchApi('/dashboard/plans', { method: 'POST', body: JSON.stringify(planData) });
export const deleteMyPlan = (planId) => fetchApi(`/dashboard/plans/${planId}`, { method: 'DELETE' });

export const getMyChannels = () => fetchApi('/dashboard/channels');
export const getMyPaymentSettings = () => fetchApi('/dashboard/payment-settings');
export const saveMyPaymentSettings = (settingsData) => fetchApi('/dashboard/payment-settings', { method: 'POST', body: JSON.stringify(settingsData) });

// New function for analytics
export const getMyAnalytics = () => fetchApi('/dashboard/analytics');
