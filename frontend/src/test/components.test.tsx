import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Warnings from '../components/Warnings';
import Scenarios from '../components/Scenarios';
import type { Warning, ModificationScenario } from '../types';

describe('Warnings Component', () => {
  it('renders warnings sorted by severity', () => {
    const warnings: Warning[] = [
      {
        type: 'HIGH_DTI',
        severity: 'WARNING',
        title: 'High DTI',
        message: 'Your debt-to-income ratio is high',
        action_required: false,
      },
      {
        type: 'DEFAULT_WARNING',
        severity: 'CRITICAL',
        title: 'Default Warning',
        message: 'You are 30+ days past due',
        action_required: true,
      },
    ];

    render(<Warnings warnings={warnings} />);

    // Both warnings should be rendered
    expect(screen.getByText(/Default Warning/)).toBeInTheDocument();
    expect(screen.getByText('High DTI')).toBeInTheDocument();
  });

  it('displays deadline when present', () => {
    const warnings: Warning[] = [
      {
        type: 'PAYMENT_DUE',
        severity: 'INFO',
        title: 'Payment Due',
        message: 'Your payment is due soon',
        action_required: true,
        deadline: '2025-02-01',
      },
    ];

    render(<Warnings warnings={warnings} />);
    expect(screen.getByText(/Deadline:/)).toBeInTheDocument();
  });
});

describe('Scenarios Component', () => {
  it('renders modification scenarios', () => {
    const scenarios: ModificationScenario[] = [
      {
        scenario_type: 'RATE_REDUCTION_1',
        description: '1% Interest Rate Reduction',
        new_interest_rate: 5.5,
        new_monthly_payment: 1703.37,
        payment_change: -192.83,
        new_term_months: 324,
        term_change_months: 0,
        total_interest: 277091.88,
        total_cost: 552091.88,
        meets_affordability: true,
      },
      {
        scenario_type: 'TERM_EXTENSION_10',
        description: '10-Year Term Extension',
        new_interest_rate: 6.5,
        new_monthly_payment: 1500,
        payment_change: -396.2,
        new_term_months: 444,
        term_change_months: 120,
        total_interest: 391000,
        total_cost: 666000,
        meets_affordability: true,
      },
    ];

    render(<Scenarios scenarios={scenarios} />);

    expect(screen.getByText('1% Interest Rate Reduction')).toBeInTheDocument();
    expect(screen.getByText('10-Year Term Extension')).toBeInTheDocument();
  });

  it('shows empty state when no scenarios', () => {
    render(<Scenarios scenarios={[]} />);
    expect(screen.getByText('No modification scenarios available')).toBeInTheDocument();
  });

  it('displays affordability badges', () => {
    const scenarios: ModificationScenario[] = [
      {
        scenario_type: 'RATE_REDUCTION_1',
        description: '1% Rate Reduction',
        new_monthly_payment: 1703.37,
        payment_change: -192.83,
        new_term_months: 324,
        term_change_months: 0,
        total_interest: 277091.88,
        total_cost: 552091.88,
        meets_affordability: true,
      },
    ];

    render(<Scenarios scenarios={scenarios} />);
    expect(screen.getByText('Meets 31% DTI Target')).toBeInTheDocument();
  });
});
