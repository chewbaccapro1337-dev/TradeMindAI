from telegram import Update
from telegram.ext import ContextTypes
import requests

from config import FMP_API_KEY
from keyboards import main_keyboard

def get_calendar():

    url = (
        f"https://financialmodelingprep.com/api/v3/"
        f"economic_calendar?apikey={FMP_API_KEY}"
    )

    response = requests.get(url)

    return response.json()

async def show_news(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("show_news started")

    events = get_calendar()
    
    print(type(events))
    print(events)    
    
    await update.message.reply_text(str(events))
    

