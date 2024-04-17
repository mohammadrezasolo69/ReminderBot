

from telegram import Update ,ReplyKeyboardRemove
from telegram.ext import CommandHandler, ContextTypes,ApplicationBuilder,ConversationHandler,MessageHandler , filters


from .config import settings,logger
from .services import create_user,get_user,session
from .keyboards import main_keyboard,get_phone_number_keyboard
from .messages import (
    start_message,
    access_management_message,

    new_reminder_title_message,
    new_reminder_cancel_message,
    new_reminder_description_message,
    new_reminder_due_date_message,
    new_reminder_date_message,
    new_reminder_confirmation_message,
    new_reminder_end,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info('start')
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
    
# ----------------------------------------------- New Reminder --------------------------------------------------------
TITLE , DESCRIPTION , DUE_DATE , DATE , CONFIRMATION = range(5)

async def new_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(text=new_reminder_title_message)

    return TITLE

async def new_reminder_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['title'] = update.message.text
    await update.message.reply_text(text=new_reminder_description_message)

    return DESCRIPTION

async def new_reminder_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['description'] = update.message.text
    await update.message.reply_text(text=new_reminder_due_date_message)

    return DUE_DATE

async def new_reminder_due_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:   
    context.user_data['due_date'] = update.message.text 
    await update.message.reply_text(text=new_reminder_date_message)

    return DATE
    
async def new_reminder_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['date'] = update.message.text 
    await update.message.reply_text(text=new_reminder_confirmation_message)

    return CONFIRMATION
    
async def new_reminder_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['confirmation'] = update.message.text 
    print(context.user_data)
    await update.message.reply_text(text=new_reminder_end)



async def new_reminderـcancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text=new_reminder_cancel_message, reply_markup=main_keyboard())


def main():
    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(settings.bot.token).build()

    # on different commands - answer in Telegram
    application.add_handlers([
        CommandHandler("start", start),
        MessageHandler(filters.Regex('^دسترسی ها$'),access_management),
        MessageHandler(filters.CONTACT,handle_contact),
        ConversationHandler(
            entry_points=[MessageHandler(filters.Regex('^یاداوری جدید$'),new_reminder)],
            states={
                TITLE:[MessageHandler(filters.TEXT & ~filters.COMMAND, new_reminder_title)],
                DESCRIPTION : [MessageHandler(filters.TEXT & ~filters.COMMAND, new_reminder_description)],
                DUE_DATE : [MessageHandler(filters.TEXT & ~filters.COMMAND, new_reminder_due_date)],
                DATE : [MessageHandler(filters.TEXT & ~filters.COMMAND, new_reminder_date)],
                CONFIRMATION : [MessageHandler(filters.TEXT & ~filters.COMMAND, new_reminder_confirmation)],
            },
            fallbacks=[CommandHandler('cancel',new_reminderـcancel)]
        )

        
    ])
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
