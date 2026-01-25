import type { DeadlineInfo } from '../types';

interface DeadlinesProps {
  deadlines: DeadlineInfo;
}

function Deadlines({ deadlines }: DeadlinesProps) {
  const formatDate = (dateStr: string | undefined) => {
    if (!dateStr) return 'TBD';
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const getForeclosureTypeDescription = (type: string) => {
    switch (type) {
      case 'JUDICIAL':
        return 'Judicial foreclosure requires court action. This process is longer but offers more protections.';
      case 'NON_JUDICIAL':
        return 'Non-judicial foreclosure does not require court involvement. This process is typically faster.';
      case 'HYBRID':
        return 'Your state allows both judicial and non-judicial foreclosure. The lender chooses the process.';
      default:
        return '';
    }
  };

  const getStageLabel = (stage: string) => {
    const labels: Record<string, string> = {
      CURRENT: 'Current',
      GRACE_PERIOD: 'Grace Period',
      LATE: 'Late',
      DEFAULT: 'Default',
      PRE_FORECLOSURE: 'Pre-Foreclosure',
      FORECLOSURE: 'Foreclosure',
      AUCTION: 'Auction',
    };
    return labels[stage] || stage;
  };

  return (
    <div>
      {/* State Info */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>
          Foreclosure Timeline in {deadlines.state_name}
        </h3>

        <div className="grid grid-2" style={{ marginBottom: '1rem' }}>
          <div>
            <div style={{ fontSize: '0.875rem', color: '#64748b' }}>Foreclosure Type</div>
            <div style={{ fontWeight: 600 }}>{deadlines.foreclosure_type.replace('_', '-')}</div>
          </div>
          <div>
            <div style={{ fontSize: '0.875rem', color: '#64748b' }}>Typical Timeline</div>
            <div style={{ fontWeight: 600 }}>
              {deadlines.timeline_days_min} - {deadlines.timeline_days_max} days
            </div>
          </div>
        </div>

        <p style={{ fontSize: '0.875rem', color: '#64748b', marginBottom: '1rem' }}>
          {getForeclosureTypeDescription(deadlines.foreclosure_type)}
        </p>

        <div style={{
          padding: '1rem',
          background: '#eff6ff',
          borderRadius: '8px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div>
            <div style={{ fontSize: '0.875rem', color: '#64748b' }}>Current Stage</div>
            <div style={{ fontWeight: 600, fontSize: '1.25rem' }}>
              {getStageLabel(deadlines.current_stage)}
            </div>
          </div>
          {deadlines.days_until_next_stage && (
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '2rem', fontWeight: 700, color: '#f97316' }}>
                {deadlines.days_until_next_stage}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b' }}>days until next stage</div>
            </div>
          )}
        </div>
      </div>

      {/* Timeline Milestones */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>Foreclosure Milestones</h3>

        <div>
          {deadlines.milestones.map((milestone, index) => (
            <div key={index} className="milestone">
              <div className={`milestone-status milestone-${milestone.status.toLowerCase()}`} />
              <div className="milestone-content">
                <div className="milestone-title">{milestone.stage}</div>
                <div className="milestone-date">
                  {milestone.status === 'PASSED' ? 'Passed' : formatDate(milestone.estimated_date)}
                  {' • '}
                  Day {milestone.days_from_first_missed} from first missed payment
                </div>
                <div className="milestone-description">{milestone.description}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Important Notice */}
      <div className="card" style={{ background: '#fef9c3', border: '1px solid #eab308' }}>
        <h3 className="card-title" style={{ marginBottom: '0.5rem' }}>Important Notice</h3>
        <p style={{ fontSize: '0.875rem' }}>
          These timelines are estimates based on state law. Actual foreclosure timelines can vary
          based on lender procedures, court backlogs, and other factors. Many lenders also have
          internal policies that may delay foreclosure. Contact your lender and a housing counselor
          for specific information about your situation.
        </p>
      </div>
    </div>
  );
}

export default Deadlines;
