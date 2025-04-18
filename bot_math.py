import telebot
import random
from telebot import types
from datetime import datetime
import math

API_TOKEN = '7632838338:AAGdVCJTTStc6Ov6FrLGZBYdNu2EjpZc-aQ'
bot = telebot.TeleBot(API_TOKEN)
user_states = {}

def log_user_request(user_id, message):
    """Функция для записи запроса пользователя в файл."""
    with open('user_requests.log', 'a', encoding='utf-8') as f:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f"{timestamp} - User ID: {user_id}, Message: {message}\n")

def calculate_hypotenuse(a, b):
    return (a ** 2 + b ** 2) ** 0.5


def calculate_cathetus(hypotenuse, cathetus):
    return (hypotenuse ** 2 - cathetus ** 2) ** 0.5


def calculate_quadratic(a, b, c):
    D = b ** 2 - 4 * a * c
    if D > 0:
        x1 = (-b - D ** 0.5) / (2 * a)
        x2 = (-b + D ** 0.5) / (2 * a)
        return f"x1 = {x1}\nx2 = {x2}"
    elif D == 0:
        x = -b / (2 * a)
        return f"x = {x}"
    else:
        return "Нет решений"

def calculate_cosine_theorem(a, b, c=None, angle=None):
    if angle is not None:
        # Находим косинус угла
        cos_angle = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        return math.acos(cos_angle) * (180 / math.pi)  # возвращаем угол в градусах
    elif c is not None:
        # Находим третью сторону
        return (a ** 2 + b ** 2 - 2 * a * b * math.cos(math.radians(c))) ** 0.5
    else:
        return "Ошибка: необходимо указать либо угол, либо третью сторону."


def calculate_triangle_area(a, b, c):
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    return area

