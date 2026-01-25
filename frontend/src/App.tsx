import { useState } from 'react';
import { useMortgage } from './hooks/useMortgage';
import MortgageList from './components/MortgageList';
import MortgageForm from './components/MortgageForm';
import Dashboard from './components/Dashboard';
import Scenarios from './components/Scenarios';
import Deadlines from './components/Deadlines';
import Warnings from './components/Warnings';
import Guidance from './components/Guidance';
import type { MortgageCreate } from './types';

type Tab = 'dashboard' | 'scenarios' | 'deadlines' | 'guidance';

function App() {
  const {
    mortgages,
    selectedMortgage,
    dashboard,
    scenarios,
    deadlines,
    warnings,
    guidance,
    loading,
    error,
    selectMortgage,
    createMortgage,
    deleteMortgage,
  } = useMortgage();

  const [showForm, setShowForm] = useState(false);
  const [activeTab, setActiveTab] = useState<Tab>('dashboard');

  const handleCreateMortgage = async (data: MortgageCreate) => {
    const mortgage = await createMortgage(data);
    setShowForm(false);
    await selectMortgage(mortgage.id);
  };

  const handleDeleteMortgage = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this mortgage?')) {
      await deleteMortgage(id);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>Mortgage Guardian</h1>
        <p>Track deadlines, calculate payments, avoid foreclosure</p>
      </header>

      <main className="main">
        {error && <div className="error">{error}</div>}

        <div className="grid grid-2">
          {/* Left sidebar - Mortgage list */}
          <div>
            <div className="card">
              <div className="card-header">
                <h2 className="card-title">Your Mortgages</h2>
                <button className="btn btn-primary" onClick={() => setShowForm(true)}>
                  Add Mortgage
                </button>
              </div>

              {loading && mortgages.length === 0 ? (
                <div className="loading">Loading...</div>
              ) : mortgages.length === 0 ? (
                <div className="empty-state">
                  <h3>No mortgages yet</h3>
                  <p>Add your first mortgage to get started</p>
                </div>
              ) : (
                <MortgageList
                  mortgages={mortgages}
                  selectedId={selectedMortgage?.id}
                  onSelect={selectMortgage}
                  onDelete={handleDeleteMortgage}
                />
              )}
            </div>
          </div>

          {/* Right content - Details */}
          <div>
            {selectedMortgage ? (
              <>
                {/* Warnings */}
                {warnings.length > 0 && <Warnings warnings={warnings} />}

                {/* Tabs */}
                <div className="tabs">
                  <button
                    className={`tab ${activeTab === 'dashboard' ? 'active' : ''}`}
                    onClick={() => setActiveTab('dashboard')}
                  >
                    Dashboard
                  </button>
                  <button
                    className={`tab ${activeTab === 'scenarios' ? 'active' : ''}`}
                    onClick={() => setActiveTab('scenarios')}
                  >
                    Modification Options
                  </button>
                  <button
                    className={`tab ${activeTab === 'deadlines' ? 'active' : ''}`}
                    onClick={() => setActiveTab('deadlines')}
                  >
                    Timeline
                  </button>
                  <button
                    className={`tab ${activeTab === 'guidance' ? 'active' : ''}`}
                    onClick={() => setActiveTab('guidance')}
                  >
                    Action Plan
                  </button>
                </div>

                {/* Tab content */}
                {activeTab === 'dashboard' && dashboard && (
                  <Dashboard dashboard={dashboard} mortgage={selectedMortgage} />
                )}
                {activeTab === 'scenarios' && <Scenarios scenarios={scenarios} />}
                {activeTab === 'deadlines' && deadlines && (
                  <Deadlines deadlines={deadlines} />
                )}
                {activeTab === 'guidance' && guidance && <Guidance guidance={guidance} />}
              </>
            ) : (
              <div className="card">
                <div className="empty-state">
                  <h3>Select a mortgage</h3>
                  <p>Choose a mortgage from the list to view details</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Add Mortgage Modal */}
      {showForm && (
        <MortgageForm
          onSubmit={handleCreateMortgage}
          onCancel={() => setShowForm(false)}
          loading={loading}
        />
      )}
    </div>
  );
}

export default App;
