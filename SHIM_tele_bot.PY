
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
add_subspace - Adds a new subspace to an existing space
view_rooms - View all rooms / spaces for the user
"""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am SHIM Bot! Select /help for more info!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Select /add_room to add rooms\nSelect /view_rooms to view your rooms\nSelect /add_subspace to add a subspace')

async def add_room_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_room'] = True
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

    context.user_data['awaiting_room'] = False

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

async def add_subspace_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Store the state that we are waiting for a subspace name
    context.user_data['awaiting_subspace'] = True
    context.user_data['space_name'] = None  # Clear previous space name if any
    await update.message.reply_text('Please enter the name of the space to which you want to add a subspace.')

async def handle_add_subspace_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = str(update.message.from_user.id)
    
    if context.user_data.get('awaiting_subspace'):
        if context.user_data.get('space_name') is None:
            # Store the space name
            context.user_data['space_name'] = text
            await update.message.reply_text('Please enter the subspace name.')
        else:
            space_name = context.user_data['space_name']
            sub_space_name = text
            try:
                response = requests.get(f'{API_URL}/spaces', params={'user_id': user_id})
                if response.status_code == 200:
                    spaces = response.json()
                    print("Spaces:", spaces)  # Debug line
                    space = next((space for space in spaces if space['space_name'] == space_name), None)
                    if space:
                        space_id = space.get('_id')
                        if space_id:
                            headers = {'Content-Type': 'application/json'}
                            print(f"Posting subspace with space_id: {space_id} and sub_space_name: {sub_space_name}")  # Debug line
                            response = requests.post(f'{API_URL}/sub_spaces', json={'space_id': str(space_id), 'sub_space_name': sub_space_name}, headers=headers)

                            if response.status_code == 201:
                                await update.message.reply_text('Subspace added successfully!')
                            else:
                                print(f'Failed to add subspace. Status code: {response.status_code}, Response: {response.text}')
                                await update.message.reply_text('Failed to add subspace. Please check the details and try again.')
                        else:
                            await update.message.reply_text(f'No id found for space: {space_name}')
                    else:
                        await update.message.reply_text(f'No space found with name: {space_name}')
                else:
                    print(f'Failed to retrieve spaces. Status code: {response.status_code}, Response: {response.text}')
                    await update.message.reply_text('Failed to retrieve spaces. Please try again later.')
            except Exception as e:
                print(f'Exception occurred: {e}')
                await update.message.reply_text('An error occurred while adding the subspace.')

            # Reset state
            context.user_data['awaiting_subspace'] = False
            context.user_data['space_name'] = None
    else:
        await update.message.reply_text('Please start the /add_subspace command first.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Check if the message is from a user interacting with an existing command
    if context.user_data.get('awaiting_subspace'):
        await handle_add_subspace_message(update, context)
    elif context.user_data.get('awaiting_room'):
        await handle_add_room_message(update, context)
    else:
        # Default behavior
        await update.message.reply_text("Please use a command to interact with the bot.")

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
    app.add_handler(CommandHandler('add_subspace', add_subspace_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)