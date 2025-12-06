import telebot

from telebot import types


#Конструктор заказов
#class Order:
    #userID: str
    #order_number: int
    #cafe: str
    #bludos: list
    #time_order: int
    #order_type: str
    #kolvo_people: int

#Массив заказов
#orders_list = []

#Переменные для обработки текущего заказа.
#now_order_cafe = ''
#now_order_bludo = ''
#now_order_bludos = []
#now_time_order = 0
#now_type_order = ''
#now_userID = ''

#ставится первым
bot = telebot.TeleBot('8209280920:AAGvxhwAz0feOSS4ymee49lqvHR6xT_9fUw')
@bot.message_handler(commands=['start'])

def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1=types.InlineKeyboardButton('кафе1', callback_data='1')
    btn2=types.InlineKeyboardButton('кафе2', callback_data='2')
    btn3=types.InlineKeyboardButton('кафе3', callback_data='3')
    btn4=types.InlineKeyboardButton('кафе4', callback_data='4')
    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    IDc = message.chat.id
    print(IDc)
    bot.send_message(message.chat.id, f'Здравствуйте,{message.from_user.first_name},где будете заказывать ? \n ',reply_markup=markup)
    @bot.callback_query_handler(func=lambda callback: True)
    def callback_message(callback):
        if callback.data == '1':
            bot.send_message(IDc, f'Хорошо, выбрано кафе1')




bot.infinity_polling()
