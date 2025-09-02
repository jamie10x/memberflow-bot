// frontend/src/components/PaymentSettings.jsx
import React, { useState, useEffect } from 'react';
import { getMyPaymentSettings, saveMyPaymentSettings } from '../apiClient';
import './PaymentSettings.css';

const tg = window.Telegram?.WebApp;

const PaymentSettings = () => {
    const [walletAddress, setWalletAddress] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // Fetch existing settings when the component loads
    useEffect(() => {
        (async () => {
            try {
                const settings = await getMyPaymentSettings();
                if (settings && settings.gateway_type === 'ton_wallet') {
                    setWalletAddress(settings.credentials?.wallet_address || '');
                }
            } catch (err) {
                setError(err.message);
                console.error("Failed to fetch payment settings:", err);
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    const handleSave = async () => {
        // Basic validation for a TON wallet address format
        if (!walletAddress || !/^[Uu][Qq][0-9a-zA-Z\-_]{46}$/.test(walletAddress)) {
            tg.showAlert("Please enter a valid TON wallet address (should start with UQ or uq).");
            return;
        }

        tg.MainButton.showProgress();
        tg.MainButton.disable();

        try {
            const settingsData = {
                gateway_type: 'ton_wallet',
                credentials: { wallet_address: walletAddress },
            };
            await saveMyPaymentSettings(settingsData);

            // Give feedback and close the app
            tg.HapticFeedback.notificationOccurred('success');
            tg.showPopup({
                title: 'Settings Saved!',
                message: 'Your TON wallet address has been saved successfully.',
                buttons: [{ type: 'ok', text: 'Great!' }]
            }, () => tg.close()); // Close the Mini App after the user clicks "Great!"

        } catch (err) {
            tg.HapticFeedback.notificationOccurred('error');
            tg.showAlert(`Error: ${err.message}`);
        } finally {
            tg.MainButton.hideProgress();
            tg.MainButton.enable();
        }
    };

    // Configure the native Telegram Main Button for this "page"
    useEffect(() => {
        tg.MainButton.setText('Save Settings');
        tg.MainButton.onClick(handleSave);
        tg.MainButton.show();

        // Cleanup: remove the event listener and hide the button when the component is unmounted
        return () => {
            tg.MainButton.offClick(handleSave);
            tg.MainButton.hide();
        }
    }, [walletAddress]); // Re-bind the handler if walletAddress changes to capture the latest state

    if (loading) return <p>Loading payment settings...</p>;
    if (error) return <div className="error-box"><p>Error: {error}</p></div>;

    return (
        <div className="payment-settings">
            <h2>TON Wallet Payments</h2>
            <p className="description">
                Enable direct, low-fee payments from subscribers to your TON wallet.
                Enter the wallet address where you'd like to receive payments (USDT).
            </p>
            <div className="form-group">
                <label htmlFor="wallet-address">Your TON Wallet Address</label>
                <input
                    id="wallet-address"
                    type="text"
                    value={walletAddress}
                    onChange={(e) => setWalletAddress(e.target.value)}
                    placeholder="UQ... or uq..."
                />
            </div>
        </div>
    );
};

export default PaymentSettings;