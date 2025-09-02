// frontend/src/components/CreatePlanForm.jsx
import React, { useState, useEffect } from 'react';
import './CreatePlanForm.css';

const CreatePlanForm = ({ onDataChange }) => { // Changed prop name for clarity
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [interval, setInterval] = useState('month');
    const [currency, setCurrency] = useState('USD');

    // This effect runs every time a form field's state changes.
    useEffect(() => {
        // We report the current state of the form back to the parent component.
        onDataChange({
            name,
            price: price ? parseFloat(price) : 0, // Ensure price is a number
            interval,
            currency,
        });
    }, [name, price, interval, currency, onDataChange]); // Dependency array

    return (
        // We don't need the <form> tag anymore since we are not using a traditional submit button.
        <div className="create-plan-form">
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