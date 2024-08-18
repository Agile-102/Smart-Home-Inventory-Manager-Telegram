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
import spacy

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')

TOKEN = '7056035301:AAGfskXNZ6JxZjxOt0yjcDvaegZ3zcUMO9Q'
BOT_USERNAME: Final = '@SHIM_Tele_Bot'
API_URL = 'https://smart-home-inventory-manager-apyq67agg-w-zheng-jies-projects.vercel.app'

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
    context.user_data['awaiting_room'] = True
    await update.message.reply_text('Please enter the room details in the format: room_name')

async def handle_add_room_message(update: Update, context: ContextTypes.DEFAULT_TYPE, room_name=None):
    if room_name is None:
        room_name = update.message.text.strip()
    
    user_id = str(update.message.from_user.id)
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{API_URL}/room/addRoom', json={'username': user_id, 'roomName': room_name}, headers=headers)

        if response.status_code == 200:
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

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{API_URL}/room/getAllRooms', json={'username': user_id}, headers=headers)

        if response.status_code == 200:
            try:
                rooms = response.json()
                if rooms:
                    room_list = "\n".join([f"- {room}" for room in rooms])
                    await update.message.reply_text(f'Your rooms:\n{room_list}')
                else:
                    await update.message.reply_text('You have no rooms added yet.')
            except ValueError as json_err:
                print(f'JSON decode error: {json_err}')
                await update.message.reply_text('Failed to decode the response. Please try again later.')
        elif response.status_code == 503:
            await update.message.reply_text('No rooms found for this user.')
        elif response.status_code == 501:
            await update.message.reply_text('User not found, please initiate contact with the bot.')
        else:
            print(f'Failed to retrieve rooms. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text('Failed to retrieve rooms. Please try again later.')
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text('An error occurred while retrieving the rooms.')

def extract_intent_and_entities(text):
    doc = nlp(text)
    intent = None
    room_name = None
    
    # Check if the text implies an 'add room' action
    if 'add' in text.lower() and 'room' in text.lower():
        intent = 'add_room'
    elif 'view' in text.lower() and 'room' in text.lower():
        intent = 'view_rooms'
    
    # Extract possible room names from entities (this part is mainly for the 'add room' action)
    for ent in doc.ents:
        if ent.label_ in {'ORG', 'GPE', 'FACILITY', 'LOC'}:  # Adjust labels based on use case
            room_name = ent.text
    
    # Additional check for room name not captured by NER (this part is mainly for the 'add room' action)
    if not room_name:
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
        # Assume the last significant token could be the room name
        if tokens:
            room_name = tokens[-1]

    return intent, room_name

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Check if the message is from a user interacting with an existing command
    if context.user_data.get('awaiting_subspace'):
        await handle_add_subspace_message(update, context)
    elif context.user_data.get('awaiting_room'):
        await handle_add_room_message(update, context)
    else:
        # Use spaCy to extract intent and entities
        intent, room_name = extract_intent_and_entities(text)
        
        if intent == 'add_room' and room_name:
            # Call the function to add a room with the extracted name
            await handle_add_room_message(update, context, room_name)
        elif intent == 'view_rooms':
            # Call the function to view rooms
            await view_rooms_command(update, context)
        else:
            await update.message.reply_text("I couldn't understand that. Please use a command or specify the action clearly.")

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

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)