import requests
import telebot
import json
from key import TOKEN,API_KEY
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
URL_WEATHER_API = 'https://api.openweathermap.org/data/2.5/weather'
#Доделать словарь с эмоджи по погоде (ключ - это id погоды пример(weather {'id': 804}),
# значение эмоджи)
EMOJI_CODE = {
    200: '⛈️',
    201: '⛈️', 
    202: '⛈️', 
    210: '⛈️', 
    211: '⛈️', 
    212: '⛈️', 
    221: '⛈️',
    230: '⛈️', 
    231: '⛈️', 
    232: '⛈️',
    300: '🌧️', 
    301: '🌧️', 
    302: '🌧️', 
    310: '🌧️', 
    311: '🌧️', 
    312: '🌧️', 
    313: '🌧️',
    314: '🌧️', 
    321: '🌧️',
    500: '🌧️', 
    501: '🌧️', 
    502: '🌧️', 
    503: '🌧️', 
    504: '🌧️', 
    511: '🌧️',
    520: '🌧️', 
    521: '🌧️', 
    522: '🌧️', 
    531: '🌧️',
    600: '🌨️', 
    601: '🌨️', 
    602: '🌨️', 
    611: '🌨️',
    612: '🌨️', 
    613: '🌨️',
    615: '🌨️', 
    616: '🌨️', 
    620: '🌨️', 
    621: '🌨️', 
    622: '🌨️',
    701: '🌫️', 
    711: '🌫️', 
    721: '🌫️', 
    731: '🌫️', 
    741: '🌫️', 
    751: '🌫️',
    761: '🌫️', 
    762: '🌫️', 
    771: '🌫️', 
    781: '🌫️',
    800: '☀️',
    801: '⛅',   
    802: '☁️',   
    803: '☁️',
    804: '☁️'
}
            

bot = telebot.TeleBot(TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))


#Нужно добавить описание погоды weather description
# Кодировка погоды для словаря EMOJI_CODE weather id
# температуру temp, температуру по ощущению 'feels like', влажность 'humidity'
#Добавлять к строке переменной message всю нужную информацию
def get_weather(lat, lon):
    params = {
    'lat': lat,
    'lon': lon,
    'units': 'metric',
    'lang': 'ru',
    'appid': API_KEY
    }
    response = requests.get(URL_WEATHER_API, params).json()
    city_name = response['name']
    message = f'🌆Погода в городе {city_name}\n{EMOJI_CODE[response["cod"]]}На улице {response["weather"][0]["description"]}\n🌡️Температура в городе:{round(response["main"]["temp"])}°С\n🗞️Ощущается как {round(response["main"]["feels_like"])}°С\n💧Влажность:{round(response["main"]["humidity"])} %'
    print(json.dumps(response, indent=2, ensure_ascii=False))
    return message

@bot.message_handler(commands = ['start',"help"])
def send_welcome(message):
    text = '🔖Отправь мне местоположение и я отправлю погоду'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

#Добавить способ определения локация пользователя.
# Для этого используйте атрибуты объекта message
# Впишите их в переменные lon и lat
@bot.message_handler(content_types = ['location'])
def send_weather(message):    
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat, lon)
    bot.send_message(message.chat.id, result, reply_markup=keyboard)
    print

# Дополните информацию о проекте
@bot.message_handler(regexp = 'О проекте')
def about_author(message):
    about_text = "🗞️Об авторе и боте🗞️\n\n"
    about_text += "👨‍💻Автор: Андрей\n"
    about_text += "🤖О боте: Бот, для получения актуальных данных о погоде\n"
    about_text += "📅Создан: [8.03.26]\n"
    about_text += "🖥️Используемые API: openweathermap.org\n"
    bot.send_message(message.chat.id, about_text, reply_markup=keyboard)
bot.infinity_polling()