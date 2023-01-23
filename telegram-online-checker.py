import asyncio
import datetime
import logging
import zoneinfo
import time
import os

from pyrogram import Client, enums
import telebot


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class TimeDefinition:
    SECONDS = 1
    MINUTES = 60
    HOURS = 60 * 60


def sleep(timeout_seconds):
    logging.info('Sleep for {}'.format(str(datetime.timedelta(seconds=timeout_seconds))))
    time.sleep(timeout_seconds)


async def main():
    client_name = 'telegram'
    api_id = os.environ['TELEGRAM_API_ID']
    api_hash = os.environ['TELEGRAM_API_HASH']
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    target_user = os.environ['TELEGRAM_TARGET_USER']
    target_chat = os.environ['TELEGRAM_TARGET_CHAT']

    bot = telebot.TeleBot(bot_token, parse_mode=None)

    async with Client(client_name, api_id, api_hash) as telegram:
        while True:
            user = await telegram.get_users(target_user)

            logging.info(user.last_online_date)
            logging.info(user.status)

            if user.status == enums.UserStatus.ONLINE:
                bot.send_message(target_chat, '{} проснулась 🤤'.format(target_user))
                logging.info('Send notification')
                sleep(5 * TimeDefinition.HOURS)
            else:
                tz = zoneinfo.ZoneInfo("Europe/Moscow")
                hour_now = datetime.datetime.now().replace(tzinfo=tz).hour
                hour_last_online = user.last_online_date.replace(tzinfo=tz).hour
                if hour_now < hour_last_online and hour_now < 5:
                    sleep((5 - hour_now) * TimeDefinition.HOURS)
                elif hour_now - hour_last_online < 5:
                    sleep((5 - (hour_now - hour_last_online)) * TimeDefinition.HOURS)
                else:
                    sleep(3 * TimeDefinition.MINUTES)

asyncio.run(main())
