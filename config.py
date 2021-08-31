import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass


class Config:
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise EnvironmentError("TOKEN 환경변수가 없습니다.")

    API_URL = os.getenv("API_URL")
    if not API_URL:
        raise EnvironmentError("API_URL 환경변수가 없습니다.")
