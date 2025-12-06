import telebot
import pandas as pd
import time
import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot import types

tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))
#Создание протокола эксель для админа

#эти массивы будут в столбцах
ExZak=[] #номера заказа
ExIm=[]  #имена пользователей
ExKaf=[] #названия ресторанов
ExBl=[]  #блюда(сами заказы)
ExDos=[] #тип доставки
ExVr=[]  #время
ExCost=[]#аена
#это имена столбцов
df = pd.DataFrame({
    '№Заказа':[],
    'Имя':[],
    'Кафе':[],
    'Блюда':[],
    'Тип доставки':[],
    'Время':[],
    'Цена':[]
})
#это внесение значений в столбцы
df['№Заказа']=ExZak
df['Имя']=ExIm
df['Кафе']=ExKaf
df['Блюда']=ExBl
df['Тип доставки']=ExDos
df['Время']=ExVr
df['Цена']=ExCost
df.to_excel('report.xlsx', index=False)

#Вытаскивание позиций меню

#дефка для вывода перечня меню определенного типа
#def(название ресторана, тип позиции меню) имена как в таблице
def menu_1 (restname, columnname): #str
    tab = pd.read_excel('menu.xlsx', sheet_name=restname)
    stolb = tab[columnname].tolist()
    return stolb

#обозначения:t-перечисление товара, c-цены
'''
siz_sup_t=menu_1('сицилия','суп')[::2]
siz_sup_c=menu_1('сицилия','суп')[1::2]
siz_sal_t=menu_1('сицилия','салат')[::2]
siz_sal_c=menu_1('сицилия','салат')[1::2]
siz_osn_t=menu_1('сицилия','основное')[::2]
siz_osn_c=menu_1('сицилия','основное')[1::2]
osk_sup_t=menu_1('осака','суп')[::2]
osk_sup_c=menu_1('осака','суп')[1::2]
osk_pas_t=menu_1('осака','паста, лапша, рис')[::2]
osk_pas_c=menu_1('осака','паста, лапша, рис')[1::2]
osk_pok_t=menu_1('осака','поке, боулы')[::2]
osk_pok_c=menu_1('осака','поке, боулы')[1::2]
min_sus_t=menu_1('мята','суши, роллы')[::2]
min_sus_c=menu_1('мята','суши, роллы')[1::2]
min_piz_t=menu_1('мята','пиццы')[::2]
min_piz_c=menu_1('мята','пиццы')[1::2]
min_ssp_t=menu_1('мята','суши с пиццей')[::2]
min_ssp_c=menu_1('мята','суши с пиццей')[1::2]
min_lan_t=menu_1('мята','ланч')[::2]
min_lan_c=menu_1('мята','ланч')[1::2]
mib_lan_t=menu_1('мясник и бык','ланч')[::2]
mib_lan_c=menu_1('мясник и бык','ланч')[1::2]
#проверОчка

supbl=menu_1('','')[::2]
supcena=menu_1('','')[1::2]
print(supbl,supcena)
'''

check_f = open('User_check.txt', 'r')
user_check_string = check_f.readline()
check_f.closed





#Конструктор заказов
class Order:
    userID: str
    order_number: int
    cafe: str
    bludos: list
    time_order: int
    order_type: str
    kolvo_people: int

#Массив заказов
orders_list = []

#Переменные для обработки текущего заказа.
now_order_cafe = ''
now_order_bludo = ''
now_order_bludos = []
now_time_order = 0
now_type_order = ''
now_userID = ''

#ставится первым
bot = AsyncTeleBot('8209280920:AAGvxhwAz0feOSS4ymee49lqvHR6xT_9fUw')

@bot.message_handler(commands=['start'])
async def start_(message):
    #Логи. Юзернейм и АйДи чата
    IDc = message.chat.id
    if not (message.from_user.username in user_check_string):
        f = open('Logs.txt', 'a')
        f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/start' + f' Несакнционированная попытка доступа')
        f.write('\n')
        f.closed
        await bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}, к сожалению, вы не являетесь сотрудником компании Оджетто. \n В противном случае обратитесь к администратору, чтобы он занёс ваш юзернейм в Telegram в базу данных этого бота.')
    else:
        f = open('Logs.txt', 'a')
        f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/start')
        f.write('\n')
        f.closed
        await bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}, данный бот предназначен для заказа еды сотрудниками компании Оджетто.')

