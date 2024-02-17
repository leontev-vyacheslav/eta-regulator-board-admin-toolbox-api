from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.data_access.database_connect import get_async_session

from src.data_models.regulator_device_data_model import RegulatorDeviceDataModel
from src.models.regulator_device_model import RegulatorDeviceModel


router = APIRouter(prefix='/regulator-devices', tags=['Regulators'])


@router.get('/')
async def get_regulators(session: AsyncSession = Depends(get_async_session)):
    query = await session.execute(select(RegulatorDeviceDataModel))

    return [
        RegulatorDeviceModel(
            id=row.id,
            name=row.name,
            mac_address=row.mac_address,
            master_key=row.master_key,
            creation_date=row.creation_date,
        )
        for row in query.scalars()
    ]
