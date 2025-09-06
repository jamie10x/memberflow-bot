// frontend/src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
import { TonConnectUIProvider } from '@tonconnect/ui-react';
import './index.css';
import App from './App.jsx';

// This is the manifest URL for your DApp.
// For now, we will point to a raw file in our public folder.
// In production, this file should be hosted at a static URL.
const manifestUrl = `${window.location.origin}/tonconnect-manifest.json`;


createRoot(document.getElementById('root')).render(
    <StrictMode>
        <TonConnectUIProvider manifestUrl={manifestUrl}>
            <HashRouter>
                <App />
            </HashRouter>
        </TonConnectUIProvider>
    </StrictMode>,
);