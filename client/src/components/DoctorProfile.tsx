import React, { FC, useContext, useState } from 'react';
import { Context } from '..';
import { observer } from 'mobx-react-lite';
import { useNavigate } from 'react-router-dom';
import TopBar from './TopBar';
import UserService
 from '../services/UserService';
import { Meet } from '../models/Meet';


const DoctorProfile: FC = () => {

    const {store} = useContext(Context);
    const navigate = useNavigate();
    const [meets, setMeets] = useState<Meet[]>([]);

    async function getMeets() {
        try {
            const response = await UserService.fetchMeetsDoctor();
            setMeets(response.data);
        } catch(e) {
            console.log(e);
        }
    }


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
        <div className='dark:bg-black h-screen'>
            <TopBar pageName='Личный кабинет Доктора' />
            <div className="dark:bg-slate-800 max-w-md mx-auto my-10 p-6 bg-white rounded-md shadow-md">
                <div className='flex flex-col p-4 mb-4'>
                    <h2 className="text-2xl font-semibold mb-6 dark:text-white text-center">Мои записи</h2>
                    <button onClick={getMeets} className="bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600">Загрузить записи</button>
                </div>
                <div className='flex flex-col my-10 rounded-md shadow-md h-96'>
                    <div className='overflow-y-auto'>
                        {meets.map(meet => (
                            <div key={meet.id} className="mb-4 flex items-left justify-between bg-gray-100 rounded-md p-6 flex-col">
                                <span>{meet.doctor_username}</span>
                                <div>
                                    <div>{meet.meet_date}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default observer(DoctorProfile);
