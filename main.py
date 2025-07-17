import uvicorn
from fastapi import FastAPI

from routers import health

app = FastAPI()
app.include_router(health.router, prefix="/health")


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7000)