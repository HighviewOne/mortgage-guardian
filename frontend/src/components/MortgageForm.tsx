import { useState, useEffect } from 'react';
import { api } from '../services/api';
import type { MortgageCreate, StateInfo } from '../types';

interface MortgageFormProps {
  onSubmit: (data: MortgageCreate) => Promise<void>;
  onCancel: () => void;
  loading: boolean;
}

function MortgageForm({ onSubmit, onCancel, loading }: MortgageFormProps) {
  const [states, setStates] = useState<StateInfo[]>([]);
  const [formData, setFormData] = useState<MortgageCreate>({
    loan_amount: 0,
    current_balance: 0,
    interest_rate: 0,
    loan_term_months: 360,
    remaining_months: 360,
    monthly_payment: 0,
    loan_start_date: '',
    last_payment_date: null,
    missed_payments: 0,
    monthly_income: 0,
    monthly_expenses: 0,
    property_value: 0,
    state: '',
    property_address: '',
  });

  useEffect(() => {
    api.states.list().then(setStates);
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'number' ? parseFloat(value) || 0 : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit(formData);
  };

  return (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h2 className="modal-title">Add New Mortgage</h2>
          <button className="modal-close" onClick={onCancel}>
            &times;
          </button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Original Loan Amount ($)</label>
              <input
                type="number"
                name="loan_amount"
                className="form-input"
                value={formData.loan_amount || ''}
                onChange={handleChange}
                required
                min="1"
                step="1000"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Current Balance ($)</label>
              <input
                type="number"
                name="current_balance"
                className="form-input"
                value={formData.current_balance || ''}
                onChange={handleChange}
                required
                min="1"
                step="1000"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Interest Rate (%)</label>
              <input
                type="number"
                name="interest_rate"
                className="form-input"
                value={formData.interest_rate || ''}
                onChange={handleChange}
                required
                min="0.1"
                max="25"
                step="0.125"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Monthly Payment ($)</label>
              <input
                type="number"
                name="monthly_payment"
                className="form-input"
                value={formData.monthly_payment || ''}
                onChange={handleChange}
                required
                min="1"
                step="0.01"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Original Term (months)</label>
              <input
                type="number"
                name="loan_term_months"
                className="form-input"
                value={formData.loan_term_months || ''}
                onChange={handleChange}
                required
                min="12"
                max="480"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Remaining Months</label>
              <input
                type="number"
                name="remaining_months"
                className="form-input"
                value={formData.remaining_months || ''}
                onChange={handleChange}
                required
                min="1"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Loan Start Date</label>
              <input
                type="date"
                name="loan_start_date"
                className="form-input"
                value={formData.loan_start_date}
                onChange={handleChange}
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label">Last Payment Date</label>
              <input
                type="date"
                name="last_payment_date"
                className="form-input"
                value={formData.last_payment_date || ''}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Missed Payments</label>
              <input
                type="number"
                name="missed_payments"
                className="form-input"
                value={formData.missed_payments || ''}
                onChange={handleChange}
                min="0"
              />
            </div>
            <div className="form-group">
              <label className="form-label">State</label>
              <select
                name="state"
                className="form-input"
                value={formData.state}
                onChange={handleChange}
                required
              >
                <option value="">Select state...</option>
                {states.map((state) => (
                  <option key={state.code} value={state.code}>
                    {state.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Monthly Income ($)</label>
              <input
                type="number"
                name="monthly_income"
                className="form-input"
                value={formData.monthly_income || ''}
                onChange={handleChange}
                min="0"
                step="100"
              />
            </div>
            <div className="form-group">
              <label className="form-label">Monthly Expenses ($)</label>
              <input
                type="number"
                name="monthly_expenses"
                className="form-input"
                value={formData.monthly_expenses || ''}
                onChange={handleChange}
                min="0"
                step="100"
              />
            </div>
          </div>

          <div className="form-group">
            <label className="form-label">Property Value ($)</label>
            <input
              type="number"
              name="property_value"
              className="form-input"
              value={formData.property_value || ''}
              onChange={handleChange}
              min="0"
              step="1000"
            />
          </div>

          <div className="form-group">
            <label className="form-label">Property Address</label>
            <input
              type="text"
              name="property_address"
              className="form-input"
              value={formData.property_address || ''}
              onChange={handleChange}
              placeholder="123 Main St, City, State ZIP"
            />
          </div>

          <div className="modal-actions">
            <button type="button" className="btn btn-secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Adding...' : 'Add Mortgage'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default MortgageForm;
