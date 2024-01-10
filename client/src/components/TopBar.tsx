import React, { FC, useContext, useEffect } from 'react';
import { Context } from '..';
import { observer } from 'mobx-react-lite';
import { useNavigate } from 'react-router-dom';
import ThemeSwitch from '../themes'
import { XCircleIcon } from '@heroicons/react/20/solid';

interface TopBarProps {
    pageName: string;
}

const TopBar: FC<TopBarProps> = ({pageName}) => {
    const { store } = useContext(Context);
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
    <div className='flex items-center justify-between py-4 px-6'>
        <h1 className='text-2xl font-semibold dark:text-white'>{pageName}</h1>
        
        <div className='flex items-center'>
            <div className='flex items-center space-x-4'>
            <ThemeSwitch />
            <button onClick={handleLogout} className='flex flex-row bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600'>
                Выйти
                <XCircleIcon className="h-6 w-6 text-white ml-2" />
            </button>
            </div>
        </div>
    </div>
    );
};

export default observer(TopBar);
