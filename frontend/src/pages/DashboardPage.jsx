// frontend/src/pages/DashboardPage.jsx
import { useEffect, useState, useCallback } from 'react';
import '../App.css';
import {
    getMyPlans,
    getMyChannels,
    createMyPlan,
    deleteMyPlan,
    getMyAnalytics,
} from '../apiClient';
import Modal from '../components/Modal';
import CreatePlanForm from '../components/CreatePlanForm';
import PaymentSettings from '../components/PaymentSettings';

const tg = window.Telegram?.WebApp;
const FRONTEND_BASE_URL = window.location.origin;

function DashboardPage() {
    const [user, setUser] = useState(null);
    const [analytics, setAnalytics] = useState({ mrr: 0, active_subscriptions: 0, subscribers: [] });
    const [plans, setPlans] = useState([]);
    const [channels, setChannels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newPlanData, setNewPlanData] = useState(null);
    const [currentPage, setCurrentPage] = useState('dashboard');

    const fetchData = useCallback(async () => {
        try {
            setLoading(true);
            const [analyticsData, plansData, channelsData] = await Promise.all([
                getMyAnalytics(),
                getMyPlans(),
                getMyChannels(),
            ]);
            setAnalytics(analyticsData);
            setPlans(plansData);
            setChannels(channelsData);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (!tg) {
            setError("This app must be run inside the Telegram client.");
            setLoading(false);
            return;
        }
        setUser(tg.initDataUnsafe?.user || null);
        tg.ready();
        tg.expand();
        fetchData().catch(console.error);
    }, [fetchData]);

    const handleCreatePlanClick = useCallback(async () => {
        // MODIFIED: Added check for channel_id
        if (!newPlanData || !newPlanData.name || newPlanData.price <= 0 || !newPlanData.channel_id) {
            tg.HapticFeedback.notificationOccurred('error');
            tg.showAlert("Please fill out all fields, including selecting a channel.");
            return;
        }
        tg.MainButton.showProgress();
        tg.MainButton.disable();
        try {
            const newPlan = await createMyPlan(newPlanData);
            setPlans(prevPlans => [...prevPlans, newPlan]);
            tg.HapticFeedback.notificationOccurred('success');
            closeCreatePlanModal();
        } catch (err) {
            tg.HapticFeedback.notificationOccurred('error');
            tg.showAlert(`Error creating plan: ${err.message}`);
        } finally {
            tg.MainButton.hideProgress();
        }
    }, [newPlanData]);

    useEffect(() => {
        if (isModalOpen) {
            tg?.MainButton.onClick(handleCreatePlanClick);
            return () => tg?.MainButton.offClick(handleCreatePlanClick);
        }
    }, [isModalOpen, handleCreatePlanClick]);

    const handleDeletePlan = async (planId) => {
        tg.showConfirm(`Are you sure you want to delete this plan?`, async (confirmed) => {
            if (confirmed) {
                try {
                    await deleteMyPlan(planId);
                    setPlans(prevPlans => prevPlans.filter(p => p.id !== planId));
                    tg.HapticFeedback.notificationOccurred('success');
                } catch (err) {
                    tg.HapticFeedback.notificationOccurred('error');
                    tg.showAlert(`Error deleting plan: ${err.message}`);
                }
            }
        });
    };

    const openCreatePlanModal = () => {
        if (channels.length === 0) {
            tg.showAlert("You must connect a channel before you can create a plan. Go back to the bot and add it as an admin to your private channel.");
            return;
        }
        setIsModalOpen(true);
        tg.MainButton.setText('Save Plan').show();
        tg.MainButton.disable();
    };

    const closeCreatePlanModal = () => {
        setIsModalOpen(false);
        tg.MainButton.hide();
    };

    const handleFormDataChange = (data) => {
        setNewPlanData(data);
        // MODIFIED: Also check for channel_id before enabling the save button
        if (data.name && data.price > 0 && data.channel_id) {
            tg.MainButton.enable();
        } else {
            tg.MainButton.disable();
        }
    };

    const handleSharePlan = (planId) => {
        const paymentLink = `${FRONTEND_BASE_URL}/#/pay/${planId}`;
        // MODIFIED: Use a more user-friendly popup for copying links.
        tg.showPopup({
            title: 'Shareable Link',
            message: 'Here is the payment link for your plan. Share it with your potential subscribers!',
            buttons: [
                { id: 'copy', type: 'default', text: 'Copy Link' },
                { type: 'close' }
            ]
        }, (buttonId) => {
            if (buttonId === 'copy') {
                tg.CloudStorage.setItem('clipboard', paymentLink, () => {
                    tg.HapticFeedback.notificationOccurred('success');
                });
            }
        });
    };

    if (loading) return <div className="App"><p>Loading Dashboard...</p></div>;
    if (error) return <div className="App"><div className="error-box"><p><strong>Error:</strong> {error}</p></div></div>;

    const renderDashboard = () => (
        <>
            <div className="analytics-grid">
                <div className="analytic-card">
                    <h3>MRR (USD)</h3>
                    <p>${analytics.mrr}</p>
                </div>
                <div className="analytic-card">
                    <h3>Active Subscribers</h3>
                    <p>{analytics.active_subscriptions}</p>
                </div>
            </div>

            <div className="section">
                <h2>Your Connected Channels</h2>
                {channels.length > 0 ? (
                    <ul className="channel-list">{channels.map((channel) => (<li key={channel.id}>✅ {channel.title}</li>))}</ul>
                ) : <p className="hint-text">You haven't connected any channels yet. Add the bot as an admin to your private Telegram channel to get started.</p>}
            </div>

            <div className="section">
                <div className="section-header">
                    <h2>Your Subscription Plans</h2>
                    <button className="create-button" onClick={openCreatePlanModal}>+ Create Plan</button>
                </div>
                {plans.length > 0 ? (
                    <ul className="plan-list">{plans.map((plan) => (
                        <li key={plan.id} className="plan-item">
                            <div className="plan-details">
                                <strong>{plan.name}</strong><span>${plan.price} / {plan.interval}</span>
                            </div>
                            <div className="plan-actions">
                                <button className="action-button" onClick={() => handleSharePlan(plan.id)}>Share</button>
                                <button className="action-button destructive" onClick={() => handleDeletePlan(plan.id)}>Delete</button>
                            </div>
                        </li>
                    ))}</ul>
                ) : <p className="hint-text">You haven't created any plans yet.</p>}
            </div>

            <div className="section">
                <h2>Active Subscribers</h2>
                {analytics.subscribers.length > 0 ? (
                    <table className="subscribers-table">
                        <thead>
                        <tr>
                            <th>Subscriber ID</th>
                            <th>Plan</th>
                            <th>Expires At</th>
                        </tr>
                        </thead>
                        <tbody>
                        {analytics.subscribers.map(sub => (
                            <tr key={sub.id}>
                                <td>{sub.subscriber.telegram_id}</td>
                                <td>{sub.plan.name}</td>
                                <td>{new Date(sub.expires_at).toLocaleDateString()}</td>
                            </tr>
                        ))}
                        </tbody>
                    </table>
                ) : <p className="hint-text">No active subscribers yet.</p>}
            </div>
        </>
    );

    return (
        <>
            <Modal show={isModalOpen} onClose={closeCreatePlanModal} title="Create a New Plan">
                {/* MODIFIED: Pass the channels list to the form */}
                <CreatePlanForm onDataChange={handleFormDataChange} channels={channels} />
            </Modal>

            <div className="app-header">
                <h1>{currentPage === 'dashboard' ? 'Dashboard' : 'Payment Settings'}</h1>
                <button className="settings-button" onClick={() => setCurrentPage(c => c === 'dashboard' ? 'settings' : 'dashboard')}>
                    {currentPage === 'dashboard' ? '⚙️ Settings' : 'Back'}
                </button>
            </div>
            {user && <p className="welcome-message">Welcome, {user?.first_name}!</p>}

            {currentPage === 'dashboard' ? renderDashboard() : <PaymentSettings />}
        </>
    );
}

export default DashboardPage;