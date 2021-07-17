import logging
import calendar
import datetime

from requests.api import options
from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

from simple_salesforce import Salesforce
import os

#####################################Data#####################################
sf = Salesforce(
username='max2433186@mindful-impala-acpsha.com', 
password='JKlw124O2kanv5kLLf', 
security_token='')

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '1841783209:AAHrDitzlrEGtxSyCUgRr2oSl-vQsgBzPK8'
bot = ''

class UserTelegram:
    def __init__(self):
        self.login = None
        self.password = None
        self.exist = False
        self.contact = None
        self.newCard = None


class Card:
    def __init__(self, keeper):
        self.date = None
        self.amount = None
        self.description = None
        self.keeper = keeper
        self.confirmCreate = None

usersTelegram = {}


#######################################Functions###########################################

######################################Handlers##############################################
def start(update, context):
    """Send a message when the command /start is issued."""
    
    userId = update._effective_user.id
    createUserIfItNeed(userId)
    isUserLog = usersTelegram[userId].exist
    if isUserLog:
        update.message.reply_text('Вы уже зарегистрированы!', reply_markup=mainMenuKeyboard())
    else:
        update.message.reply_text('Введите логин', reply_markup=ReplyKeyboardRemove())
    # sf.Contact.create({'LastName':'simple_salesforce','Email':'example@example.com'})

def echo(update, context):
    """Echo the user message."""
    userId = update._effective_user.id

    if userId not in usersTelegram:
        start(update,context)
        return

    if usersTelegram[userId].exist == False:
        login(update, context)
    else:
        echoForExistUser(update,context)

    #update.message.reply_text(update.message.text)

def end(update, context):
    userId = update._effective_user.id
    usersTelegram.pop(userId)
    update.message.reply_text('До свидания!',
                            reply_markup=ReplyKeyboardRemove())

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

######################################Handlers##############################################

######################################Helper handlers##############################################

def login(update, context):
    userId = update._effective_user.id
    user = usersTelegram[userId]

    if user.login == None:
       user.login =  update.message.text
       update.message.reply_text('Введите пароль')
    else:
        user.password = update.message.text
        try:
            user.contact = sf.query(f"SELECT Id, Name, Email, Office__c, Admin__c FROM Contact WHERE Email ='{user.login}' AND Password__c ='{user.password}' LIMIT 1")
            throwExceptionIfContactEmpty(user.contact)        
            user.exist = True
            update.message.reply_text('Авторизация прошла успешно ',
                            reply_markup=mainMenuKeyboard())
        except Exception:
            update.message.reply_text('Неправильный логин или пароль.Попробуйте Снова')
            refreshUser(user)
            start(update,context)
            return

def echoForExistUser(update,context):
    message = update.message.text.lower()
    userId = update._effective_user.id
    user = usersTelegram[userId]
    userContactId = user.contact['records'][0]['Id']
    if message == 'текущий баланс':
        balance = sf.apexecute('Contact/'+userContactId, method='GET')
        update.message.reply_text(str(balance)+'$',
                            reply_markup=mainMenuKeyboard())
    elif message == 'создать карточку':
        user.card = Card(userContactId)
        update.message.reply_text('На какой день желаете создать карточку?',
                            reply_markup=createCardKeyboard())
    elif message == 'отмена':
        cancelToMainMenu(update,user)
    elif user.card != None:
        creatingCard(update,user,message)

def creatingCard(update,user,message):
    if user.card.date == None or user.card.date == True:
        creatingCardDate(update,user,message)
    elif user.card.amount == None or user.card.amount == True:
        creatingCardAmount(update,user,message)
    elif user.card.description == None or user.card.description == True:
        creatingCardDecription(update,user,message)
    elif isinstance(user.card.description,str):
        confirmCreateCard(update,user,message)
        

def creatingCardDate(update,user,message):
    if user.card.date == None:
        creatingCardDateNone(update,user,message)
    elif user.card.date == True:
        try:
            cardDate = getStringAsDateAndValidate(message)
            user.card.date = cardDate
            creatingCardAmount(update,user,message)
        except Exception as e:
            update.message.reply_text('Кажется вы неправильно ввели дату. Попробуйте еще раз или обратитесь к администратору. Пример: 2021-03-31',
                                reply_markup=cancelKeyboard())
            #update.message.reply_text(str(e))

