from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from auth.models import User
from app.diagnoses.model import Diagnosis


Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, index=True)

    # доктор который запись делает
    doctor_id = Column(UUID(as_uuid=True), ForeignKey(User.id), nullable=False)

    description = Column(String, nullable=True)
    diagnose = Column(Integer, ForeignKey(Diagnosis.id), nullable=True)