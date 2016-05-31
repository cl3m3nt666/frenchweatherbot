#!/usr/bin/env python
# encoding: utf-8


import telebot
import weather
import os
import requests

#EMOJI
SMILE = u'\U0001F609'
CRYINGFACE = u'\U0001F622'


API_TOKEN = ' API KEY '

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start'
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, """ Bonjour a toi !! :) Je suis un bot pour la météo francaise ! """ + SMILE)

# /help
@bot.message_handler(commands=['help'])
def help(m):
	cid = m.chat.id
	bot.send_message(cid, "*Bot Help Page*\n\n ", parse_mode="Markdown")

# /help
@bot.message_handler(commands=['parisnow'])
def help(m):
	cid = m.chat.id
	bot.send_message(cid,weather.currentWeather(weather.getJson("paris".replace (" ", "_"))), parse_mode="Markdown")

# Handle '/weather'
@bot.message_handler(commands=['weather'])
def send_weather(message):
    cid = message.chat.id
    msg = bot.reply_to(message, "Tu veux la meteo de quelle ville ? " + SMILE + SMILE )
    bot.register_next_step_handler(msg, weatherseach)

def weatherseach(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
    try:
        latlon = weather.getLatLon(weather.getJson(message.text));
        if latlon:
            bot.send_location(cid, latlon[0], latlon[1])
        bot.send_message(cid,weather.currentWeather(weather.getJson(message.text.replace(" ", "_"))))
    except Exception as e:
        bot.reply_to(message, CRYINGFACE + ' oooops je suis trop fatigue pour y arriver..' + str(e))

# Handle '/weather'
@bot.message_handler(commands=['forecast'])
def send_forecast(message):
    cid = message.chat.id
    msg = bot.reply_to(message, "Tu veux la meteo de quelle ville ? " + SMILE + SMILE )
    bot.register_next_step_handler(msg, forecastseach)

def forecastseach(message):
    cid = message.chat.id
    bot.send_chat_action(cid, 'typing')
    try:
        latlon = weather.getLatLon(weather.getJson(message.text));
        if latlon:
            bot.send_location(cid, latlon[0], latlon[1])
        bot.send_message(cid,weather.forecast(weather.getJson(message.text.replace(" ", "_"))))
    except Exception as e:
        bot.reply_to(message, CRYINGFACE + ' oooops je suis trop fatigue pour y arriver..' + str(e))

bot.polling()
