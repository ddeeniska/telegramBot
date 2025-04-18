import telebot

API_TOKEN = '7632838338:AAGOxyxPHj0KLz2qYuDl_PWZWRwpLSAYm9M'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])  # Обработка команды /start
def send_welcome(message):
    bot.reply_to(message, "Привет! Я ваш бот. Как я могу помочь вам?")

@bot.message_handler(commands=['help'])  # Обработка команды /help
def send_help(message):
    bot.reply_to(message, "Доступные команды:\n/start - Приветствие\n/help - Помощь")

@bot.message_handler(func=lambda message: True)  # Обработка текстовых сообщений
def echo_all(message):
    bot.reply_to(message, f"Вы сказали: {message.text}")

if __name__ == '__main__':  # Запуск бота
    bot.polling(none_stop=True)
