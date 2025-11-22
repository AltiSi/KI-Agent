export interface Document {
  id: number;
  title: string;
  filename: string;
  category: string | null;
  summary: string | null;
  important_info: string | null;
  next_steps: string | null;
  created_at: string;
}

export interface Task {
  id: number;
  title: string;
  description: string | null;
  priority: 'niedrig' | 'mittel' | 'hoch' | 'dringend';
  due_date: string | null;
  completed: boolean;
  completed_at: string | null;
  document_id: number | null;
  created_at: string;
}

export interface Appointment {
  id: number;
  title: string;
  description: string | null;
  appointment_date: string;
  location: string | null;
  reminder_sent: boolean;
  document_id: number | null;
  created_at: string;
}

export interface ShoppingItem {
  id: number;
  item: string;
  quantity: string | null;
  checked: boolean;
  created_at: string;
}

export interface ShoppingList {
  id: number;
  name: string;
  created_at: string;
  items: ShoppingItem[];
}

export interface Reminder {
  id: number;
  title: string;
  description: string | null;
  reminder_type: string;
  reminder_time: string | null;
  recurring: boolean;
  recurring_pattern: string | null;
  active: boolean;
  created_at: string;
}

export interface Dashboard {
  upcoming_tasks: Task[];
  upcoming_appointments: Appointment[];
  daily_summary: string;
  pending_tasks_count: number;
  today_appointments_count: number;
}
