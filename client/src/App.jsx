import { BrowserRouter as Routeur, Routes, Route } from 'react-router-dom';

import Dashboard from './containers/Dashboard';
import Equipment from './containers/Equipment';
import Calendar from './containers/Calendar';
import User from './containers/User';
import Error from './containers/Error';
import Register from './containers/Register';
import Login from './containers/Login';
import ProtectedRoute from './utils/ProtectedRoute';

function App() {
  return (
    <Routeur>
      <Routes>
        <Route path='/login' element={<Login />} />
        <Route path='*' element={<Error />} />
        <Route element={<ProtectedRoute />}>
            <Route path='/register' element={<Register />} />
            <Route path='/' element={<Dashboard />} />
            <Route path='/dashboard' element={<Dashboard />} />
            <Route path='/equipements' element={<Equipment />} />
            <Route path='/calendrier' element={<Calendar />} />
            <Route path='/utilisateurs' element={<User />} />
        </Route>
      </Routes>
    </Routeur>
  )
}

export default App