def creatingCardDateNone(update,user,message):
    if message == 'сегодня':
        today = datetime.datetime.today()
        user.card.date = getStringAsDateAndValidate(str(today.day))
        creatingCardAmount(update,user,message)
    elif message == 'календарь':
        update.message.reply_text('Выберите число')
        replyMessage = """Или Введите дату вручную(день-месяц-число)
Пример:
2021-03-31
        """
        update.message.reply_text(replyMessage,
                            reply_markup=daysOfMonthKeyboard())
        user.card.date = True

def creatingCardAmount(update,user,message):
    if user.card.amount == None:
        update.message.reply_text('Введите сумму')
        user.card.amount = True
    elif user.card.amount == True:
        try:
            cardAmount = float(message)
            user.card.amount = cardAmount
            creatingCardDecription(update,user,message)
        except Exception as e:
            update.message.reply_text('Кажется вы неправильно ввели сумму. Попробуйте еще раз или обратитесь к администратору. Пример: 5.014',
                    reply_markup=cancelKeyboard())

def creatingCardDecription(update,user,message):
    if user.card.description == None:
        update.message.reply_text('Введите описание')
        user.card.description = True
    elif user.card.description == True:
        user.card.description = update.message.text
        confirmCreateCard(update,user,message)

def confirmCreateCard(update,user,message):
    if user.card.confirmCreate == None:
        update.message.reply_text('Вы уверены что хотите создать следующую карточку?')
        update.message.reply_text('Дата: ' + str(user.card.date))
        update.message.reply_text('Сумма: ' + str(user.card.amount)+'$')
        update.message.reply_text('Описание: ' + user.card.description, reply_markup=confirmKeyboard())
        user.card.confirmCreate = True
    elif user.card.confirmCreate == True:
        createCardInSalesforce(update,user)
        user.card = None

def createCardInSalesforce(update,user):
    try:
        something = sf.Expense_Card__c.create({'CardDate__c': user.card.date,'Amount__c':str(user.card.amount),'Description__c':user.card.description,'CardKeeper__c':user.card.keeper})
        user.card = None
        update.message.reply_text('Карточка успешно создана!', reply_markup=mainMenuKeyboard())
    except Exception as e:
        update.message.reply_text('Извините, карточку не получилось создать', reply_markup=mainMenuKeyboard())
        for err in e.content:
            update.message.reply_text(str(err['message']))


def cancelToMainMenu(update,user):
    user.card = None
    update.message.reply_text('Что вы хотите сделать?',
                            reply_markup=mainMenuKeyboard())

######################################Helper handlers##############################################


#########################Keyboards############################
def mainMenuKeyboard():
    options = [['Текущий баланс'],['Создать карточку']]
    return ReplyKeyboardMarkup(options)

def cancelKeyboard():
    options = [['Отмена']]
    return ReplyKeyboardMarkup(options, one_time_keyboard=True)

def createCardKeyboard():
    options = [['Сегодня'],['Календарь'],['Отмена']]
    return ReplyKeyboardMarkup(options, one_time_keyboard=True)

def daysOfMonthKeyboard():
    options = getOptionsForDaysOfMonthKeyboard()
    return ReplyKeyboardMarkup(options, one_time_keyboard=True)

def confirmKeyboard():
    options = [['Да'],['Отмена']]
    return ReplyKeyboardMarkup(options, one_time_keyboard=True)

#########################Keyboards############################

#########################Utils############################
def getOptionsForDaysOfMonthKeyboard():
    options = []
    rowOptions = []
    now = datetime.datetime.now()
    daysInMonth = calendar.monthrange(now.year, now.month)[1]
    count = 1
    while count <= daysInMonth:
        strCount = str(count)
        if len(rowOptions) >= 4 or count == daysInMonth:
            rowOptions.append(strCount)
            options.append(rowOptions)
            rowOptions = []
        else: 
            rowOptions.append(strCount)

        count += 1
    return options

def getStringAsDateAndValidate(message):
    dateStrResult = ''
    if len(message) < 3:
        now = datetime.datetime.now()
        dateStrResult = str(now.year)+'-'+str(now.month)+'-'+message
    else:
        dateStrResult = message
    
    dateStrForValidate = dateStrResult + ' 00:00:00'
    dateObject = datetime.datetime.strptime(dateStrForValidate, '%Y-%m-%d %H:%M:%S')
    return dateStrResult

def createUserIfItNeed(userId):
     if userId not in usersTelegram:
        usersTelegram[userId] = UserTelegram()

def refreshUser(user):
    user.login = None
    user.password = None
    user.exist = False
    user.contact = None

def throwExceptionIfContactEmpty(contact):
    totalSize = int(contact['totalSize'])
    if totalSize < 1:
        raise Exception('Contact empty')

#########################Utils############################

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler('end',end))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://frozen-scrubland-72051.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()