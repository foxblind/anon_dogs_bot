import random
from telegram.update import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, CallbackQueryHandler
from telegram.user import User
from telegram import ReplyKeyboardMarkup, Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.files.photosize import PhotoSize
from database import DataBase
from utils import send_copy, get_input_media


def _next_dialog(update: Update, context: CallbackContext):
    user: User = update.message.from_user

    base = DataBase()
    companion_id = base.reset_companion(str(user.id))

    base.set_status(str(user.id), "pause")
    base.set_status(companion_id, "pause")

    if len(companion_id):
        keyboard = [["Искать нового собеседника 👀"]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        context.bot.send_message(companion_id, "Собеседник покинул чат.", reply_markup=markup)

    awaiting = base.get_waiting()

    if not len(awaiting):
        base.set_status(str(user.id), "waiting")

        keyboard = [['Закончить поиск 🖐🏻']]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        update.message.reply_text("Поиск свободных собеседников", reply_markup=markup)

        base.close()

    else:

        new_companion_id = random.choice(awaiting)[0]
        base.set_status(str(user.id), "chatting")
        base.set_status(new_companion_id, "chatting")

        base.set_companion(str(user.id), new_companion_id)

        keyboard = [["Искать нового собеседника 👀"], ["Закончить диалог 🖐🏻"]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        context.bot.send_message(user.id, "Собеседник найден 🐵", reply_markup=markup)
        context.bot.send_message(str(new_companion_id), "Собеседник найден 🐵", reply_markup=markup)

        base.close()


def _stop_dialog(update: Update, context: CallbackContext):
    user: User = update.message.from_user

    base = DataBase()

    companion_id = base.reset_companion(str(user.id))
    base.set_status(str(user.id), "pause")
    base.set_status(companion_id, "pause")

    keyboard = [["Начать диалог 🚀"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    if len(str(companion_id)):
        context.bot.send_message(companion_id, "Собеседник покинул чат.", reply_markup=markup)
        context.bot.send_message(user.id, "Вы закончили связь с Вашим собеседником🙄.", reply_markup=markup)
    else:
        context.bot.send_message(user.id, "Вы прервали поиск собеседника 🙄.", reply_markup=markup)

    base.close()


def _filter_message(update: Update, context: CallbackContext):
    base = DataBase()
    message: Message = update.message
    companion = base.get_companion(str(message.from_user.id))

    if type(message.effective_attachment) is list:
        file_id = message.effective_attachment[-1].file_id
        file_name = ""
        file_type = f"{PhotoSize}"
    else:
        file_id = message.effective_attachment.file_id
        file_name = ""
        file_type = f"{type(message.effective_attachment)}"

    if len(companion):
        base.save_filtered(str(message.from_user.id), str(message.message_id), str(message.from_user.id),
                           companion, message.caption or "", file_name, file_id, file_type)

        base.save_message(f"{message.message_id}",
                          f"{message.from_user.id}",
                          f"{message.from_user.id}",
                          companion, message.text or message.caption or "", file_id)

        alert_message = "Собеседник отправил файл, который может содержать порно. Показать?"

        show_btn = InlineKeyboardButton("Показать", callback_data=f"show_{message.from_user.id}_{message.message_id}")
        markup = InlineKeyboardMarkup([[show_btn]])

        photo = open("spoiler.jpg", "rb")

        context.bot.send_photo(companion, photo, caption=alert_message, reply_markup=markup)

        base.close()


def _not_allowed(update: Update, context: CallbackContext):
    update.message.reply_text("Стикеры, круглые видео, местоположение и контакты не поддерживаются.")


def _message(update: Update, context: CallbackContext):
    message: Message = update.message

    base = DataBase()
    companion = base.get_companion(str(message.from_user.id))

    if len(companion):
        if message.effective_attachment is not None:
            file_id = message.effective_attachment.file_id
        else: file_id = ""
        base.save_message(f"{message.message_id}",
                          f"{message.from_user.id}",
                          f"{message.from_user.id}",
                          companion, message.text or message.caption or "", file_id)
        send_copy(companion, message.text or message.caption or "", file_id, f"{type(message.effective_attachment)}", context.bot)
    base.close()


def _show_filtered(update: Update, context: CallbackContext):
    callback: CallbackQuery = update.callback_query
    src_chat, src_message = str(callback.data).split("_")[1:]

    base = DataBase()

    file_id, content_type, text = base.get_filtered(src_chat, src_message)
    message: Message = callback.message
    message.edit_media(get_input_media(file_id, content_type))
    if len(text):
        context.bot.edit_message_caption(callback.from_user.id, callback.message.message_id, caption=text)

    base.close()


def handle():
    return [MessageHandler(Filters.text("Искать нового собеседника 👀"), _next_dialog),
            MessageHandler(Filters.text("Начать диалог 🚀"), _next_dialog),
            MessageHandler(Filters.text("Закончить диалог 🖐🏻") | Filters.text("Закончить поиск 🖐🏻"), _stop_dialog),
            MessageHandler(Filters.text | Filters.audio | Filters.voice, _message),
            MessageHandler(Filters.photo | Filters.document | Filters.video, _filter_message),
            MessageHandler(Filters.venue | Filters.location | Filters.contact | Filters.video_note |
                           Filters.animation | Filters.sticker, _not_allowed),
            CallbackQueryHandler(_show_filtered, pattern="^show_[0-9]{6,9}_[0-9]{1,10}$")]
