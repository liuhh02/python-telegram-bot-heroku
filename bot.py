import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.exist = False
        self.contact = None

usersTelegram = {}

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    userId = update._effective_user.id
    createUserIfItNeed(userId)
    isUserLog = usersTelegram[userId].exist
    if isUserLog:
        update.message.reply_text('Вы уже зарегистрированы!')
    else:
        update.message.reply_text('Введите логин')
    # sf.Contact.create({'LastName':'simple_salesforce','Email':'example@example.com'})

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    userId = update._effective_user.id

    if userId not in usersTelegram:
        start(update,context)
        return

    message = update.message.text.lower()
    if usersTelegram[userId].exist == False:
        login(update, context)
    elif message == '/bye' or message == '/end':
        usersTelegram.pop(userId)
    else:
        update.message.reply_text('ты не должен видеть это сообщение')

    #update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

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
            update.message.reply_text('Авторизация прошла успешно ' + str(user.contact))
        except Exception:
            update.message.reply_text('Неправильный логин или пароль.Попробуйте Снова')
            refreshUser(user)
            start(update,context)
            return
        # x = bool(user.contact)
        # if bool:
        #     update.message.reply_text('Авторизация прошла успешно ' + str(user.contact))
        # else:
        #     update.message.reply_text('Неправильный логин или пароль.Попробуйте Снова')

def createUserIfItNeed(userId):
     if userId not in usersTelegram:
        usersTelegram[userId] = UserTelegram(None,None)

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
    global bot
    bot = updater.bot
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

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