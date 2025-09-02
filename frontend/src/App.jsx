// frontend/src/App.jsx
import { useEffect, useState, useCallback } from 'react';
import './App.css';
import { getMyPlans, getMyChannels, createMyPlan } from './apiClient';
import Modal from './components/Modal';
import CreatePlanForm from './components/CreatePlanForm';
import PaymentSettings from './components/PaymentSettings';

const tg = window.Telegram?.WebApp;

function App() {
    const [user, setUser] = useState(null);
    const [plans, setPlans] = useState([]);
    const [channels, setChannels] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [newPlanData, setNewPlanData] = useState(null);
    const [currentPage, setCurrentPage] = useState('dashboard'); // 'dashboard' or 'settings'

    useEffect(() => {
        if (!tg) {
            setError("This app must be run inside the Telegram client.");
            setLoading(false);
            return;
        }
        setUser(tg.initDataUnsafe?.user || null);
        tg.ready();
        tg.expand();

        (async () => {
            try {
                const [plansData, channelsData] = await Promise.all([getMyPlans(), getMyChannels()]);
                setPlans(plansData);
                setChannels(channelsData);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        })();
    }, []);

    const handleCreatePlanClick = useCallback(async () => {
        if (!newPlanData || !newPlanData.name || newPlanData.price <= 0) {
            tg.HapticFeedback.notificationOccurred('error');
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
            tg.MainButton.onClick(handleCreatePlanClick);
            return () => tg.MainButton.offClick(handleCreatePlanClick);
        }
    }, [isModalOpen, handleCreatePlanClick]);

    const openCreatePlanModal = () => {
        setIsModalOpen(true);
        tg.MainButton.setText('Save Plan');
        tg.MainButton.disable();
        tg.MainButton.show();
    };

    const closeCreatePlanModal = () => {
        setIsModalOpen(false);
        tg.MainButton.hide();
    };

    const handleFormDataChange = (data) => {
        setNewPlanData(data);
        if (data.name && data.price > 0) {
            tg.MainButton.enable();
        } else {
            tg.MainButton.disable();
        }
    };

    if (loading) return <div className="App"><p>Loading...</p></div>;
    if (error) return <div className="App"><div className="error-box"><p><strong>An error occurred:</strong> {error}</p></div></div>;

    const renderDashboard = () => (
        <>
            <div className="section">
                <h2>Your Connected Channels</h2>
                {channels.length > 0 ? (
                    <ul>{channels.map((channel) => (<li key={channel.id}>✅ {channel.title}</li>))}</ul>
                ) : <p>You haven't connected any channels yet.</p>}
            </div>
            <div className="section">
                <div className="section-header">
                    <h2>Your Subscription Plans</h2>
                    <button className="create-button" onClick={openCreatePlanModal}>+ Create Plan</button>
                </div>
                {plans.length > 0 ? (
                    <ul>{plans.map((plan) => (<li key={plan.id}><strong>{plan.name}</strong> - ${plan.price} / {plan.interval}</li>))}</ul>
                ) : <p>You haven't created any plans yet.</p>}
            </div>
        </>
    );

    return (
        <div className="App">
            <Modal show={isModalOpen} onClose={closeCreatePlanModal} title="Create a New Plan">
                <CreatePlanForm onDataChange={handleFormDataChange} />
            </Modal>

            <div className="app-header">
                <h1>{currentPage === 'dashboard' ? 'Dashboard' : 'Payment Settings'}</h1>
                <button className="settings-button" onClick={() => setCurrentPage(currentPage === 'dashboard' ? 'settings' : 'dashboard')}>
                    {currentPage === 'dashboard' ? '⚙️ Settings' : 'Back'}
                </button>
            </div>
            {user && <p className="welcome-message">Welcome, {user?.first_name}!</p>}

            {currentPage === 'dashboard' ? renderDashboard() : <PaymentSettings />}
        </div>
    );
}

export default App;