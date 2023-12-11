from app.dal import BaseRepo
from app.meetings.model import Meeting
from sqlalchemy import select



class MeetRepo(BaseRepo[Meeting]):
    model = Meeting

    async def get_by_user_uuid(self, user_id):
        q = select(Meeting).where(Meeting.pacient_id==user_id)
        exe = await self.session.execute(q)
        return exe.scalars().all()