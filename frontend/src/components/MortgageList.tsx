import type { Mortgage } from '../types';

interface MortgageListProps {
  mortgages: Mortgage[];
  selectedId?: number;
  onSelect: (id: number) => void;
  onDelete: (id: number) => void;
}

function MortgageList({ mortgages, selectedId, onSelect, onDelete }: MortgageListProps) {
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      maximumFractionDigits: 0,
    }).format(amount);
  };

  return (
    <div className="mortgage-list">
      {mortgages.map((mortgage) => (
        <div
          key={mortgage.id}
          className={`mortgage-item ${selectedId === mortgage.id ? 'selected' : ''}`}
          onClick={() => onSelect(mortgage.id)}
        >
          <div className="mortgage-item-info">
            <div className="mortgage-item-address">
              {mortgage.property_address || `Mortgage #${mortgage.id}`}
            </div>
            <div className="mortgage-item-balance">
              Balance: {formatCurrency(mortgage.current_balance)} | {mortgage.state}
            </div>
          </div>
          <button
            className="btn btn-secondary"
            onClick={(e) => {
              e.stopPropagation();
              onDelete(mortgage.id);
            }}
          >
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}

export default MortgageList;
