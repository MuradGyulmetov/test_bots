from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    'Reply with keyboard when user send /start command'

    inline_keyboard = [[InlineKeyboardButton(text="Seria A", callback_data="Seria A"),
                        InlineKeyboardButton(text="Bundesliga", callback_data="Bundesliga")],

                       [InlineKeyboardButton(text="Seria A and Bundesliga", callback_data="Seria A and Bundesliga")]]

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    update.message.reply_text("Please choose: ", reply_markup=reply_markup)

def get_callback_query(update, context):
    query = update.callback_query
    query.edit_message_text(text="You've chosen: {}".format(query.data))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
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

    updater = Updater(token=TOKEN,
                      use_context=True,
                      request_kwargs=REQUEST_KWARGS,
                      )
    dispatcher = updater.dispatcher

    start_handler = CommandHandler("start", start)
    callback_query_handler = CallbackQueryHandler(get_callback_query)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(callback_query_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()
