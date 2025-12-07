import telebot
import pandas as pd
import time
import asyncio
import random
from telebot.async_telebot import AsyncTeleBot
from telebot import types
current_time=time.time()
local_time=time.localtime(current_time)
#Обьявление проверки на админа
admin_status = False
ad_f = open('admins.txt', 'r')
admin_password = ad_f.readline().replace('\n', '')

tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))
#Создание протокола эксель для админа

#эти массивы будут в столбцах
ExZak=[] #номера заказа
ExIm=[]  #имена пользователей
ExKaf=[] #названия ресторанов
ExBl= []  #блюда(сами заказы)
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



check_f = open('User_check.txt', 'r')
user_check_string = check_f.readline()
check_f.closed
now_excel_str = 0
now_excel_stolb = 'A'

        
#Конструктор заказоd
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

@bot.message_handler(commands=['admin_reg'])
async def admin_r(message):
    IDc = message.chat.id
    f = open('Logs.txt', 'a')
    f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/admin_reg')
    f.write('\n')
    f.closed
    await bot.send_message(message.chat.id, 'Введите ключ админа.')
    @bot.message_handler(content_types=['text'])
    async def admin_pass(message11):
        if message11.text == admin_password:
            await bot.send_message(message.chat.id, 'Ваш статус админа успешно подтверждён')
            global admin_status
            admin_status = True

