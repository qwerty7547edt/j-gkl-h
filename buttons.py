from telebot import types


b1 = '🦋 Модели'
b2 = '🏦 Кошелек'
b0 = '👩‍💻 Техническая поддержка'
b3 = '🎁 Промокод'
b19 = '📒 Информация'

b4 = 'Изменить киви🥝'
b5 = 'Статистика📊'
b6 = 'Рассылка📨'
b9 = '➕ Добавить анкету'
b22 = '📸Добавить фото'
b10 = '✖️Удалить анкету'
b7 = '❌Закрыть'

b8 = 'Реф ссылка📎'
b11 = '❌Закрыть'

b12 = '📈 Пополнить Баланс'
b112 = '📉 Вывести Баланс'
b13 = '🏠 Главное меню📍'

b14 = '🔥 Заказать'
b16 = '⏪Предыдущая'
b17 = 'Следующая⏩'
b18 = 'Создать Промокод🔑'

b20 = '❌Отмена'


def bal():
    markup = types.ReplyKeyboardMarkup(True)
    key1 = types.KeyboardButton(b12)
    key3 = types.KeyboardButton(b112)
    key2 = types.KeyboardButton(b20)
    markup.add(key1, key3)
    markup.add(key2)
    return markup


def empty():
    markup = types.ReplyKeyboardMarkup(True)
    return markup


def cancel():
    markup = types.ReplyKeyboardMarkup(True)
    key1 = types.KeyboardButton(b20)
    markup.add(key1)
    return markup


def otzivi():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Сайт Хабр", url='https://habr.com/ru/all/')
    markup.add(button1)
    return markup


def userpanel():
    markup = types.ReplyKeyboardMarkup(True)
    key1 = types.KeyboardButton(b1)
    key2 = types.KeyboardButton(b2)
    key3 = types.KeyboardButton(b0)
    key4 = types.KeyboardButton(b3)
    key5 = types.KeyboardButton(b19)

    markup.add(key1)
    markup.add(key2, key5, key4)
    markup.add(key3)

    return markup


def menu():
    markup = types.ReplyKeyboardMarkup(True)
    key1 = types.KeyboardButton(b11)

    markup.add(key1)

    return markup
