
"""
Smart-Home-Inventory-Manager / SHIM Telegram Bot
Binded to Telegram User: WZJ99
Telegram: https://t.me/WZJ99

Database hosted by MongoDB
API hosted by Vercel
MongoDB and Vercel Project created by Wong Zheng Jie

Make sure to pip install python-telegram-bot and requests
Run the command:
pip install python-telegram-bot requests

Run the script with command:
python SHIM_tele_bot.PY

"""

import requests
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '7056035301:AAGfskXNZ6JxZjxOt0yjcDvaegZ3zcUMO9Q'
BOT_USERNAME: Final = '@SHIM_Tele_Bot'
API_URL = 'https://smart-home-inventory-manager-ht6vqwtnw-w-zheng-jies-projects.vercel.app/api'

# Commands
"""
start - Starts the bot
help - Provides help for SHIM Tele Bot
add_room - Adds a new room / space
view_rooms - View all rooms / spaces for the user
"""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am SHIM Bot! Select /help for more info!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Select /add_room to add rooms\nSelect /view_rooms to view your rooms')

async def add_room_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the room details in the format: room_name')

async def handle_add_room_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    room_name = update.message.text.strip()
    user_id = str(update.message.from_user.id)
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{API_URL}/spaces', json={'user_id': user_id, 'space_name': room_name}, headers=headers)

        if response.status_code == 201:
            await update.message.reply_text('Room added successfully!')
        else:
            print(f'Failed to add room. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text('Failed to add room. Please check the details and try again.')
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text('An error occurred while adding the room.')

async def view_rooms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)  # Ensure user_id is a string

    # Sending data to the API for retrieving rooms
    try:
        response = requests.get(f'{API_URL}/spaces', params={'user_id': user_id})

        if response.status_code == 200:
            try:
                rooms = response.json()
                if rooms:
                    room_list = "\n".join([f"- {room['space_name']}" for room in rooms])
                    await update.message.reply_text(f'Your rooms:\n{room_list}')
                else:
                    await update.message.reply_text('You have no rooms added yet.')
            except ValueError as json_err:
                print(f'JSON decode error: {json_err}')
                await update.message.reply_text('Failed to decode the response. Please try again later.')
        else:
            print(f'Failed to retrieve rooms. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text('Failed to retrieve rooms. Please try again later.')
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text('An error occurred while retrieving the rooms.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text.strip()

    print(f'User ({update.message.chat.id}) in private: "{text}"')

    # Assume any non-command text input is a room name
    await handle_add_room_message(update, context)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Bot Starting...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add_room', add_room_command))
    app.add_handler(CommandHandler('view_rooms', view_rooms_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex('add_room'), handle_add_room_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)