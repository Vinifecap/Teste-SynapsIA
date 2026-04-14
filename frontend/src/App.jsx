import { BrowserRouter, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import UploadPage from './pages/UploadPage'
import ReportPage from './pages/ReportPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/"             element={<HomePage />} />
        <Route path="/upload"       element={<UploadPage />} />
        <Route path="/report/:id"   element={<ReportPage />} />
      </Routes>
    </BrowserRouter>
  )
}
