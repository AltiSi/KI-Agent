import { useEffect, useState } from 'react';
import { dashboardApi } from '../services/api';
import type { Dashboard as DashboardType } from '../types';
import { format } from 'date-fns';
import { de } from 'date-fns/locale';
import { CheckSquare, Calendar, AlertCircle } from 'lucide-react';

export default function Dashboard() {
  const [dashboard, setDashboard] = useState<DashboardType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await dashboardApi.get();
      setDashboard(data);
    } catch (error) {
      console.error('Fehler beim Laden des Dashboards:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Laden...</div>;
  }

  if (!dashboard) {
    return <div className="text-center py-12">Fehler beim Laden</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-gray-600">Willkommen zurück! 👋</p>
      </div>

      {/* KI-Zusammenfassung */}
      <div className="card bg-gradient-to-r from-primary-500 to-primary-600 text-white">
        <h2 className="text-xl font-semibold mb-3">Dein Tag im Überblick</h2>
        <p className="text-primary-50">{dashboard.daily_summary}</p>
      </div>

      {/* Statistiken */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-orange-100 rounded-lg">
              <CheckSquare className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                Offene Aufgaben
              </p>
              <p className="text-2xl font-bold text-gray-900">
                {dashboard.pending_tasks_count}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Calendar className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">
                Termine heute
              </p>
              <p className="text-2xl font-bold text-gray-900">
                {dashboard.today_appointments_count}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Anstehende Aufgaben */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <CheckSquare className="w-5 h-5 mr-2" />
          Anstehende Aufgaben
        </h2>

        {dashboard.upcoming_tasks.length === 0 ? (
          <p className="text-gray-500">Keine anstehenden Aufgaben 🎉</p>
        ) : (
          <div className="space-y-3">
            {dashboard.upcoming_tasks.slice(0, 5).map((task) => (
              <div
                key={task.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <div className={`badge badge-${task.priority}`}>
                    {task.priority}
                  </div>
                  <span className="font-medium">{task.title}</span>
                </div>
                {task.due_date && (
                  <span className="text-sm text-gray-600">
                    {format(new Date(task.due_date), 'dd. MMM yyyy', {
                      locale: de,
                    })}
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Anstehende Termine */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4 flex items-center">
          <Calendar className="w-5 h-5 mr-2" />
          Nächste Termine
        </h2>

        {dashboard.upcoming_appointments.length === 0 ? (
          <p className="text-gray-500">Keine anstehenden Termine</p>
        ) : (
          <div className="space-y-3">
            {dashboard.upcoming_appointments.slice(0, 5).map((appointment) => (
              <div
                key={appointment.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div>
                  <p className="font-medium">{appointment.title}</p>
                  {appointment.location && (
                    <p className="text-sm text-gray-600">
                      📍 {appointment.location}
                    </p>
                  )}
                </div>
                <span className="text-sm font-medium text-primary-600">
                  {format(
                    new Date(appointment.appointment_date),
                    'dd. MMM, HH:mm',
                    { locale: de }
                  )}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
