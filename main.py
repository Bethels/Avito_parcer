from aiogram.utils import executor
from bot_setup import dp
import handlers
import logging
# ads.register_ads_handlers(dp)
# common.register_common_handlers(dp)
logging.basicConfig(level=logging.INFO)

# handlers.fsm.register_fsm_handlers(dp)
executor.start_polling(dp, skip_updates=True)
