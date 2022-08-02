import telebot
from extensions import APIException, Convertor
from config import TOKEN, currencies
import traceback
from telebot import types


bot = telebot.TeleBot(TOKEN)


conversion_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for var in currencies.keys():
    buttons.append(types.KeyboardButton(var.capitalize()))

conversion_markup.add(*buttons)


@bot.message_handler(commands=['start', 'help'])
def greeting(message: telebot.types.Message):
    text = "Я бот, который поможет Вам с конвертацией валюты!\n\
Все, что Вам понадобится, это написать в чате или кликнуть на команду: /convert\n \n" \
           "Но перед этим, советую Вам посмотреть список доступных валют. " \
           "Для этого Вам понадобится написать в чате или кликнуть на следующую команду:\n/values"
    bot.send_message(message.chat.id, f'Приветствую, {message.chat.first_name}! \n \n{text}')


@bot.message_handler(commands=['values'])
def show_values(message: telebot.types.Message):
    text = "Валюты, которые Вы можете использовать: \n"
    for i in currencies.keys():
        text = '\n'.join((text, i))
    example = "Чтобы провести конвертацию, напишите в чате, или кликните на команду: /convert"
    bot.send_message(message.chat.id, f'{text} \n\n{example}')


@bot.message_handler(commands=['convert'])
def show_choices(message: telebot.types.Message):
    text = "Выберите валюту, из которой Вы хотите конвертировать: "
    bot.send_message(message.chat.id, text, reply_markup=conversion_markup)
    bot.register_next_step_handler(message, base_value)


def base_value(message: telebot.types.Message):
    base = message.text.strip()
    text = "Выберите валюту, в которую Вы хотите конвертировать: "
    bot.send_message(message.chat.id, text, reply_markup=conversion_markup)
    bot.register_next_step_handler(message, quote_value, base)


def quote_value(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = "Введите количество конвертируемой валюты: "
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_value, base, quote)


def amount_value(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_value = Convertor.get_value(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f'Неизвестная ошибка: \n{e}')
    else:
        text = f'Стоимость {amount} {base} в {quote} составляет {new_value}.'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
