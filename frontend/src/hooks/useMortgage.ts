import { useState, useEffect, useCallback } from 'react';
import { api } from '../services/api';
import type {
  Mortgage,
  MortgageCreate,
  MortgageUpdate,
  PaymentDashboard,
  ModificationScenario,
  DeadlineInfo,
  Warning,
  GuidanceResponse,
} from '../types';

interface UseMortgageReturn {
  mortgages: Mortgage[];
  selectedMortgage: Mortgage | null;
  dashboard: PaymentDashboard | null;
  scenarios: ModificationScenario[];
  deadlines: DeadlineInfo | null;
  warnings: Warning[];
  guidance: GuidanceResponse | null;
  loading: boolean;
  error: string | null;
  selectMortgage: (id: number) => Promise<void>;
  createMortgage: (data: MortgageCreate) => Promise<Mortgage>;
  updateMortgage: (id: number, data: MortgageUpdate) => Promise<void>;
  deleteMortgage: (id: number) => Promise<void>;
  refresh: () => Promise<void>;
}

export function useMortgage(): UseMortgageReturn {
  const [mortgages, setMortgages] = useState<Mortgage[]>([]);
  const [selectedMortgage, setSelectedMortgage] = useState<Mortgage | null>(null);
  const [dashboard, setDashboard] = useState<PaymentDashboard | null>(null);
  const [scenarios, setScenarios] = useState<ModificationScenario[]>([]);
  const [deadlines, setDeadlines] = useState<DeadlineInfo | null>(null);
  const [warnings, setWarnings] = useState<Warning[]>([]);
  const [guidance, setGuidance] = useState<GuidanceResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadMortgages = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.mortgages.list();
      setMortgages(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load mortgages');
    } finally {
      setLoading(false);
    }
  }, []);

  const loadMortgageDetails = useCallback(async (id: number) => {
    try {
      setLoading(true);
      setError(null);

      const [mortgage, dashboardData, scenariosData, deadlinesData, warningsData, guidanceData] =
        await Promise.all([
          api.mortgages.get(id),
          api.dashboard.get(id),
          api.scenarios.get(id),
          api.deadlines.get(id),
          api.warnings.get(id),
          api.guidance.get(id),
        ]);

      setSelectedMortgage(mortgage);
      setDashboard(dashboardData);
      setScenarios(scenariosData);
      setDeadlines(deadlinesData);
      setWarnings(warningsData);
      setGuidance(guidanceData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load mortgage details');
    } finally {
      setLoading(false);
    }
  }, []);

  const selectMortgage = useCallback(
    async (id: number) => {
      await loadMortgageDetails(id);
    },
    [loadMortgageDetails]
  );

  const createMortgage = useCallback(
    async (data: MortgageCreate): Promise<Mortgage> => {
      setLoading(true);
      setError(null);
      try {
        const mortgage = await api.mortgages.create(data);
        await loadMortgages();
        return mortgage;
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to create mortgage';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [loadMortgages]
  );

  const updateMortgageData = useCallback(
    async (id: number, data: MortgageUpdate): Promise<void> => {
      setLoading(true);
      setError(null);
      try {
        await api.mortgages.update(id, data);
        await loadMortgages();
        if (selectedMortgage?.id === id) {
          await loadMortgageDetails(id);
        }
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to update mortgage';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [loadMortgages, loadMortgageDetails, selectedMortgage]
  );

  const deleteMortgageData = useCallback(
    async (id: number): Promise<void> => {
      setLoading(true);
      setError(null);
      try {
        await api.mortgages.delete(id);
        if (selectedMortgage?.id === id) {
          setSelectedMortgage(null);
          setDashboard(null);
          setScenarios([]);
          setDeadlines(null);
          setWarnings([]);
          setGuidance(null);
        }
        await loadMortgages();
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to delete mortgage';
        setError(message);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [loadMortgages, selectedMortgage]
  );

  const refresh = useCallback(async () => {
    await loadMortgages();
    if (selectedMortgage) {
      await loadMortgageDetails(selectedMortgage.id);
    }
  }, [loadMortgages, loadMortgageDetails, selectedMortgage]);

  useEffect(() => {
    loadMortgages();
  }, [loadMortgages]);

  return {
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
    updateMortgage: updateMortgageData,
    deleteMortgage: deleteMortgageData,
    refresh,
  };
}
