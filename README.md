# iron-id-bot

A Telegram inline bot that adds a touch of humor to your messages by tagging them with unique UUIDs. Choose from Irony, Sarcasm, or Meme styles to spice up your conversations in any chat.

## Inspiration

This project was inspired by the [@opensource_findings](https://t.me/opensource_findings) Telegram channel and its community, whose insights and open source discoveries provided valuable motivation and guidance.


## Features

- Responds to inline queries with three styled message templates.
- Each message includes a unique UUID for easy tracking.
- Simple commands: `/start` and `/help`.

## Usage

1. In any chat, type `@<bot_username> <your message>`
2. Select a style (Irony, Sarcasm, Meme) from the suggestions.
3. Send the generated message with a unique UUID tag.

## Requirements

- Python 3.13+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library

## Installation

Set environment variables:

```sh
export BOT_TOKEN='your_bot_token'
export BOT_USERNAME='your_bot_username'
```

Run the bot:
```sh
uv run bot.py
```

## License

MIT License