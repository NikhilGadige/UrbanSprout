import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';
import { ApiKeyProvider } from './context/ApiKeyContext';
import Navbar from './components/Navbar';
import ApiKeyGate from './components/ApiKeyGate';

import Home from './pages/Home';
import SpacePlanner from './pages/SpacePlanner';
import GrowCalendar from './pages/GrowCalendar';
import MyGarden from './pages/MyGarden';
import DiseaseDetector from './pages/DiseaseDetector';
import CompanionPlanting from './pages/CompanionPlanting';
import PlantGuides from './pages/PlantGuides';
import PlantDoctorChat from './pages/PlantDoctorChat';
import History from './pages/History';
import Login from './pages/Login';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <Router>
      <LanguageProvider>
        <AuthProvider>
          <ApiKeyProvider>
            <div className="min-h-screen bg-forest-950 flex flex-col text-forest-50 select-none antialiased">
              <Navbar />
              <main className="flex-grow">
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/planner" element={<ApiKeyGate><SpacePlanner /></ApiKeyGate>} />
                  <Route path="/calendar" element={<ApiKeyGate><GrowCalendar /></ApiKeyGate>} />
                  <Route path="/my-garden" element={<MyGarden />} />
                  <Route path="/detect" element={<ApiKeyGate><DiseaseDetector /></ApiKeyGate>} />
                  <Route path="/companion" element={<ApiKeyGate><CompanionPlanting /></ApiKeyGate>} />
                  <Route path="/guides" element={<ApiKeyGate><PlantGuides /></ApiKeyGate>} />
                  <Route path="/chat" element={<ApiKeyGate><PlantDoctorChat /></ApiKeyGate>} />
                  <Route path="/history" element={<History />} />
                  <Route path="/login" element={<Login />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="*" element={<NotFound />} />
                </Routes>
              </main>
            </div>
          </ApiKeyProvider>
        </AuthProvider>
      </LanguageProvider>
    </Router>
  );
}
