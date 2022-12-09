from fastapi import FastAPI
from routes.user import user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
#adding cors uris
origins =[
    "http://localhost:8000",
    "http://localhost:8001",
    "https://127.0.0.1:8000",
    "https://127.0.0.1:8001",
    "http://localhost:4200",
    "https://localhost:4200",
    "http://192.168.1.11:4200",
    "https://192.168.1.11:4200",
    "http://192.168.1.35:8000",
    "https://192.168.1.35:8000",
    "http://192.168.1.35:4200",
    "https://192.168.1.35:4200",
    "http://192.168.100.81:4200",
    "https://192.168.1.81:4200",
    "https://main.d12wuq988la98b.amplifyapp.com",
    "http://main.d12wuq988la98b.amplifyapp.com",
    "https://main.d12wuq988la98b.amplifyapp.com:4200",
    "http://main.d12wuq988la98b.amplifyapp.com:4200"

    
]
#adding middleware uris
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user)



