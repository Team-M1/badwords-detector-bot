import os

from client import bot

# os가 windows가 아니면 uvloop를 사용
if os.name != "nt":
    import uvloop

    uvloop.install()

bot.run()
