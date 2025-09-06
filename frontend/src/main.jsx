// frontend/src/main.jsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { HashRouter } from 'react-router-dom';
import { TonConnectUIProvider } from '@tonconnect/ui-react';
import './index.css';
import App from './App.jsx';
import ErrorBoundary from './ErrorBoundary.jsx';

const manifestUrl = `${window.location.origin}/tonconnect-manifest.json`;

createRoot(document.getElementById('root')).render(
    <StrictMode>
        {/* V-- WRAP EVERYTHING INSIDE THE ERROR BOUNDARY --V */}
        <ErrorBoundary>
            <TonConnectUIProvider manifestUrl={manifestUrl}>
                <HashRouter>
                    <App />
                </HashRouter>
            </TonConnectUIProvider>
        </ErrorBoundary>
        {/* A-- END OF WRAPPER --A */}
    </StrictMode>,
);