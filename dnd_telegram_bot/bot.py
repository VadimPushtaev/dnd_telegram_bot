#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from pathlib import Path

from dice_parser.parser import DiceParser
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def roll_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if "parser" not in context.user_data:
        context.chat_data["parser"] = DiceParser()

    to_roll = ''.join(context.args)
    dice_parser = context.user_data["parser"]
    result = dice_parser.parse(to_roll)

    logger.info("Rolled '%s', got [%s] `%s`", to_roll, result.string, result.value)

    await update.message.reply_text(str(result.value))


def main() -> None:
    """Start the bot."""
    with Path(__file__).parent.parent.joinpath("token").open("r") as token_file:
        token = token_file.read().strip()
        application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("roll", roll_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)
