import React, { FC, useContext, useState } from 'react';
import { Context } from '..';

const RegistrationForm: FC = () => {
    const [username, setUsername] = useState<string>('');
    const [email, setEmail] = useState<string>('')
    const [password, setPassword] = useState<string>('');

    const {store} = useContext(Context)

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
                <label htmlFor="email">Email:</label>
                <input
                    type="text"
                    id="email"
                    placeholder='email'
                    value={email}
                    onChange={e => setEmail(e.target.value)}
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
            <button onClick={() => store.registration(username, email, password)}>Register</button>
        </div>
    );
};

export default RegistrationForm;
