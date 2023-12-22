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

    const [doctors] = useState([
        { id: 1, name: 'Доктор Иванов' },
        { id: 2, name: 'Доктор Петров' },
        { id: 3, name: 'Доктор Сидоров' },
    ]);

    const handleAppointment = (doctorId: number) => {
        console.log(`Вы записались к доктору с ID ${doctorId}`);
    };

    return (
        <div>
            <button onClick={handleLogout} className='bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600'>Выйти</button>
            <div className="max-w-md mx-auto my-10 p-6 bg-white rounded-md shadow-md">
            <h2 className="text-2xl font-semibold mb-6 text-center">Список докторов</h2>
            <div>
                {doctors.map(doctor => (
                    <div key={doctor.id} className="mb-4 flex items-center justify-between bg-gray-100 rounded-md p-4">
                        <span>{doctor.name}</span>
                        <button
                            onClick={() => handleAppointment(doctor.id)}
                            className="bg-blue-500 text-white font-semibold py-2 px-4 rounded-md focus:outline-none hover:bg-blue-600"
                        >
                            Записаться
                        </button>
                    </div>
                ))}
            </div>
        </div>
        </div>
    );
};

export default observer(DoctorProfile);
