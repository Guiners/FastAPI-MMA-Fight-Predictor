from typing import List, Union

from fastapi import Depends, FastAPI, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.database_menagers.database_manager_getter import \
    DatabaseManagerGetter
from app.db.database_menagers.database_manager_updater import \
    DatabaseManagerUpdater
from app.db.models.fighters import Fighters
from app.middleware.middlewares import log_requests
from app.schemas import ExtendedFighter as ExtendedFighterSchema
from app.schemas.extended_fighter import ExtendedFighter, ExtendedFighterFilter
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.tools.tools import handle_empty_response

app = FastAPI()

app.middleware("http")(log_requests)


@app.get("/")
async def root():
    return {"message": "Hello World"}


#######################################GET METHODS#############################################


@app.get("/base_fighter/get_all")
@handle_empty_response
async def get_all_base_fighters_list(
    db: AsyncSession = Depends(get_db),
) -> List[FighterSchema]:
    return await DatabaseManagerGetter(db, False).get_all_fighters_records()


@app.get("/extended_fighter/get_all")
@handle_empty_response
async def get_all_extended_fighters_list(
    db: AsyncSession = Depends(get_db),
) -> List[ExtendedFighterSchema]:
    return await DatabaseManagerGetter(db, True).get_all_fighters_records()


@app.get("/base_fighter/id/{fighter_id}")
@handle_empty_response
async def get_base_fighter_by_id(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> FighterSchema:
    return await DatabaseManagerGetter(db, False).get_fighter_by_id(fighter_id)


@app.get("/extended_fighter/id/{fighter_id}")
@handle_empty_response
async def get_extended_fighter_by_id(
    fighter_id: int, db: AsyncSession = Depends(get_db)
) -> ExtendedFighterSchema:
    return await DatabaseManagerGetter(db, True).get_fighter_by_id(fighter_id)


@app.get("/base_fighter/country/{country}")
@handle_empty_response
async def get_fighters_data_by_country(
    country: str, db: AsyncSession = Depends(get_db)
) -> Union[List[FighterSchema], FighterSchema]:
    return await DatabaseManagerGetter(db, False).get_fighters_by_country(country)


@app.get("/extended_fighter/country/{country}")
@handle_empty_response
async def get_extended_fighters_by_country(
    country: str, db: AsyncSession = Depends(get_db)
) -> Union[List[ExtendedFighterSchema], ExtendedFighterSchema]:
    return await DatabaseManagerGetter(db, True).get_fighters_by_country(country)


@app.get("/base_fighter/{name}/{nickname}/{surname}")
@handle_empty_response
async def get_base_fighter_by_name_nickname_surname(
    name: str, nickname: str, surname: str, db: AsyncSession = Depends(get_db)
) -> FighterSchema:
    return await DatabaseManagerGetter(db, False).get_fighter_by_name_nickname_surname(
        name, nickname, surname
    )


@app.get("/extended_fighter/{name}/{nickname}/{surname}")
@handle_empty_response
async def get_extended_fighter_by_name_nickname_surname(
    name: str, nickname: str, surname: str, db: AsyncSession = Depends(get_db)
) -> ExtendedFighterSchema:
    return await DatabaseManagerGetter(db, True).get_fighter_by_name_nickname_surname(
        name, nickname, surname
    )


@app.get("/extended_fighter_stats/search")
@handle_empty_response
async def search_fighters(
    fighter_filters: FighterFilter = Depends(), db: AsyncSession = Depends(get_db)
) -> Union[List[ExtendedFighterSchema], ExtendedFighterSchema]:
    return await DatabaseManagerGetter(db, True).search_extended_fighter(
        fighter_filters
    )


# #######################################POST METHODS#############################################


@app.post("/base_fighter/create")
async def create_base_fighter(
    fighter_data: FighterFilter = Depends(), db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, False).add_fighter(fighter_data)


@app.post("/extended_fighter/create")
async def create_extended_fighter(
    fighter_data: ExtendedFighterFilter, db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, True).add_fighter(fighter_data)


@app.post("/base_fighter/create_multiple")
async def create_multiple_base_fighter(
    fighters_data: List[FighterFilter], db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, False).add_multiple_fighters(fighters_data)


@app.post("/extended_fighter/create_multiple")
async def create_multiple_extended_fighter(
    fighters_data: List[ExtendedFighterFilter], db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, True).add_multiple_fighters(fighters_data)


#
#
# #######################################PUT METHODS#############################################
#
#
@app.put("/base_fighter/update/id/{fighter_id}")
@handle_empty_response
async def update_base_fighter_by_id(
    fighter_id: int,
    fighter_data: FighterFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await DatabaseManagerUpdater(db, False).update_fighter_by_id(
        fighter_id, fighter_data
    )


@app.put("/extended_fighter/update/id/{fighter_id}")
@handle_empty_response
async def update_extended_fighter_by_id(
    fighter_id: int,
    fighter_data: ExtendedFighterFilter,
    db: AsyncSession = Depends(get_db),
):
    return await DatabaseManagerUpdater(db, True).update_fighter_by_id(
        fighter_id, fighter_data
    )


@app.put("/base_fighter/update/name/{name}/{nickname}/{surname}")
# @handle_empty_response
async def update_base_fighter_by_name(
    name: str,
    nickname: str,
    surname: str,
    fighter_data: FighterFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await DatabaseManagerUpdater(
        db, False
    ).update_fighter_by_name_nickname_surname(name, nickname, surname, fighter_data)


@app.put("/extended_fighter/update/name/{name}/{nickname}/{surname}")
@handle_empty_response
async def update_extended_fighter_by_name(
    name: str,
    nickname: str,
    surname: str,
    fighter_data: ExtendedFighterFilter,
    db: AsyncSession = Depends(get_db),
):
    return await DatabaseManagerUpdater(
        db, True
    ).update_fighter_by_name_nickname_surname(name, nickname, surname, fighter_data)


# #
# #
# #######################################DELETE METHODS#############################################
#
#
@app.delete("/base_fighter/id/{fighter_id}")
@handle_empty_response
async def delete_base_fighter(fighter_id: int, db: AsyncSession = Depends(get_db)):
    return await DatabaseManagerUpdater(db, False).remove_record_by_fighter_id(
        fighter_id
    )


@app.delete("/extended_fighter/id/{fighter_id}")
@handle_empty_response
async def delete_extended_fighter(fighter_id: int, db: AsyncSession = Depends(get_db)):
    return await DatabaseManagerUpdater(db, True).remove_record_by_fighter_id(
        fighter_id
    )


@app.delete("/base_fighter/delete_multiple/id/{fighter_id}")
@handle_empty_response
async def delete_multiple_base_fighter(
    list_of_ids: List[int] = Query, db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, False).remove_multiple_records(list_of_ids)


@app.delete("/extended_fighter/delete_multiple/id/{fighter_id}")
@handle_empty_response
async def delete_multiple_extended_fighter(
    list_of_ids: List[int] = Query, db: AsyncSession = Depends(get_db)
):
    return await DatabaseManagerUpdater(db, True).remove_multiple_records(list_of_ids)
