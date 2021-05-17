import logging
import calendar
import datetime
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
    def __init__(self):
        self.date = None
        self.amount = None
        self.description = None
        self.keeper = None

usersTelegram = {}

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    
    userId = update._effective_user.id
    createUserIfItNeed(userId)
    isUserLog = usersTelegram[userId].exist
    if isUserLog:
        update.message.reply_text('Вы уже зарегистрированы!', reply_markup=ReplyKeyboardRemove())
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

def echoForExistUser(update,context):
    message = update.message.text.lower()
    userId = update._effective_user.id
    user = usersTelegram[userId]
    if message == 'текущий баланс':
        userContactId = user.contact['records'][0]['Id']
        balance = sf.apexecute('Contact/'+userContactId, method='GET')
        update.message.reply_text(str(balance),
                            reply_markup=mainMenuKeyboard())
    elif message == 'создать карточку':
        user.card = Card()
        update.message.reply_text('На какой день желаете создать карточку?',
                            reply_markup=createCardKeyboard())
    elif user.card != None:
        creatingCard(update,user,message)
    
    update.message.reply_text('ты не должен видеть это сообщение')

def creatingCard(update,user,message):
    update.message.reply_text('creatingCard')
    if user.card.date == None or user.card.date == True:
        creatingCardDate(update,user,message)
    elif user.card.amount == None or user.card.amount == True:
        creatingCardAmount(update,user,message)
    elif user.card.description == None or user.card.description == True:
        creatingCardDecription(update,user,message)

def creatingCardDate(update,user,message):
    update.message.reply_text('creatingCardDate ' + str(user.card.date))
    if user.card.date == None:
        creatingCardDateNone(update,user,message)
    elif user.card.date == True:
        update.message.reply_text('True')
        getDateFromString(update,message)

def creatingCardDateNone(update,user,message):
    if message == 'сегодня':
        'here should be code'
    elif message == 'календарь':
        update.message.reply_text('Выберите число')
        replyMessage = """Или Введите дату вручную(день-месяц-число)
Пример:
2021-03-31
        """
        update.message.reply_text(replyMessage,
                            reply_markup=daysOfMonthKeyboard())
    elif message == 'отмена':
        update.message.reply_text('Что вы хотите сделать?',
                            reply_markup=mainMenuKeyboard())
    user.card.date = True

def creatingCardAmount(update,user,message):
    ''
def creatingCardDecription(update,user,message):
    ''

def getDateFromString(update,message):
    if len(message) < 3:
        now = datetime.datetime.now()
        dateStr = str(now.year)+'-'+str(now.month)+'-'+message
        dateObject = datetime.strptime(dateStr, '%Y-%m-%d').date()
        update.message.reply_text(str(dateObject),
                            reply_markup=ReplyKeyboardRemove())

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def end(update, context):
    userId = update._effective_user.id
    usersTelegram.pop(userId)
    update.message.reply_text('До свидания!',
                            reply_markup=ReplyKeyboardRemove())

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
        #str(user.contact['records'][0]['Id'])
        # x = bool(user.contact)
        # if bool:
        #     update.message.reply_text('Авторизация прошла успешно ' + str(user.contact))
        # else:
        #     update.message.reply_text('Неправильный логин или пароль.Попробуйте Снова')

#########################Keyboards############################
def mainMenuKeyboard():
    options = [['Текущий баланс'],['Создать карточку']]
    return ReplyKeyboardMarkup(options)

def createCardKeyboard():
    options = [['Сегодня'],['Календарь'],['Отмена']]
    return ReplyKeyboardMarkup(options, one_time_keyboard=True)

def daysOfMonthKeyboard():
    options = getOptionsForDaysOfMonthKeyboard()
    return ReplyKeyboardMarkup(options, one_time_keyboard=True)

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
        # if (count == daysInMonth):
        #     lenOptions = len(options)
        #     options[lenOptions].append(strCount)
        # elif (len(rowOptions) >= 4):
        #     rowOptions.append(strCount)
        #     options.append(rowOptions)
        #     rowOptions = []
        # else:
        #     rowOptions.append(strCount)
        count += 1
    return options



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


    # OrderedDict([
    # ('totalSize', 1), 
    # ('done', True), 
    # ('records', [OrderedDict([
    #                 ('attributes', OrderedDict([
    #                                 ('type', 'Contact'), 
    #                                 ('url', '/services/data/v42.0/sobjects/Contact/0035g000003X49iAAC')])), 
    #                 ('Id', '0035g000003X49iAAC'), 
    #                 ('Email', 'worker2@gmail.com')])])])

    #  OrderedDict([
    #      ('attributes', OrderedDict([
    #          ('type', 'Contact'), 
    #          ('url', '/services/data/v42.0/sobjects/Contact/0035g000003X49iAAC')])), 
    #      ('Id', '0035g000003X49iAAC'), 
    #      ('Email', 'worker2@gmail.com')])

