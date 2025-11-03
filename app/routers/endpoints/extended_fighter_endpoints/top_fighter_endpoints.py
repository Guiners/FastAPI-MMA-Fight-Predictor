from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.fighters.fighter_getter import FighterGetter
from app.templates import templates

extended_top_router = APIRouter(prefix="/top")

IS_EXTENDED = True


@extended_top_router.get(
    "/wins", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_top_extended_fighters_by_wins(
    request: Request, limit: int, db: AsyncSession = Depends(get_db)
):
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "wins", limit
    )
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )


@extended_top_router.get(
    "/loss", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_top_fighters_by_loss(
    request: Request, limit: int, db: AsyncSession = Depends(get_db)
):
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "loss", limit
    )
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )


@extended_top_router.get(
    "/wins/ko", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_top_fighters_by_ko_wins(
    request: Request, limit: int, db: AsyncSession = Depends(get_db)
):
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "win_by_ko_tko", limit
    )
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )


@extended_top_router.get(
    "/loss/ko", status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def get_top_fighters_by_ko_loss(
    request: Request, limit: int, db: AsyncSession = Depends(get_db)
):
    fighters = await FighterGetter(db, IS_EXTENDED).get_fighters_by_param_with_limit(
        "loss_by_ko_tko", limit
    )
    return templates.TemplateResponse(
        "fighter_list.html", {"request": request, "fighters": fighters}
    )
