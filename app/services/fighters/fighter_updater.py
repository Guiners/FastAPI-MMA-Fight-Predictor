from typing import List, Union

from sqlalchemy import delete

from app.services.fighters.fighter_utils import (
    FighterUtils,
)
from app.db.models.fighters import Fighters
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.schemas.fighter import FighterFilter


class FighterUpdater(FighterUtils):

    async def add_fighter(
        self, fighter_data: Union[FighterFilter, ExtendedFighterFilter]
    ) -> bool:
        data = fighter_data.model_dump(exclude_none=True)
        if self.is_extended:
            self.convert_stats_dicts_to_models(data)
        self.db.add(Fighters(**data))
        await self.db.commit()
        return True

    async def add_multiple_fighters(
        self, fighters_data: List[Union[FighterFilter, ExtendedFighterFilter]]
    ):
        fighters_to_add = []
        for fighter_data in fighters_data:
            data = fighter_data.model_dump(exclude_none=True)
            if self.is_extended:
                self.convert_stats_dicts_to_models(data)
            fighters_to_add.append(Fighters(**data))

        if fighters_to_add:
            self.db.add_all(fighters_to_add)
            await self.db.commit()

        return [True for _ in fighters_to_add]

    async def _update_fighter(self, fighter, fighter_data: FighterFilter):
        data = fighter_data.model_dump(exclude_none=True)

        if self.is_extended:
            self.convert_stats_dicts_to_models(data)

        for key, value in data.items():
            setattr(fighter, key, value)

        await self.db.commit()
        await self.db.refresh(fighter)
        return True

    async def update_fighter_by_id(self, fighter_id: int, fighter_data: FighterFilter):
        fighter = await self._get_records_by_single_value(
            "fighter_id", fighter_id, False
        )
        return await self._update_fighter(fighter, fighter_data)

    async def update_fighter_by_name_nickname_surname(
        self, name: str, nickname: str, surname: str, fighter_data: FighterFilter
    ):
        fighter = await self.get_fighter_by_name_nickname_surname(
            name, nickname, surname, False
        )
        return await self._update_fighter(fighter, fighter_data)

    async def remove_record_by_fighter_id(self, fighter_id: int):
        fighter = await self.db.get(Fighters, fighter_id)
        if fighter:
            await self.db.delete(fighter)
            await self.db.commit()
            return True
        return None

    async def remove_multiple_records(self, list_of_ids: List[int]):
        if not list_of_ids:
            return []
        stmt = delete(Fighters).where(Fighters.fighter_id.in_(list_of_ids))
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result
