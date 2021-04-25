# This Python file uses the following encoding: utf-8
import telebot
from telebot import types
from collections import defaultdict
from random import randint, random
from time import sleep
from telebot.apihelper import answer_callback_query
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import os

token = '1626437067:AAF1LOEOpgJjv58io8XZFN2IO6K9J-TNtXo'
bot = telebot.TeleBot(token)
level = {}
inventories = {}
life = {}

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


# @bot.message_handler(commands=["start"])
def start_game(update, contex):
    user = update.message.chat.id
    life[user] = 10
    level[user] = 0
    inventories[user] = []
    bot.send_chat_action(user, action='typing')
    sleep(random() * 2 + 3.)
    bot.send_message(user, f"Привет! Это игра День выборов.\n\nТы единственный честный наблюдатель на участке. Твоя задача: не допустить фальсификаций и получить итоговый протокол.\n\nУ тебя есть *{life[user]} жизней*. За каждую пропущенное нарушение у тебя будут отниматься жизни. Если жизней не останется, то фальсификаторы выиграют.", parse_mode='Markdown')
    process_game(user, level[user], inventories[user], life[user])


#@bot.callback_query_handler(func=lambda call: True)
def user_answer(call, contex):
    print('_________________')
    print(call)
    print(contex)
    print('_________________')
    user = call.callback_query.message.chat.id
    #bot.delete_message(call.message.chat.id, call.message.message_id)
    process_answer(user, call.callback_query.data)
    
