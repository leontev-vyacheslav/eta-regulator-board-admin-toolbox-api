from fastapi import FastAPI

app = FastAPI(
    description='ETA Regulator Board Admin Toolbox',
    version='1.0.0',
    title='eta_regulator_board_admin_toolbox',
)

@app.get('/')
async def root():
    return {"message": "Hello World"}
