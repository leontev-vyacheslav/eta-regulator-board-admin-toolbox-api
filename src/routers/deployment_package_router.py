from fastapi import File, HTTPException, Response, UploadFile, status
from fastapi import APIRouter


router = APIRouter(prefix='/deployments', tags=['Deployments'])

@router.post('/')
async def upload_deployments(file: UploadFile = File(...)):
    if file.content_type != 'application/zip':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='That format filer is not allowed!')

    with open(f'data/deployment/{file.filename}', 'wb') as f:
        f.write(file.file.read())

    return Response(status_code=status.HTTP_200_OK)
