"""File with settings and configs for the project"""

import os

from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = 'a8906ba1367b4fe455c9804207d4268cef42b1c9026ff8c6805802bc009036ea'


BASEDIR = os.getcwd()
LOGDIR = "logs"
LOGFILE = "moviestar.log"
BIND = "0.0.0.0"

WORKERS = os.environ.get("WORKERS")
RELOAD = os.environ.get("RELOAD")
ORIGINS = "*"
