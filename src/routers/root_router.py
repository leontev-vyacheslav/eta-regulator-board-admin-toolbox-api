from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(prefix='', tags=['Root'])


@router.get('/')
async def root():
    return RedirectResponse('/docs')
