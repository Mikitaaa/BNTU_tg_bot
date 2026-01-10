from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackContext, filters
import logging
import time
from Text_generator import getTextResponse
from Config_handler import load_config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

config = load_config('config.txt')
bot_token = config['bot_token']

lastUpdateTime = time.time()

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Привет! Я отвечу на твои вопросы 🙂")

async def handle_message(update: Update, context: CallbackContext) -> None:
    global lastUpdateTime

    chat_id = update.effective_chat.id

    if update.message.date.timestamp() < lastUpdateTime:
        return
    
    member = await context.bot.get_chat_member(chat_id, context.bot.id)
    if member.status in ["kicked", "left"]:
        return
    
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    response = getTextResponse(update.message.text.lower())
    await context.bot.send_message(chat_id=chat_id, text=response)

    lastUpdateTime = time.time()

def main():
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
