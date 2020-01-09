from telegram.ext import Updater, Dispatcher, CommandHandler
import telegram

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

updater = Updater(token=TOKEN, use_context=True, request_kwargs=REQUEST_KWARGS)
dispatcher = updater.dispatcher

def send_alarm(context):
    context.bot.send_message(chat_id=context.job.context, text='ALARM!')

def callback_timer(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text="Setting alarm to 30 sec, to stop send /stop command")

    context.job_queue.run_repeating(send_alarm, 30, 0, context=update.message.chat_id)

def stop_alarm(update: telegram.Update, context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Timer stopped")
    context.job_queue.stop()


timer_handler = CommandHandler('timer', callback_timer)
stop_handler = CommandHandler('stop', stop_alarm)
dispatcher.add_handler(timer_handler)
dispatcher.add_handler(stop_handler)

updater.start_polling()