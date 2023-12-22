import React, { FC, useContext, useState } from 'react';
import { Context } from '..';
import { observer } from 'mobx-react-lite';

const AppointmentForm: FC = () => {

    const {store} = useContext(Context);

    return (
        <div>
            зашел? а теперь выйди
            <button onClick={()=> store.logout()}>Выйти</button>
        </div>
    );
};

export default observer(AppointmentForm);
