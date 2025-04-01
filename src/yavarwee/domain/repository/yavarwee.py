from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.yavarwee.domain.model.yavarwee_result import YavarweeResult


class YavarweeResultRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, yavarwee_result: YavarweeResult):
        self.session.add(yavarwee_result)

    async def find_by_uuid(self, uuid: str) -> YavarweeResult:
        statement = select(YavarweeResult).where(YavarweeResult.uuid == uuid)
        result = await self.session.exec(statement)
        return result.first()