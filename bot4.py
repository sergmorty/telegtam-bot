#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:40:32 2022

@author: sergio
"""

import os
import telebot
from datetime import datetime
from dotenv import load_dotenv

import rpn

def load_env():
    dotenv_path = os.path.join(os.path.dirname(__file__),'.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

load_env()

bot = telebot.TeleBot(os.environ['TOKEN'])

@bot.message_handler(commands = ['start'])
def start(message):
    kb = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    square = telebot.types.KeyboardButton(text = 'Решить квадратное уравнение')
    expr = telebot.types.KeyboardButton(text = 'Решить арифметическое выражение')
    kb.add(expr, square)
    bot.send_message(message.chat.id, 'Привет, что тебя интересут?', reply_markup=kb)

@bot.message_handler(func = lambda x: x.text == 'Решить квадратное уравнение')
def reply(message):
    sent = bot.reply_to(message, 'Введите коеффициенты ax^2 + bx + c в виде: a b c, например: -1 2 3')
    bot.register_next_step_handler(sent, square)

@bot.message_handler(func = lambda x: x.text == 'Решить арифметическое выражение')
def reply(message):
    sent = bot.reply_to(message, 'Введите арифметическое выражение, например: 5!^2/4+3')
    bot.register_next_step_handler(sent, expr)


def expr(message):
    text = ''
    try:
        r = rpn.RPN(message.text)
        text = str(r.calc())
    except IndexError:
        text = 'Неверное выражение'
    kb = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    square = telebot.types.KeyboardButton(text = 'Решить квадратное уравнение')
    expr = telebot.types.KeyboardButton(text = 'Решить арифметическое выражение')
    kb.add(expr, square)

    bot.send_message(message.chat.id, text, reply_markup=kb)
    
def square(message):
    try:
        lst = [int(i) for i in message.text.split()]
        if len(lst) != 3:
            raise ValueError()
    except ValueError:
        bot.send_message(message.chat.id, 'Коеффициенты должны быть числовыми и их должно быть 3')
        return
    d = lst[1]*lst[1] - 4*lst[0]*lst[2]
    if d < 0:
        bot.send_message(message.chat.id, 'Дискриминант меньше 0. Корней нет.')
    else:
        sq = d ** 0.5
        x1 = (-lst[1] - sq) / (2*lst[0])
        x2 = (-lst[1] + sq) / (2*lst[0])
        bot.send_message(message.chat.id, f'Дискриминант {d}. Корни: {x1}; {x2}.')
        
bot.polling()