@bot.message_handler(commands=['make_order'])

async def main(message):
    if not (message.from_user.username in user_check_string):
        IDc = message.chat.id
        f = open('Logs.txt', 'a')
        f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/start' + f' Несакнционированная попытка доступа')
        f.write('\n')
        f.closed
        await bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}, к сожалению, вы не являетесь сотрудником компании Оджетто. \n В противном случае обратитесь к администратору, чтобы он занёс ваш юзернейм в Telegram в базу данных этого бота.')
    else:
        markup = types.InlineKeyboardMarkup()
        btn1=types.InlineKeyboardButton('"Сицилия"', callback_data='1')
        btn2=types.InlineKeyboardButton('"Мята food"', callback_data='2')
        btn3=types.InlineKeyboardButton('"Осака"', callback_data='3')
        btn4=types.InlineKeyboardButton('"Мясник и Бык"', callback_data='4')
        btn5=types.InlineKeyboardButton('Заказ онлайн', callback_data='5')
        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        IDc = message.chat.id
        f = open('Logs.txt', 'a')
        f.write(f' {str(IDc):15}' + ' ' + (f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/make_order'))
        f.write('\n')
        f.closed
        await bot.send_message(message.chat.id, f'{message.from_user.first_name}, \n Где будете заказывать ? \n Описания ресторанов: \n «Сицилия» — пиццерия в Таганроге, где подают блюда европейской, итальянской и японской кухни. \n Адрес: ул. Петровская, 67а. \n Телефон: +7 (800) 737-77-78. \n Режим работы: пн.-вс.: 09:00–24:00. \n Служба доставки: пн.-вс.: 9:00–23:00. \n В меню: пицца, суши и роллы, горячие блюда и супы. \n Особенности: есть терраса, детская комната, бизнес-ланч, заказ еды с доставкой. \n По отзывам посетителей, в 2024 году у пиццерии был высокий рейтинг (5,0) на «Яндекс Картах». \n\n«Мята Food» — кафе в Таганроге, где подают блюда европейской, итальянской, тайской и японской кухни. \n Адрес: улица Чехова, 63. \n Телефон: +7 952 410-05-25. \n Режим работы: пн-сб: 11:00–24:00; вс: 11:00–02:00. \n Некоторые блюда: пицца, сэндвичи, бургеры, суши, сашими, японская лапша. \n По отзывам посетителей, у заведения есть как положительные,  так и отрицательные оценки. (Рейтинг 4.8 на Яндекс.Картах) \n \n «Осака» — суши-бар в Таганроге. \n Адрес: ул. Петровская, 84, 1-й этаж. \n Телефон: +7 (8634) 34-36-90. \nОсобенности: \n Живая музыка \n Банкетный зал \n Летняя веранда \n Wi-Fi. \n В меню — суши и роллы, пицца, блюда европейской, итальянской, паназиатской, японской и восточной кухни. \n Суши-бар «Осака» работает ежедневно с 11:00 до 24:00. \n В заведении есть собственная курьерская служба. Можно заказать суши на дом или в офис. \n Телефон доставки: +7 (8634) 36-73-02. \n Бесплатная доставка: при заказе от 800 рублей. \n Рейтинг: 4,8 на Яндекс Картах. \n\n«Мясник и Бык» — ресторан в Таганроге, предлагающий блюда европейской и итальянской кухни. \n Адрес: ул. Петровская, 68а. \n Телефон: +7 (8634) 47-74-54. \n График работы: ежедневно с 11:00 до 24:00. \n В основе меню — мясные блюда: стейки из различных видов мяса, приготовленные на гриле или в смокере, бургеры, мясные закуски. Помимо мясных блюд, в меню представлены салаты, супы и гарниры, а также десерты.',reply_markup=markup)


        #Ответ на выбор ресторана
        @bot.callback_query_handler(func=lambda callback: True)
        async def callback_message(callback):
            if callback.data == '1':
                await bot.send_message(callback.message.chat.id, 'Хорошо, выбран ресторан "Сицилия". \n Вот его меню: ')
                await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            if callback.data == '2':
                await bot.send_message(callback.message.chat.id, 'Хорошо, выбрано кафе "Мята food". \n Вот его меню: ')
                await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            if callback.data == '3':
                await bot.send_message(callback.message.chat.id, 'Хорошо, выбран суши-бар "Осака". \n Вот его меню: ')
                await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            if callback.data == '4':
                await bot.send_message(callback.message.chat.id, 'Хорошо, выбран ресторан "Мясник и Бык". \n Вот его меню: ')
                await bot.delete_message(callback.message.chat.id, callback.message.message_id)
            if callback.data == '5':
                markup1 = types.InlineKeyboardMarkup()
                btn11=types.InlineKeyboardButton('Сайт пиццерии "Сицилия"', url='https://taganrog.pizza-sicilia.ru/')
                btn21=types.InlineKeyboardButton('Сайт кафе "Мята food"', url='https://myata-food.ru/')
                btn31=types.InlineKeyboardButton('Сайт ресторана "Мясник и Бык"', url='https://butcher-bull.ru/call-online')
                btn41=types.InlineKeyboardButton('Сайт суши-бара "Осака"', url='https://taganrog.sushiosaka.ru/')
                btn51=types.InlineKeyboardButton('Сервис доставки "Яндекс.Еда"', url='https://eda.yandex.ru/?utm_medium=cpc&utm_source=yasearch&utm_campaign=704307793.%5BEDA%5DMX_Srv_Rf_Brand_Search&utm_content=17367627184&utm_term=---autotargeting%7Cpid%7C205669267523%7Caid%7C17367627184%7Ctype1%7Cdesktop%7Cnone%7Csearch&etext=2202.SwNyd8UDzVL_4Iu0wosiW6QcB5M86ERF-tqS1_xzBYZsZ3NpZmxqaXZsbHRndXJo.792dff1d173b359ec7b5c39983c82a4f01c1c470&yclid=7440376692682522623&ybaip=1')
                markup1.row(btn11, btn21)
                markup1.row(btn31, btn41)
                markup1.row(btn51)
                await bot.send_message(callback.message.chat.id, f'Хорошо, вы выбрали онлайн заказ. \nВам предложены сайты указанных ранее ресторанов, а также сервис доставки "Яндекс.Еда"', reply_markup=markup1)
                await bot.delete_message(callback.message.chat.id, callback.message.message_id)
#Отправка таблицы эксель ботом
@bot.message_handler(commands=['report'])
async def send_excel(message):
    IDc = message.chat.id
    f = open('Logs.txt', 'a')
    f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/report')
    f.write('\n')
    f.closed
    with open('report.xlsx', 'rb') as file:
        await bot.send_document(
            chat_id=message.chat.id,
            document=file,
            caption='Вот ваш Excel файл с отчетом'
        )
    await bot.reply_to(message, "Файл успешно отправлен!")

    #Отправка логов бота админу
@bot.message_handler(commands=['logs'])
async def send_logs(message):
    IDc = message.chat.id
    f = open('Logs.txt', 'a')
    f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/logs')
    f.write('\n')
    f.closed
    with open('Logs.txt', 'rb') as fi:
        await bot.send_document(
            chat_id=message.chat.id,
            document=fi,
            caption='Вот ваш файл с логами'
        )
    await bot.reply_to(message, "Файл успешно отправлен!")
 #Добавление пользователей админом
@bot.message_handler(commands=['add_user'])
async def add_user(message):
    IDc = message.chat.id
    f = open('Logs.txt', 'a')
    f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/add_user')
    f.write('\n')
    f.closed
    await bot.send_message(message.chat.id, f'Здравствуйте, админ {message.from_user.first_name}, добавьте юзернейм сотрудника, который вам нужен. \n ВАЖНОЕ ПРИМЕЧАНИЕ: \n Юзернейм должен быть БЕЗ символа @ и "t.me:\\". \n Иначе бот неверно распознает пользователя, а вы же этого не хотите.')
    @bot.message_handler(content_types=['text'])
    async def write_user(message1):
        check_f = open('User_check.txt', 'a')
        check_f.write(message1.text)
        check_f.closed
        await bot.reply_to(message1, "Сотрудник комании Оджетто успешно внесён в список!")
asyncio.run(bot.polling())
