import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { ArrowLeft, Phone, Mail, MapPin, Shield } from "lucide-react";
import {
  patients as patientsApi,
  appointments as appointmentsApi,
  observations as observationsApi,
} from "../api/client";
import type { Patient, Appointment, Observation } from "../types";
import StatusBadge from "../components/StatusBadge";

export default function PatientDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [patient, setPatient] = useState<Patient | null>(null);
  const [appointmentList, setAppointments] = useState<Appointment[]>([]);
  const [observationList, setObservations] = useState<Observation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    Promise.all([
      patientsApi.get(id),
      appointmentsApi.list({ patient_id: id }),
      observationsApi.list({ patient_id: id }),
    ])
      .then(([p, a, o]) => {
        setPatient(p);
        setAppointments(a);
        setObservations(o);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <p className="mt-8 text-center text-gray-400">Loading...</p>;
  }
  if (!patient) {
    return <p className="mt-8 text-center text-gray-400">Patient not found.</p>;
  }

  const age = Math.floor(
    (Date.now() - new Date(patient.date_of_birth).getTime()) /
      (365.25 * 24 * 3600 * 1000),
  );

  return (
    <div>
      <Link
        to="/patients"
        className="mb-4 inline-flex items-center gap-1 text-sm text-gray-500 hover:text-gray-700"
      >
        <ArrowLeft className="h-4 w-4" /> Back to patients
      </Link>

      {/* Header */}
      <div className="rounded-xl border bg-white p-6 shadow-sm">
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold">
              {patient.first_name} {patient.last_name}
            </h1>
            <p className="text-gray-500">
              MRN: {patient.mrn} &middot; {age} years &middot;{" "}
              <span className="capitalize">{patient.gender}</span>
            </p>
          </div>
          <span
            className={`rounded-full px-3 py-1 text-sm font-medium ${
              patient.active
                ? "bg-green-100 text-green-700"
                : "bg-gray-100 text-gray-500"
            }`}
          >
            {patient.active ? "Active" : "Inactive"}
          </span>
        </div>

        <div className="mt-4 grid grid-cols-1 gap-3 text-sm sm:grid-cols-2 lg:grid-cols-4">
          {patient.phone && (
            <div className="flex items-center gap-2 text-gray-600">
              <Phone className="h-4 w-4" /> {patient.phone}
            </div>
          )}
          {patient.email && (
            <div className="flex items-center gap-2 text-gray-600">
              <Mail className="h-4 w-4" /> {patient.email}
            </div>
          )}
          {patient.city && (
            <div className="flex items-center gap-2 text-gray-600">
              <MapPin className="h-4 w-4" /> {patient.city}, {patient.state}{" "}
              {patient.zip_code}
            </div>
          )}
          {patient.insurance_provider && (
            <div className="flex items-center gap-2 text-gray-600">
              <Shield className="h-4 w-4" /> {patient.insurance_provider} (
              {patient.insurance_id})
            </div>
          )}
        </div>

        {patient.allergies && (
          <div className="mt-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">
            <strong>Allergies:</strong> {patient.allergies}
          </div>
        )}
        {patient.notes && (
          <div className="mt-3 rounded-lg bg-yellow-50 p-3 text-sm text-yellow-800">
            <strong>Notes:</strong> {patient.notes}
          </div>
        )}
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Vitals / Observations */}
        <div className="rounded-xl border bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold">Recent Observations</h2>
          {observationList.length === 0 ? (
            <p className="mt-4 text-sm text-gray-400">No observations.</p>
          ) : (
            <div className="mt-3 divide-y">
              {observationList.map((o) => (
                <div
                  key={o.id}
                  className="flex items-center justify-between py-2.5"
                >
                  <div>
                    <p className="font-medium">{o.display_name}</p>
                    <p className="text-xs text-gray-400">
                      Code: {o.code} &middot;{" "}
                      {new Date(o.issued_at).toLocaleString()}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-semibold">
                      {o.value ?? o.value_string ?? "—"}
                    </span>
                    {o.unit && (
                      <span className="ml-1 text-sm text-gray-500">
                        {o.unit}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Appointments */}
        <div className="rounded-xl border bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold">Appointments</h2>
          {appointmentList.length === 0 ? (
            <p className="mt-4 text-sm text-gray-400">No appointments.</p>
          ) : (
            <div className="mt-3 divide-y">
              {appointmentList.map((a) => (
                <div key={a.id} className="py-3">
                  <div className="flex items-center justify-between">
                    <p className="font-medium capitalize">
                      {a.appointment_type.replace("-", " ")}
                    </p>
                    <StatusBadge status={a.status} />
                  </div>
                  <p className="mt-1 text-sm text-gray-500">{a.reason}</p>
                  <p className="text-xs text-gray-400">
                    {new Date(a.scheduled_at).toLocaleString()} &middot;{" "}
                    {a.duration_minutes} min
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
