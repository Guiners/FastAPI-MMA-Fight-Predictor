import typing

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.fighters import Fighters
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.schemas.fighter import FighterFilter
from app.services.fighters.fighter_utils import FighterUtils


class FighterUpdater(FighterUtils):
    """
    Service class responsible for creating, updating, and deleting fighter records.
    Inherits from FighterUtils for shared database query logic.
    """

    async def add_fighter(
        self, fighter_data: FighterFilter | ExtendedFighterFilter
    ) -> bool:
        """
        Add a single fighter to the database.

        Args:
            fighter_data (FighterFilter | ExtendedFighterFilter): Fighter data to insert.

        Returns:
            bool: True if the fighter was successfully added.
        """
        data = fighter_data.model_dump(exclude_none=True)
        if self.is_extended:
            self.convert_stats_dicts_to_models(data)
        self.db.add(Fighters(**data))
        await self.db.commit()
        return True

    async def add_multiple_fighters(
        self, fighters_data: typing.List[FighterFilter | ExtendedFighterFilter]
    ) -> typing.List[bool]:
        """
        Add multiple fighters to the database in a single transaction.

        Args:
            fighters_data (list[FighterFilter | ExtendedFighterFilter]): List of fighter data to insert.

        Returns:
            list[bool]: List of True values for each successfully added fighter.
        """
        fighters_to_add: typing.List[Fighters] = []
        for fighter_data in fighters_data:
            data = fighter_data.model_dump(exclude_none=True)
            if self.is_extended:
                self.convert_stats_dicts_to_models(data)
            fighters_to_add.append(Fighters(**data))

        if fighters_to_add:
            self.db.add_all(fighters_to_add)
            await self.db.commit()

        return [True for _ in fighters_to_add]

    async def _update_fighter(
        self, fighter: Fighters, fighter_data: FighterFilter | ExtendedFighterFilter
    ) -> None:
        """
        Update an existing fighter record with new data.

        Args:
            fighter (Fighters): The fighter instance to update.
            fighter_data (FighterFilter | ExtendedFighterFilter): Data for updating the fighter.

        Returns:
            None
        """
        data = fighter_data.model_dump(exclude_none=True)
        if self.is_extended:
            self.convert_stats_dicts_to_models(data)

        for key, value in data.items():
            setattr(fighter, key, value)

        await self.db.commit()
        await self.db.refresh(fighter)

    async def update_fighter_by_id(
        self, fighter_id: int, fighter_data: FighterFilter | ExtendedFighterFilter
    ) -> None:
        """
        Update a fighter by their unique ID.

        Args:
            fighter_id (int): Fighter ID.
            fighter_data (FighterFilter | ExtendedFighterFilter): Updated fighter data.

        Returns:
            None
        """
        fighter = await self._get_records_by_single_value(
            "fighter_id", fighter_id, False, True
        )
        return await self._update_fighter(fighter, fighter_data)

    async def update_fighter_by_name_nickname_surname(
        self,
        name: str,
        nickname: str,
        surname: str,
        fighter_data: FighterFilter | ExtendedFighterFilter,
    ) -> None:
        """
        Update a fighter using a combination of name, nickname, and surname.

        Args:
            name (str): Fighter's first name.
            nickname (str): Fighter's nickname.
            surname (str): Fighter's surname.
            fighter_data (FighterFilter | ExtendedFighterFilter): Updated fighter data.

        Returns:
            None
        """
        fighter = await self.get_fighter_by_name_nickname_surname(
            name, nickname, surname, False, True
        )
        return await self._update_fighter(fighter, fighter_data)

    async def remove_record_by_fighter_id(self, fighter_id: int) -> bool:
        """
        Remove a fighter record from the database by its ID.

        Args:
            fighter_id (int): The fighter's ID.

        Returns:
            bool: True if the record was successfully deleted.
        """
        fighter = await self.db.get(Fighters, fighter_id)
        await self.db.delete(fighter)
        await self.db.commit()
        return True

    async def remove_multiple_records(
        self, list_of_ids: typing.List[int]
    ) -> typing.Any:
        """
        Remove multiple fighters from the database by their IDs.

        Args:
            list_of_ids (list[int]): List of fighter IDs to delete.

        Returns:
            Any: The result of the delete operation (SQLAlchemy execution result).
        """
        if not list_of_ids:
            return []
        stmt = delete(Fighters).where(Fighters.fighter_id.in_(list_of_ids))
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result
