import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";

import ClinicianDashboard from "./pages/clinician/Dashboard";
import PatientDashboard from "./pages/patient/Dashboard";

import Layout from "./components/common/Layout";

import Tasks from "./pages/patient/Tasks";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />

          <Route path="/clinician" element={<ClinicianDashboard />} />
          <Route path="/patient" element={<PatientDashboard />} />
          <Route path="/patient/tasks" element={<Tasks />} />

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;