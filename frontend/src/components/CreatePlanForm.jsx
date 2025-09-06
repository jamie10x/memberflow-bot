// frontend/src/components/CreatePlanForm.jsx
import React, { useState, useEffect } from 'react';
import './CreatePlanForm.css';

const CreatePlanForm = ({ onDataChange, channels }) => { // Added channels prop
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [interval, setInterval] = useState('month');
    const [currency] = useState('USD');
    // ADDED: State to hold the selected channel ID
    const [channelId, setChannelId] = useState('');

    // Set the default selected channel to the first one when the component mounts
    useEffect(() => {
        if (channels && channels.length > 0) {
            setChannelId(channels[0].id);
        }
    }, [channels]);

    useEffect(() => {
        onDataChange({
            name,
            price: price ? parseFloat(price) : 0,
            interval,
            currency,
            channel_id: channelId ? parseInt(channelId, 10) : null, // Pass channel_id up
        });
    }, [name, price, interval, currency, channelId, onDataChange]);

    return (
        <div className="create-plan-form">
            {/* ADDED: Channel selector dropdown */}
            <div className="form-group">
                <label htmlFor="plan-channel">Channel</label>
                <select
                    id="plan-channel"
                    value={channelId}
                    onChange={(e) => setChannelId(e.target.value)}
                    required
                    disabled={!channels || channels.length === 0}
                >
                    {channels && channels.length > 0 ? (
                        channels.map(channel => (
                            <option key={channel.id} value={channel.id}>
                                {channel.title}
                            </option>
                        ))
                    ) : (
                        <option>Please connect a channel first</option>
                    )}
                </select>
            </div>

            <div className="form-group">
                <label htmlFor="plan-name">Plan Name</label>
                <input
                    id="plan-name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g., Monthly Masterclass"
                    required
                />
            </div>
            <div className="form-group">
                <label htmlFor="plan-price">Price (USD)</label>
                <input
                    id="plan-price"
                    type="number"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                    placeholder="e.g., 30.00"
                    required
                    step="0.01"
                    min="0.50"
                />
            </div>
            <div className="form-group">
                <label htmlFor="plan-interval">Billing Interval</label>
                <select id="plan-interval" value={interval} onChange={(e) => setInterval(e.target.value)}>
                    <option value="month">Monthly</option>
                    <option value="year">Yearly</option>
                </select>
            </div>
        </div>
    );
};

export default CreatePlanForm;