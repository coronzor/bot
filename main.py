import config
import telebot
import random
import requests
import weath

from telebot import types

bot = telebot.TeleBot(config.TOKEN)
url = 'http://api.openweathermap.org/data/2.5/weather'
api_weather = config.WEATHER

@bot.message_handler(commands=["start"])
def welcome(message):
    sti = open("static/welcome.webp", 'rb')
    bot.send_sticker(message.chat.id, sti)

    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")
    item3 = types.KeyboardButton("⛅️ Погода")

    markup.add(item1, item2, item3)

    bot.send_message(
        message.chat.id,
        "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот .".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=markup
    )



@bot.message_handler(content_types=["text"])
def start_message(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0,100)))
        elif message.text == '⛅️ Погода':
            # bot.send_message(message.chat.id, "Введи название.")
            # weath.weather_send

            def weather_send(message):
                s_city = message.text

                params = {'APPID': api_weather, 'q': s_city, 'units': 'metric'}
                result = requests.get(url, params=params)
                weather = result.json()

                bot.send_message(message.chat.id, "В городе " + str(weather['name'])
                                 + "Температура" + str(float(weather["main"]['temp'])) + " °C\n"
                                 + "Максимальная температура " + str(float(weather["main"]['temp_max'])) + " °C\n"
                                 + "Минимальная температура" + str(float(weather["main"]['temp_min'])) + " °C\n"
                                 + "Скорость ветра" + str(float(weather["wind"]['speed'])) + " \n")

                if weather["main"]['temp'] < 0:
                    bot.send_message(message.chat.id, "Надень лучше пуховик.")
                elif weather["main"]['temp'] > 20:
                    bot.send_message(message.chat.id, "Шорты и футболка.")
                else:
                    bot.send_message(message.chat.id, "Посмотри во что другие одеты.")




        elif message.text == '😊 Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Как в сказке.", callback_data='good')
            item2 = types.InlineKeyboardButton("Бывало и лучше.", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'А ты угадай', reply_markup=markup)
        else:
            bot.send_message(message.chat.id,  message.text)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Чем дальше, тем страшнее.')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Но как раньше уже не будет.')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                text='Попытка неплохая.',reply_markup=None)

            # show alert
            # bot.answer_callback_query(chat_id=call.message.chat.id, show_alert=False, text='MAZAFAKA!11')

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)

