// Mortgage types matching backend schemas

export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type ForeclosureType = 'JUDICIAL' | 'NON_JUDICIAL' | 'HYBRID';
export type ForeclosureStage = 'CURRENT' | 'GRACE_PERIOD' | 'LATE' | 'DEFAULT' | 'PRE_FORECLOSURE' | 'FORECLOSURE' | 'AUCTION';
export type MilestoneStatus = 'PASSED' | 'CURRENT' | 'UPCOMING';
export type WarningType = 'PAYMENT_DUE' | 'LATE_NOTICE' | 'DEFAULT_WARNING' | 'PRE_FORECLOSURE' | 'FORECLOSURE_NOTICE' | 'AUCTION_IMMINENT' | 'HIGH_DTI' | 'UNDERWATER';
export type WarningSeverity = 'INFO' | 'WARNING' | 'URGENT' | 'CRITICAL';
export type ScenarioType = 'RATE_REDUCTION_1' | 'RATE_REDUCTION_2' | 'TERM_EXTENSION_10' | 'TERM_EXTENSION_20' | 'PRINCIPAL_FORBEARANCE' | 'COMBINATION';
export type Priority = 'IMMEDIATE' | 'HIGH' | 'MEDIUM' | 'LOW';
export type ResourceType = 'GOVERNMENT' | 'NONPROFIT' | 'LEGAL' | 'FINANCIAL';

export interface MortgageCreate {
  loan_amount: number;
  current_balance: number;
  interest_rate: number;
  loan_term_months: number;
  remaining_months: number;
  monthly_payment: number;
  loan_start_date: string;
  last_payment_date?: string | null;
  missed_payments?: number;
  monthly_income?: number;
  monthly_expenses?: number;
  property_value?: number;
  state: string;
  property_address?: string;
}

export interface MortgageUpdate {
  current_balance?: number;
  interest_rate?: number;
  remaining_months?: number;
  monthly_payment?: number;
  last_payment_date?: string | null;
  missed_payments?: number;
  monthly_income?: number;
  monthly_expenses?: number;
  property_value?: number;
  property_address?: string;
}

export interface Mortgage extends MortgageCreate {
  id: number;
  created_at: string;
  updated_at: string;
}

export interface PaymentDashboard {
  mortgage_id: number;
  current_monthly_payment: number;
  days_past_due: number;
  total_arrears: number;
  late_fees_estimate: number;
  risk_level: RiskLevel;
  dti_ratio: number;
  next_payment_due?: string;
  ltv_ratio?: number;
}

export interface ModificationScenario {
  scenario_type: ScenarioType;
  description: string;
  new_interest_rate?: number;
  new_monthly_payment: number;
  payment_change: number;
  new_term_months: number;
  term_change_months: number;
  total_interest: number;
  total_cost: number;
  meets_affordability: boolean;
}

export interface Milestone {
  stage: string;
  days_from_first_missed: number;
  estimated_date?: string;
  description: string;
  status: MilestoneStatus;
}

export interface DeadlineInfo {
  state: string;
  state_name: string;
  foreclosure_type: ForeclosureType;
  timeline_days_min: number;
  timeline_days_max: number;
  current_stage: ForeclosureStage;
  days_until_next_stage?: number;
  milestones: Milestone[];
}

export interface Warning {
  type: WarningType;
  severity: WarningSeverity;
  title: string;
  message: string;
  action_required: boolean;
  deadline?: string;
}

export interface GuidanceStep {
  step_number: number;
  title: string;
  description: string;
  priority: Priority;
  deadline_days?: number;
  phone_number?: string;
  url?: string;
}

export interface Resource {
  name: string;
  type: ResourceType;
  description: string;
  phone?: string;
  url?: string;
  state_specific: boolean;
}

export interface GuidanceResponse {
  risk_level: RiskLevel;
  summary: string;
  immediate_steps: GuidanceStep[];
  resources: Resource[];
  lender_script?: string;
}

export interface PaymentCalculationRequest {
  principal: number;
  annual_rate: number;
  term_months: number;
}

export interface PaymentCalculationResponse {
  monthly_payment: number;
  total_interest: number;
  total_cost: number;
}

export interface StateInfo {
  code: string;
  name: string;
  foreclosure_type: ForeclosureType;
  timeline_days_min: number;
  timeline_days_max: number;
  notes?: string;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}
