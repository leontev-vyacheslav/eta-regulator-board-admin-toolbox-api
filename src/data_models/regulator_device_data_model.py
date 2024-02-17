from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.data_models.base_data_model import BaseDataModel


class RegulatorDeviceDataModel(BaseDataModel):
    __tablename__ = 'regulator_device'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    mac_address: Mapped[str] = mapped_column(String)
    master_key: Mapped[str] = mapped_column(String)
    creation_date: Mapped[str] = mapped_column(String)
