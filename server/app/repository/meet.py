from app.repository.dal import BaseRepo
from app.models.meet import Meeting
from sqlalchemy import select



class MeetRepo(BaseRepo[Meeting]):
    model = Meeting

    async def get_by_user_uuid(self, user_id):
        q = select(Meeting).where(Meeting.pacient_id==user_id)
        exe = await self.session.execute(q)
        return exe.scalars().all()


    async def get_by_user_uuid_for_doctor(self, user_id):
        q = select(Meeting).where(Meeting.doctor_id==user_id)
        exe = await self.session.execute(q)
        return exe.scalars().all()


    async def get_by_doctor_and_time(self, doctor_id, meet_date):
        q = select(Meeting).where(
                Meeting.doctor_id == doctor_id,
                Meeting.meet_date == meet_date
            )
        exe = await self.session.execute(q)
        return exe.scalars().all()
