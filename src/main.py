from fastapi import FastAPI

from src.routers.access_token_router import router as access_token_router
from src.routers.root_router import router as root_router
from src.routers.regulator_device_router import router as regulator_device_router


app = FastAPI(
    title='eta_regulator_board_admin_toolbox',
    description='ETA Regulator Board Admin Toolbox',
    version='1.0.0',
)



app.include_router(root_router)
app.include_router(regulator_device_router)
app.include_router(access_token_router)
