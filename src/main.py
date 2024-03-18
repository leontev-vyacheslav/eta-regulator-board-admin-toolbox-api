from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketio import ASGIApp, AsyncServer

from src.routers.access_token_router import router as access_token_router
from src.routers.root_router import router as root_router
from src.routers.regulator_device_router import router as regulator_device_router
from src.routers.deployment_package_router import router as deployment_package_router
from src.routers.backup_router import router as backup_router
from src.routers.auth_router import router as auth_router

app = FastAPI(
    title='eta_regulator_board_admin_toolbox',
    description='ETA Regulator Board Admin Toolbox',
    version='1.0.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root_router)
app.include_router(regulator_device_router)
app.include_router(access_token_router)
app.include_router(deployment_package_router)
app.include_router(backup_router)
app.include_router(auth_router)

socket_io_server = AsyncServer(async_mode='asgi')

app.mount("/", ASGIApp(socket_io_server))

app.state.socket_io_server = socket_io_server
