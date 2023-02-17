from fastapi.middleware.cors import CORSMiddleware

from src.core.app import app
from src.core.settings import ORIGINS

origins = ["http://localhost:8000",]
for o in ORIGINS.split(","):
    origins.append(o)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)
