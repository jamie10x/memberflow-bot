// frontend/src/App.jsx
import { useEffect, useState } from 'react';
import './App.css';
import { getMyPlans, getMyChannels } from './apiClient';

// Assign the global Telegram object to a constant.
// This is safe because it's only assigned once.
const tg = window.Telegram?.WebApp;

function App() {
    const [user, setUser] = useState(null);
    const [plans, setPlans] = useState([]);
    const [channels, setChannels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Check for the Telegram WebApp object.
        if (!tg) {
            setError("This app must be run inside the Telegram client.");
            setLoading(false);
            return;
        }

        // Set user data immediately for a better UI experience.
        setUser(tg.initDataUnsafe?.user || null);
        tg.ready();
        tg.expand();

        // Use an Immediately Invoked Function Expression (IIFE)
        // to handle the async data fetching. This resolves the
        // "Promise returned from fetchData is ignored" warning.
        (async () => {
            try {
                const [plansData, channelsData] = await Promise.all([
                    getMyPlans(),
                    getMyChannels(),
                ]);
                setPlans(plansData);
                setChannels(channelsData);
            } catch (err) {
                setError(err.message);
                console.error("Failed to fetch dashboard data:", err);
            } finally {
                setLoading(false);
            }
        })();
    }, []); // Empty array ensures this effect runs only once on mount.

    // Render a loading state while fetching data.
    if (loading) {
        return <div className="App"><p>Loading your data...</p></div>;
    }

    // Render an error state if something went wrong.
    if (error) {
        return (
            <div className="App">
                <div className="error-box">
                    <p><strong>An error occurred:</strong></p>
                    <p>{error}</p>
                </div>
            </div>
        );
    }

    // Render the main dashboard content.
    return (
        <div className="App">
            <h1>Dashboard</h1>
            {/* Use optional chaining (?.) to safely access properties */}
            {/* This resolves the "Unresolved variable first_name" warning. */}
            {user && <p className="welcome-message">Welcome, {user?.first_name}!</p>}

            <div className="section">
                <h2>Your Connected Channels</h2>
                {channels.length > 0 ? (
                    <ul>
                        {channels.map((channel) => (
                            <li key={channel.id}>✅ {channel.title}</li>
                        ))}
                    </ul>
                ) : <p>You haven't connected any channels yet.</p>}
            </div>

            <div className="section">
                <h2>Your Subscription Plans</h2>
                {plans.length > 0 ? (
                    <ul>
                        {plans.map((plan) => (
                            <li key={plan.id}>
                                <strong>{plan.name}</strong> - ${plan.price} / {plan.interval}
                            </li>
                        ))}
                    </ul>
                ) : <p>You haven't created any plans yet.</p>}
            </div>
        </div>
    );
}

export default App;