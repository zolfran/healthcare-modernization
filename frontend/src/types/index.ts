export interface Patient {
  id: string;
  mrn: string;
  first_name: string;
  last_name: string;
  date_of_birth: string;
  gender: string;
  email: string | null;
  phone: string | null;
  address_line1: string | null;
  address_line2: string | null;
  city: string | null;
  state: string | null;
  zip_code: string | null;
  insurance_provider: string | null;
  insurance_id: string | null;
  allergies: string | null;
  notes: string | null;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Practitioner {
  id: string;
  npi: string;
  first_name: string;
  last_name: string;
  specialty: string;
  email: string | null;
  phone: string | null;
  department: string | null;
  active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Appointment {
  id: string;
  patient_id: string;
  practitioner_id: string;
  scheduled_at: string;
  duration_minutes: number;
  status: string;
  appointment_type: string;
  reason: string | null;
  notes: string | null;
  created_at: string;
  updated_at: string;
}

export interface Observation {
  id: string;
  patient_id: string;
  code: string;
  display_name: string;
  value: number | null;
  value_string: string | null;
  unit: string | null;
  status: string;
  issued_at: string;
  notes: string | null;
  created_at: string;
}
