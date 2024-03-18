from pathlib import Path
from fastapi import APIRouter
from fastapi.responses import FileResponse

from src.data_access.database_connect import DB_URL, DB_FILE

router = APIRouter(prefix='/backups', tags=['Backups'])

@router.get("/")
async def get_database():
    root = Path(__file__).parent.parent.parent

    return FileResponse(
        path= f'{root}/{DB_URL}/{DB_FILE}',
        filename=DB_FILE,
        media_type="application/zip",
    )
