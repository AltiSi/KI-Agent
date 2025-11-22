import axios from 'axios';
import type {
  Document,
  Task,
  Appointment,
  ShoppingList,
  ShoppingItem,
  Reminder,
  Dashboard
} from '../types';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Documents
export const documentsApi = {
  upload: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const { data } = await api.post<Document>('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  },
  getAll: async () => {
    const { data } = await api.get<Document[]>('/documents/');
    return data;
  },
  getById: async (id: number) => {
    const { data } = await api.get<Document>(`/documents/${id}`);
    return data;
  },
  delete: async (id: number) => {
    await api.delete(`/documents/${id}`);
  },
};

// Tasks
export const tasksApi = {
  create: async (task: Partial<Task>) => {
    const { data } = await api.post<Task>('/tasks/', task);
    return data;
  },
  getAll: async (completed?: boolean) => {
    const { data } = await api.get<Task[]>('/tasks/', {
      params: completed !== undefined ? { completed } : {},
    });
    return data;
  },
  getById: async (id: number) => {
    const { data } = await api.get<Task>(`/tasks/${id}`);
    return data;
  },
  update: async (id: number, updates: Partial<Task>) => {
    const { data } = await api.patch<Task>(`/tasks/${id}`, updates);
    return data;
  },
  delete: async (id: number) => {
    await api.delete(`/tasks/${id}`);
  },
  toggleComplete: async (id: number, completed: boolean) => {
    const { data } = await api.patch<Task>(`/tasks/${id}`, { completed });
    return data;
  },
};

// Appointments
export const appointmentsApi = {
  create: async (appointment: Partial<Appointment>) => {
    const { data } = await api.post<Appointment>('/appointments/', appointment);
    return data;
  },
  getAll: async (upcoming?: boolean) => {
    const { data } = await api.get<Appointment[]>('/appointments/', {
      params: upcoming !== undefined ? { upcoming } : {},
    });
    return data;
  },
  getToday: async () => {
    const { data } = await api.get<Appointment[]>('/appointments/today');
    return data;
  },
  delete: async (id: number) => {
    await api.delete(`/appointments/${id}`);
  },
};

// Shopping Lists
export const shoppingApi = {
  createList: async (name: string) => {
    const { data } = await api.post<ShoppingList>('/shopping/lists', { name });
    return data;
  },
  getLists: async () => {
    const { data } = await api.get<ShoppingList[]>('/shopping/lists');
    return data;
  },
  getList: async (id: number) => {
    const { data } = await api.get<ShoppingList>(`/shopping/lists/${id}`);
    return data;
  },
  deleteList: async (id: number) => {
    await api.delete(`/shopping/lists/${id}`);
  },
  addItem: async (listId: number, item: Partial<ShoppingItem>) => {
    const { data } = await api.post<ShoppingItem>(`/shopping/lists/${listId}/items`, item);
    return data;
  },
  toggleItem: async (itemId: number, checked: boolean) => {
    const { data } = await api.patch(`/shopping/items/${itemId}/check`, null, {
      params: { checked },
    });
    return data;
  },
  deleteItem: async (itemId: number) => {
    await api.delete(`/shopping/items/${itemId}`);
  },
};

// Reminders
export const remindersApi = {
  create: async (reminder: Partial<Reminder>) => {
    const { data } = await api.post<Reminder>('/reminders/', reminder);
    return data;
  },
  getAll: async (activeOnly = true) => {
    const { data } = await api.get<Reminder[]>('/reminders/', {
      params: { active_only: activeOnly },
    });
    return data;
  },
  toggle: async (id: number) => {
    const { data } = await api.patch<Reminder>(`/reminders/${id}/toggle`);
    return data;
  },
  delete: async (id: number) => {
    await api.delete(`/reminders/${id}`);
  },
};

// Dashboard
export const dashboardApi = {
  get: async () => {
    const { data } = await api.get<Dashboard>('/dashboard/');
    return data;
  },
};

export default api;
