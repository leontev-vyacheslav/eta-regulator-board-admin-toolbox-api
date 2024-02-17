from datetime import datetime
from pydantic import BaseModel


class RegulatorDeviceModel(BaseModel):
    id: str

    name: str

    mac_address: str

    master_key: str

    creation_date: str

    creation_date: datetime
