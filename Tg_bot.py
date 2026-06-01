from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackContext, filters
import logging
import os
from Text_generator import getTextResponse

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot_token = os.environ['BOT_TOKEN']
if not bot_token:
    raise ValueError("BOT_TOKEN не задан в переменных окружения")

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="Привет! Я отвечу на твои вопросы 🙂")

async def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    try:
        member = await context.bot.get_chat_member(chat_id, context.bot.id)
        if member.status in ["kicked", "left"]:
            return
    except Exception as e:
        logging.error(f"Error checking chat member: {e}")
        return

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        response = getTextResponse(update.message.text.lower())
        await context.bot.send_message(chat_id=chat_id, text=response)
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Извините, произошла ошибка.")


def main():
    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
