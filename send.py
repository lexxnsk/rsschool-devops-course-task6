from telethon import TelegramClient
import time
import asyncio
import os

# Your 'api_id' and 'api_hash' (you get these from https://my.telegram.org/auth)
# api_id = 'xxxxxxxx'  # Replace with your actual API ID
# api_hash = 'yyyyyyyy'  # Replace with your actual API hash

# Your phone number for initial login
# phone_number = 'zzzzzzzz'  # Replace with your phone number (with country code)

# Get the values from environment variable
api_id = os.getenv('API_ID')  
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

# print(api_id, api_hash, phone_number)  # Just for testing

# The bot's username (e.g., 'my_bot')
bot_username = 'tristaprogrammista_bot'

# The message you want to send to the bot
message_to_send = "300"

# Create the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

async def send_and_receive():
    # Connect to the client
    await client.start(phone=phone_number)  # Automatically handle phone number

    # Send a message to the bot
    sent_message = await client.send_message(bot_username, message_to_send)
    # print(f"Sent: {sent_message}")

    # Wait for a reply from the bot, only process messages with an ID greater than sent_message.id
    # print("Waiting for bot's reply...")
    async for message in client.iter_messages(bot_username):
        # print(f"Bot's reply: {message}")

        # Ensure the message is from the bot (out=False means it's incoming)
        if message.id == sent_message.id - 1 and not message.out:
            print(f"Bot's reply: {message.text}")
            break  # Exit after receiving the first valid reply
    else:
        # If no valid message was received after the loop finishes
        raise ValueError("Bot is dead")

    await client.disconnect()

# Run the async function
asyncio.run(send_and_receive())