# import logging
# from typing import Dict
# import os

# from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
# from telegram.ext import (
#     Updater,
#     CommandHandler,
#     MessageHandler,
#     Filters,
#     ConversationHandler,
#     CallbackContext,
# )


# PORT = int(os.environ.get('PORT', 5000))
# TOKEN = '1841783209:AAHrDitzlrEGtxSyCUgRr2oSl-vQsgBzPK8'

# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)

# CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

# reply_keyboard = [
#     ['Age', 'Favourite colour'],
#     ['Number of siblings', 'Something else...'],
#     ['Done'],
# ]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


# def facts_to_str(user_data: Dict[str, str]) -> str:
#     facts = list()

#     for key, value in user_data.items():
#         facts.append(f'{key} - {value}')

#     return "\n".join(facts).join(['\n', '\n'])


# def start(update: Update, _: CallbackContext) -> int:
#     update.message.reply_text(
#         "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
#         "Why don't you tell me something about yourself?",
#         reply_markup=markup,
#     )

#     return CHOOSING


# def regular_choice(update: Update, context: CallbackContext) -> int:
#     text = update.message.text
#     context.user_data['choice'] = text
#     update.message.reply_text(f'Your {text.lower()}? Yes, I would love to hear about that!')

#     return TYPING_REPLY


# def custom_choice(update: Update, _: CallbackContext) -> int:
#     update.message.reply_text(
#         'Alright, please send me the category first, for example "Most impressive skill"'
#     )

#     return TYPING_CHOICE


# def received_information(update: Update, context: CallbackContext) -> int:
#     user_data = context.user_data
#     text = update.message.text
#     category = user_data['choice']
#     user_data[category] = text
#     del user_data['choice']

#     update.message.reply_text(
#         "Neat! Just so you know, this is what you already told me:"
#         f"{facts_to_str(user_data)} You can tell me more, or change your opinion"
#         " on something.",
#         reply_markup=markup,
#     )

#     return CHOOSING


# def done(update: Update, context: CallbackContext) -> int:
#     user_data = context.user_data
#     if 'choice' in user_data:
#         del user_data['choice']

#     update.message.reply_text(
#         f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
#         reply_markup=ReplyKeyboardRemove(),
#     )

#     user_data.clear()
#     return ConversationHandler.END


# def main() -> None:
#     # Create the Updater and pass it your bot's token.
#     updater = Updater(TOKEN)

#     # Get the dispatcher to register handlers
#     dispatcher = updater.dispatcher

#     # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],
#         states={
#             CHOOSING: [
#                 MessageHandler(
#                     Filters.regex('^(Age|Favourite colour|Number of siblings)$'), regular_choice
#                 ),
#                 MessageHandler(Filters.regex('^Something else...$'), custom_choice),
#             ],
#             TYPING_CHOICE: [
#                 MessageHandler(
#                     Filters.text & ~(Filters.command | Filters.regex('^Done$')), regular_choice
#                 )
#             ],
#             TYPING_REPLY: [
#                 MessageHandler(
#                     Filters.text & ~(Filters.command | Filters.regex('^Done$')),
#                     received_information,
#                 )
#             ],
#         },
#         fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
#     )

#     dispatcher.add_handler(conv_handler)

#     # Start the Bot
#     updater.start_webhook(listen="0.0.0.0",
#                           port=int(PORT),
#                           url_path=TOKEN)
#     updater.bot.setWebhook('https://frozen-scrubland-72051.herokuapp.com/' + TOKEN)

#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()


# if __name__ == '__main__':
#     main()


import logging
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
    if message == 'текущий баланс':
        'here should be code'
        update.message.reply_text('101')
    elif message == 'создать карточку':
        reply_keyboard = createCardKeyboard()
        update.message.reply_text('На какой день желаете создать карточку?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    elif message == 'сегодня':
        'here should be code'
    elif message == 'календарь':
        'here should be code'
    elif message == 'отмена':
        reply_keyboard = mainMenuKeyboard()
        update.message.reply_text('Что вы хотите сделать?',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    update.message.reply_text('ты не должен видеть это сообщение')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def end(update, context):
    userId = update._effective_user.id
    usersTelegram.pop(userId)

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
            reply_keyboard = mainMenuKeyboard()
            update.message.reply_text('Авторизация прошла успешно',
                            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
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

#########################Keyboards############################
def mainMenuKeyboard():
    return [['Текущий баланс', 'Создать карточку']]

def createCardKeyboard():
    return [['Сегодня','Календарь','Отмена']]

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

