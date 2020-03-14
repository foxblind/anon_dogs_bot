from telegram.update import Update
from telegram.ext import CallbackContext, MessageHandler, Filters, CommandHandler
from database import DataBase
import csv
from utils import is_admin
def _get_users(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        base = DataBase()

        users = base.get_users()
        base.close()
        with open("users.csv", "w", newline="") as users_file:

            writer = csv.writer(users_file, delimiter=";")
            writer.writerow(users[0].keys())
            for user in users:
                writer.writerow(user)

        update.message.reply_document(open("users.csv", "rb"))


def _get_chats(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        base = DataBase()

        chats = base.get_chats_history()
        base.close()

        with open("chats.csv", "w", newline="") as users_file:
            writer = csv.writer(users_file, delimiter=";")
            writer.writerow(chats[0].keys())
            for chat in chats:
                writer.writerow(chat)

        update.message.reply_document(open("chats.csv", "rb"))


def _get_filtered(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        base = DataBase()

        filtered = base.get_all_filtered()
        base.close()
        if len(filtered):
            with open("filtered.csv", "w", newline="") as users_file:
                writer = csv.writer(users_file, delimiter=";")
                writer.writerow(filtered[0].keys())
                for message in filtered:
                    writer.writerow(message)

            update.message.reply_document(open("filtered.csv", "rb"))

        else:
            update.message.reply_text("empty")


def _get_messages(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        base = DataBase()
        if len(update.message.text.split("_"))>1:
            user = update.message.text.split("_")[1]
        else:
            user = ""
        messages = base.get_messages(user)
        base.close()

        with open("messages.csv", "w", newline="") as users_file:
            writer = csv.writer(users_file, delimiter=";")
            writer.writerow(messages[0].keys())
            for message in messages:
                writer.writerow(message)

        update.message.reply_document(open("messages.csv", "rb"))


def _help(update: Update, context: CallbackContext):
    if is_admin(update.message.from_user.id):
        update.message.reply_text("/users\n/hist\n/filtered\n/msgs")


def handle():
    return [CommandHandler("users", _get_users),
            CommandHandler("hist", _get_chats),
            CommandHandler("filtered", _get_filtered),
            CommandHandler("msgs", _get_messages),
            CommandHandler("help", _help)]