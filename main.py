import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from routers import health, auth, producer, dashboard 

app = FastAPI()

origins = [
    "http://localhost:4200",  # Angular local
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],              
)

app.include_router(health.router, prefix="/api/health")
app.include_router(auth.router, prefix="/api")
app.include_router(producer.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")



if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7001)