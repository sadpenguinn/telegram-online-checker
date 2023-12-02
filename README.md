# telegram-online-checker

## Description

Bot notifies when target Telegram user become online
after long offline period.

## Dependencies

### Telegram Bot

Provide it's token with `TELEGRAM_BOT_TOKEN`.
Also, you should provide chat ID with this bot in `TELEGRAM_TARGET_CHAT`.

### Telegram API

Provide credentials with `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`.

### Target Telegram User

You must fill his ID in `TELEGRAM_TARGET_USER`.

## Build & Run

```
docker build -t telegram-online-checker -f Dockerfile . && \
docker run -e TELEGRAM_API_ID={your-id} -e TELEGRAM_API_HASH={your-hash} -e TELEGRAM_BOT_TOKEN={your-bot-token} -e TELEGRAM_TARGET_CHAT={your-chat-id} -e TELEGRAM_TARGET_USER={target-user-id} telegram-online-checker
```
