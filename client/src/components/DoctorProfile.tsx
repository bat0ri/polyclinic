import React, { FC, useContext, useState } from 'react';
import { Context } from '..';
import { observer } from 'mobx-react-lite';
import { useNavigate } from 'react-router-dom';


const DoctorProfile: FC = () => {

    const {store} = useContext(Context);
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            store.logout();
            navigate('/login');
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
            Приветствую доктор
            <button onClick={handleLogout}>Выйти</button>
        </div>
    );
};

export default observer(DoctorProfile);
