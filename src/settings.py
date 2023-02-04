from envparse import Env

env = Env()

DATABASE_URL = "postgresql+asyncpg://postgres:Daimondi12@localhost:5432/Nevless"
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:Daimondi12@localhost:5432/Nevless"
SECRET_KEY: str = env.str("SECRET_KEY", default="secret_key")
ALGORITHM: str = env.str("ALGORITHM", default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
