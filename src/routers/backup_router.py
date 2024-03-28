import io
import zipfile
import json
from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth_helper import authorize
from src.data_access.database_connect import get_async_session


router = APIRouter(prefix='/backups', tags=['Backups'])


@router.get('/')
@authorize()
async def get_database(
    # pylint: disable=unused-argument
    request: Request,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_archive:
        for table in ['user', 'regulator_device']:
            raw = (await session.execute(text(f'SELECT array_to_json(array_agg(row_to_json(t))) FROM "{table}" t;'))).first()
            json_text = json.dumps(raw[0])
            zip_archive.writestr(f'{table}.json', json_text)
    zip_buffer.seek(0)

    return StreamingResponse(
        content=zip_buffer,
        media_type='application/zip',
        headers={'Content-Disposition': f'attachment; filename="eta_regulator_box_admin_database_dump_{datetime.now().strftime("%Y%m%dT%H%M%S")}.zip"'},
    )
