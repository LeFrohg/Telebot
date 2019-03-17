#coding=utf-8

import time
import numbers
import subprocess
import json
import pigpio

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler)
from wifi import Cell
from wireless import Wireless

################################################################

TOKEN = 'INSERT_THE_BOT_TOKEN'
ID = INSERT_USER_ID

################################################################

pi = pigpio.pi()

pi.set_mode(2, pigpio.OUTPUT)

def convert(angle):
	return 530 + (9.4 * angle)

with open(r'/*edite_la_ruta*/conf.json') as file:
	data = json.load(file)
	pi.set_servo_pulsewidth(2, convert(data['default']))

################################################################

data = {}
print("Bot online!")

################################################################

def start(bot, update):
	if update.message.chat_id == ID:
		update.message.reply_text("Este es un bot que permite controlar un dispensador de comida para peces")

def set(bot, update, args):
	if update.message.chat_id == ID:
		if len(args) == 2:
			sub = args[0]
			dato = args[1]

			with open(r'/*edite_la_ruta*/conf.json') as file:
				data = json.load(file)
				if sub == "angle":
					data['angle'] = int(dato)
					update.message.reply_text("Se modificó el valor del ángulo a: {}".format(data['angle']))
				elif sub == "time":
					data['time'] = int(dato)
					update.message.reply_text("Se modificó el valor del tiempo a: {}".format(data['time']))
				elif sub == "default":
					data['default'] = int(dato)
					update.message.reply_text("Se modificó el valor de default a: {}".format(data['default']))		
				with open(r'/*edite_la_ruta*/conf.json', 'w') as f:
					json.dump(data, f)
		elif len(args) == 1:
			if args[0] == "info":
				with open(r'/*edite_la_ruta*/conf.json', 'r') as file:
					data = json.load(file)
					update.message.reply_text("Ángulo de apertura: {}".format(data['angle']))
					update.message.reply_text("Tiempo en segundos: {}".format(data['time']))
					update.message.reply_text("Ángulo por defecto: {}".format(data['default']))
			else:
				update.message.reply_text("Error, argumento desconocido.")
		else:
			update.message.reply_text("El comando espera al menos 1 argumentos: ")
			update.message.reply_text("angle - Define el ángulo de apertura [0-180]")
			update.message.reply_text("time - Define el tiempo de espera antes de regresar a la posición inicial")
			update.message.reply_text("default - Define el ángulo inicial. Por defecto es 0")
			update.message.reply_text("info - Muestra los valores guardados")

def vaciar(bot, update):
	if update.message.chat_id == ID:
		update.message.reply_text("Se ha iniciado el proceso de vaciado")
		with open(r'/*edite_la_ruta*/conf.json') as file:
			data = json.load(file)
			pi.set_servo_pulsewidth(2, convert(data['angle']))
			time.sleep(data['time'])
			pi.set_servo_pulsewidth(2, convert(data['default']))
		update.message.reply_text("El proceso de vaciado ha terminado")

def wifi(bot, update, args):
	if update.message.chat_id == ID:
		if len(args) == 1:
			if args[0] == "scan":
				update.message.reply_text("Encontré las siguientes redes:")
				update.message.reply_text("------------------------------")
				for cell in Cell.all('wlan0'):
					print cell.ssid
					update.message.reply_text(cell.ssid)
				update.message.reply_text("------------------------------")
		elif len(args) == 3:
			if args[0] == "add":
				wireless = Wireless()
				wireless.interface()
				if wireless.connect(ssid=args[1], password=args[2]) == True:
					update.message.reply_text("Red añadida con éxito")
				else:
					update.message.reply_text("Algo salió mal!")
#################################################################

def main():
	updater = Updater(TOKEN)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("vaciar", vaciar))
	dp.add_handler(CommandHandler("set", set, pass_args=True))
	dp.add_handler(CommandHandler("wifi", wifi, pass_args=True))


	updater.start_polling()

	updater.idle()

if __name__ == '__main__':
	main()
