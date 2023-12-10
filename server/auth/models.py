import email
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import declarative_base
import datetime
from enum import Enum


Base = declarative_base()

class Roles(str, Enum):
    ROLE_PACIENT = "ROLE_PACIENT"
    ROLE_DOCKTOR = "ROLE_DOCKTOR"
    ROLE_SUPERADMIN = "ROLE_SUPERADMIN"


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String)
    hash_password = Column(String, nullable=False)
    email = Column(String, nullable= False)
    is_active = Column(Boolean, default=True)

    phone_number = Column(String, nullable= True)
    first_name = Column(String, nullable= True)
    last_name = Column(String, nullable= True)
    create_date = Column(DateTime, default=datetime.datetime.now(), nullable= True)
    update_date = Column(DateTime, nullable= True)

    roles = Column(ARRAY(String), nullable=True)


    @property
    def is_superadmin(self) -> bool:
        return Roles.ROLE_SUPERADMIN in self.roles

    @property
    def is_doctor(self) -> bool:
        return Roles.ROLE_DOCKTOR in self.roles