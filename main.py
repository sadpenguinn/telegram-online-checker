import asyncio
import datetime
import logging
import zoneinfo
import time
import os

from pyrogram import Client, enums
import telebot
import dotenv

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger('pyrogram').setLevel(logging.WARNING)


class TimeDefinition:
    SECONDS = 1
    MINUTES = 60
    HOURS = 60 * 60


class LastSeenState:
    hour = 0
    day = 0


def sleep(timeout_seconds):
    logging.info('Sleep for {}'.format(str(datetime.timedelta(seconds=timeout_seconds))))
    time.sleep(timeout_seconds)


def last_seen_day_and_hour(user, tz):
    if user.status == enums.UserStatus.ONLINE:
        last_seen_date = datetime.datetime.now().replace(tzinfo=tz)
    else:
        last_seen_date = user.last_online_date.replace(tzinfo=tz)
    return last_seen_date.day, last_seen_date.hour


def same_day_and_hour(current_day, current_hour, previous_day, previous_hour):
    return current_day == previous_day and current_hour == previous_hour


def less_then_5_hours(current_day, current_hour, previous_day, previous_hour):
    err = 'Invalid days/hours range. Day: {}, Hour: {}, PrevDay: {}, PrevHour: {}'.format(current_day, current_hour, previous_day, previous_hour)

    if current_day < previous_day:
        # Сделать проверку по месяцам и годам
        pass

    if current_day == previous_day:
        if current_hour < previous_hour:
            logging.error(err)
            return None
        return current_hour - previous_hour < 5

    hours_past_day = 24 - previous_hour
    return current_hour + hours_past_day < 5


async def main():
    dotenv.load_dotenv()

    api_id = os.environ['TELEGRAM_API_ID']
    api_hash = os.environ['TELEGRAM_API_HASH']
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    target_user = os.environ['TELEGRAM_TARGET_USER']
    target_chat = os.environ['TELEGRAM_TARGET_CHAT']

    tz = zoneinfo.ZoneInfo("Europe/Moscow")
    state = LastSeenState()
    bot = telebot.TeleBot(bot_token, parse_mode=None)

    async with Client(':memory:', api_id, api_hash) as telegram:
        user = await telegram.get_users(target_user)
        state.day, state.hour = last_seen_day_and_hour(user, tz)
        logging.info('Initial day and hour: {}, {}'.format(state.day, state.hour))

        while True:
            user = await telegram.get_users(target_user)
            day, hour = last_seen_day_and_hour(user, tz)
            logging.info('Last day and hour: {}, {}'.format(day, hour))

            if same_day_and_hour(day, hour, state.day, state.hour):

                now = datetime.datetime.now().replace(tzinfo=tz)
                logging.info('Now day and hour: {}, {}'.format(now.day, now.hour))
                if not less_then_5_hours(now.day, now.hour, day, hour):
                    sleep(3 * TimeDefinition.MINUTES)
                    continue

                sleep(1 * TimeDefinition.HOURS)
                continue

            if less_then_5_hours(day, hour, state.day, state.hour):
                sleep(1 * TimeDefinition.HOURS)
                state.day, state.hour = day, hour
                continue
            else:
                bot.send_message(target_chat, '{} проснулась 🤤'.format(target_user))
                logging.info('Send notification')
                sleep(1 * TimeDefinition.HOURS)
                state.day, state.hour = day, hour
                continue


asyncio.run(main())
