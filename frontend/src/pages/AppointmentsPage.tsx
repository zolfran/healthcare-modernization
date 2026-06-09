import { useEffect, useState } from "react";
import { appointments as appointmentsApi } from "../api/client";
import type { Appointment } from "../types";
import StatusBadge from "../components/StatusBadge";

const STATUSES = [
  "all",
  "scheduled",
  "confirmed",
  "in-progress",
  "completed",
  "cancelled",
  "no-show",
];

export default function AppointmentsPage() {
  const [appointmentList, setAppointments] = useState<Appointment[]>([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    appointmentsApi
      .list({ status: filter === "all" ? undefined : filter })
      .then(setAppointments)
      .finally(() => setLoading(false));
  }, [filter]);

  return (
    <div>
      <h1 className="text-2xl font-bold">Appointments</h1>
      <p className="text-gray-500">Schedule and manage appointments</p>

      <div className="mt-5 flex flex-wrap gap-2">
        {STATUSES.map((s) => (
          <button
            key={s}
            onClick={() => {
              setLoading(true);
              setFilter(s);
            }}
            className={`rounded-full px-3 py-1 text-sm font-medium capitalize transition ${
              filter === s
                ? "bg-primary-600 text-white"
                : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="mt-8 text-center text-gray-400">Loading...</p>
      ) : (
        <div className="mt-5 overflow-hidden rounded-xl border bg-white shadow-sm">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-gray-50 text-xs uppercase text-gray-500">
              <tr>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Scheduled</th>
                <th className="px-4 py-3">Duration</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Reason</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {appointmentList.map((a) => (
                <tr key={a.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 capitalize font-medium">
                    {a.appointment_type.replace("-", " ")}
                  </td>
                  <td className="px-4 py-3">
                    {new Date(a.scheduled_at).toLocaleString()}
                  </td>
                  <td className="px-4 py-3">{a.duration_minutes} min</td>
                  <td className="px-4 py-3">
                    <StatusBadge status={a.status} />
                  </td>
                  <td className="px-4 py-3 text-gray-500">
                    {a.reason ?? "—"}
                  </td>
                </tr>
              ))}
              {appointmentList.length === 0 && (
                <tr>
                  <td colSpan={5} className="py-6 text-center text-gray-400">
                    No appointments found
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
