import { useEffect, useState } from 'react';
import { tasksApi } from '../services/api';
import type { Task } from '../types';
import { format } from 'date-fns';
import { de } from 'date-fns/locale';
import { CheckSquare, Plus, Trash2 } from 'lucide-react';

export default function Tasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showCompleted, setShowCompleted] = useState(false);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'mittel' as Task['priority'],
    due_date: '',
  });

  useEffect(() => {
    loadTasks();
  }, [showCompleted]);

  const loadTasks = async () => {
    try {
      const data = await tasksApi.getAll(showCompleted ? undefined : false);
      setTasks(data);
    } catch (error) {
      console.error('Fehler beim Laden der Aufgaben:', error);
    }
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTask.title.trim()) return;

    try {
      await tasksApi.create({
        ...newTask,
        due_date: newTask.due_date ? new Date(newTask.due_date).toISOString() : null,
      });
      setNewTask({ title: '', description: '', priority: 'mittel', due_date: '' });
      setShowAddForm(false);
      loadTasks();
    } catch (error) {
      console.error('Fehler beim Erstellen:', error);
    }
  };

  const handleToggleComplete = async (task: Task) => {
    try {
      await tasksApi.toggleComplete(task.id, !task.completed);
      loadTasks();
    } catch (error) {
      console.error('Fehler beim Aktualisieren:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Aufgabe wirklich löschen?')) return;

    try {
      await tasksApi.delete(id);
      setTasks(tasks.filter((t) => t.id !== id));
    } catch (error) {
      console.error('Fehler beim Löschen:', error);
    }
  };

  const pendingTasks = tasks.filter((t) => !t.completed);
  const completedTasks = tasks.filter((t) => t.completed);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Aufgaben</h1>
        <button
          onClick={() => setShowAddForm(!showAddForm)}
          className="btn btn-primary"
        >
          <Plus className="w-4 h-4 mr-2 inline" />
          Neue Aufgabe
        </button>
      </div>

      {/* Neue Aufgabe Formular */}
      {showAddForm && (
        <div className="card">
          <h2 className="text-lg font-semibold mb-4">Neue Aufgabe erstellen</h2>
          <form onSubmit={handleAddTask} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Titel *
              </label>
              <input
                type="text"
                className="input w-full"
                value={newTask.title}
                onChange={(e) =>
                  setNewTask({ ...newTask, title: e.target.value })
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
                value={newTask.description}
                onChange={(e) =>
                  setNewTask({ ...newTask, description: e.target.value })
                }
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Priorität
                </label>
                <select
                  className="input w-full"
                  value={newTask.priority}
                  onChange={(e) =>
                    setNewTask({
                      ...newTask,
                      priority: e.target.value as Task['priority'],
                    })
                  }
                >
                  <option value="niedrig">Niedrig</option>
                  <option value="mittel">Mittel</option>
                  <option value="hoch">Hoch</option>
                  <option value="dringend">Dringend</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Fällig am
                </label>
                <input
                  type="date"
                  className="input w-full"
                  value={newTask.due_date}
                  onChange={(e) =>
                    setNewTask({ ...newTask, due_date: e.target.value })
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

      {/* Filter */}
      <div className="flex items-center space-x-4">
        <button
          onClick={() => setShowCompleted(false)}
          className={`px-4 py-2 rounded-lg font-medium ${
            !showCompleted
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          Offen ({pendingTasks.length})
        </button>
        <button
          onClick={() => setShowCompleted(true)}
          className={`px-4 py-2 rounded-lg font-medium ${
            showCompleted
              ? 'bg-primary-600 text-white'
              : 'bg-gray-200 text-gray-700'
          }`}
        >
          Alle ({tasks.length})
        </button>
      </div>

      {/* Aufgabenliste */}
      <div className="space-y-3">
        {tasks.length === 0 ? (
          <div className="card text-center py-12 text-gray-500">
            <CheckSquare className="w-12 h-12 mx-auto mb-3 text-gray-400" />
            <p>Keine Aufgaben vorhanden</p>
          </div>
        ) : (
          tasks.map((task) => (
            <div
              key={task.id}
              className={`card ${
                task.completed ? 'bg-gray-50 opacity-75' : ''
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => handleToggleComplete(task)}
                    className="mt-1 w-5 h-5 text-primary-600 rounded focus:ring-primary-500"
                  />
                  <div className="flex-1">
                    <div className="flex items-center space-x-2">
                      <h3
                        className={`font-semibold ${
                          task.completed
                            ? 'line-through text-gray-500'
                            : 'text-gray-900'
                        }`}
                      >
                        {task.title}
                      </h3>
                      <span className={`badge badge-${task.priority}`}>
                        {task.priority}
                      </span>
                    </div>
                    {task.description && (
                      <p className="text-sm text-gray-600 mt-1">
                        {task.description}
                      </p>
                    )}
                    {task.due_date && (
                      <p className="text-sm text-gray-500 mt-1">
                        📅{' '}
                        {format(new Date(task.due_date), 'dd. MMM yyyy', {
                          locale: de,
                        })}
                      </p>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(task.id)}
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
