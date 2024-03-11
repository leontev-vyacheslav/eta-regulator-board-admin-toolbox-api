from pydantic import BaseModel
from pydantic.alias_generators import to_camel


class RegulatorDeviceModel(BaseModel):

    id: str

    name: str

    mac_address: str

    master_key: str

    creation_date: str

    class Config:
        from_attributes = True
        alias_generator=to_camel

