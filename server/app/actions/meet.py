from fastapi import APIRouter, Depends, HTTPException
from app.repository.meet import MeetRepo 
from auth.security import JWTBearer, get_current_user
from app.schemas.meet import CreateMeeting, DropMeeting
from auth.models import User
from app.models.meet import Meeting 

import smtplib
from email.message import EmailMessage

from celery import Celery
from config import SMTP_USER, SMTP_PASS



SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_template_meet(username: str):
    ''' Функция создает шаблон email после успешной записи на прием '''
    email = EmailMessage()
    email['Subject'] = 'Вы успешно записались на прием'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        f"""
        <div style="font-family: 'Arial', sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #F3F4F6; padding: 20px;">
                <h1 style="color: #EF4444; font-size: 24px; font-weight: bold;">
                    Здравствуйте, {username}!
                </h1>
                <p style="color: #374151; font-size: 16px; margin-top: 20px;">
                    Спасибо, что записались на прием к врачу. Мы ждем вас!
                </p>
            </div>
        </div>
        """,
        subtype='html'
    )
    return email


@celery.task
def send_email_report_meet(username: str):
    ''' Celery-task: отправка email после создание записи на прием '''
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)


async def create_meeting(
    meeting_data: CreateMeeting,
    repo: MeetRepo = Depends(MeetRepo),
    current_user: User = Depends(get_current_user)
):

    existing_meetings = await repo.get_by_doctor_and_time(
        doctor_id=meeting_data.doctor_id,
        meet_date=meeting_data.meet_date
    )

    if existing_meetings:
        return {"detail": "У этого врача уже есть запись на это время."}

    new_meeting = Meeting(
        pacient_id=current_user.id,
        meet_date=meeting_data.meet_date,
        doctor_id=meeting_data.doctor_id,
        doctor_username=meeting_data.doctor_username
    )

    created_meeting = await repo.insert(new_meeting)
    await repo.close()

    send_email_report_meet.delay(current_user.username)

    return created_meeting