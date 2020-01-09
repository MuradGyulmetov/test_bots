from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging


TOKEN = '1028159381:AAEbO0IMSHfDdplDOmIUZAndHAmbhqysUuY'
REQUEST_KWARGS = {
    'proxy_url': 'socks4://171.103.9.22:4145/',
    # Optional, if you need authentication:
    'urllib3_proxy_kwargs': {
        'assert_hostname': 'False',
        'cert_reqs': 'CERT_NONE'
        # 'username': 'user',
        # 'password': 'password'
    }
}
#1) create Updater to get data from user
try:
    updater = Updater(token=TOKEN,
                      use_context=True,
                      request_kwargs=REQUEST_KWARGS)
except Exception as e:
    print(e)
#2)create Dispatcher to handle data from Updater
dispatcher = updater.dispatcher

#Create JobQueue
job = updater.job_queue
#3)create Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
#4)create callback function to return the result
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello I'm statBot")

def m_list(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.update_id)

def echo(update, context):
    reply = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    result = list()
    result.append(InlineQueryResultArticle(
                                    id=query,
                                    title="Returned result",
                                    input_message_content=InputTextMessageContent(message_text=query.upper())
    ))
    context.bot.answer_inline_query(update.inline_query.id, results=result)

def callback_30(context):
    context.bot.send_message(chat_id='@zasodush', text='Text every 30 sec')

#5)create handler to math the command from user to callback function
start_handler = CommandHandler('start', start)
#Handler for function wich return list of words
list_handler = CommandHandler('list', m_list)
#This is MessageHandler, is used along with Filters
message_handler = MessageHandler(Filters.text, echo)
#This is inline query handler
inline_handler = InlineQueryHandler(inline_caps)
#6)add handler to dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(inline_handler)

every_30 = job.run_repeating(callback_30, 30, first=0)
updater.start_polling()
