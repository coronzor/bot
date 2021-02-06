import config
import telebot 

bot = telebot.TeleBot(config.TOKEN) 

@bot.message_handler(commands=["start"])
def welcome(message):
    sti = open("static/welcome.webp", 'rb')
    bot.send_sticker(message.chat.id, sti)
    ans = 'ghbfsfsl'
    print(f'sfsjfs {ans} ')
    answer = (f'Вечер в хату, {ans}. ')

    bot.send_message(
        message.chat.id, answer, format(message.from_user, bot.get_me()),
        parse_mode='html'
    )

@bot.message_handler(content_types=["text"])
def start_message(message):
    bot.send_message(message.chat.id,  message.text)

bot.polling(none_stop=True)




