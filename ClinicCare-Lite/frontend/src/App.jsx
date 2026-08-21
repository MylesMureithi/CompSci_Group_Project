import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";

import Layout from "./components/common/Layout";

// Patient-Side imports
import PatientDashboard from "./pages/patient/Dashboard";
import Tasks from "./pages/patient/Tasks";
import PatientForms from "./pages/patient/Forms";
import Outcomes from "./pages/patient/Outcomes";
import PatientMessages from "./pages/patient/Messages";

// Clinician-side imports
import ClinicianDashboard from "./pages/clinician/Dashboard";
import ClinicianForms from "./pages/clinician/Forms";
import ClinicianMessages from "./pages/clinician/Messages";
import ClinicianReviews from "./pages/clinician/Reviews";
import ClinicianSubmissions from "./pages/clinician/Submissions";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />

          // Patient routes
          <Route path="/patient" element={<PatientDashboard />} />
          <Route path="/patient/tasks" element={<Tasks />} />
          <Route path="/patient/forms" element={<PatientForms />} />
          <Route path="/patient/outcomes" element={<Outcomes />} />
          <Route path="/patient/messages" element={<PatientMessages />} />

          // Clinician routes
          <Route path="/clinician" element={<ClinicianDashboard />} />
          <Route path="/clinician/forms" element={<ClinicianForms />} />
          <Route path="/clinician/messages" element={<ClinicianMessages />} />
          <Route path="/clinician/reviews" element={<ClinicianReviews />} />
          <Route path="/clinician/reviews/:id" element={<ClinicianReviews />} />
          <Route path="/clinician/submissions" element={<ClinicianSubmissions />} />

          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;