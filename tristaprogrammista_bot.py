import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Define the bot token as a variable
TRISTA_BOT_TOKEN = "8032258559:AAEDdGjciGE5egx1frzBZFdGViOLq1lPObk"

# # Retrieve the bot token from the environment variable
# TRISTA_BOT_TOKEN = os.getenv("TRISTA_BOT_TOKEN")
# if not TRISTA_BOT_TOKEN:
#     raise ValueError("Bot token not found! Ensure TRISTA_BOT_TOKEN is set.")

# Define a function to handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()
    # Check if the message is "300", "trista", or "триста"
    if user_message in ["300", "trista", "триста"]:
        await update.message.reply_text("otsosi u programmista")
    else:
        await update.message.reply_text("Wrong word! I expect 300\\trista\триста")

# Define a start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hi! Please, enter word 300\\trista\триста")

def main() -> None:
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token(TRISTA_BOT_TOKEN).build()

    # Add handlers for start command and messages
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()