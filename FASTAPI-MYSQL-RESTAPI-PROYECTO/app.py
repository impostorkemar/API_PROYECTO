from fastapi import FastAPI
from routes.user import user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
#adding cors uris
origins =[
    "http://localhost:8000",
    "http://localhost:8001",
]
#adding middleware uris
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(user)



