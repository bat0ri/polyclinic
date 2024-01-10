import React, { useContext, useEffect, useState } from 'react';
import './tailwindcss.css'
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';
import { Context } from '.';
import { observer } from 'mobx-react-lite';
import AppointmentForm from './components/AppointmentForm';
import { User } from './models/User';
import UserService from './services/UserService';
import { Routes, Route } from 'react-router-dom';
import DoctorProfile from './components/DoctorProfile';



function App() {
    
    const {store} = useContext(Context);
    const [users, setUsers] = useState<User[]>([]);

    useEffect(() => {
        if (localStorage.getItem('access')) {
            store.checkAuth()
        }
    }, [])

    if(store.isLoading) {
        return(
        <div>Загрузка</div>
        )
    }

    async function getDoctors() {
        try {
            const response = await UserService.fetchDoctors();
            setUsers(response.data);
        } catch(e) {
            console.log(e)
        }
    }

    if(!store.isAuth) {
        return (
            <div>
                <Routes>
                    <Route path='/login' element={<LoginForm/>}></Route>
                    <Route path='/singup' element={<RegistrationForm/>}></Route>
                </Routes>
            </div>
        )
    }
    
  return (
    <div className="App">
        <Routes>
            <Route path='/home' element={<AppointmentForm/>}/>
            <Route path="/profile" element={<DoctorProfile/>}/>
        </Routes>
    </div>
  );
}

export default observer(App);
