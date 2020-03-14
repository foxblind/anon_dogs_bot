import logging

from telegram.ext import Updater, Dispatcher
from handlers import start_handler, dialog_handler, admin_handler




class Bot:
    def __init__(self, token):
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)
        self._updater = Updater(token, use_context=True)
        self._dispatcher: Dispatcher = self._updater.dispatcher

        self._set_handlers()

    def _set_handlers(self):
        self._dispatcher.add_handler(start_handler.handle())

        for handler in admin_handler.handle():
            self._dispatcher.add_handler(handler)

        for handler in dialog_handler.handle():
            self._dispatcher.add_handler(handler)



    def start(self):
        self._updater.start_polling()
        self._updater.idle()


