from pydantic import BaseModel, Field


class RegulatorDeviceModel(BaseModel):

    id: str

    name: str

    mac_address: str = Field(alias='macAddress')

    master_key: str = Field(alias='masterKey')

    creation_date: str = Field(alias='creationDate')

    # model_config = ConfigDict(alias_generator=to_camel)
