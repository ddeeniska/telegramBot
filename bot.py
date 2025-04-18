import telebot
import random
import telegram
from telebot import types

API_TOKEN = '7632838338:AAGOxyxPHj0KLz2qYuDl_PWZWRwpLSAYm9M'
bot = telebot.TeleBot(API_TOKEN)

flag_equation, flag_circle_s, flag_circle_p, flag_katet = False, False, False, False
flag_gipot = False


@bot.message_handler(commands=['start'])  # Обработка команды /start
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.add('Математика', 'Вопрос')
    bot.send_message(message.chat.id, "Привет! Я бот, который помогает с разными задачами.", reply_markup=keyboard)


@bot.message_handler(commands=['help'])  # Обработка команды /help
def send_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start - Приветствие\n/help - "
                                      "Помощь")


@bot.message_handler(content_types=['text'])  # Обработка команды /question
def ask_question(message):  # Извлекаем текст вопроса после команды
    global flag_equation, flag_circle_s, flag_circle_p, flag_circle_s, flag_katet, flag_gipot
    if message.text == 'Математика':
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Квадратное уравнение', 'Т. Пифагора')
        keyboard.row('Длина окружности', 'Площадь круга')
        bot.send_message(message.chat.id, "Чем вам помочь?", reply_markup=keyboard)
    elif message.text == 'Т. Пифагора':
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.add('Катет', 'Гипотенуза')
        bot.send_message(message.chat.id, "Какая сторона неизвестна?", reply_markup=keyboard)
    elif message.text == 'Катет':
        bot.send_message(message.chat.id, "Напишите гипотенузу и катет")
        flag_katet = True
    elif message.text == 'Гипотенуза':
        bot.send_message(message.chat.id, "Напишите длину катетов через пробел")
        flag_gipot = True
    elif message.text == 'Квадратное уравнение':
        bot.send_message(message.chat.id, "Напишите через пробел a, b, c")
        flag_equation = True
    elif message.text == 'Длина окружности':
        bot.send_message(message.chat.id, "Введите радиус")
        flag_circle_p = True
    elif message.text == 'Площадь круга':
        bot.send_message(message.chat.id, "Введите радиус")
        flag_circle_s = True
    elif flag_gipot:
        a, b = map(float, message.text.split())
        c = (a * a + b * b) ** 0.5
        c = int(c) if c % 1 == 0 else c
        if c == 0 or a == 0 or b == 0:
            bot.send_message(message.chat.id, 'Ошибка')
        else:
            bot.send_message(message.chat.id, str(c))
        flag_gipot = False
    elif flag_katet:
        nums = list(map(float, message.text.split()))
        g = max(nums)
        k = min(nums)
        c = (g * g - k * k) ** 0.5
        c = int(c) if c % 1 == 0 else c
        if c == 0 or g == 0 or k == 0:
            bot.send_message(message.chat.id, 'Ошибка')
        else:
            bot.send_message(message.chat.id, str(c))
        flag_katet = False
    elif flag_equation:
        a, b, c = map(float, message.text.split())
        D = b ** 2 - 4 * a * c
        if D > 0:
            x1 = (-b - D ** 0.5) / 2 * a
            x1 = int(x1) if x1 % 1 == 0 else x1
            x2 = (-b + D ** 0.5) / 2 * a
            x2 = int(x2) if x2 % 1 == 0 else x2
            bot.send_message(message.chat.id, f"x1 = {x1}\nx2 = {x2}")
        elif D == 0:
            bot.send_message(message.chat.id, f"x = 0")
        else:
            bot.send_message(message.chat.id, f"Нет решений")
        flag_equation = False
    elif flag_circle_s:
        r = float(message.text)
        bot.send_message(message.chat.id, str(3.14 * r * r))
        flag_circle_s = False
    elif flag_circle_p:
        r = float(message.text)
        bot.send_message(message.chat.id, str(3.14 * 2 * r))
        flag_circle_p = False
    else:
        bot.send_message(message.chat.id, 'Не понимаю')


if __name__ == '__main__':  # Запуск бота
    bot.polling(none_stop=True)
