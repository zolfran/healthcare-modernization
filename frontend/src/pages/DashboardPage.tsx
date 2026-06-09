import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Users, CalendarDays, Activity, AlertTriangle } from "lucide-react";
import { patients as patientsApi, appointments as appointmentsApi } from "../api/client";
import type { Patient, Appointment } from "../types";
import StatusBadge from "../components/StatusBadge";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: React.ElementType;
  color: string;
}

function StatCard({ label, value, icon: Icon, color }: StatCardProps) {
  return (
    <div className="rounded-xl border bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{label}</p>
          <p className="mt-1 text-2xl font-bold">{value}</p>
        </div>
        <div className={`rounded-lg p-3 ${color}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const [patientList, setPatients] = useState<Patient[]>([]);
  const [appointmentList, setAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([patientsApi.list(), appointmentsApi.list()])
      .then(([p, a]) => {
        setPatients(p);
        setAppointments(a);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center text-gray-400">
        Loading...
      </div>
    );
  }

  const upcoming = appointmentList.filter(
    (a) => a.status === "scheduled" || a.status === "confirmed",
  );
  const completed = appointmentList.filter((a) => a.status === "completed");
  const urgent = appointmentList.filter(
    (a) => a.appointment_type === "urgent" && a.status !== "completed",
  );

  return (
    <div>
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="mt-1 text-gray-500">
        Healthcare modernization platform overview
      </p>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          label="Total Patients"
          value={patientList.length}
          icon={Users}
          color="bg-primary-500"
        />
        <StatCard
          label="Upcoming Appointments"
          value={upcoming.length}
          icon={CalendarDays}
          color="bg-indigo-500"
        />
        <StatCard
          label="Completed Visits"
          value={completed.length}
          icon={Activity}
          color="bg-green-500"
        />
        <StatCard
          label="Urgent Cases"
          value={urgent.length}
          icon={AlertTriangle}
          color="bg-red-500"
        />
      </div>

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
        {/* Recent patients */}
        <div className="rounded-xl border bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold">Recent Patients</h2>
          <div className="mt-3 divide-y">
            {patientList.slice(0, 5).map((p) => (
              <Link
                key={p.id}
                to={`/patients/${p.id}`}
                className="flex items-center justify-between py-3 hover:bg-gray-50 -mx-2 px-2 rounded"
              >
                <div>
                  <p className="font-medium">
                    {p.last_name}, {p.first_name}
                  </p>
                  <p className="text-sm text-gray-500">MRN: {p.mrn}</p>
                </div>
                <span className="text-xs text-gray-400">
                  {new Date(p.created_at).toLocaleDateString()}
                </span>
              </Link>
            ))}
          </div>
        </div>

        {/* Upcoming appointments */}
        <div className="rounded-xl border bg-white p-5 shadow-sm">
          <h2 className="text-lg font-semibold">Upcoming Appointments</h2>
          <div className="mt-3 divide-y">
            {upcoming.slice(0, 5).map((a) => (
              <div
                key={a.id}
                className="flex items-center justify-between py-3"
              >
                <div>
                  <p className="font-medium capitalize">
                    {a.appointment_type.replace("-", " ")}
                  </p>
                  <p className="text-sm text-gray-500">{a.reason}</p>
                </div>
                <div className="text-right">
                  <StatusBadge status={a.status} />
                  <p className="mt-1 text-xs text-gray-400">
                    {new Date(a.scheduled_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
            {upcoming.length === 0 && (
              <p className="py-4 text-center text-sm text-gray-400">
                No upcoming appointments
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
