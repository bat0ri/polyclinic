import React, { FC, useContext, useState } from 'react';
import { Context } from '..';
import { observer } from 'mobx-react-lite';
import { useNavigate, Link } from 'react-router-dom';


const LoginForm: FC = () => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');

    const navigate = useNavigate();

    const {store} = useContext(Context);

    const handleLogin = async () => {
        try {
            await store.login(username, password);
            if (store.isAuth && store.user.roles && store.user.roles.includes("ROLE_DOCTOR")) {
                navigate('/profile');
            } else {
                navigate('/home');
            }
        } catch (e: any) {
            if ('response' in e && e.response?.data?.message) {
                console.log(e.response.data.message);
            } else {
                console.log('An error occurred:', e);
            }
        }
    };

    return (
        <div>
            <div>
                <label htmlFor="username">Username:</label>
                <input
                    type="text"
                    id="username"
                    placeholder='username'
                    value={username}
                    onChange={e => setUsername(e.target.value)}
                />
            </div>
            <div>
                <label htmlFor="password">Password:</label>
                <input
                    type="password"
                    id="password"
                    value={password}
                    placeholder='pass'
                    onChange={e => setPassword(e.target.value)}
                />
            </div>
            <button onClick={handleLogin}>Login</button>
            <Link to="/singup">Зарегистрироваться</Link>
        </div>
    );
};

export default observer(LoginForm);
