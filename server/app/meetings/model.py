from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from auth.models import User
from datetime import datetime

Base = declarative_base()


class Meeting(Base):
    __tablename__ = 'meeting'

    id = Column(Integer, primary_key=True, index=True)

    pacient_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    doctor_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)
    doctor_username = Column(String, nullable=True)

    create_date = Column(DateTime, default=datetime.now(), nullable= True)
    meet_date = Column(DateTime, nullable=False)