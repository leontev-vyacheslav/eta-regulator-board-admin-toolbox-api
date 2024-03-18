from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.data_models.base_data_model import BaseDataModel


class UserDataModel(BaseDataModel):
    __tablename__ = 'user'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    login: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
