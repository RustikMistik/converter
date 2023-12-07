import telebot
import requests

TOKEN = '6733534110:AAEyyzek5ocB6WMMTTGC1-2D57tmk9obg4o' # Не разобрался как его засунуть в отдельный файл, при импорте ошибка, но нет времени, дедлайн я уже пропустил(

bot = telebot.TeleBot(TOKEN)

# API для получения курсов валют
exchange_api_url = 'https://api.exchangerate-api.com/v4/latest/USD'

# Обработчик команды /start
@bot.message_handler(commands=['start',])
def handle_start(message):
    bot.send_message(message.chat.id, f"Привет! Я бот для конвертации валют.\n\n "
                                      f"Для конвертации используйте команду /convert <валюта из которой переводим> <валюта в которую переводим> <количество валюты>\n"
                                      f" например: /convert USD RUB 13\n\n"
                                      f"Больше команд ты найдёшь в /help"
                                      f"\n\nПока что это всё!")

# Обработчик команды для конвертации валюты
@bot.message_handler(commands=['convert'])
def handle_convert(message):
    try:
        # Разбиваем сообщение на части
        parts = message.text.split()

        # Проверяем, что введено правильное количество параметров
        if len(parts) != 4:
            bot.send_message(message.chat.id, f"Неверное количество параметров. \nИспользуйте: /convert <валюта_1> <валюта_2> <количество>\n"
                                              f"например: /convert USD RUB 13")
            return

        # Извлекаем параметры
        base = parts[1].upper()
        quote = parts[2].upper()
        amount = float(parts[3])

        # Получаем курсы валют
        response = requests.get(exchange_api_url)
        data = response.json()
        rates = data['rates']

        # Проверяем, что валюты существуют в списке
        if base not in rates or quote not in rates:
            bot.send_message(message.chat.id, f"Неверные коды валют. \n"
                                              f"Пожалуйста, используйте обозначения USD, EUR, RUB и т.д.")
            return

        # Выполняем конвертацию
        result = amount * rates[quote] / rates[base]

        # Отправляем результат
        bot.send_message(message.chat.id, f"{amount} {base} в {quote} это: {result:.2f} единиц.")
        # Прописываем исключение для ошибок чисто на всякий случай
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    bot.send_message(message.chat.id, f"Я конечно это оценить не могу, но думаю там что-то хорошее! \nА теперь пропиши /start")
    pass

@bot.message_handler(commands=['hi'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}! \n\nНайдёшь ошибки в моей работе - пиши моему создателю https://vk.com/rustikmistik\n"
                                      f"Чтобы поделиться мной -  t.me/rub_usd_eur_bot")
    pass

@bot.message_handler(commands=['help',])
def handle_start(message):
    bot.send_message(message.chat.id, f"Список команд помимо основного функционала:\n"
                                      f"/hi (приветствие тебя по имени в телеграме)\n"
                                      f"/start (инфо о том, как проводить конвертацию)\n"
                                      f"/values (какие валюты можно сконвертировать)\n"
                                      f"Также ты можешь отправить мне фото с мемом, и я его оценю)"
                     )
@bot.message_handler(commands=['values',])
def codes(message):
    bot.send_message(message.chat.id, f"Все коды валюты различных стран ты можешь найти тут:\n"
                                      f"https://www.iban.ru/currency-codes"
                     )

@bot.message_handler(content_types=['photo'])
def meme(message: telebot.types.Message):
    bot.reply_to(message, f"Найс мем, ору в голосину XD")
    pass

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)