import type { Warning } from '../types';

interface WarningsProps {
  warnings: Warning[];
}

function Warnings({ warnings }: WarningsProps) {
  const getSeverityClass = (severity: string) => {
    return `alert alert-${severity.toLowerCase()}`;
  };

  const formatDate = (dateStr: string | undefined) => {
    if (!dateStr) return null;
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  // Sort by severity
  const sortedWarnings = [...warnings].sort((a, b) => {
    const severityOrder = { CRITICAL: 0, URGENT: 1, WARNING: 2, INFO: 3 };
    return (severityOrder[a.severity] || 4) - (severityOrder[b.severity] || 4);
  });

  return (
    <div style={{ marginBottom: '1.5rem' }}>
      {sortedWarnings.map((warning, index) => (
        <div key={index} className={getSeverityClass(warning.severity)}>
          <div className="alert-title">
            {warning.severity === 'CRITICAL' && '🚨 '}
            {warning.severity === 'URGENT' && '⚠️ '}
            {warning.title}
          </div>
          <div className="alert-message">{warning.message}</div>
          {warning.deadline && (
            <div style={{ marginTop: '0.5rem', fontSize: '0.875rem', fontWeight: 500 }}>
              Deadline: {formatDate(warning.deadline)}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default Warnings;
