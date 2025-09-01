// frontend/src/App.jsx
import './App.css';
import WebApp from '@twa-dev/sdk';
import { useEffect, useState } from 'react';

function App() {
    const [userData, setUserData] = useState(null);

    useEffect(() => {
        // Check if the WebApp object is available and has user data
        if (WebApp.initDataUnsafe?.user) {
            setUserData(WebApp.initDataUnsafe.user);
        }
    }, []);

    return (
        <div className="App">
            <h1>Welcome to MemberFlow!</h1>
            <p>This is your creator dashboard, running live inside Telegram.</p>

            {userData ? (
                <div className="user-data">
                    <h2>Your Telegram Info:</h2>
                    <p><strong>ID:</strong> {userData.id}</p>
                    <p><strong>Name:</strong> {userData.first_name} {userData.last_name}</p>
                    <p><strong>Username:</strong> @{userData.username}</p>
                </div>
            ) : (
                <p>Loading Telegram user data...</p>
            )}

        </div>
    );
}

export default App;