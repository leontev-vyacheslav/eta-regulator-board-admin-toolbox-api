from datetime import datetime
from pathlib import Path

from pydantic import BaseModel


class DeploymentPackage(BaseModel):
    file: Path
    date: datetime | None
