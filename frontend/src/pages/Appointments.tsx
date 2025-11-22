import { useEffect, useState } from 'react';
import { appointmentsApi } from '../services/api';
import type { Appointment } from '../types';
import { format } from 'date-fns';
import { de } from 'date-fns/locale';
import { Calendar, Plus, Trash2 } from 'lucide-react';

export default function Appointments() {
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newAppointment, setNewAppointment] = useState({
    title: '',
    description: '',
    appointment_date: '',
    location: '',
  });

  useEffect(() => {
    loadAppointments();
  }, []);

  const loadAppointments = async () => {
    try {
      const data = await appointmentsApi.getAll(true);
      setAppointments(data);
    } catch (error) {
      console.error('Fehler beim Laden der Termine:', error);
    }
  };

  const handleAddAppointment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAppointment.title.trim() || !newAppointment.appointment_date) return;

    try {
      await appointmentsApi.create({
        ...newAppointment,
        appointment_date: new Date(newAppointment.appointment_date).toISOString(),
      });
      setNewAppointment({ title: '', description: '', appointment_date: '', location: '' });
      setShowAddForm(false);
      loadAppointments();
    } catch (error) {
      console.error('Fehler beim Erstellen:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Termin wirklich löschen?')) return;

    try {
      await appointmentsApi.delete(id);
      setAppointments(appointments.filter((a) => a.id !== id));
    } catch (error) {
      console.error('Fehler beim Löschen:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Termine</h1>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="btn btn-primary"
        >
          <Plus className="w-4 h-4 mr-2 inline" />
          Neuer Termin
        </button>
      </div>

      {/* Neuer Termin Formular */}
      {showAddForm && (
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Neuen Termin erstellen</h2>
          <form onSubmit={handleAddAppointment} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Titel *
              </label>
              <input
                type="text"
                className="input w-full"
                value={newAppointment.title}
                onChange={(e) =>
                  setNewAppointment({ ...newAppointment, title: e.target.value })
                }
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Beschreibung
              </label>
              <textarea
                className="input w-full"
                rows={3}
                value={newAppointment.description}
                onChange={(e) =>
                  setNewAppointment({ ...newAppointment, description: e.target.value })
                }
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Datum & Uhrzeit *
                </label>
                <input
                  type="datetime-local"
                  className="input w-full"
                  value={newAppointment.appointment_date}
                  onChange={(e) =>
                    setNewAppointment({
                      ...newAppointment,
                      appointment_date: e.target.value,
                    })
                  }
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Ort
                </label>
                <input
                  type="text"
                  className="input w-full"
                  value={newAppointment.location}
                  onChange={(e) =>
                    setNewAppointment({ ...newAppointment, location: e.target.value })
                  }
                />
              </div>
            </div>

            <div className="flex space-x-3">
              <button type="submit" className="btn btn-primary">
                Erstellen
              </button>
              <button
                type="button"
                onClick={() => setShowAddForm(false)}
                className="btn btn-secondary"
              >
                Abbrechen
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Terminliste */}
      <div className="space-y-3">
        {appointments.length === 0 ? (
          <div className="card text-center py-12 text-gray-500">
            <Calendar className="w-12 h-12 mx-auto mb-3 text-gray-400" />
            <p>Keine anstehenden Termine</p>
          </div>
        ) : (
          appointments.map((appointment) => (
            <div key={appointment.id} className="card">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3">
                    <Calendar className="w-5 h-5 text-primary-600" />
                    <h3 className="font-semibold text-gray-900">
                      {appointment.title}
                    </h3>
                  </div>
                  {appointment.description && (
                    <p className="text-sm text-gray-600 mt-2 ml-8">
                      {appointment.description}
                    </p>
                  )}
                  <div className="mt-2 ml-8 space-y-1">
                    <p className="text-sm text-primary-600 font-medium">
                      📅{' '}
                      {format(
                        new Date(appointment.appointment_date),
                        "EEEE, dd. MMMM yyyy 'um' HH:mm 'Uhr'",
                        { locale: de }
                      )}
                    </p>
                    {appointment.location && (
                      <p className="text-sm text-gray-600">
                        📍 {appointment.location}
                      </p>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(appointment.id)}
                  className="text-gray-400 hover:text-red-600 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
