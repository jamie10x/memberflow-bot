// frontend/src/pages/CheckoutPage.jsx
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { TonConnectButton, useTonConnectUI, useTonWallet } from '@tonconnect/ui-react';
import { getPublicPlanDetails, initTonPayment, verifyTonPayment } from '../apiClient';
import './CheckoutPage.css';

function CheckoutPage() {
    const { planId } = useParams();
    const [tonConnectUI] = useTonConnectUI();
    const wallet = useTonWallet();
    const tg = window.Telegram?.WebApp;

    /** @type {[import('../apiClient').Plan | null, Function]} */
    const [plan, setPlan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [paymentStatus, setPaymentStatus] = useState('idle'); // idle, processing, verifying, success, failed

    useEffect(() => {
        if (tg) {
            tg.ready();
            tg.expand();
        }

        (async () => {
            try {
                if (!planId) throw new Error("No Plan ID specified in the URL.");
                const planData = await getPublicPlanDetails(planId);
                setPlan(planData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        })();
    }, [planId]);

    const handlePayment = async () => {
        if (!plan || !wallet || !tg?.initDataUnsafe?.user) {
            tg.showAlert("Please connect your wallet. Make sure you are running this inside Telegram.");
            return;
        }

        try {
            setPaymentStatus('processing');
            setError(null);

            const user = tg.initDataUnsafe.user;

            // Step 1: Tell our backend we are starting a payment.
            const paymentDetails = await initTonPayment({
                plan_id: plan.id,
                telegram_id: user.id,
                username: user.username,
            });

            // Step 2: Construct the transaction for the user's wallet.
            const transaction = {
                validUntil: Math.floor(Date.now() / 1000) + 360, // Transaction is valid for 6 minutes
                messages: [{
                    address: paymentDetails.to_wallet,
                    amount: paymentDetails.amount,
                    // CRITICAL FIX: The memo should be a plain string. The wallet handles encoding it as a comment.
                    // Do NOT use btoa() here.
                    payload: paymentDetails.memo
                }]
            };

            // Step 3: Send the transaction to the wallet. This opens the confirmation sheet.
            await tonConnectUI.sendTransaction(transaction);

            setPaymentStatus('verifying');

            // Step 4: Ask our backend to verify the transaction on the blockchain.
            await verifyTonPayment({ boc_hash: paymentDetails.boc_hash });

            // Step 5: Success!
            setPaymentStatus('success');
            tg.HapticFeedback.notificationOccurred('success');
            tg.showPopup({
                title: 'Payment Successful!',
                message: 'You now have access to the channel. The bot will send you an invite link shortly.'
            }, () => tg.close());

        } catch (err) {
            setPaymentStatus('failed');
            const errorMessage = err?.message || 'An unknown error occurred.';
            setError(`Payment failed: ${errorMessage}`);
            tg.HapticFeedback.notificationOccurred('error');
            console.error(err);
        }
    };

    if (loading) return <div className="App"><p>Loading plan details...</p></div>;
    if (error && paymentStatus !== 'failed') return <div className="App"><div className="error-box"><p>Error: {error}</p></div></div>;
    if (!plan) return <div className="App"><p>Plan not found.</p></div>;

    return (
        <div className="checkout-page">
            <div className="ton-connect-button-container"><TonConnectButton /></div>
            <h1>{plan.name}</h1>
            <div className="price-display">
                ${plan.price}<span> / {plan.interval}</span>
            </div>
            <p className="description">Subscribe to get instant access.</p>

            {paymentStatus === 'success' ? (
                <div className="success-message">✅ Payment complete! Check your DMs for an invite link.</div>
            ) : (
                <button
                    className="pay-button"
                    onClick={handlePayment}
                    disabled={!wallet || paymentStatus === 'processing' || paymentStatus === 'verifying'}
                >
                    { wallet ?
                        (paymentStatus === 'processing' ? 'Confirm in Wallet...' :
                            (paymentStatus === 'verifying' ? 'Verifying...' : 'Proceed to Pay'))
                        : 'Connect Wallet to Pay'
                    }
                </button>
            )}

            {error && paymentStatus === 'failed' && <div className="error-box"><p>Error: {error}</p></div>}
        </div>
    );
}

export default CheckoutPage;