# from pydantic import BaseModel
# from typing import Optional
# from src import TunedModel
#
# class SignUpModel(BaseModel):
#     user_id: Optional[int]
#     nickname: str
#     email_address: str
#     password: str
#     is_active: Optional[bool]
#     is_subscriber: Optional[bool]
from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = 'a8906ba1367b4fe455c9804207d4268cef42b1c9026ff8c6805802bc009036ea'


class LoginModel(BaseModel):
    nickname: str
    password: str
