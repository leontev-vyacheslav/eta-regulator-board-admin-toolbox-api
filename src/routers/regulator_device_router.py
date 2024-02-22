from fastapi import Depends, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.data_access.database_connect import get_async_session
from src.data_models.regulator_device_data_model import RegulatorDeviceDataModel
from src.models.regulator_device_model import RegulatorDeviceModel


router = APIRouter(prefix='/regulator-devices', tags=['Regulators'])


@router.get('/')
async def get_regulators(session: AsyncSession = Depends(get_async_session)):
    query = await session.execute(select(RegulatorDeviceDataModel))

    devices = [
        {
            "id": row.id,
            "name": row.name,
            "macAddress": row.mac_address,
            "masterKey": row.master_key,
            "creationDate": row.creation_date,
        }
        for row in query.scalars()
    ]

    return devices


@router.get('/{device_id}')
async def get_regulator(device_id: str, session: AsyncSession = Depends(get_async_session)):
    device = await session.get(RegulatorDeviceDataModel, device_id)

    if device is None:
        return Response(status_code=400)

    return device

@router.post('/')
async def post_regulator(device: RegulatorDeviceModel, session: AsyncSession = Depends(get_async_session)):
    device_data = RegulatorDeviceDataModel(
        id=device.id,
        name=device.name,
        mac_address=device.mac_address,
        master_key=device.master_key,
        creation_date=device.creation_date,
    )

    session.add(device_data)
    await session.commit()
    await session.refresh(device_data)

    return {
            "id": device_data.id,
            "name": device_data.name,
            "macAddress": device_data.mac_address,
            "masterKey": device_data.master_key,
            "creationDate": device_data.creation_date,
        }


@router.delete('/{device_id}')
async def delete_regulator(device_id: str, session: AsyncSession = Depends(get_async_session)):
    device_data = await session.get(RegulatorDeviceDataModel, device_id)

    if device_data is None:
        return Response(status_code=400)

    device = {
            "id": device_data.id,
            "name": device_data.name,
            "macAddress": device_data.mac_address,
            "masterKey": device_data.master_key,
            "creationDate": device_data.creation_date,
        }

    await session.delete(device_data)
    await session.commit()

    return device


@router.put('/')
async def put_regulator(device: RegulatorDeviceModel, session: AsyncSession = Depends(get_async_session)):
    device_data = await session.get(RegulatorDeviceDataModel, device.id)

    if device_data is None:
        return Response(status_code=400)

    device_data.name = device.name
    device_data.mac_address = device.mac_address
    device_data.master_key = device.master_key

    await session.commit()

    return {
            "id": device.id,
            "name": device.name,
            "macAddress": device.mac_address,
            "masterKey": device.master_key,
            "creationDate": device.creation_date,
        }
