import asyncio
from telegram import Bot
from telegram.request import HTTPXRequest

TOKEN = "8711419545:AAFoSdmOeLubWxrRMfJntlheWLdZeQr_rgU"

async def main():
    request = HTTPXRequest(
        proxy="socks5://qMLzj4:r5NZWQ@168.81.42.247:8000"
    )

    bot = Bot(token=TOKEN, request=request)
    me = await bot.get_me()
    print(me)

asyncio.run(main())
