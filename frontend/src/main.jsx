// frontend/src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
import { TonConnectUIProvider } from '@tonconnect/ui-react';
import './index.css';
import App from './App.jsx';
import ErrorBoundary from './ErrorBoundary.jsx';

const manifestUrl = `${window.location.origin}/tonconnect-manifest.json`;

// --- NEW ROBUST INITIALIZATION ---

function renderApp() {
    const rootElement = document.getElementById('root');
    if (!rootElement) {
        console.error("Root element not found");
        return;
    }

    const root = createRoot(rootElement);
    root.render(
        <StrictMode>
            <ErrorBoundary>
                <TonConnectUIProvider manifestUrl={manifestUrl}>
                    <HashRouter>
                        <App />
                    </HashRouter>
                </TonConnectUIProvider>
            </ErrorBoundary>
        </StrictMode>
    );
}

// Check if the Telegram script is loaded.
// It might take a moment to inject the `window.Telegram` object.
if (window.Telegram?.WebApp) {
    // If it's already there, render immediately.
    renderApp();
} else {
    // If not, wait for the 'telegram.WebApp.ready' event.
    // This is a more reliable way to ensure the script is ready.
    // We add a timeout as a fallback in case the event doesn't fire.
    let timeout;

    const onTelegramReady = () => {
        clearTimeout(timeout);
        window.removeEventListener('telegram.WebApp.ready', onTelegramReady);
        renderApp();
    };

    window.addEventListener('telegram.WebApp.ready', onTelegramReady);

    // Fallback timeout: If the ready event doesn't fire after 2 seconds,
    // try to render anyway. This covers edge cases.
    timeout = setTimeout(() => {
        console.warn("Telegram WebApp ready event timed out. Attempting to render anyway.");
        window.removeEventListener('telegram.WebApp.ready', onTelegramReady);
        renderApp();
    }, 2000);
}