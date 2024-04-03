

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes,ApplicationBuilder


from config import settings,logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_html(text='سلام جیگرمممممم')



def main():
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(settings.bot.token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()