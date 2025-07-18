import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from routers import health, producer

app = FastAPI()
app.include_router(health.router, prefix="/health")
app.include_router(producer.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7001)