# Water Consumption Tracker Bot

## Description

This Telegram bot is designed to help users track their water consumption. The user can enter the amounts of water consumed in mililiters and view their past consumptions based on the date selected and the total amount of water consumed.

## Telegram Bot Setup

1. Create a new bot using the BotFather on Telegram
2. Copy the token provided by the BotFather
3. Edit the .env file and add the token to the TELEGRAM_TOKEN variable

## Running the bot

1. Clone the repository

```bash
git clone
```

2. Build the docker image

```bash
docker build -t water-consumption-bot .
```

3. Run the docker container

```bash
docker run --restart unless-stopped -d water-consumption-bot
```

## Usage

1. Start the bot by sending the /start command
2. Enter the amount of water consumed in mililiters sending the /add command followed by the amount
3. View the total amount of water consumed by sending the /view command
4. Select a date to view the amount of water consumed on that date.
