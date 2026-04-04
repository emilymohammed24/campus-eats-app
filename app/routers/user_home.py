from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import status
from sqlmodel import select
from app.models.restaurant import Restaurant
from app.dependencies.session import SessionDep
from app.dependencies.auth import AuthDep, IsUserLoggedIn, get_current_user, is_admin
from . import router, templates


@router.get("/app", response_class=HTMLResponse)
async def user_home_view(
    request: Request,
    user: AuthDep,
    db:SessionDep
):
    restaurants = db.exec(select(Restaurant)).all()

    return templates.TemplateResponse(
        request=request, 
        name="app.html",
        context={
            "user": user,
            "restaurants": restaurants
        }
    )