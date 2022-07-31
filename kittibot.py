import os, requests
from telegram import ReplyKeyboardMarkup, Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from dotenv import load_dotenv


load_dotenv()
updater = Updater(token=os.getenv('TOKEN'))
bot = Bot(token=os.getenv('TOKEN'))
button = ReplyKeyboardMarkup([['/newcat', '/newdog']], resize_keyboard=True)
CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'

def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я KittyBot!')

def get_cat_image():
    try:
        response = requests.get(CAT_URL)
    except Exception:
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def get_dog_image():
    try:
        response = requests.get(DOG_URL)
    except Exception:
        new_url = 'https://api.thecatapi.com/v1/images/search'
        response = requests.get(new_url)

    response = response.json()
    random_dog = response[0].get('url')
    return random_dog

def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_cat_image())

def new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_dog_image())

def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_cat_image())

def main():
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
