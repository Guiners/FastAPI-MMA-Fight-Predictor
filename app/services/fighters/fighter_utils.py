from sqlalchemy import asc, desc, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from app.constants import MODELS_LIST
from app.db.models import Base, BaseStats, ExtendedStats, FightsResults
from app.db.models.fighters import Fighters
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.schemas.extended_fighter import ExtendedFighterFilter
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.exceptions.custom_api_exceptions import NotFoundException
from app.tools.logger import logger

BASE_STMT = select(Fighters)
EXTENDED_STMT = (
    select(Fighters)
    .join(BaseStats, Fighters.fighter_id == BaseStats.fighter_id, isouter=True)
    .join(ExtendedStats, Fighters.fighter_id == ExtendedStats.fighter_id, isouter=True)
    .join(FightsResults, Fighters.fighter_id == FightsResults.fighter_id, isouter=True)
    .options(
        joinedload(Fighters.base_stats),
        joinedload(Fighters.extended_stats),
        joinedload(Fighters.fights_results),
    )
)


class FighterUtils:
    def __init__(self, db: AsyncSession, extended: bool = False):
        self.db = db
        self.is_extended = extended
        self.stmt = EXTENDED_STMT if extended else BASE_STMT
        self.fighter_schema = ExtendedFighterSchema if extended else FighterSchema

    @staticmethod
    def build_where_stmt(filters: FighterFilter | ExtendedFighterFilter):
        filters_dict = filters.model_dump(exclude_none=True)
        logger.debug(f"fighter filter: {filters_dict}")
        where_stmt = []
        for field, value in filters_dict.items():
            if hasattr(Fighters, field):
                column = getattr(Fighters, field)
                where_stmt.append(column == value)
            else:
                raise ValueError(f"Column '{field}' does not exist in Fighters model")
        return where_stmt

    @staticmethod
    def convert_stats_dicts_to_models(data):
        data["base_stats"] = BaseStats(**data["base_stats"])
        data["extended_stats"] = ExtendedStats(**data["extended_stats"])
        data["fights_results"] = FightsResults(**data["fights_results"])

    async def _get_records_with_where_stmt(
        self, where_stmt: list, validate: bool = True, lock_record: bool = False
    ):
        if lock_record:
            records = await self.db.execute(
                self.stmt.where(*where_stmt).with_for_update()
            )
        else:
            records = await self.db.execute(self.stmt.where(*where_stmt))

        fighters_list = records.scalars().all()

        if not fighters_list:
            raise NotFoundException

        convert = self.fighter_schema.model_validate if validate else (lambda x: x)

        if len(fighters_list) > 1:
            return [convert(fighter) for fighter in fighters_list]

        return convert(fighters_list[0])

    # todo typing
    async def _get_records_by_single_value(
        self,
        column: str,
        value: str | int,
        validate: bool = True,
        lock_record: bool = False,
    ):
        column_attr = getattr(Fighters, column)
        return await self._get_records_with_where_stmt(
            [column_attr == value], validate, lock_record
        )

    async def get_fighter_by_name_nickname_surname(
        self,
        name: str,
        nickname: str,
        surname: str,
        validate: bool = True,
        lock_record: bool = False,
    ):
        where_stmt = [
            Fighters.name == name,
            Fighters.nickname == nickname,
            Fighters.surname == surname,
        ]
        return await self._get_records_with_where_stmt(
            where_stmt, validate, lock_record
        )

    async def get_fighters_by_param_with_limit(
        self, param_name: str, limit: int, order: str = "desc"
    ):
        column, _ = self._get_column_if_param_in_tables(param_name)

        order_func = desc if order.lower() == "desc" else asc
        result = await self.db.execute(
            self.stmt.order_by(order_func(column)).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    def _get_column_if_param_in_tables(param_name: str):
        for model in MODELS_LIST:
            if hasattr(model, param_name):
                return getattr(model, param_name), model
        raise ValueError(f"Invalid column name: {param_name}")

    async def get_grouped_stat(
        self,
        param_name1: str,
        param_name2: str,
        math_func1,
        math_func2=func.count,
        label1="stat",
        label2="count",
    ):
        column1, model1 = self._get_column_if_param_in_tables(param_name1)
        column2, model2 = self._get_column_if_param_in_tables(param_name2)

        if model1 == model2:
            model2 = aliased(model2)

        stmt = (
            select(
                column1,
                math_func1(column2).label(label1),
                math_func2(model1.fighter_id).label(label2),
            )
            .join(model2, model1.fighter_id == model2.fighter_id)
            .group_by(column1)
            .having(math_func2(model1.fighter_id) > 1)
            .order_by(math_func1(column2).desc())
        )

        result = await self.db.execute(stmt)
        return result.mappings().all()

    async def clear_all_tables(self) -> None:
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            logger.info(f"Truncating: {table}")
            await self.db.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;')
            )
        await self.db.commit()
