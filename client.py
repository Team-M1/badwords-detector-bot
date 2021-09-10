import re
from urllib.parse import quote

import aiohttp
import hikari
import lightbulb
from lightbulb import slash_commands

from config import Config

bot = lightbulb.Bot(
    token=Config.TOKEN, slash_commands_only=True, intents=hikari.Intents.ALL
)
apiurl = Config.API_URL
pattern = re.compile(r"[ㄱ-ㅣ가-힣]")


async def predict_label(text: str) -> int:
    "입력으로 들어온 text의 레이블을 예측해서 반환합니다."

    url = f"{apiurl}/predict/{quote(text)}"
    async with session.get(url) as resp:
        resp_dict = await resp.json()
    label = resp_dict["label"]
    return label


@bot.listen()
async def on_ready(event: hikari.StartedEvent) -> None:
    "봇이 시작될 때 호출되는 함수"
    global session
    session = aiohttp.ClientSession()
    print(f"봇이 준비되었습니다!\n{event}")


@bot.listen()
async def on_stop(event: hikari.StoppingEvent) -> None:
    "봇이 종료될 때 호출되는 함수"
    await session.close()
    print(f"봇이 종료되었습니다!\n{event}")


async def message_filter(event) -> None:
    "입력으로 들어온 메세지를 검열하는 기능"

    # GuildMessageCreateEvent, GuildMessageUpdateEvent 두 가지 이벤트에
    # 대응하기 위해 @bot.listen을 붙이지 않고, 아래쪽에
    # bot.subscribe로 등록했습니다.

    # 메세지를 보낸 사람이 봇이거나 메세지의 내용이 없으면
    if event.is_bot or not event.content:
        return

    text = event.content

    # 메세지가 한글이 아니면
    if not pattern.search(text):
        return

    # 메세지의 레이블 예측 -> 0, 1, 2
    label = await predict_label(text)

    if label == 1:
        await event.message.delete()
        await event.message.respond(f"나쁜말은 금지야! {event.author.mention}\n -> ||{text}||")

    elif label == 2:
        await event.message.delete()
        await event.message.respond(f"와 완전 말넘심... {event.author.mention}")


# 슬래시 커맨드
class Echo(slash_commands.SlashCommand):
    description: str = "보낸 메세지를 따라합니다."
    text: str = slash_commands.Option("반복할 메세지")
    enabled_guilds = [879644005221167114]

    async def callback(self, context):
        await context.respond(context.options["text"].value)


class Ping(slash_commands.SlashCommand):
    description: str = "봇의 생존여부를 확인합니다."

    async def callback(self, context):
        await context.respond("pong!")


class Invite(slash_commands.SlashCommand):
    description: str = "봇 초대 링크를 생성합니다."

    async def callback(self, context):
        if not Config.CLIENT_ID:
            embed = hikari.Embed(
                description="CLIENT_ID가 없어서 초대링크를 만들 수 없어!"
            ).set_author(
                name=f"{bot.get_me().username} 초대하기", icon=bot.get_me().avatar_url
            )
        else:
            url = f"https://discord.com/api/oauth2/authorize?client_id={Config.CLIENT_ID}&permissions=277025417216&scope=bot%20applications.commands"
            embed = hikari.Embed(description=f"[여기]({url})를 눌러 날 초대할 수 있어!").set_author(
                name=f"{bot.get_me().username} 초대하기", icon=bot.get_me().avatar_url
            )
        await context.respond(embed)


# 봇에 커맨드 등록
bot.subscribe(hikari.GuildMessageCreateEvent, message_filter)
bot.subscribe(hikari.GuildMessageUpdateEvent, message_filter)
bot.add_slash_command(Echo)
bot.add_slash_command(Ping)
bot.add_slash_command(Invite)
