
from fastapi import APIRouter

from src.models.access_token_model import AccessTokenModel
from src.models.regulator_device_model import RegulatorDeviceModel
from src.utils.encoding import create_access_token


router = APIRouter(prefix='/access-token', tags=['Access Token'])

@router.get('/')
async def get_access_token(device: RegulatorDeviceModel):
    access_token = create_access_token(
        mac_address=device.mac_address,
        duration=8,
        key=device.master_key
    )

    return AccessTokenModel(token=access_token)
