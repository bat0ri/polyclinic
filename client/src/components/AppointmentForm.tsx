import React, { FC, useContext, useEffect, useState } from 'react';
import { Context } from '..';
import { observer } from 'mobx-react-lite';
import { useNavigate } from 'react-router-dom';
import { User } from '../models/User';
import UserService from '../services/UserService';
import { Meet } from '../models/Meet';
import TopBar from './TopBar';

const AppointmentForm: FC = () => {

    const {store} = useContext(Context);
    const navigate = useNavigate();

    const [doctors, setDoctors] = useState<User[]>([]);
    const [selectedDate, setSelectedDate] = useState<string>('2002-10-19');

    const [meets, setMeets] = useState<Meet[]>([]);



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


    async function getDoctors() {
        try {
            const response = await UserService.fetchDoctors();
            setDoctors(response.data);
        } catch(e) {
            console.log(e)
        }
    }

    async function getMeets() {
        try {
            const response = await UserService.fetchMeets();
            setMeets(response.data);
        } catch(e) {
            console.log(e);
        }
    }


    const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setSelectedDate(e.target.value);
    };

    const handleAppointment = async (doctorId: string, doctorName: string | null) => {
        const selectedDateTime = new Date(selectedDate);
        const formattedDate = selectedDateTime.toISOString();
        console.log(`Вы записались к доктору с ID ${doctorId} на ${formattedDate}`);
        try {
            UserService.makeMeet(formattedDate, doctorId, doctorName);
        } catch(e) {
            console.log(e);
        }
    };

    return (
        <div className='bg-white dark:bg-black'>
            <TopBar pageName='Сервис записи к врачу'/>
            <div className='flex flex-row p-5 w-full h-full'>
                <div className="max-w-md mx-auto my-10 p-6 dark:bg-slate-800 rounded-md shadow-md">
                    <h2 className="text-2xl font-semibold mb-6 text-center dark:text-white">Список докторов</h2>
                    <div className='flex flex-row'>
                        <button onClick={getDoctors} className="bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600 mb-4">
                            Загрузить докторов
                        </button>
                        <div className='flex flex-col p-3'>
                            <label htmlFor="appointmentDate" className="block mb-2 text-gray-800 dark:text-white">Выберите дату записи:</label>
                            <input
                                type="date"
                                id="appointmentDate"
                                value={selectedDate}
                                onChange={handleDateChange}
                                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-500"
                            />
                        </div>
                    </div>
                    <div>
                        {doctors.map(doctor => (
                            <div key={doctor.id} className="mb-4 flex items-center justify-between bg-gray-100 rounded-md p-4">
                                <span>{doctor.username}</span>
                                <button
                                    onClick={() => handleAppointment(doctor.id, doctor.username)}
                                    className="bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600"
                                >
                                    Записаться
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
                <div className='w-1/3 mx-auto my-10 p-6 h-screen bg-white dark:bg-slate-900 rounded-md shadow-md flex flex-col'>
                    <h1 className='text-2xl font-semibold mb-6 text-center w-auto dark:text-white'>Мои записи</h1>
                    <button onClick={getMeets} className="w-1/3 bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600 mb-4">
                        Загрузить записи
                    </button>
                    <div className='my-10 rounded-md shadow-md overflow-y-auto'>
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

export default observer(AppointmentForm);
