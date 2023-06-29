import logging


async def on_startup(_):
    logging.info("Bot was started")


# функция при выключении бота
async def on_shutdown(_):
    logging.info('Bot was stopped')