@bot.message_handler(commands=['start'])
async def start_(message):
    #Логи. Юзернейм и АйДи чата
    IDc = message.chat.id
    if not(message.from_user.username in user_check_string):
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
    if local_time.tm_hour>=12:
        bot.stop_polling #когда у вас дедлайн,заносите время дедлайна в if
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
            global now_order_cafe, now_order_bludos, now_userID
            userID = random.randint(0, 40000)
            print(now_userID)
            # Выбор ресторана
            if callback.data == '1':
                now_order_cafe = 'Сицилия'
                await bot.send_message(
                chat_id=callback.message.chat.id,
                text=f'Хорошо, выбран ресторан "Сицилия". \nВот его меню: \n\nСУПЫ:\n1. Домашняя лапша — 390 руб.\n2. Пряный тори — 420 руб.\n3. Крем-суп из шампиньонов — 350 руб.\n4. Борщ с курицей — 380 руб.\n\nСАЛАТЫ:\n5. Винегрет — 280 руб.\n6. Азиатский с цыпленком — 450 руб.\n7. Салат с курицей — 420 руб.\n\nОСНОВНЫЕ БЛЮДА:\n8. Карбонара паста — 520 руб.\n9. Шницель с рисом — 480 руб.\n10. Котлета с пюре — 450 руб.\n\nВыберите код нужного вам блюда (от 1 до 10). Для добавления ещё одного блюда напишите "+", для завершения "f".',
                )
                
                @bot.message_handler(content_types=['text'])
                async def sicilia_handler(message1):
                    if message1.chat.id == callback.message.chat.id:
                        if message1.text == '1':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбрана домашняя лапша. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Домашняя лапша')
                        elif message1.text == '2':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбран пряный тори. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Пряный тори')
                        elif message1.text == '3':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбран суп из шампиньонов. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Суп из шампиньонов')
                        elif message1.text == '4':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбран борщ с курицей. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Борщ с курицей')
                        elif message1.text == '5':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбран винегрет. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Винегрет')
                        elif message1.text == '6':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбран азиатский с цыпленком. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Азиатский с цыпленком')
                        elif message1.text == '7':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбран салат с курицей. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Салат с курицей')
                        elif message1.text == '8':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбрана карбонара паста. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Карбонара паста')
                        elif message1.text == '9':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбран шницель с рисом. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Шницель с рисом')
                        elif message1.text == '10':
                            await bot.send_message(message1.chat.id, 'Хорошо, выбрана котлета с пюре. Если хотите выбрать что-то ещё, напишите "+". Если надо завершить заказ, напишите "f"')
                            now_order_bludos.append('Котлета с пюре')
                        elif message1.text == '+':
                            await bot.send_message(message1.chat.id, 'Отлично! Напишите код следующего блюда из меню "Сицилия":\n\n1. Домашняя лапша\n2. Пряный тори\n3. Крем-суп из шампиньонов\n4. Борщ с курицей\n5. Винегрет\n6. Азиатский с цыпленком\n7. Салат с курицей\n8. Карбонара паста\n9. Шницель с рисом\n10. Котлета с пюре')
                        elif message1.text == 'f':
                            await bot.send_message(callback.message.chat.id, f'Заказ в ресторан "Сицилия" сделан! Ваш заказ: {", ".join(now_order_bludos)}. Спасибо за использование!')
                        else:
                            await bot.send_message(message1.chat.id, 'Пожалуйста, введите код блюда от 1 до 10, "+" для добавления или "f" для завершения')
    
            elif callback.data == '2':
                now_order_cafe = 'Мята food'
                await bot.send_message(
                chat_id=callback.message.chat.id,
                text=f'Хорошо, выбран ресторан "Мята food". \nВыберите блюдо: \n\n Суши, роллы\n·1 Два ролла чикен фреш 8шт – Роллы со свежей курицей.\n·2 Два ролла запеченный чикен 8шт – Запеченные роллы с курицей.\n·3 Два ролла сяки грин 8шт – Роллы с лососем и авокадо.\n·4 Два рола оши хот 8шт – Острые запеченные роллы.\n\nПиццы\n·5 Комбо дуэт пепперони 25см сырная 25см – Две пиццы: пепперони и сырная.\n·6 Комбо три цыпленка – Комбо с тремя куриными пиццами.\n\nСуши с пиццей (комбо)\n·7 Комбо лайт пепперони 25см , кани грин 8шт – Пицца пепперони и роллы с крабом.\n·8 Комбо ужин барбекю 25см токио макси 10шт – Пицца барбекю и большие роллы.\n\nЛанч\n·9 Ланч 1 суп лапша , сэндвич с ветчиной – Суп с лапшой и сэндвич. \n·10Ланч 2 бульон с сухариками сэндвичь с ветчиной – Бульон и сэндвич.\n·11 Ланч 3 паста карбонара , сэндвич с курицей – Паста карбонара и сэндвич.\n·12 Ланч 4 паста болоньзе сэндвичь с курицей – Паста болоньезе и сэндвич.',
                )
        
                @bot.message_handler(content_types=['text'])
                async def myata_handler(message1):
                    if message1.chat.id == callback.message.chat.id:
                        if message1.text == '1':
                            await bot.send_message(message1.chat.id, 'Выбрано два ролла чикен фреш 8шт')
                            now_order_bludos.append('Чикен фреш')
                        elif message1.text == '2':
                            await bot.send_message(message1.chat.id, 'Выбрано два ролла запечённый чикен 8шт')
                            now_order_bludos.append('Запечённый чикен')
                        elif message1.text == '3':
                            await bot.send_message(message1.chat.id, 'Выбраны Два ролла сяки грин 8шт')
                            now_order_bludos.append('Сяки грин')
                        elif message1.text == '4':
                            await bot.send_message(message1.chat.id, 'Выбраны Два ролла оши хот 8шт')
                            now_order_bludos.append('Оши хот')
                        elif message1.text == '5':
                            await bot.send_message(message1.chat.id, 'Выбрано Комбо дуэт пепперони 25 см')
                            now_order_bludos.append('Пепперони 25 см')
                        elif message1.text == '6':
                            await bot.send_message(message1.chat.id, 'Выбрано Комбо три цыплёнка')
                            now_order_bludos.append('Три цыплёнка')
                        elif message1.text == '7':
                            await bot.send_message(message1.chat.id, 'Выбран Комбо лайт пепперони и кани грин 8 шт')
                            now_order_bludos.append('Лайт пепперони и кани грин')
                        elif message1.text == '8':
                            await bot.send_message(message1.chat.id, 'Выбран Комбо ужин барбекю')
                            now_order_bludos.append('Комобо ужин барбекю')
                        elif message1.text == '9':
                            await bot.send_message(message1.chat.id, 'Выбран Ланч: Суп, лапша, сэндвич')
                            now_order_bludos.append('Чикен фреш')
                        elif message1.text == '10':
                            await bot.send_message(message1.chat.id, 'Выбран Ланч: Бульон с сухариками, сэндвич с ветчиной')
                            now_order_bludos.append('Чикен фреш')
                        elif message1.text == '11':
                            await bot.send_message(message1.chat.id, 'Выбрано Ланч: паста карбонара, сэндвич с курицей')
                            now_order_bludos.append('Чикен фреш')
                        elif message1.text == '12':
                            await bot.send_message(message1.chat.id, 'Выбран Ланч: Паста болоньезе и сэндвич с курицей')
                            now_order_bludos.append('Чикен фреш')
                        elif message1.text == '+':
                            await bot.send_message(message1.chat.id, 'Отлично! Напишите код следующего блюда из меню "Сицилия":\n\n1. Домашняя лапша\n2. Пряный тори\n3. Крем-суп из шампиньонов\n4. Борщ с курицей\n5. Винегрет\n6. Азиатский с цыпленком\n7. Салат с курицей\n8. Карбонара паста\n9. Шницель с рисом\n10. Котлета с пюре')
                        elif message1.text == 'f':
                            await bot.send_message(callback.message.chat.id, f'Заказ в ресторан "Сицилия" сделан! Ваш заказ: {", ".join(now_order_bludos)}. Спасибо за использование!')
                        else:
                            await bot.send_message(message1.chat.id, 'Пожалуйста, введите код блюда от 1 до 12, "+" для добавления или "f" для завершения')
            elif callback.data == '3':
                now_order_cafe = 'Осака'
                await bot.send_message(
                chat_id=callback.message.chat.id,
                text=f'Хорошо, выбран ресторан "Осака". \nВыберите Вот его меню: \n\n Супы:\n·1 Суп чаудер с кальмаром и креветками – Густой сливочный суп с морепродуктами.\n·2 Том-ям с креветкой и лососем – Острый и кислый тайский суп.\n·3 Сырный суп с креветками и шпинатом – Сырный крем-суп с креветками.\n·4 Том-ям с креветкой – Классический том-ям с креветками.\n·5 Суп-лапша домашний – Домашний суп с лапшой.\n·6 Крем-суп грибной – Нежный крем-суп из грибов.\n\nПаста, лапша, рис\n·7 Феттуччине 4 сыра – Паста в сливочном сырном соусе.\n·8 Японская лапша харусаме с кальмаром и мидиями – Лапша с морепродуктами.\n·9 Карбонара с беконом в сливочном соусе – Паста карбонара со сливками.',
                )
        
                @bot.message_handler(content_types=['text'])
                async def osaka_handler(message1):
                    if message1.chat.id == callback.message.chat.id:
                        if message1.text == '1':
                            await bot.send_message(message1.chat.id, 'Выбран суп чаудер с кальмаром и креветками')
                            now_order_bludos.append('Чаудер с кальмаром и креветками')
                        elif message1.text == '2':
                            await bot.send_message(message1.chat.id, 'Выбран том-ям с креветкой и лососем')
                            now_order_bludos.append('Том-ям с креветкой и лососем')
                        elif message1.text == '3':
                            await bot.send_message(message1.chat.id, 'Выбран сырный суп с креветками и шпинатом')
                            now_order_bludos.append('Сырный суп с креветками и шпинатом')
                        elif message1.text == '4':
                            await bot.send_message(message1.chat.id, 'Выбран том-ям с креветкой')
                            now_order_bludos.append('Том-ям с креветкой')
                        elif message1.text == '5':
                            await bot.send_message(message1.chat.id, 'Выбран суп-лапша домашний')
                            now_order_bludos.append('Суп лапша домашний')
                        elif message1.text == '6':
                            await bot.send_message(message1.chat.id, 'Выбран крем-суп грибной')
                            now_order_bludos.append('Крем-суп грибной')
                        
                        elif message1.text == '7':
                            await bot.send_message(message1.chat.id, 'Выбрано феттуччине 4 сыра')
                            now_order_bludos.append('Феттуччине 4 сыра')
                        elif message1.text == '8':
                            await bot.send_message(message1.chat.id, 'Выбрана японская лапша харусаме с кальмаром и мидиями')
                            now_order_bludos.append('Харусаме кальмар-мидии')
                        elif message1.text == '9':
                            await bot.send_message(message1.chat.id, 'Выбрана карбонара с беконом в сливочном соусе')
                            now_order_bludos.append('Карбонара с беконом в сливочном соусе')
                        elif message1.text == '+':
                            await bot.send_message(message1.chat.id, 'Отлично! Напишите код следующего блюда из меню "Сицилия":\n\n1. Домашняя лапша\n2. Пряный тори\n3. Крем-суп из шампиньонов\n4. Борщ с курицей\n5. Винегрет\n6. Азиатский с цыпленком\n7. Салат с курицей\n8. Карбонара паста\n9. Шницель с рисом\n10. Котлета с пюре')
                        elif message1.text == 'f':
                            await bot.send_message(callback.message.chat.id, f'Заказ в ресторан "Сицилия" сделан! Ваш заказ: {", ".join(now_order_bludos)}. Спасибо за использование!')
                        else:
                            await bot.send_message(message1.chat.id, 'Пожалуйста, введите код блюда от 1 до 12, "+" для добавления или "f" для завершения')
            elif callback.data == '4':
                now_order_cafe = 'Мясник и Бык'
                await bot.send_message(
                chat_id=callback.message.chat.id,
                text=f'Хорошо, выбран ресторан "Мясник и Бык". \nСегодняшний ланч: \n\nЛанч по дням недели — Меню ланча, обновляемое ежедневно.\n\nДля заказа ланча напишите "ланч".',
                )
                @bot.message_handler(content_types=['text'])
                async def myaso(message1):
                    if message1.chat.id == callback.message.chat.id:
                        if message1.text == 'Ланч':
                            await bot.send_message(message1.chat.id, 'Вы заказали ланч в "Мяснике и Быке"')
                            now_order_bludos.append('Ланч в "Мяснике и Быке"')
    
            elif callback.data == '5':
                markup45 = types.InlineKeyboardMarkup()
                btn11=types.InlineKeyboardButton('Сайт "Сицилии"', url='https://taganrog.pizza-sicilia.ru/')
                btn21=types.InlineKeyboardButton('Сайт "Мята food"', url='https://myata-food.ru/')
                btn31=types.InlineKeyboardButton('Сайт "Осаки"', url='https://taganrog.sushiosaka.ru/')
                btn41=types.InlineKeyboardButton('Сайт "Мясника и Быка"', url='https://butcher-bull.ru/call-online')
                btn51=types.InlineKeyboardButton('Сай сервиса доставки "Яндекс.Еда"', url='https://eda.yandex.ru/?utm_medium=cpc&utm_source=yasearch&utm_campaign=704307793.%5BEDA%5DMX_Srv_Rf_Brand_Search&utm_content=17367627184&utm_term=---autotargeting%7Cpid%7C205669267523%7Caid%7C17367627184%7Ctype1%7Cdesktop%7Cnone%7Csearch&etext=2202.SwNyd8UDzVL_4Iu0wosiW6QcB5M86ERF-tqS1_xzBYZsZ3NpZmxqaXZsbHRndXJo.792dff1d173b359ec7b5c39983c82a4f01c1c470&yclid=7440376692682522623&ybaip=1=')
                markup45.row(btn11, btn21)
                markup45.row(btn31, btn41)
                markup45.row(btn51)
                await bot.send_message(
                chat_id=callback.message.chat.id,
                text='Заказ онлайн доступен через сайты ресторанов или доставки еды.', reply_markup=markup45
                )
            zuk=''
            for i in range(0, len(now_order_bludos)):
                zuk+=now_order_bludos[i]
            print(zuk)
            ExBl.append(zuk)
            ExKaf.append(now_order_cafe)
            df['Кафе']=ExKaf
            df['Блюда']=ExBl
            df.to_excel('report.xlsx', index=False)

                
                