def process_game(user, level, inventory, life):
    kb = types.InlineKeyboardMarkup()

    if life <= 0:
        bot.send_message(user, f'Вы проиграли. Чтобы начать заново введите /start', parse_mode='Markdown')
        level = -1

    #  Прибытие на участок
    if level == 0:
        bot.send_chat_action(user, action='typing')
        sleep(random() * 2 + 3.)
        kb.add(types.InlineKeyboardButton(text="Идти на участок", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Осмотреться вокруг", callback_data="2"))
        bot.send_message(user, f"*Утро. Время 07:25*\n\n❤️ Жизней осталось: {life}\n\nВы подходите к избирательному участку №665, который находится в школе №13. Вокруг никого, но у вас какое-то нехорошее предчувствие. Может быть стоит осмотреть территорию вокруг школы. Или не тратить время и сразу идти на участок.\n\n*Что будете делать?*", reply_markup=kb, parse_mode='Markdown')

    #  Открытие участка
    elif level == 1:
        kb.add(types.InlineKeyboardButton(text="Осмотреть участок", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Осмотреть книги избирателей", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Сесть и не мешать комиссии работать", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="Устроить драку", callback_data="4"))
        bot.send_message(user, f"*Утро. Время 07:30*\n\n❤️ Жизней осталось: {life}\n\nВы регистрируетесь на избирательном участке. Комиссия кажется дружелюбной. Вам предлагают сесть за стол для наблюдателей и пока не мешать комиссии работать. До открытия участка осталось всего полчаса.\n\n*Что будете делать?*", reply_markup=kb, parse_mode='Markdown')

    #  Осмотр книг избирателей
    elif level == 1.1:
        kb.add(types.InlineKeyboardButton(text="Книга 1", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Книга 2", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Книга 3", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="Все книги с ошибками", callback_data="4"))
        bot.send_message(user, "Перед вами три книги избирателей. Возможно с ними что-то не так. Вы их по очереди осматриваете\n\n*Книга 1*. На книге есть и печать и подпись на обортной стороне. Внутри книга пустая: без ФИО и года рождения и адреса.\n\n*Книга 2*. На книге есть и печать и подпись на обортной стороне. Заполнены данные избирателей, но не заполнен заголовок страницы.\n\n*Книга 3*. На книге есть и печать и подпись на обортной стороне. Заполнены данные избирателей, но не заполнен заголовок страницы. \n\n *Какая из книг заполнена верно?*", reply_markup=kb, parse_mode='Markdown')

    #  Выездное голосование
    elif level == 2:
        kb.add(types.InlineKeyboardButton(text="Отпустить группу", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Поехать вместе с выездной группой", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Потребовать перенести выезд", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="Устроить драку", callback_data="4"))
        bot.send_message(user, f'*Утро. Время 09:02*\n\n❤️ Жизней осталось: {life}\n\nНа участок медленно приходят избиратели. Ничего особенного не происходит. Вдруг председатель комиссии объявляет, что группа для проведения выездного голосования отправляется через пять минут.\n\n*Что будете делать?*', parse_mode='Markdown', reply_markup=kb)
    
    #  Вброс на участке
    elif level == 3:
        kb.add(types.InlineKeyboardButton(text="Отобрать пачку", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Начать орать", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Звонить в полицию", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="Писать жалобу", callback_data="4"))
        kb.add(types.InlineKeyboardButton(text="Начать снимать", callback_data="5"))
        bot.send_message(user, f'*День. Время 12:34*\n\n❤️ Жизней осталось: {life}\n\nК урне подходит мужчина. Вы видите в его руке небольшую стопку листов. Кажется, он собирается их вбросить. Времени на раздумие нет.\n\n*Что будете делать?*', reply_markup=kb, parse_mode='Markdown')
    
    #  Вброс не произошёл
    elif level == 3.1:
        kb.add(types.InlineKeyboardButton(text="За полицией", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="За книгами избирателей", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="За председателем", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="За урнами", callback_data="4"))
        bot.send_message(user, f'Итак, мужчина убежал. Комиссия гасит оставленные на полу бюллетени. Вы пишите жалобу и теперь никому не доверяете на участке.\n\n*За чем будете следить в первую очередь*?', reply_markup=kb, parse_mode='Markdown')

    #  Вброс произошёл
    elif level == 3.2:
        kb.add(types.InlineKeyboardButton(text="Наблюдать за полицией", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Наблюдать за книгами избирателей", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Наблюдать за председателем", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="Наблюдать за урнами", callback_data="4"))
        bot.send_message(user, f'Аккуратная стопка бюллетеней лежит на дне урны. Вы видите, что все отметки проставлены за провластного кандидата. Кажется, что выборы на этом участке закончились. \n\n*Что будете делать?*', reply_markup=kb, parse_mode='Markdown')

    #  На участок звонит соцработник
    elif level == 4:
        kb.add(types.InlineKeyboardButton(text="Разрешить включить пенсионерку в реестр", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Не разрешить включить пенсионерку в реестр", callback_data="2"))
        bot.send_message(user, f'*День. Время 13:01*\n\n❤️ Жизней осталось: {life}\n\nРаздаётся звонок телефона. Трубку снимает секретарь. Некоторое время слушает, а потом зовёт к телефону председателя. И громко объясняет ей, что звонит соцработник и просит оформить заявку на надомное голосование для пенсионерки, которая не может сама ходить.\n\nПо переговорам председателя и секретаря вы понимаете, что обратился не сам человек, который будет голосовать. *Что будете делать?*', reply_markup=kb, parse_mode='Markdown')
    
    # Можно ли включить в реестр "надомников" того, кто обратился после 14:00
    elif level == 5:
        kb.add(types.InlineKeyboardButton(text="Разрешить включить женщину в реестр", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Не разрешить включить женщину в реестр", callback_data="2"))
        bot.send_message(user, f'*День. Время 14:30*\n\n❤️ Жизней осталось: {life}\n\nСнова звонок. Секретарь поднимает трубку и внимательно слушает. Ситуация как в прошлый раз: к секретарю подходит председатель и у них начинается бурное обсуждение. Из их разговора вы понимаете, что позвонила больная женщина, которая не сможет сама прийти на участок. Поэтому просит внести её в список “надомников”.\n\nНа этот раз избиратель сам просит, чтобы к нему приехала выездная группа. *Что будете делать?*', reply_markup=kb, parse_mode='Markdown')

    #  Второе голосование на дому
    elif level == 6:
        kb.add(types.InlineKeyboardButton(text="Да, всё в порядке", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Нет, слишком мало избирателей в реестре для выезда", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Нет, слишком много бюллетеней", callback_data="3"))
        bot.send_message(user, f'*День. Время 15:02*\n\n❤️ Жизней осталось: {life}\n\nПредседатель объявляет, что через полчаса поедет вторая выездная группа. Вы просите председателя ознакомить вас с реестром и бюллетенями, которые берёт с собой группа. Председатель показывает вам реестр. В нём всего пять фамилий. И показывает вам десять бюллетеней. По два бюллетеня на каждого избирателя: основной и запасной. \n\n*Всё в порядке?*', reply_markup=kb, parse_mode='Markdown')

    # Второе голосование на дому. В квартире
    elif level == 7:
        kb.add(types.InlineKeyboardButton(text="Да, разрешить проголосовать", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Нет, он не может проголосовать", callback_data="2"))
        bot.send_message(user, f'*День. Время 15:32*\n\n❤️ Жизней осталось: {life}\n\nВы с выездной группой входите в квартиру. Комиссия выдаёт женщине бюллетень и она без раздумий ставит “галку” напротив фамилии одного из кандидатов. Вдруг, из соседней комнаты выходит не менее пожилой мужчина и простит дать ему тоже проголосовать. Он утверждает, что звонил на участок и просил включить его в список для голосования на дому. Сам он до участка вряд ли сможет дойти и в подтверждение показывает справку об инвалидности. Члены комиссии и другие наблюдатели не против. Ведь у них есть пара запасных бюллетеней. \n\n*Разрешите пенсионеру проголосовать?*', reply_markup=kb, parse_mode='Markdown')

    # Второе голосование на дому. Возвращение на участок
    elif level == 8:
        kb.add(types.InlineKeyboardButton(text="Составить акт сразу", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Разрешить составить акт позже", callback_data="2"))
        bot.send_message(user, f'*День. Время 16:32*\n\n❤️ Жизней осталось: {life}\n\nВы с выездной группой возвращаетесь на участок. Здесь сейчас куча избирателей. В кабинки для голосования буквально выстроились очереди. Кажется, что к вечеру все вспомнили, что сегодня выборы. Поэтому председатель говорит, что акт о выездном голосовании составят после окончания голосования. Да и тем более вы же сами проконтролировали выездное голосование.\n\n*Разрешите составить акт позже?*', reply_markup=kb, parse_mode='Markdown')

    # Подсчёт голосов. Начало подсчёта
    elif level == 9:
        kb.add(types.InlineKeyboardButton(text="Наблюдать за списками избирателей", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Наблюдать за вскрытием урн", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Наблюдать за гашением бюллетеней", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="Потребовать не вести подсчёт параллельно", callback_data="4"))
        bot.send_message(user, f'*Вечер. Время 20:02*\n\n❤️ Жизней осталось: {life}\n\nПредседатель объявляет окончание голосования и распоряжается о начале процедуры подсчёта голосов. Члены комиссии, которые лениво сидели за столами целый день, вдруг ожили и приступили к подсчёту: одни ножницами и ножами стали отрезать левые углы у неиспользованных бюллетеней,  другие начали работать со списками, а председатель и секретарь приготовились к вскрытию переносных и стационарных урн. Кажется, что каждый из членов комиссии прекрасно знает, что нужно делать дальше. Все хотят поскорее всё подсчитать и уйти домой пораньше.\n\n*Что будете делать?*', reply_markup=kb, parse_mode='Markdown')

    # Подсчёт голосов. Начало подсчёта 2
    elif level == 9.1:
        kb.add(types.InlineKeyboardButton(text="Вариант 1", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Вариант 2", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Вариант 3", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="Вариант 4", callback_data="4"))
        bot.send_message(user, f'“Ну мы тут теперь до утра сидеть будем”, — недовольно сказала председатель и попросила напомнить ей порядок подсчёта голосов.\n\n1. Работа со списком → Гашение → Вскрытие стационарных ящиков → Вскрытие переносных ящиков → Сортировка → Подсчёт голосов в пачках → Проверка контрольных соотношений → Упаковка документов → Проведение итогового заседания → Заполнение и подписание протокола → Выдача заверенных копий протокола\n\n2. Вскрытие стационарных ящиков → Вскрытие переносных ящиков → Сортировка → Подсчёт голосов в пачках → Работа со списком → Гашение → Проверка контрольных соотношений → Упаковка документов → Проведение итогового заседания → Заполнение и подписание протокола → Выдача заверенных копий протокола\n\n3. Гашение → Работа со списком → Вскрытие переносных ящиков → Вскрытие стационарных ящиков → Сортировка → Подсчёт голосов в пачках → Проверка контрольных соотношений → Упаковка документов → Проведение итогового заседания → Заполнение и подписание протокола → Выдача заверенных копий протокола\n\n4. Гашение → Работа со списком → Вскрытие переносных ящиков → Вскрытие стационарных ящиков → Сортировка → Подсчёт голосов в пачках → Уточнение результата выборов в вышестоящей комиссии → Упаковка документов → Проведение итогового заседания → Заполнение и подписание протокола → Выдача заверенных копий протокола', reply_markup=kb, parse_mode='Markdown')

    # Подсчёт голосов. Проверка контрольных соотношений
    elif level == 10:
        kb.add(types.InlineKeyboardButton(text="Всё в порядке", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="В урнах бюллетеней меньше, чем выдано", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="В урнах бюллетеней больше, чем выдано", callback_data="4"))
        bot.send_photo(user,photo=open(r"C:\Users\kiril\OneDrive\Projects\gg\big_protokol.png", "rb"), caption=f'*Ночь. Время 01:30*\n\n❤️ Жизней осталось: {life}\n\nКомиссия закончила считать бюллетени и занесла цифры в увеличенную форму итогового протокола. Нужно быстро проверить контрольные соотношения. *Всё ли тут нормально?*\n\n**Как проверить контрольные соотношения?**\n- Число выданных бюллетеней в помещении для голосования + Число бюллетеней выданных вне помещения (надомное голосование) = Число бюллетеней в стационарном ящике + Число бюллетеней в переносном ящике\n- Действительные бюллетени = Сумма голосов всех кандидатов', reply_markup=kb, parse_mode='Markdown')

    #  Подсчёт голосов. Выдача итогового протокола
    elif level == 11:
        kb.add(types.InlineKeyboardButton(text="С протоколом всё в порядке", callback_data="1"))
        kb.add(types.InlineKeyboardButton(text="Нет подписей членов комиссии", callback_data="2"))
        kb.add(types.InlineKeyboardButton(text="Не указано время заверения копии", callback_data="3"))
        kb.add(types.InlineKeyboardButton(text="Контрольные соотношения не бьются", callback_data="4"))
        kb.add(types.InlineKeyboardButton(text="Копия не заверена председателем", callback_data="5"))
        bot.send_photo(user, open(r"C:\Users\kiril\OneDrive\Projects\gg\protokol.jpg", 'rb'), reply_markup=kb, caption=f'*Ночь. Время 02:12*\n\n❤️ Жизней осталось: {life}\n\nПодсчет наконец закончен. Председатель выдаёт вам копию протокола об  итогах голосования.\n\n*С ним всё в порядке?*', parse_mode='Markdown')
    
    if level == 99 and life > 0:
        bot.send_message(user, f'*Ночь. Время 03:02*\n\n❤️ Жизней осталось: {life}\n\nПочти без сил, но с итоговым протоколом ты уходишь с участка. Тебе удалось не допустить серьёзных нарушений. Правда, твой кандидат всё равно проиграл. Он отстал от соперника всего на несколько голосов. Такое тоже бывает и не всё на выборах зависит от наблюдателей. Но именно благодаря тебе выборы прошли честно и это самое важное.', reply_markup=kb, parse_mode='Markdown')

def process_answer(user, answer):
    #  Прибытие на участок
    if level[user] == 0:
        if answer == "1":
            bot.send_message(user, "Вы вовремя пришли на участок. Но возможно возле участка осталась незаконная агитация.")
            level[user] = 2

        elif answer == "2":
            bot.send_message(user, "Вы осмотрели местность вокруг участка. Ничего подозрительно вокруг не оказалось. Вы только зря потратили время и опоздали на открытие участка. Книги избирателей никто не осмотрел. Урны опечатаны без вас")
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            level[user] = 2
            life[user] = life[user] - 1
    
    #  Открытие участка
    elif level[user] == 1:
        if answer == "1":
            bot.send_message(user, "Вы осмотрели участок. Из нарушений разве что висящий портрет одного из кандидатов в холле. Пока вы с секретарём его снимаете, председатель и члены комиссии делали какие-то пометки в книгах избирателей")
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            level[user] = 2
            life[user] = life[user] - 1

        elif answer == "2":
            bot.send_message(user, "Председатель сначала уклоняется, но под угрозой жалобы соглашается дать посмотреть несколько книг на ваш выбор")
            level[user] = 1.1

        elif answer == "3":
            bot.send_message(user, "Вам удалось немного подремать до открытия участка. Когда вы проснулись в урне для голосования уже лежала пачка бюллетеней.")
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            level[user] = 2
            life[user] = life[user] - 1

        elif answer == "4":
            bot.send_message(user, "Председатель только на вид была хрупкой и старенькой женщиной. Откуда вам было знать, что она семикратный чемпион СССР по женскому боксу. Два удара в корпус, один в челюсть и вы без сознания лежите на полу. Полицейские надели на вас наручники, скоро вас увезут в отделение. На этом ваше наблюдение закончилось. ")
            life[user] = life[user] - 10

    # Осмотр книг
    elif level[user] == 1.1:
        if answer == "1":
            bot.send_message(user, "Эта книга с нарушениями. ФИО, года рождения и адрес должны быть заполнены к открытию участка")
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            level[user] = 2
            life[user] = life[user] - 1

        elif answer == "2":
            bot.send_message(user, "Эта книга с нарушениями. Заголовки страниц должны быть заполнены к открытию участка")
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            level[user] = 2
            life[user] = life[user] - 1

        elif answer == "3":
            bot.send_message(user, "Эта книга с нарушениями. В книге не должно быть никаких пометок — это признак готовящейся фальсификации. Например, так комиссия может отмеать тех, кто обычно не приходит голосовать и голосовать за них.")
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            level[user] = 2
            life[user] = life[user] - 1

        elif answer == "4":
            bot.send_message(user, "На всех книгах есть нарушения. Вы просите председателя их устранить.")
            level[user] = 2

    #  Выездное голосование
    elif level[user] == 2:
        if answer == "1":
            bot.send_message(user, "Комиссия уезжает с 50 бюллетенями и незаполенным списком для надомников.")
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            level[user] = 3
            life[user] = life[user] - 1

        elif answer == "2":
            bot.send_message(user, "Комиссия уезжает с 50 бюллетенями и незаполенным списком для надомников. Вы вместе с комиссией устроили поквартирный обход по спискам соцработников. Комиссия благодарит вас за помощь.")
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            level[user] = 3

        elif answer == "3":
            bot.send_message(user, "Вы объясняете, что о выезде нужно объявлять не менее, чем за полчаса до отправления группы. А также осматриваете выписку из реестра о надомном голосовании. Оказывается, что там не было ни одной фамилии. Председатель неохотно заполняет выписку и переносит выезд.")
            level[user] = 3

        elif answer == "4":
            bot.send_message(user, "Председатель только на вид была хрупкой и старенькой женщиной. Откуда вам было знать, что она семикратный чемпион СССР по женскому боксу. Два удара в корпус, один в челюсть и вы без сознания лежите на полу. Полицейские надели на вас наручники, скоро вас увезут в отделение. На этом ваше наблюдение закончилось. ")
            life[user] = life[user] - 10
    
    #  Вброс на участке
    elif level[user] == 3:
        if answer == "1":
            bot.send_message(user, 'Мужчина с пачкой начал громко возмущаться. На это тут же реагируют члены комиссии: "Да этот наблюдатель на избирателей нападает. Вы посмотрите! Ненормальный! Полиция!". Вас тут же окружает толпа громких женщин из комиссии.\n\nВы пытаетесь указывать полицейским, что у мужчины в руках пачка бюллетеней. Но они вас почти не слышат. "Ладно, в участке разберёмся", — говорит лейтенант и уводит вас с участка.', parse_mode='Markdown')
            life[user] = life[user] - 10
        elif answer == "2" or answer == "5":
            bot.send_message(user, 'Мужчина пугается, бросает пачку на пол и убегает с участка.')
            level[user] = 3.1
        elif answer == "3":
            bot.send_message(user, 'Вы быстро набираете номер полиции и рассказываете дежурному, что на участке, кажется, готовится вброс. На что вам отвечают: "Когда вбросят — тогда и звоните. Мы то что сделать можем?". Мужчина тем временем засовывает пачку в урну и уходит с участка.')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 3.2
        elif answer == "4":
            bot.send_message(user, 'Пока вы пишите жалобу, мужчину опускате пачку в урну и уходит с участка. А председатель отказывается принимать вашу жалобу. "Какой мужчина? Какая пачка? Мы ничего не видели. Не мешайте, пожалуйста, комиссии работать" ')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 3.2

    #  Вброс не произошёл
    elif level[user] == 3.1 or level[user] == 3.2:
        if answer == "1":
            bot.send_message(user, 'Вы внимательно следите за полицией. Правда, зачем непонятно. Полицейские равнодушными взглядами втречают избирателей. О чём-то переговариваются друг с другом. Иногда перестают шевелиться совсем. Будто экономят силы на что-то более важное.', parse_mode='Markdown')
            level[user] = 4
        elif answer == "2":
            bot.send_message(user, 'Да, лучше внимательнее следить за книгами избирателей. Вброшенные бюллетени ещё необходимо "легализовать". В случае вброса в урне будут лежать бюллетени, которые избиратели не получали. *Чтобы скрыть фальсификацию члены комиссии должны будут внести в список избирателей фальшивые записи о выдачи бюллетеней.*', parse_mode='Markdown')
            level[user] = 4
        elif answer == "3":
            bot.send_message(user, 'Председатель замечает, что за ней ведётся слежка. И в ответ начинает вас сверлить взглядом от которого в школе шарахаются ученики и другие преподаватели. Вам становится не по себе. И с председателя вы переключаетесь на рассматривание потолка в школе.')
            level[user] = 4
        elif answer == "4":
            bot.send_message(user, 'Вы внимтаельно смотрите за урной и теми, кто к ней приближается. Но похоже ещё одного вброса не планируется.')
            level[user] = 4
        elif answer == "5":
            bot.send_message(user, 'Вы внимтаельно смотрите за урной и теми, кто к ней приближается. Но похоже ещё одного вброса не планируется.')
            level[user] = 4

    #  На участок звонит соцработник
    elif level[user] == 4:
        if answer == "1":
            bot.send_message(user, 'Всё верно. Подать заявление о выездном голосовании можно лично и через третьих лиц. В том числе через родственников и соцработников.', parse_mode='Markdown')
            level[user] = 5
        elif answer == "2":
            bot.send_message(user, 'Председатель объясняет, что подать заявление о выездном голосовании можно через третьих лиц и отчитывает вас за то, что мешаете комиссии работать. Это тот случай, когда комиссия знает правило лучше вас. Председатель даёт вам 67 ФЗ «Об основных гарантиях избирательных прав» и рекомендуют внимательнее с ним ознакомиться.')
            level[user] = 5

    # Можно ли включить в реестр "надомников" того, кто обратился после 14:00
    elif level[user] == 5:
        if answer == "1":
            bot.send_message(user, 'Неправильно. Время уже 14:30. Приём заявлений на выездное голосование заканчивается за шесть часов до конца дня голосования, то есть в 14:00. Поэтому включить женщину в реестр для надомного голосования уже нельзя.', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 6
        elif answer == "2":
            bot.send_message(user, 'Верно. Приём заявлений на выездное голосование заканчивается за шесть часов до конца дня голосования, то есть обычно в 14:00. К сожалению, включить женщину в реестр для надомного голосования уже нельзя.')
            level[user] = 6

    # Второе голосование на дому
    elif level[user] == 6:
        if answer == "1":
            bot.send_message(user, 'Председатель собирается дать группе дополнительные бюллетени. По закону *количество бюллетеней не должно быть больше 5%, чем избирателей в реестре*. То есть всего две дополнительные бюллетени, если избирателей менее 40 человек.', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 7
        elif answer == "2":
            bot.send_message(user, 'Выезд состоится даже если в реестре всего один человек. А вот бюллетеней группа собирается взять больше, чем им требуется. По закону *количество бюллетеней не должно быть больше 5%, чем избирателей в реестре*. То есть всего две дополнительные бюллетени, если избирателей менее 40 человек.')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 7
        elif answer == "3":
            bot.send_message(user, 'Верно. Выездная группа собирается взять больше бюллетеней, чем должно быть. По закону *количество бюллетеней не должно быть больше 5%, чем избирателей в реестре*. То есть всего две дополнительные бюллетени, если "надомников" менее 40 человек.', parse_mode='Markdown')
            level[user] = 7

    # Второе голосование на дому. В квартире
    elif level[user] == 7:
        if answer == "1":
            bot.send_message(user, 'Пенсионер всех поблагодарил за то, что ему не надо будет идти на участок. А по пути обратно комиссия с вашего позволения помогла проголосовать встреченным пенсионерам. Вам кажется, что вы сделали хорошее дело, но самом деле помогли нарушить закон. Ведь проголосовать на дому может только тот, кто обратился в избирательную комиссию в течение 10 дней до дня голосования. В этому случае надо было порекомендовать избирателю прийти на участок самостоятельно.', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 8
        elif answer == "2":
            bot.send_message(user, 'Пенсионер вас обругал и ушёл обратно в свою комнату. Всё что можно тут сделать — это порекомендовать ему самостоятельно дойти до участка. Ведь закон запрещает выдавать бюллетени тем, кто не зарегистрирован в реестре надомного голосования. ')
            level[user] = 8

    # Второе голосование на дому. Возвращение на участок
    elif level[user] == 8:
        if answer == "1":
            bot.send_message(user, 'Верно. Акт нужно составить сразу по возвращению выедной группы', parse_mode='Markdown')
            level[user] = 9
        elif answer == "2":
            bot.send_message(user, 'Неверно. Акт нужно составить сразу по возвращению выедной группы')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 9

    # Подсчёт голосов. Начало подсчёта
    elif level[user] == 9:
        if answer == "1":
            bot.send_message(user, 'Неверно. Вспомним базовые принципы подсчёта голосов.\n\n- Подсчет голосов начинается сразу после окончания голосования и ведётся непрерывно\n\n- Подсчёт голосов ведётся поэтапно. Причём этапы не должны выполняться одновременно, то есть нельзя одновременно гасить неиспользованные бюллетени и работать со списками.\n\nНа практике нередко приходится сталкиваться с тем, что комиссия, стремясь ускорить работу, пытается параллельно выполнять сразу несколько этапов подсчета. Такие действия следует немедленно пресекать, указывая комиссии на обязательность соблюдения требований закона.', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 10
        elif answer == "2":
            bot.send_message(user, 'Неверно. Вспомним базовые принципы подсчёта голосов.\n\n- Подсчет голосов начинается сразу после окончания голосования и ведётся непрерывно\n\n- Подсчёт голосов ведётся поэтапно. Причём этапы не должны выполняться одновременно, то есть нельзя одновременно гасить неиспользованные бюллетени и работать со списками.\n\nНа практике нередко приходится сталкиваться с тем, что комиссия, стремясь ускорить работу, пытается параллельно выполнять сразу несколько этапов подсчета. Такие действия следует немедленно пресекать, указывая комиссии на обязательность соблюдения требований закона.')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 10
        elif answer == "3":
            bot.send_message(user, 'Неверно. Вспомним базовые принципы подсчёта голосов.\n\n- Подсчет голосов начинается сразу после окончания голосования и ведётся непрерывно\n\n- Подсчёт голосов ведётся поэтапно. Причём этапы не должны выполняться одновременно, то есть нельзя одновременно гасить неиспользованные бюллетени и работать со списками.\n\nНа практике нередко приходится сталкиваться с тем, что комиссия, стремясь ускорить работу, пытается параллельно выполнять сразу несколько этапов подсчета. Такие действия следует немедленно пресекать, указывая комиссии на обязательность соблюдения требований закона.')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 10
        elif answer == "4":
            bot.send_message(user, 'Верно. Подсчёт голосов ведётся поэтапно. Причём этапы не должны выполняться одновременно. Но на практике нередко приходится сталкиваться с тем, что комиссия, стремясь ускорить работу, пытается параллельно выполнять сразу несколько этапов подсчета. Такие действия следует немедленно пресекать, указывая комиссии на обязательность соблюдения требований закона.')
            level[user] = 9.1

    # Подсчёт голосов. Начало подсчёта 2
    elif level[user] == 9.1:
        if answer == "1":
            bot.send_message(user, 'Неверно. Правильно вот так: Гашение → Работа со списком → Вскрытие переносных ящиков → Вскрытие стационарных ящиков → Сортировка → Подсчёт голосов в пачках → Проверка контрольных соотношений → Упаковка документов → Проведение итогового заседания → Заполнение и подписание протокола → Выдача заверенных копий протокола', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 10
        elif answer == "2":
            bot.send_message(user, 'Неверно. Правильно вот так: Гашение → Работа со списком → Вскрытие переносных ящиков → Вскрытие стационарных ящиков → Сортировка → Подсчёт голосов в пачках → Проверка контрольных соотношений → Упаковка документов → Проведение итогового заседания → Заполнение и подписание протокола → Выдача заверенных копий протокола', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 10
        elif answer == "3":
            bot.send_message(user, 'Верно. Каждый этап логично вытекает из другого. ', parse_mode='Markdown')
            level[user] = 10
        elif answer == "4":
            bot.send_message(user, 'Неверно. Да и что за уточнение результата выборов в вышестоящей комиссии?', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 10

    # Подсчёт голосов. Проверка контрольных соотношений
    elif level[user] == 10:
        if answer == "1":
            bot.send_message(user, 'Неверно. Комиссия выдала на 175 бюллетеней больше, чем содержится в ящиках для голосования.', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 11
        elif answer == "2":
            bot.send_message(user, 'Верно. Комиссия выдала на 175 бюллетеней больше, чем содержится в ящиках для голосования. ', parse_mode='Markdown')
            level[user] = 11
        elif answer == "3":
            bot.send_message(user, 'Неверно. Комиссия выдала на 175 бюллетеней больше, чем содержится в ящиках для голосования.', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 11
        elif answer == "4":
            bot.send_message(user, 'Неверно. Комиссия выдала на 175 бюллетеней больше, чем содержится в ящиках для голосования.', parse_mode='Markdown')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 11

    # Подсчёт голосов. Выдача итогового протокола
    elif level[user] == 11:
        if answer == "3":
            bot.send_message(user, 'Верно. И без этой мелочи протокол является недействительным', parse_mode='Markdown')
            level[user] = 99
        else:
            bot.send_message(user, 'Неверно. На этом протоколе не указано время заверения копии. Без этой мелочи протокол является недействительным')
            bot.send_message(user, f'💔 Минус одна жизнь.', parse_mode='Markdown')
            life[user] = life[user] - 1
            level[user] = 99

    process_game(user, level[user], inventories[user], life[user])

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start_game))
    dp.add_handler(CallbackQueryHandler(user_answer))
    #dp.add_handler(CommandHandler("help", help))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=token)
    updater.bot.setWebhook('https://voting-day-bot.herokuapp.com/' + token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    #updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
