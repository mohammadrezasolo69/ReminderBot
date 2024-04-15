

from telegram import Update , KeyboardButton,ReplyKeyboardMarkup , InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes,ApplicationBuilder,MessageHandler,filters

from .services import create_user
from .config import settings,logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = create_user(user=update.message.from_user)
    await update.message.reply_html(text='سلام جیگرمممممم')
    

    """Send a message when the command /start is issued."""
    user = get_user(telegram_id=update.message.from_user.id)
    print(user)
    if user is not None:
        users = all_users()
        await update.message.reply_text(text=f'users: \n {users}')
    else:
        await update.message.reply_text(text=f'not permission')


def main():
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(settings.bot.token).build()

    # on different commands - answer in Telegram
    application.add_handlers([
        CommandHandler("start", start),
        
    ])
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
