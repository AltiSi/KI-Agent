import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import Documents from './pages/Documents';
import Tasks from './pages/Tasks';
import Appointments from './pages/Appointments';
import Shopping from './pages/Shopping';
import Reminders from './pages/Reminders';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/documents" element={<Documents />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/appointments" element={<Appointments />} />
          <Route path="/shopping" element={<Shopping />} />
          <Route path="/reminders" element={<Reminders />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
