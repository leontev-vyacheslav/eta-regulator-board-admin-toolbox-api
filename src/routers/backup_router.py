from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, Response

from src.utils.auth_helper import authorize

router = APIRouter(prefix='/backups', tags=['Backups'])


@router.get('/')
@authorize()
async def get_database(
    # pylint: disable=unused-argument
    request: Request,
):
    root = Path(__file__).parent.parent.parent

    return Response(status_code=200)
    # return FileResponse(
    #     path=f'{root}/{DB_URL}/{DB_FILE}',
    #     filename=DB_FILE,
    #     media_type='application/zip',
    # )
