const BASE_URL = "/api/v1";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API ${res.status}: ${body}`);
  }
  if (res.status === 204) return undefined as unknown as T;
  return res.json() as Promise<T>;
}

// --- Patients ---
import type { Patient, Practitioner, Appointment, Observation } from "../types";

export const patients = {
  list: (params?: { search?: string; active?: boolean }) => {
    const qs = new URLSearchParams();
    if (params?.search) qs.set("search", params.search);
    if (params?.active !== undefined) qs.set("active", String(params.active));
    return request<Patient[]>(`/patients/?${qs}`);
  },
  get: (id: string) => request<Patient>(`/patients/${id}`),
  create: (data: Partial<Patient>) =>
    request<Patient>("/patients/", { method: "POST", body: JSON.stringify(data) }),
};

// --- Practitioners ---
export const practitioners = {
  list: (params?: { specialty?: string }) => {
    const qs = new URLSearchParams();
    if (params?.specialty) qs.set("specialty", params.specialty);
    return request<Practitioner[]>(`/practitioners/?${qs}`);
  },
  get: (id: string) => request<Practitioner>(`/practitioners/${id}`),
};

// --- Appointments ---
export const appointments = {
  list: (params?: { patient_id?: string; status?: string }) => {
    const qs = new URLSearchParams();
    if (params?.patient_id) qs.set("patient_id", params.patient_id);
    if (params?.status) qs.set("status", params.status);
    return request<Appointment[]>(`/appointments/?${qs}`);
  },
  get: (id: string) => request<Appointment>(`/appointments/${id}`),
};

// --- Observations ---
export const observations = {
  list: (params?: { patient_id?: string; code?: string }) => {
    const qs = new URLSearchParams();
    if (params?.patient_id) qs.set("patient_id", params.patient_id);
    if (params?.code) qs.set("code", params.code);
    return request<Observation[]>(`/observations/?${qs}`);
  },
};
