from fastapi import Request

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse

from app.db.database import get_db
from app.schemas.fighter import Fighter as FighterSchema
from app.schemas.fighter import FighterFilter
from app.services.fighters.fighter_getter import FighterGetter
from app.services.fighters.fighter_updater import FighterUpdater
from app.tools.utils import handle_empty_response
from app.templates import templates

base_id_router = APIRouter(prefix="/id")

IS_EXTENDED = False

#
# @base_id_router.get("/{fighter_id}", status_code=status.HTTP_200_OK)
# @handle_empty_response
# async def get_base_fighter_by_id(
#     fighter_id: int, db: AsyncSession = Depends(get_db)
# ) -> FighterSchema:
#     return await FighterGetter(db, IS_EXTENDED).get_fighter_by_id(fighter_id)





@base_id_router.get("/{fighter_id}", status_code=status.HTTP_200_OK, response_class=HTMLResponse)
async def get_base_fighter_by_id(
    request: Request, fighter_id: int, db: AsyncSession = Depends(get_db)
):
    fighter = await FighterGetter(db, IS_EXTENDED).get_fighter_by_id(fighter_id)
    return templates.TemplateResponse("fighter.html", {"request": request, "fighter": fighter})

@base_id_router.delete("/{fighter_id}", status_code=status.HTTP_200_OK)
@handle_empty_response
async def delete_base_fighter(fighter_id: int, db: AsyncSession = Depends(get_db)):
    return await FighterUpdater(db, IS_EXTENDED).remove_record_by_fighter_id(fighter_id)


@base_id_router.put("/{fighter_id}", status_code=status.HTTP_202_ACCEPTED)
@handle_empty_response
async def update_base_fighter_by_id(
    fighter_id: int,
    fighter_data: FighterFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await FighterUpdater(db, IS_EXTENDED).update_fighter_by_id(
        fighter_id, fighter_data
    )
