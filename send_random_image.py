import requests
from telegram import Bot

bot = Bot(token='5534444700:AAGqlDYK820tpT4tVaFBe99O1vV8sUly2pY')
URL = 'https://api.thecatapi.com/v1/images/search'
response = requests.get(URL).json()
chat_id = 5245286301
random_cat_url = response[0].get('url')
bot.send_photo(chat_id, random_cat_url)
