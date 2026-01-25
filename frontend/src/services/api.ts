/**
 * Centralized API client for Mortgage Guardian backend
 */

/// <reference types="vite/client" />

import type {
  Mortgage,
  MortgageCreate,
  MortgageUpdate,
  PaymentDashboard,
  ModificationScenario,
  DeadlineInfo,
  Warning,
  GuidanceResponse,
  PaymentCalculationRequest,
  PaymentCalculationResponse,
  StateInfo,
  HealthResponse,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new ApiError(
      response.status,
      errorData.detail || `HTTP error ${response.status}`
    );
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json();
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  return handleResponse<T>(response);
}

// Health check
export async function healthCheck(): Promise<HealthResponse> {
  return request<HealthResponse>('/health');
}

// Mortgage CRUD operations
export async function listMortgages(): Promise<Mortgage[]> {
  return request<Mortgage[]>('/api/v1/mortgages');
}

export async function getMortgage(id: number): Promise<Mortgage> {
  return request<Mortgage>(`/api/v1/mortgages/${id}`);
}

export async function createMortgage(data: MortgageCreate): Promise<Mortgage> {
  return request<Mortgage>('/api/v1/mortgages', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

export async function updateMortgage(
  id: number,
  data: MortgageUpdate
): Promise<Mortgage> {
  return request<Mortgage>(`/api/v1/mortgages/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  });
}

export async function deleteMortgage(id: number): Promise<void> {
  return request<void>(`/api/v1/mortgages/${id}`, {
    method: 'DELETE',
  });
}

// Dashboard and calculations
export async function getPaymentDashboard(
  mortgageId: number
): Promise<PaymentDashboard> {
  return request<PaymentDashboard>(
    `/api/v1/mortgages/${mortgageId}/dashboard`
  );
}

export async function getModificationScenarios(
  mortgageId: number
): Promise<ModificationScenario[]> {
  return request<ModificationScenario[]>(
    `/api/v1/mortgages/${mortgageId}/scenarios`
  );
}

export async function getDeadlines(mortgageId: number): Promise<DeadlineInfo> {
  return request<DeadlineInfo>(`/api/v1/mortgages/${mortgageId}/deadlines`);
}

export async function getWarnings(mortgageId: number): Promise<Warning[]> {
  return request<Warning[]>(`/api/v1/mortgages/${mortgageId}/warnings`);
}

export async function getGuidance(
  mortgageId: number
): Promise<GuidanceResponse> {
  return request<GuidanceResponse>(`/api/v1/mortgages/${mortgageId}/guidance`);
}

// Standalone calculations
export async function calculatePayment(
  data: PaymentCalculationRequest
): Promise<PaymentCalculationResponse> {
  return request<PaymentCalculationResponse>('/api/v1/calculate/payment', {
    method: 'POST',
    body: JSON.stringify(data),
  });
}

// State information
export async function listStates(): Promise<StateInfo[]> {
  return request<StateInfo[]>('/api/v1/states');
}

// Export API client object
export const api = {
  healthCheck,
  mortgages: {
    list: listMortgages,
    get: getMortgage,
    create: createMortgage,
    update: updateMortgage,
    delete: deleteMortgage,
  },
  dashboard: {
    get: getPaymentDashboard,
  },
  scenarios: {
    get: getModificationScenarios,
  },
  deadlines: {
    get: getDeadlines,
  },
  warnings: {
    get: getWarnings,
  },
  guidance: {
    get: getGuidance,
  },
  calculate: {
    payment: calculatePayment,
  },
  states: {
    list: listStates,
  },
};

export { ApiError };
export default api;
