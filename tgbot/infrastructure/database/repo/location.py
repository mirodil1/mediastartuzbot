from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .base import BaseRepo
from  infrastructure.database.models.location import Region, District, Mahalla


class LocationRepo(BaseRepo):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_regions(self) -> List[Region]:
        stmt = select(Region).where(Region.is_active == True).order_by(Region.name)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_districts_by_region_name(self, region_name: str) -> List[District]:
        stmt = (
            select(District)
            .join(Region, District.region_id == Region.id)
            .where(Region.name == region_name, District.is_active == True)
            .order_by(District.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_mahallas_by_district_name(
            self, district_name: str,
            region_name: str
    ) -> List[Mahalla]:
        stmt = (
            select(Mahalla)
            .join(District, Mahalla.district_id == District.id)
            .join(Region, District.region_id == Region.id)
            .where(
                District.name == district_name,
                Region.name == region_name,
                Mahalla.is_active == True
            )
            .order_by(Mahalla.name)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_mahalla_by_name(self, mahalla_name: str, district_name: str) -> Mahalla:
        stmt = (
            select(Mahalla)
            .join(District, Mahalla.district_id == District.id)
            .where(
                Mahalla.name == mahalla_name,
                District.name == district_name,
                Mahalla.is_active == True,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()
