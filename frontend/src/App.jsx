// frontend/src/App.jsx
import { Routes, Route } from 'react-router-dom';
import './App.css';
import DashboardPage from './pages/DashboardPage';
import CheckoutPage from './pages/CheckoutPage';

function App() {
    return (
        <div className="App">
            <Routes>
                {/* Route for the private creator dashboard */}
                {/* Example: https://...ngrok.app/#/ */}
                <Route path="/" element={<DashboardPage />} />

                {/* Route for the public subscriber checkout page */}
                {/* Example: https://...ngrok.app/#/pay/1 */}
                <Route path="/pay/:planId" element={<CheckoutPage />} />
            </Routes>
        </div>
    );
}

export default App;