import logging
import os
import sys
from dataclasses import dataclass
from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    InlineQueryHandler,
)

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


@dataclass
class MessageTemplate:
    """Simple message template style with title, emoji, and alias."""

    title: str
    emoji: str
    alias: str

    def full_msg_id(self, msg_id: str) -> str:
        """Return alias with message id."""
        return f'{self.alias}id:{msg_id}'

    def build_msg(self, query: str, msg_id: str) -> str:
        """Return full formated message."""
        return f'{query}\n\n{self.full_msg_id(msg_id)}'


MESSAGE_TEMPLATES: tuple[MessageTemplate, ...] = (
    MessageTemplate('Irony', '🤨', 'iron'),
    MessageTemplate('Sarcasm', '😒', 'sarcasm'),
    MessageTemplate('Meme', '😂', 'meme'),
)

BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')

START_REPLY_TEXT = (
    "Hello! 👋 I'm a Telegram inline bot that adds a touch of humor to your "
    f'messages. Type your text after typing @{BOT_USERNAME} in any chat to '
    'get fun replies in Irony, Sarcasm, or Meme styles — each tagged with a '
    'unique UUID for easy tracking.\n\nUse /help to see how to use me.'
)

HELP_REPLY_TEXT = (
    'How to use this bot:\n\n'
    f'1. In any chat, type @{BOT_USERNAME} <your message>\n'
    '2. Choose a style (Irony, Sarcasm, or Meme)\n'
    '3. Send the generated message with a unique UUID tag.\n\n'
    'This makes your conversations more expressive and fun!'
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command by sending a welcome message."""
    if not update.message or not update.message.from_user:
        return
    logger.debug('Received /start from user %s', update.message.from_user.id)
    await update.message.reply_text(START_REPLY_TEXT)


async def help_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle the /help command by sending usage instructions."""
    if not update.message or not update.message.from_user:
        return
    logger.debug('Received /help from user %s', update.message.from_user.id)
    await update.message.reply_text(HELP_REPLY_TEXT)


async def inline_query(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle inline queries by returning message templates with UUID tags."""
    if not update.inline_query:
        return
    inline_query_text = update.inline_query.query
    message_uuid = str(uuid4())

    if not inline_query_text:
        return

    logger.debug(
        'Handling inline query: "%s" with UUID: %s',
        inline_query_text,
        message_uuid,
    )

    msg_templates = [
        InlineQueryResultArticle(
            id=str(uuid4()),
            title=f'{template.emoji} {template.title}',
            input_message_content=InputTextMessageContent(
                template.build_msg(inline_query_text, message_uuid)
            ),
            description=template.full_msg_id(message_uuid),
        )
        for template in MESSAGE_TEMPLATES
    ]

    await update.inline_query.answer(msg_templates)


def main() -> None:
    """Start the Telegram bot application."""
    if not BOT_TOKEN or not BOT_USERNAME:
        logger.error(
            'BOT_TOKEN and BOT_USERNAME must be set in environment variables.'
        )
        sys.exit('Missing BOT_TOKEN or BOT_USERNAME environment variables.')

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))

    application.add_handler(InlineQueryHandler(inline_query))

    logger.info('Starting bot polling...')
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
