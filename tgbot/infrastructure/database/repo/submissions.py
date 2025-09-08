from typing import Optional
from datetime import date, datetime

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from infrastructure.database.repo.base import BaseRepo
from infrastructure.database.models import Submission, TgUser


class SubmissionRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_submission(
        self,
        tg_user_id: int,
        full_name: str,
        date_of_birth: date,
        area_id: int,
        photo: str,
        education: str,
        phone_number: str,
        profession: Optional[str] = None,
        certificate: Optional[str] = None,
        creative_work: Optional[str] = None,
        is_accepted: bool = False,
    ) -> Submission:
        insert_stmt = (
            insert(Submission)
            .values(
                tg_user_id=tg_user_id,
                full_name=full_name,
                date_of_birth=date_of_birth,
                area_id=area_id,
                photo=photo,
                education=education,
                profession=profession,
                certificate=certificate,
                creative_work=creative_work,
                phone_number=phone_number,
                is_accepted=is_accepted,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            .returning(Submission)
        )
        result = await self.session.execute(insert_stmt)
        await self.session.commit()
        return result.scalar_one()

    async def get_submission_by_tguser_id(self, tg_user_id: str) -> Optional[Submission]:
        stmt = (
            select(Submission)
            .join(Submission.tguser)
            .where(TgUser.user_id == str(tg_user_id))
            .options(joinedload(Submission.tguser))
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
