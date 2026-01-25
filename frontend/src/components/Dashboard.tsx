import type { PaymentDashboard, Mortgage } from '../types';

interface DashboardProps {
  dashboard: PaymentDashboard;
  mortgage: Mortgage;
}

function Dashboard({ dashboard, mortgage }: DashboardProps) {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 2,
    }).format(amount);
  };

  const formatDate = (dateStr: string | undefined) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getRiskClass = (level: string) => {
    return `risk-badge risk-${level.toLowerCase()}`;
  };

  return (
    <div>
      {/* Risk Level Banner */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h3 style={{ marginBottom: '0.5rem' }}>Payment Status</h3>
            <span className={getRiskClass(dashboard.risk_level)}>
              {dashboard.risk_level} RISK
            </span>
          </div>
          {dashboard.days_past_due > 0 && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '2rem', fontWeight: 700, color: '#ef4444' }}>
                {dashboard.days_past_due}
              </div>
              <div style={{ fontSize: '0.875rem', color: '#64748b' }}>Days Past Due</div>
            </div>
          )}
        </div>
      </div>

      {/* Stats Grid */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>Payment Overview</h3>
        <div className="grid grid-3">
          <div className="stat">
            <div className="stat-value">{formatCurrency(dashboard.current_monthly_payment)}</div>
            <div className="stat-label">Monthly Payment</div>
          </div>
          <div className="stat">
            <div className="stat-value" style={{ color: dashboard.total_arrears > 0 ? '#ef4444' : '#22c55e' }}>
              {formatCurrency(dashboard.total_arrears)}
            </div>
            <div className="stat-label">Total Arrears</div>
          </div>
          <div className="stat">
            <div className="stat-value" style={{ color: dashboard.late_fees_estimate > 0 ? '#f97316' : '#22c55e' }}>
              {formatCurrency(dashboard.late_fees_estimate)}
            </div>
            <div className="stat-label">Est. Late Fees</div>
          </div>
        </div>
      </div>

      {/* Financial Ratios */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>Financial Health</h3>
        <div className="grid grid-2">
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <span>Debt-to-Income Ratio</span>
              <strong style={{ color: dashboard.dti_ratio > 43 ? '#ef4444' : dashboard.dti_ratio > 36 ? '#f97316' : '#22c55e' }}>
                {dashboard.dti_ratio.toFixed(1)}%
              </strong>
            </div>
            <div style={{
              height: '8px',
              background: '#e2e8f0',
              borderRadius: '4px',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${Math.min(dashboard.dti_ratio, 100)}%`,
                height: '100%',
                background: dashboard.dti_ratio > 43 ? '#ef4444' : dashboard.dti_ratio > 36 ? '#f97316' : '#22c55e',
                transition: 'width 0.3s'
              }} />
            </div>
            <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem' }}>
              Target: &lt;36% | Max for modification: 31%
            </div>
          </div>

          {dashboard.ltv_ratio && (
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <span>Loan-to-Value Ratio</span>
                <strong style={{ color: dashboard.ltv_ratio > 100 ? '#ef4444' : '#22c55e' }}>
                  {dashboard.ltv_ratio.toFixed(1)}%
                </strong>
              </div>
              <div style={{
                height: '8px',
                background: '#e2e8f0',
                borderRadius: '4px',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${Math.min(dashboard.ltv_ratio, 100)}%`,
                  height: '100%',
                  background: dashboard.ltv_ratio > 100 ? '#ef4444' : '#22c55e',
                  transition: 'width 0.3s'
                }} />
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.25rem' }}>
                {dashboard.ltv_ratio > 100 ? 'Underwater: You owe more than home value' : 'Positive equity'}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Loan Details */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>Loan Details</h3>
        <table className="table">
          <tbody>
            <tr>
              <td>Original Loan Amount</td>
              <td style={{ textAlign: 'right' }}>{formatCurrency(mortgage.loan_amount)}</td>
            </tr>
            <tr>
              <td>Current Balance</td>
              <td style={{ textAlign: 'right' }}>{formatCurrency(mortgage.current_balance)}</td>
            </tr>
            <tr>
              <td>Interest Rate</td>
              <td style={{ textAlign: 'right' }}>{mortgage.interest_rate}%</td>
            </tr>
            <tr>
              <td>Remaining Term</td>
              <td style={{ textAlign: 'right' }}>{mortgage.remaining_months} months ({Math.round(mortgage.remaining_months / 12)} years)</td>
            </tr>
            <tr>
              <td>Next Payment Due</td>
              <td style={{ textAlign: 'right' }}>{formatDate(dashboard.next_payment_due)}</td>
            </tr>
            <tr>
              <td>Last Payment Made</td>
              <td style={{ textAlign: 'right' }}>{formatDate(mortgage.last_payment_date || undefined)}</td>
            </tr>
            <tr>
              <td>Missed Payments</td>
              <td style={{ textAlign: 'right', color: mortgage.missed_payments > 0 ? '#ef4444' : 'inherit' }}>
                {mortgage.missed_payments}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Dashboard;
