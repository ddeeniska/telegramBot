import telebot
import random
import telegram
from telebot import types

API_TOKEN = '7632838338:AAGOxyxPHj0KLz2qYuDl_PWZWRwpLSAYm9M'
bot = telebot.TeleBot(API_TOKEN)

flag_question = False
flag_equation = False


@bot.message_handler(commands=['start'])  # Обработка команды /start
def send_welcome(message):
    bot.send_message(message.chat.id,
                 "Я бот-справочник. Какая информация вам нужна?", )


@bot.message_handler(commands=['help'])  # Обработка команды /help
def send_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start - Приветствие\n/help - "
                          "Помощь\n/question <ваш_вопрос> - Задайте мне вопрос, и я отвечу на него.")


@bot.message_handler(commands=['question'])  # Обработка команды /question
def ask_question(message):  # Извлекаем текст вопроса после команды
    global flag_question
    flag_question = True
    bot.send_message(message.chat.id, "Чем вам помочь? (квадратное уравнение)")


@bot.message_handler(func=lambda message: True if flag_question else False)  # Обработка текстовых сообщений
def what_question(message):
    global flag_question, flag_equation
    if message.text == 'квадратное уравнение':
        bot.send_message(message.chat.id, "Напишите через пробел a, b, c")
        flag_equation = True
    else:
        bot.send_message(message.chat.id, f"Вы спросили: {message.text}")
    flag_question = False


@bot.message_handler(func=lambda message: True if flag_equation else False)
def solve_equation(message):
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


if __name__ == '__main__':  # Запуск бота
    bot.polling(none_stop=True)
