import React, { FC, useContext, useState } from 'react';
import { Context } from '..';
import { observer } from 'mobx-react-lite';
import { useNavigate } from 'react-router-dom';
import { User } from '../models/User';
import UserService from '../services/UserService';
import { Meet } from '../models/Meet';

const AppointmentForm: FC = () => {

    const {store} = useContext(Context);
    const navigate = useNavigate();

    const [doctors, setDoctors] = useState<User[]>([]);
    const [selectedDate, setSelectedDate] = useState<string>('');

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
            const response = UserService.makeMeet(formattedDate, doctorId, doctorName);
            console.log(response);
            getMeets();
        } catch(e) {
            console.log(e);
        }
    };

    

    return (
        <div>
            <button onClick={handleLogout} className='bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600'>Выйти</button>
            <div className='flex flex-row p-5 w-full h-full'>
            <div className="max-w-md mx-auto my-10 p-6 bg-white rounded-md shadow-md">
                <h2 className="text-2xl font-semibold mb-6 text-center">Список докторов</h2>
                <div className='flex flex-row'>
                    <button onClick={getDoctors} className="bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600 mb-4">
                        Загрузить докторов
                    </button>
                    <div className='flex flex-col p-3'>
                        <label htmlFor="appointmentDate" className="block mb-2 text-gray-800">Выберите дату записи:</label>
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
            <div className='flex flex-col items-center shadow-sm bg-slate-200/50 w-1/3'>
                <h1 className='text-2xl font-semibold mb-6 text-center'>Мои записи</h1>
            <div className='bg-slate-200/40 "max-w-md mx-auto my-10 p-6 bg-white rounded-md shadow-md '>
                {meets.map(meet => (
                    <div key={meet.id} className="mb-4 flex items-center justify-between bg-gray-100 rounded-md p-4">
                        <span>{meet.doctor_username}</span>
                    </div>
                ))}
            </div>
            </div>
            </div>
        </div>
    );
};

export default observer(AppointmentForm);