def calculate_polygon_area(n, side_length):
    area = (n * side_length ** 2) / (4 * math.tan(math.pi / n))
    return area

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(True, False)
    keyboard.add('Математика', 'Вопрос')
    bot.send_message(message.chat.id, "Привет! Я бот, который помогает с разными задачами.", reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n/start - Приветствие и кнопки действий\n/help - Помощь")
    bot.send_message(message.chat.id, "Вы можете написать 'вопрос' и задать интересующий вас вопрос, на который "
                                      "я постараюсь ответить")

@bot.message_handler(content_types=['text'])
def ask_question(message):
    user_id = message.chat.id
    # Логируем запрос пользователя
    log_user_request(user_id, message.text)
    # Инициализируем состояние пользователя, если его нет
    if user_id not in user_states:
        user_states[user_id] = {}
    state = user_states[user_id]
    if message.text == 'Математика':
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Квадратное уравнение', 'Т. Пифагора')
        keyboard.row('Длина окружности', 'Площадь круга')
        keyboard.row('Теорема косинусов', 'Площадь треугольника')
        keyboard.row('Площадь многоугольника', 'Назад')
        bot.send_message(message.chat.id, "Чем вам помочь?", reply_markup=keyboard)

    elif message.text == 'Назад':
        send_welcome(message)

    elif message.text == 'Вопрос' or message.text == 'вопрос':
        bot.send_message(message.chat.id, "Задайте ваш вопрос, на который можно ответить да или нет")
        state['waiting_for'] = 'user_question'

    elif message.text == 'Т. Пифагора':
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.add('Катет', 'Гипотенуза')
        bot.send_message(message.chat.id, "Какая сторона неизвестна?", reply_markup=keyboard)

    elif message.text == 'Катет':
        bot.send_message(message.chat.id, "Напишите гипотенузу и катет через пробел")
        state['waiting_for'] = 'katet'

    elif message.text == 'Гипотенуза':
        bot.send_message(message.chat.id, "Напишите длину катетов через пробел")
        state['waiting_for'] = 'hypotenuse'

    elif message.text == 'Квадратное уравнение':
        bot.send_message(message.chat.id, "Напишите через пробел a, b, c")
        state['waiting_for'] = 'quadratic'

    elif message.text == 'Длина окружности':
        bot.send_message(message.chat.id, "Введите радиус")
        state['waiting_for'] = 'circle_perimeter'

    elif message.text == 'Площадь круга':
        bot.send_message(message.chat.id, "Введите радиус")
        state['waiting_for'] = 'circle_area'

    elif message.text == 'Теорема косинусов':
        keyboard = types.ReplyKeyboardMarkup(True, True)
        keyboard.row('Найти сторону', 'Найти угол')
        keyboard.row('Назад')
        bot.send_message(message.chat.id, "Что вы хотите найти?", reply_markup=keyboard)
        state['waiting_for'] = 'cosine_choice'

    elif message.text == 'Площадь треугольника':
        bot.send_message(message.chat.id, "Введите длины сторон треугольника через пробел, например: 3 4 5")
        state['waiting_for'] = 'triangle_area'

    elif message.text == 'Площадь многоугольника':
        bot.send_message(message.chat.id, "Введите количество сторон и длину стороны через пробел (например: 5 6):")
        state['waiting_for'] = 'polygon_area'

    elif 'waiting_for' in state:
        try:
            if state['waiting_for'] == 'hypotenuse':
                try:
                    a, b = map(float, message.text.split())
                    result = calculate_hypotenuse(a, b)
                    bot.send_message(message.chat.id, str(result))
                except Exception:
                    bot.send_message(message.chat.id, 'Неверные числа')
                del state['waiting_for']

            elif state['waiting_for'] == 'katet':
                hypotenuse, cathetus = map(float, message.text.split())
                result = calculate_cathetus(hypotenuse, cathetus)
                bot.send_message(message.chat.id, str(result))
                del state['waiting_for']

            elif state['waiting_for'] == 'quadratic':
                a, b, c = map(float, message.text.split())
                result = calculate_quadratic(a, b, c)
                bot.send_message(message.chat.id, result)
                del state['waiting_for']

            elif state['waiting_for'] in ['circle_area', 'circle_perimeter']:
                r = float(message.text)
                if state['waiting_for'] == 'circle_area':
                    result = 3.14 * r ** 2
                else:
                    result = 3.14 * 2 * r
                bot.send_message(message.chat.id, str(result))
                del state['waiting_for']

            elif state['waiting_for'] == 'cosine_choice':
                if message.text == 'Найти сторону':
                    bot.send_message(message.chat.id, "Введите стороны a и b и угол между ними (в градусах):")
                    state['waiting_for'] = 'cosine_side'
                elif message.text == 'Найти угол':
                    bot.send_message(message.chat.id, "Введите стороны a и b и третью сторону c (противолежащую углу):")
                    state['waiting_for'] = 'cosine_angle'

            elif state['waiting_for'] == 'polygon_area':
                n, side_length = map(int, message.text.split())
                result = calculate_polygon_area(n, side_length)
                bot.send_message(message.chat.id, str(result))
                del state['waiting_for']

            elif state['waiting_for'] == 'triangle_area':
                a, b, c = map(float, message.text.split())
                result = calculate_triangle_area(a, b, c)
                bot.send_message(message.chat.id, str(result))
                del state['waiting_for']

            elif state['waiting_for'] == 'cosine_side':
                a, b, angle = map(float, message.text.split())
                result = calculate_cosine_theorem(a, b, angle=angle)
                bot.send_message(message.chat.id, str(result))
                del state['waiting_for']

            elif state['waiting_for'] == 'cosine_angle':
                a, b, c = map(float, message.text.split())
                result = calculate_cosine_theorem(a, b, c=c)
                bot.send_message(message.chat.id, str(result))
                del state['waiting_for']

            elif state['waiting_for'] == 'user_question':
                answers = ['да', 'нет', 'наверное', 'возможно', 'точно нет', 'точно да', 'гойда']
                response = random.choice(answers)
                bot.send_message(message.chat.id, response)
                del state['waiting_for']

        except ValueError:
            bot.send_message(message.chat.id, "Ошибка: неверный ввод. Пожалуйста, попробуйте еще раз.")
    else:
        bot.send_message(message.chat.id, 'Не понимаю')


if __name__ == '__main__':
    bot.polling(none_stop=True)


