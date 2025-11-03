from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.fighter import FighterFilter
from app.services.fighters.fighter_getter import FighterGetter
from app.templates import templates

extended_search_router = APIRouter(prefix="/search")

IS_EXTENDED = True


@extended_search_router.get(
    "", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def search_fighters(
    request: Request,
    fighter_filters: FighterFilter = Depends(),
    db: AsyncSession = Depends(get_db),
):
    fighters = await FighterGetter(db, IS_EXTENDED).search_extended_fighter(
        fighter_filters
    )
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )
