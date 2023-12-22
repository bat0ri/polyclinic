import React, { useContext, useEffect, useState } from 'react';
import logo from './logo.svg';
import LoginForm from './components/LoginForm';
import RegistrationForm from './components/RegistrationForm';
import { Context } from '.';
import { observer } from 'mobx-react-lite';
import AppointmentForm from './components/AppointmentForm';
import { User } from './models/User';
import UserService from './services/UserService';

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

    if(!store.isAuth) {
        return (
            <div>
                <LoginForm/>
            </div>
        )
    }

    async function getUsers() {
        try {
            const response = await UserService.fetchUsers();
            setUsers(response.data);
        } catch(e) {
            console.log(e)
        }
    }
    
  return (
    <div className="App">

    </div>
  );
}

export default observer(App);

{/*<AppointmentForm/>
        <button onClick={ () => store.logout()}>Выйти</button>

        <div>
            <button onClick={getUsers}>список пользаков</button>
        </div>
        { users.map(user =>
            <div key={user.email}>{user.email}</div>
            )}*/}