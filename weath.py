def weather_send(message):
    s_city = message.text

    try:
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

    except:
        bot.send_message(message.chat.id, "Город " + s_city + " - в твоём воображении")