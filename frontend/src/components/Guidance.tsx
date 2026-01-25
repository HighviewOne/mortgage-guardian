import { useState } from 'react';
import type { GuidanceResponse } from '../types';

interface GuidanceProps {
  guidance: GuidanceResponse;
}

function Guidance({ guidance }: GuidanceProps) {
  const [showScript, setShowScript] = useState(false);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'IMMEDIATE':
        return '#ef4444';
      case 'HIGH':
        return '#f97316';
      case 'MEDIUM':
        return '#3b82f6';
      default:
        return '#64748b';
    }
  };

  const getResourceTypeColor = (type: string) => {
    switch (type) {
      case 'GOVERNMENT':
        return '#3b82f6';
      case 'NONPROFIT':
        return '#22c55e';
      case 'LEGAL':
        return '#8b5cf6';
      default:
        return '#64748b';
    }
  };

  return (
    <div>
      {/* Summary */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>Your Situation</h3>
        <p>{guidance.summary}</p>
      </div>

      {/* Action Steps */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>Action Steps</h3>

        {guidance.immediate_steps.map((step) => (
          <div key={step.step_number} className="step">
            <div
              className="step-number"
              style={{ background: getPriorityColor(step.priority) }}
            >
              {step.step_number}
            </div>
            <div className="step-content">
              <div className="step-title">
                {step.title}
                {step.deadline_days && (
                  <span style={{
                    marginLeft: '0.5rem',
                    fontSize: '0.75rem',
                    color: getPriorityColor(step.priority),
                    fontWeight: 'normal'
                  }}>
                    (Within {step.deadline_days} days)
                  </span>
                )}
              </div>
              <div className="step-description">{step.description}</div>
              {step.phone_number && (
                <a href={`tel:${step.phone_number}`} className="step-link">
                  📞 {step.phone_number}
                </a>
              )}
              {step.url && (
                <a href={step.url} target="_blank" rel="noopener noreferrer" className="step-link" style={{ marginLeft: step.phone_number ? '1rem' : 0 }}>
                  🔗 Visit Website
                </a>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Lender Script */}
      {guidance.lender_script && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Lender Call Script</h3>
            <button
              className="btn btn-secondary"
              onClick={() => setShowScript(!showScript)}
            >
              {showScript ? 'Hide Script' : 'Show Script'}
            </button>
          </div>

          {showScript && (
            <div className="script-box">
              {guidance.lender_script}
            </div>
          )}

          {!showScript && (
            <p style={{ fontSize: '0.875rem', color: '#64748b' }}>
              We've prepared a script to help you communicate with your lender effectively.
              Click "Show Script" to view it.
            </p>
          )}
        </div>
      )}

      {/* Resources */}
      <div className="card">
        <h3 className="card-title" style={{ marginBottom: '1rem' }}>Helpful Resources</h3>

        <div className="grid grid-2">
          {guidance.resources.map((resource, index) => (
            <div key={index} className="resource">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                <div className="resource-name">{resource.name}</div>
                <span
                  className="resource-type"
                  style={{ color: getResourceTypeColor(resource.type) }}
                >
                  {resource.type}
                </span>
              </div>
              <div className="resource-description">{resource.description}</div>
              <div className="resource-contact">
                {resource.phone && (
                  <a href={`tel:${resource.phone}`} style={{ marginRight: '1rem' }}>
                    📞 {resource.phone}
                  </a>
                )}
                {resource.url && (
                  <a href={resource.url} target="_blank" rel="noopener noreferrer">
                    🔗 Website
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Guidance;
