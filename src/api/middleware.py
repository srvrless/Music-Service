from fastapi.middleware.cors import CORSMiddleware

from src.core.app import app
from src.core.settings import ORIGINS

origins = []
for o in ORIGINS.split(","):
    origins.append(o)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
