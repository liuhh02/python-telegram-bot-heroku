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
username = None
password = None
user = None

class UserTelegram:
    def __init__(self, login, password, id):
        self.login = login
        self.password = password
        self.id = id

usersTelegram = []

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def start(update, context):
    """Send a message when the command /start is issued."""
    
    update.message.reply_text(update.update_id)
    sf.Contact.create({'LastName':'simple_salesforce','Email':'example@example.com'})

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    global user
    if user == None:
        login(update)
    else:
        update.message.reply_text('ты не должен видеть это сообщение')

    #update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def login(update):
    global username
    global password
    global user
    if username == None:
       username =  update.message.text
       update.message.reply_text('Введите пароль')
    else:
        password = update.message.text
        user = 'User'
        update.message.reply_text('Авторизация прошла успешно')

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