#Отправка таблицы эксель ботом
@bot.message_handler(commands=['report'])
async def send_excel(message):
    IDc = message.chat.id
    f = open('Logs.txt', 'a')
    f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/report')
    f.write('\n')
    f.closed
    if admin_status:
        with open('report.xlsx', 'rb') as file:
            await bot.send_document(
                chat_id=message.chat.id,
                document=file,
                caption='Вот ваш Excel файл с отчетом'
            )
        await bot.reply_to(message, "Файл успешно отправлен!")
    else:
        await bot.send_message(message.chat.id, 'Вы не явялетесь админом. Команда заблокирована.')

        
    #Отправка логов бота админу
@bot.message_handler(commands=['logs'])
async def send_logs(message):
    IDc = message.chat.id
    f = open('Logs.txt', 'a')
    f.write(f' {str(IDc):15}' + ' ' + f'{message.from_user.username:35}' + ' ' + f'{tconv(message.date):22}' + f'/logs')
    f.write('\n')
    f.closed
    if admin_status:
        with open('Logs.txt', 'rb') as fi:
            await bot.send_document(
                chat_id=message.chat.id,
                document=fi,
                caption='Вот ваш файл с логами'
            )
        await bot.reply_to(message, "Файл успешно отправлен!")
    else:
        await bot.send_message(message.chat.id, 'Вы не явялетесь админом. Команда заблокирована.')
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
    async def write_user(message4):
        check_f = open('User_check.txt', 'a')
        check_f.write(message.text)
        check_f.closed
        await bot.reply_to(message4, "Сотрудник комании Оджетто успешно внесён в список!")


        
asyncio.run(bot.polling())



