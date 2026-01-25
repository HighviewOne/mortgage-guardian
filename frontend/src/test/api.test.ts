import { describe, it, expect, vi, beforeEach } from 'vitest';
import { api, ApiError } from '../services/api';

// Mock fetch
const mockFetch = vi.fn();
globalThis.fetch = mockFetch;

describe('API Client', () => {
  beforeEach(() => {
    mockFetch.mockClear();
  });

  describe('healthCheck', () => {
    it('returns health status on success', async () => {
      const mockResponse = {
        status: 'healthy',
        timestamp: '2025-01-25T00:00:00Z',
        version: '1.0.0',
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await api.healthCheck();
      expect(result).toEqual(mockResponse);
      expect(mockFetch).toHaveBeenCalledWith('/health', expect.any(Object));
    });

    it('throws ApiError on failure', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        json: () => Promise.resolve({ detail: 'Server error' }),
      });

      await expect(api.healthCheck()).rejects.toThrow(ApiError);
    });
  });

  describe('mortgages', () => {
    it('lists mortgages', async () => {
      const mockMortgages = [
        { id: 1, loan_amount: 300000, state: 'CA' },
        { id: 2, loan_amount: 250000, state: 'TX' },
      ];

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockMortgages),
      });

      const result = await api.mortgages.list();
      expect(result).toEqual(mockMortgages);
    });

    it('creates mortgage', async () => {
      const newMortgage = {
        loan_amount: 300000,
        current_balance: 275000,
        interest_rate: 6.5,
        loan_term_months: 360,
        remaining_months: 324,
        monthly_payment: 1896.2,
        loan_start_date: '2022-01-15',
        state: 'CA',
      };

      const createdMortgage = { ...newMortgage, id: 1, created_at: '2025-01-25', updated_at: '2025-01-25' };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 201,
        json: () => Promise.resolve(createdMortgage),
      });

      const result = await api.mortgages.create(newMortgage);
      expect(result).toEqual(createdMortgage);
      expect(mockFetch).toHaveBeenCalledWith(
        '/api/v1/mortgages',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify(newMortgage),
        })
      );
    });

    it('deletes mortgage', async () => {
      mockFetch.mockResolvedValueOnce({
        ok: true,
        status: 204,
      });

      await api.mortgages.delete(1);
      expect(mockFetch).toHaveBeenCalledWith(
        '/api/v1/mortgages/1',
        expect.objectContaining({
          method: 'DELETE',
        })
      );
    });
  });

  describe('dashboard', () => {
    it('gets payment dashboard', async () => {
      const mockDashboard = {
        mortgage_id: 1,
        current_monthly_payment: 1896.2,
        days_past_due: 45,
        total_arrears: 3792.4,
        late_fees_estimate: 189.62,
        risk_level: 'MEDIUM',
        dti_ratio: 42.5,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockDashboard),
      });

      const result = await api.dashboard.get(1);
      expect(result).toEqual(mockDashboard);
    });
  });

  describe('calculate', () => {
    it('calculates payment', async () => {
      const request = {
        principal: 275000,
        annual_rate: 6.5,
        term_months: 324,
      };

      const mockResponse = {
        monthly_payment: 1896.2,
        total_interest: 339448.8,
        total_cost: 614448.8,
      };

      mockFetch.mockResolvedValueOnce({
        ok: true,
        json: () => Promise.resolve(mockResponse),
      });

      const result = await api.calculate.payment(request);
      expect(result).toEqual(mockResponse);
    });
  });
});
