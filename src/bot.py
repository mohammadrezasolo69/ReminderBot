

from telegram import Update 
from telegram.ext import CommandHandler, ContextTypes,ApplicationBuilder,ConversationHandler,MessageHandler , filters

from .services import create_user,get_user,session
from .messages import start_message,access_management_message
from .config import settings,logger
from .keyboards import main_keyboard,get_phone_number_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = create_user(user=update.message.from_user)
    await update.message.reply_text(text=start_message,reply_markup=main_keyboard())



async def access_management(update:Update,context:ContextTypes.DEFAULT_TYPE)-> None:
    user = get_user(telegram_id=update.message.from_user.id)
    if user.phone_number:
        await update.message.reply_text(text=f"شماره موبایل شما :‌ {user.phone_number}")
                                        
    else:                                  
        await update.message.reply_text(text=access_management_message,reply_markup=get_phone_number_keyboard())
    

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = get_user(telegram_id=update.message.from_user.id)
    user.phone_number = update.message.contact.phone_number
    session.commit()
    
    await update.message.reply_text(text="مرسی گلم",reply_markup=main_keyboard())
    


def main():
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(settings.bot.token).build()

    # on different commands - answer in Telegram
    application.add_handlers([
        CommandHandler("start", start),
        MessageHandler(filters.Regex('^دسترسی ها$'),access_management),
        MessageHandler(filters.CONTACT,handle_contact),
        ConversationHandler(
            entry_points=[MessageHandler(filters.Regex('^دسترسی ها$'),access_management)],
            states={},
            fallbacks=[]
        )

        
    ])
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
