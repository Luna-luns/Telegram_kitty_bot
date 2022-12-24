import os
import requests
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackContext
from dotenv import load_dotenv

URL = 'https://api.thecatapi.com/v1/images/search'
load_dotenv()
token = os.getenv('TOKEN')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def wake_up(update: Update, context: CallbackContext):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Welcome, {name}! Look at the cat I found for you',
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())


def say_hi(update: Update, context: CallbackContext):
    chat = update.effective_chat
    text = update.message.text
    if text in ['Hi', 'Hello', 'hi', 'hello']:
        context.bot.send_message(chat_id=chat.id, text="Hello, I'm a KittyBot Lolla!")
    elif text in ["How are you?", "What's up?", "how are you?", "what's up?"]:
        context.bot.send_message(chat_id=chat.id, text="All is cool ^_^")
    else:
        context.bot.send_message(chat_id=chat.id, text="Sorry, I don't understand you :(")


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Error when requesting the main API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token=token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
