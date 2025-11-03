import typing

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.fighter import Fighter as FighterSchema
from app.services.fighters.fighter_getter import FighterGetter
from app.templates import templates
from app.tools.utils import handle_empty_response

base_country_router = APIRouter(prefix="/country")

IS_EXTENDED = False


@base_country_router.get("/{country}", status_code=status.HTTP_200_OK)
async def get_fighters_data_by_country(
    request: Request, country: str, db: AsyncSession = Depends(get_db)
):
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_country(country)
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )
