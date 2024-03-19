from pathlib import Path
from fastapi import File, HTTPException, Request, Response, UploadFile, status
from fastapi import APIRouter
from fastapi.responses import FileResponse
from src.utils.auth_helper import authorize
from src.utils.debugging import is_debug
from src.utils.deployments import get_deployment_packages


router = APIRouter(prefix="/deployments", tags=["Deployments"])


@router.get("/list")
@authorize()
async def get_deployments(
    # pylint: disable=unused-argument
    request: Request,
    web_app: str | None = None,
):
    deployment_packages = get_deployment_packages(web_app)

    return deployment_packages


@router.post("/")
@authorize()
async def upload_deployment(
    # pylint: disable=unused-argument
    request: Request,
    file: UploadFile = File(...),
):
    if Path(file.filename).suffix != ".zip":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That format filer is not allowed!",
        )

    with open(
        (f"data/deployment/{file.filename}" if is_debug() else f"_internal/data/deployment/{file.filename}"),
        "wb",
    ) as f:
        f.write(file.file.read())

    return Response(status_code=status.HTTP_200_OK)


@router.get("/")
@authorize()
async def download_deployment(
    # pylint: disable=unused-argument
    request: Request,
    web_app: str,
):
    deployment_packages = get_deployment_packages(web_app)

    last_deployment_package = deployment_packages[-1] if deployment_packages else None

    if last_deployment_package is None:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return FileResponse(
        path=last_deployment_package.file,
        filename=last_deployment_package.file.name,
        media_type="application/zip",
    )
