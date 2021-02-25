import config
import telebot
import random

from telebot import types

bot = telebot.TeleBot(config.TOKEN) 

@bot.message_handler(commands=["start"])
def welcome(message):
    sti = open("static/welcome.webp", 'rb')
    bot.send_sticker(message.chat.id, sti)
    # ans = 'ghbfsfsl'
    # print(f'sfsjfs {ans} ')
    # answer = (f'Вечер в хату, {ans}. ')
    # Не понял зачем эти 3 строчки вообще написал.

    # Keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😊 Как дела?")

    markup.add(item1, item2)

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

