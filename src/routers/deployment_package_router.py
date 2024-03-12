from pathlib import Path
from datetime import datetime
from typing import List
from fastapi import File, HTTPException, Response, UploadFile, status
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.utils.debugging import is_debug
class DeploymentPackage(BaseModel):
    file: Path
    date: datetime | None


router = APIRouter(prefix="/deployments", tags=["Deployments"])

@router.post("/")
async def upload_deployment(file: UploadFile = File(...)):
    if Path(file.filename).suffix != ".zip":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That format filer is not allowed!",
        )

    with open(
        (
            f"data/deployment/{file.filename}"
            if is_debug()
            else f"_internal/data/deployment/{file.filename}"
        ),
        "wb",
    ) as f:
        f.write(file.file.read())

    return Response(status_code=status.HTTP_200_OK)


@router.get("/")
async def download_deployment(web_app: str):
    deployment_package_path = (
        "data/deployment/" if is_debug() else "_internal/data/deployment/"
    )

    def strptime(s: str):
        try:
            return datetime.strptime(s, "%Y%m%dT%H%M%S")
        except ValueError:
            return None

    deployment_packages: List[DeploymentPackage] = sorted(
        [
            package
            for package in (
                DeploymentPackage(file=path, date=strptime(path.stem.split("_")[-1]))
                for path in Path(deployment_package_path).iterdir()
                if path.suffix == ".zip" and web_app in path.name
            )
            if package.date is not None
        ],
        key=lambda p: p.date,
    )

    last_deployment_package = deployment_packages[-1] if deployment_packages else None

    if last_deployment_package is not None:
        return FileResponse(
            path=last_deployment_package.file,
            filename=last_deployment_package.file.name,
            media_type="application/zip",
        )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
