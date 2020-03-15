from telegram.update import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, run_async
from telegram.user import User
from telegram import ReplyKeyboardMarkup
from database import DataBase
from handlers.dialog_handler import _stop_dialog

@run_async
def _start(update: Update, context: CallbackContext):
    
    user: User = update.message.from_user

    base = DataBase()

    result = base.get_user(f"{user.id}")

    if not result:
        base.add_user(f"{user.id}", user.first_name, user.last_name or "", user.username or "")
    else:
        _stop_dialog(update, context)
    base.close()

    keyboard = [["Начать диалог 🚀"]]

    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    update.message.reply_text("Начните поиск собеседника", reply_markup=markup)
    return ConversationHandler.END


def handle():
    return CommandHandler("start", _start)
