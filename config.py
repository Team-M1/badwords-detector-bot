import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    TOKEN = os.getenv("TOKEN")
    if not TOKEN:
        raise EnvironmentError("TOKEN 환경변수가 없습니다.")

    API_URL = os.getenv("API_URL")
    if not API_URL:
        raise EnvironmentError("API_URL 환경변수가 없습니다.")
    API_URL = API_URL.rstrip("/")

    CLIENT_ID = os.getenv("CLIENT_ID")
    if not CLIENT_ID:
        print("CLIENTID 환경변수가 없습니다. 초대링크를 생성할 수 없습니다.")
