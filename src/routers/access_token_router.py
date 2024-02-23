from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.data_access.database_connect import get_async_session
from src.data_models.regulator_device_data_model import RegulatorDeviceDataModel
from src.models.access_token_model import AccessTokenModel
from src.utils.encoding import create_access_token


router = APIRouter(prefix='/access-token', tags=['Access Token'])

@router.get('/{device_id}')
async def get_access_token(device_id: str, duration: int, session: AsyncSession = Depends(get_async_session)):
    device = await session.get(RegulatorDeviceDataModel, device_id)

    if device is None:
        return Response(status_code=400)

    access_token = create_access_token(mac_address=device.mac_address, duration=duration, key=device.master_key)

    return AccessTokenModel(token=access_token)
