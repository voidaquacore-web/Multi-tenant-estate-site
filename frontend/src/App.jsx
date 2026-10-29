import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import ProtectedRoute from './ProtectedRoute.jsx'


export default function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path='/login' element={<Login />} />
      <Route path='/dashboard' element={<ProtectedRoute><Dashboard/></ProtectedRoute> } />
    </Routes>
    </BrowserRouter>
  )
}
