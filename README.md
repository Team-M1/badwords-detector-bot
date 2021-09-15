<img src="https://i.imgur.com/nd1GE2U.png" width="200">

# 나쁜말 요정

함께 만든 API [Team-M1/korean-malicious-comments-api](https://github.com/Team-M1/korean-malicious-comments-api)와 같이 사용할 목적으로 만들어진 디스코드 봇입니다.



## 사용방법

#### 1. 도커

```sh
docker run -d \
    -e TOKEN=봇 토큰 \
    -e API_URL=API루트주소 \
    -e CLIENT_ID=봇 클라이언트아이디 \
    ks2515/badwords-detector-bot
```

3가지 환경변수를 필요로 합니다.

`TOKEN`: 디스코드 봇 토큰입니다.

`API_URL`: [Team-M1/korean-malicious-comments-api](https://github.com/Team-M1/korean-malicious-comments-api) 사용할 API의 주소입니다.

`CLIENT_ID`: (옵션) 디스코드 봇 클라이언트 ID입니다. 봇 초대링크를 생성할 때에만 사용됩니다.

#### docker-compose

docker-compose로 api와 봇을 동시에 서비스 할 수 있습니다.

```yaml
version: "3"

services:
  api:
    image: ks2515/kmca

  bot:
    depends_on:
      - api
    image: ks2515/badwords-detector-bot
    environment:
      - API_URL=http://api
    env_file:
      - .env
```

간단한 예는 위와 같습니다. 이 예에서 TOKEN과 CLIENT_ID 환경변수는 `.env`파일 안에 있게 됩니다. `environment`에 직접 작성해도 무방합니다.


#### 2. heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

위 버튼을 누르는 것으로 heroku로 배포할 수 있습니다.

위와 똑같이 `TOKEN`, `API_URL`, `CLIENT_ID` (옵션) 환경변수를 필요로 합니다.



#### 3. 로컬

```sh
python -OO main.py
```

hikari에서는 최소 하나의 `-O`옵션을 넣고 실행하는 것을 권장하고 있습니다. [hikari](https://github.com/hikari-py/hikari) 깃허브 페이지를 참고하세요.

`.env`파일을 만들어 이 안에 환경변수를 설정하면 됩니다.

```py
# .env

TOKEN=봇토큰
API_URL=API 루트주소
CLIENT_ID=봇 클라이언트 ID
```



### 초대하기

```
https://discord.com/api/oauth2/authorize?client_id={클라이언트 아이디}&permissions=277025417216&scope=bot%20applications.commands
```



## 기능

![검열예시](https://i.imgur.com/tL5Gyd9.png)

채팅방에 올라온 글을 API로 보내 예측된 레이블 값을 받습니다. 레이블 값이 1이나 2이면 채팅을 검열합니다.



#### 슬래시 커맨드

`/invite`

봇 초대링크를 생성합니다. `CLIENT_ID`가 필요합니다.

![초대예시](https://i.imgur.com/6oqfv43.png)