import { useEffect, useState } from 'react';
import { remindersApi } from '../services/api';
import type { Reminder } from '../types';
import { Bell, Plus, Trash2, ToggleLeft, ToggleRight } from 'lucide-react';

export default function Reminders() {
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newReminder, setNewReminder] = useState({
    title: '',
    description: '',
    reminder_type: 'allgemein',
    reminder_time: '',
    recurring: false,
    recurring_pattern: '',
  });

  useEffect(() => {
    loadReminders();
  }, []);

  const loadReminders = async () => {
    try {
      const data = await remindersApi.getAll(false);
      setReminders(data);
    } catch (error) {
      console.error('Fehler beim Laden:', error);
    }
  };

  const handleAddReminder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newReminder.title.trim()) return;

    try {
      await remindersApi.create({
        ...newReminder,
        reminder_time: newReminder.reminder_time
          ? new Date(newReminder.reminder_time).toISOString()
          : null,
      });
      setNewReminder({
        title: '',
        description: '',
        reminder_type: 'allgemein',
        reminder_time: '',
        recurring: false,
        recurring_pattern: '',
      });
      setShowAddForm(false);
      loadReminders();
    } catch (error) {
      console.error('Fehler beim Erstellen:', error);
    }
  };

  const handleToggleActive = async (id: number) => {
    try {
      await remindersApi.toggle(id);
      loadReminders();
    } catch (error) {
      console.error('Fehler:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Erinnerung wirklich löschen?')) return;

    try {
      await remindersApi.delete(id);
      setReminders(reminders.filter((r) => r.id !== id));
    } catch (error) {
      console.error('Fehler:', error);
    }
  };

  const reminderTypes = [
    { value: 'allgemein', label: 'Allgemein', emoji: '📌' },
    { value: 'trinken', label: 'Trinken', emoji: '💧' },
    { value: 'medikamente', label: 'Medikamente', emoji: '💊' },
    { value: 'müll', label: 'Müll', emoji: '🗑️' },
    { value: 'bewegung', label: 'Bewegung', emoji: '🏃' },
    { value: 'pause', label: 'Pause', emoji: '☕' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Erinnerungen</h1>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="btn btn-primary"
        >
          <Plus className="w-4 h-4 mr-2 inline" />
          Neue Erinnerung
        </button>
      </div>

      {/* Neue Erinnerung Formular */}
      {showAddForm && (
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Neue Erinnerung erstellen</h2>
          <form onSubmit={handleAddReminder} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Titel *
              </label>
              <input
                type="text"
                className="input w-full"
                value={newReminder.title}
                onChange={(e) =>
                  setNewReminder({ ...newReminder, title: e.target.value })
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
                rows={2}
                value={newReminder.description}
                onChange={(e) =>
                  setNewReminder({ ...newReminder, description: e.target.value })
                }
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Typ
                </label>
                <select
                  className="input w-full"
                  value={newReminder.reminder_type}
                  onChange={(e) =>
                    setNewReminder({ ...newReminder, reminder_type: e.target.value })
                  }
                >
                  {reminderTypes.map((type) => (
                    <option key={type.value} value={type.value}>
                      {type.emoji} {type.label}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Zeitpunkt
                </label>
                <input
                  type="datetime-local"
                  className="input w-full"
                  value={newReminder.reminder_time}
                  onChange={(e) =>
                    setNewReminder({ ...newReminder, reminder_time: e.target.value })
                  }
                />
              </div>
            </div>

            <div>
              <label className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  checked={newReminder.recurring}
                  onChange={(e) =>
                    setNewReminder({ ...newReminder, recurring: e.target.checked })
                  }
                  className="w-4 h-4 text-primary-600 rounded"
                />
                <span className="text-sm font-medium text-gray-700">
                  Wiederkehrend
                </span>
              </label>

              {newReminder.recurring && (
                <select
                  className="input w-full mt-2"
                  value={newReminder.recurring_pattern}
                  onChange={(e) =>
                    setNewReminder({
                      ...newReminder,
                      recurring_pattern: e.target.value,
                    })
                  }
                >
                  <option value="">Muster wählen</option>
                  <option value="täglich">Täglich</option>
                  <option value="wöchentlich">Wöchentlich</option>
                  <option value="monatlich">Monatlich</option>
                </select>
              )}
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

      {/* Erinnerungsliste */}
      <div className="space-y-3">
        {reminders.length === 0 ? (
          <div className="card text-center py-12 text-gray-500">
            <Bell className="w-12 h-12 mx-auto mb-3 text-gray-400" />
            <p>Keine Erinnerungen vorhanden</p>
          </div>
        ) : (
          reminders.map((reminder) => {
            const typeInfo = reminderTypes.find(
              (t) => t.value === reminder.reminder_type
            ) || reminderTypes[0];

            return (
              <div
                key={reminder.id}
                className={`card ${
                  !reminder.active ? 'bg-gray-50 opacity-75' : ''
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-2xl">{typeInfo.emoji}</span>
                      <h3 className="font-semibold text-gray-900">
                        {reminder.title}
                      </h3>
                      {reminder.recurring && (
                        <span className="badge bg-purple-100 text-purple-800">
                          {reminder.recurring_pattern}
                        </span>
                      )}
                    </div>
                    {reminder.description && (
                      <p className="text-sm text-gray-600 mt-2">
                        {reminder.description}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleToggleActive(reminder.id)}
                      className={`p-2 rounded-lg transition-colors ${
                        reminder.active
                          ? 'text-primary-600 hover:bg-primary-50'
                          : 'text-gray-400 hover:bg-gray-100'
                      }`}
                      title={reminder.active ? 'Deaktivieren' : 'Aktivieren'}
                    >
                      {reminder.active ? (
                        <ToggleRight className="w-6 h-6" />
                      ) : (
                        <ToggleLeft className="w-6 h-6" />
                      )}
                    </button>
                    <button
                      onClick={() => handleDelete(reminder.id)}
                      className="text-gray-400 hover:text-red-600 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
