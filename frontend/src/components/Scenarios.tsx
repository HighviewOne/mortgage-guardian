import type { ModificationScenario } from '../types';

interface ScenariosProps {
  scenarios: ModificationScenario[];
}

function Scenarios({ scenarios }: ScenariosProps) {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 2,
    }).format(amount);
  };

  const formatChange = (amount: number) => {
    const sign = amount < 0 ? '' : '+';
    return `${sign}${formatCurrency(amount)}/mo`;
  };

  if (scenarios.length === 0) {
    return (
      <div className="card">
        <div className="empty-state">
          <p>No modification scenarios available</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '0.5rem' }}>Loan Modification Scenarios</h3>
        <p style={{ color: '#64748b', marginBottom: '1.5rem', fontSize: '0.875rem' }}>
          These are potential options to discuss with your lender. Actual terms will vary.
        </p>

        <div className="grid grid-2">
          {scenarios.map((scenario) => (
            <div key={scenario.scenario_type} className="scenario">
              <div className="scenario-title">{scenario.description}</div>

              <div className="scenario-payment">
                {formatCurrency(scenario.new_monthly_payment)}
              </div>

              <div className={`scenario-change ${scenario.payment_change < 0 ? 'positive' : 'negative'}`}>
                {formatChange(scenario.payment_change)}
              </div>

              <div className="scenario-details">
                {scenario.new_interest_rate && (
                  <div>New Rate: {scenario.new_interest_rate}%</div>
                )}
                {scenario.term_change_months !== 0 && (
                  <div>Term Change: {scenario.term_change_months > 0 ? '+' : ''}{scenario.term_change_months} months</div>
                )}
                <div>Total Interest: {formatCurrency(scenario.total_interest)}</div>
                <div>Total Cost: {formatCurrency(scenario.total_cost)}</div>
              </div>

              <span className={`scenario-badge ${scenario.meets_affordability ? 'scenario-affordable' : 'scenario-unaffordable'}`}>
                {scenario.meets_affordability ? 'Meets 31% DTI Target' : 'Above DTI Target'}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>Understanding Your Options</h3>

        <div style={{ marginBottom: '1rem' }}>
          <strong>Rate Reduction</strong>
          <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
            Lowering your interest rate reduces your monthly payment without extending your term.
            This is often the preferred option if you can qualify.
          </p>
        </div>

        <div style={{ marginBottom: '1rem' }}>
          <strong>Term Extension</strong>
          <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
            Extending your loan term spreads payments over more years, reducing monthly costs.
            However, you'll pay more total interest over the life of the loan.
          </p>
        </div>

        <div>
          <strong>Principal Forbearance</strong>
          <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
            A portion of your principal is set aside and doesn't accrue interest. It becomes a
            balloon payment due when you sell, refinance, or at the end of your loan term.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Scenarios;
