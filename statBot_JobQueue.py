from telegram.ext import Updater, Dispatcher, JobQueue
import telegram.ext
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

try:
    updater = Updater(token=TOKEN,
                  use_context=True,
                  request_kwargs=REQUEST_KWARGS)
except Exception as e:
    print(e)

j = updater.job_queue
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def callback_minute(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='@zasodush', text="Text every minute")

minute_job = j.run_once(callback_minute, 60)
minute_job.enabled = False
updater.start_polling()
