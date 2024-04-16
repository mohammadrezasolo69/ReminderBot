from telegram import Update , KeyboardButton,ReplyKeyboardMarkup

def main_keyboard():
    keyboard = [[KeyboardButton('یاداوری جدید'),KeyboardButton('یاداوری ها')],[KeyboardButton('دسترسی ها')]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True,one_time_keyboard=True)

    return markup


def get_phone_number_keyboard():
    keyboard=[[KeyboardButton(text="ارسال شماره موبایل", request_contact=True)]]
    markup = ReplyKeyboardMarkup(keyboard=keyboard,resize_keyboard=True,one_time_keyboard=True)
    
    return markup