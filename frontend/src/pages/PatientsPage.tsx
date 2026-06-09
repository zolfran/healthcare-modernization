import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Search } from "lucide-react";
import { patients as patientsApi } from "../api/client";
import type { Patient } from "../types";

export default function PatientsPage() {
  const [patientList, setPatients] = useState<Patient[]>([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      patientsApi
        .list({ search: search || undefined })
        .then(setPatients)
        .finally(() => setLoading(false));
    }, 250);
    return () => clearTimeout(timer);
  }, [search]);

  return (
    <div>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Patients</h1>
          <p className="text-gray-500">Manage patient records</p>
        </div>
      </div>

      <div className="relative mt-5">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
        <input
          className="w-full rounded-lg border bg-white py-2.5 pl-10 pr-4 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500"
          placeholder="Search by name or MRN..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {loading ? (
        <p className="mt-8 text-center text-gray-400">Loading...</p>
      ) : (
        <div className="mt-5 overflow-hidden rounded-xl border bg-white shadow-sm">
          <table className="w-full text-left text-sm">
            <thead className="border-b bg-gray-50 text-xs uppercase text-gray-500">
              <tr>
                <th className="px-4 py-3">MRN</th>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Date of Birth</th>
                <th className="px-4 py-3">Gender</th>
                <th className="px-4 py-3">Insurance</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {patientList.map((p) => (
                <tr key={p.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-mono text-xs">{p.mrn}</td>
                  <td className="px-4 py-3">
                    <Link
                      to={`/patients/${p.id}`}
                      className="font-medium text-primary-600 hover:underline"
                    >
                      {p.last_name}, {p.first_name}
                    </Link>
                  </td>
                  <td className="px-4 py-3">
                    {new Date(p.date_of_birth).toLocaleDateString()}
                  </td>
                  <td className="px-4 py-3 capitalize">{p.gender}</td>
                  <td className="px-4 py-3">{p.insurance_provider ?? "—"}</td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${
                        p.active
                          ? "bg-green-100 text-green-700"
                          : "bg-gray-100 text-gray-500"
                      }`}
                    >
                      {p.active ? "Active" : "Inactive"}
                    </span>
                  </td>
                </tr>
              ))}
              {patientList.length === 0 && (
                <tr>
                  <td colSpan={6} className="py-6 text-center text-gray-400">
                    No patients found
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
