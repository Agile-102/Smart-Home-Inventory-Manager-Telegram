# Information
"""
Smart-Home-Inventory-Manager / SHIM Telegram Bot
Put together by: SIM x UOL Agile Software Projects @Team 102, Aug 2024
Website Information and Support Link: https://shim-web.vercel.app/

Binded to Telegram User: WZJ99
Telegram: https://t.me/WZJ99
"""

# Commands
"""
start - Starts the bot
help - Provides help for SHIM Tele Bot
add_room - Adds a new room / space
view_rooms - View all rooms / spaces for the user
delete_room - deletes a specific room
update_room - updates the name of a room
add_item_to_room - adds an item to a room
view_room_items - views the items in a room
edit_room_item - edit the items in a room
delete_room_item - deletes a specific item from a room
"""

# Pre-requisites and maintenance info
"""
Make sure to pip install python-telegram-bot and requests
Run the command:
pip install python-telegram-bot requests

Run the script with command:
python SHIM_tele_bot.PY
"""

# imports
import requests
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import spacy

# Load the English NLP model
nlp = spacy.load('en_core_web_sm')

TOKEN = '7056035301:AAGfskXNZ6JxZjxOt0yjcDvaegZ3zcUMO9Q'
BOT_USERNAME: Final = '@SHIM_Tele_Bot'
API_URL = 'https://smart-home-inventory-manager-api.vercel.app'

# start and help commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am SHIM Bot! Select /help for more info!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Select /add_room to add rooms\nSelect /view_rooms to view your rooms\nSelect /delete_room to delete a room.\nSelect /update_room to update a room name.\nSelect /edit_room_item to edit an item in a room.')

# Add rooms
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

# View rooms
async def view_rooms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)

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

# Update room name
async def update_room_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_update_room'] = True
    await update.message.reply_text('Please provide the current room name followed by the new room name, e.g., "kitchen1, kitchen2" or "rename kitchen1 to kitchen2".')

async def handle_update_room_message(update: Update, context: ContextTypes.DEFAULT_TYPE, old_name=None, new_name=None):
    if old_name is None or new_name is None:
        await update.message.reply_text('Please provide both the current room name and the new room name.')
        return

    user_id = str(update.message.from_user.id)
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.patch(f'{API_URL}/room/editRoom', json={'username': user_id, 'oldName': old_name, 'newName': new_name}, headers=headers)

        if response.status_code == 200:
            await update.message.reply_text('Room updated successfully!')
        else:
            print(f'Failed to update room. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text('Failed to update room. Please check the details and try again.')
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text('An error occurred while updating the room.')

    context.user_data['awaiting_update_room'] = False

# Delete rooms
async def delete_room_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_room_deletion'] = True
    await update.message.reply_text('Please enter the room name to delete.')

async def handle_delete_room_message(update: Update, context: ContextTypes.DEFAULT_TYPE, room_name=None):
    if room_name is None:
        room_name = update.message.text.strip()

    user_id = str(update.message.from_user.id)
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(f'{API_URL}/room/deleteRoom', json={'username': user_id, 'roomName': room_name}, headers=headers)

        if response.status_code == 200:
            await update.message.reply_text('Room deleted successfully!')
        else:
            print(f'Failed to delete room. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text('Failed to delete room. Please check the details and try again.')
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text('An error occurred while deleting the room.')

    context.user_data['awaiting_room_deletion'] = False

# Add item to room
async def add_item_to_room_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_item'] = True
    await update.message.reply_text('Please enter the room name followed by the item name in the format: room_name, item_name.')

async def handle_add_item_to_room_message(update: Update, context: ContextTypes.DEFAULT_TYPE, room_name=None, item_name=None):
    if room_name is None or item_name is None:
        await update.message.reply_text('Please provide both the room name and the item name.')
        return

    user_id = str(update.message.from_user.id)
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{API_URL}/room/addItem', json={'username': user_id, 'roomName': room_name, 'itemName': item_name}, headers=headers)

        if response.status_code == 200:
            await update.message.reply_text('Item added to room successfully!')
        else:
            print(f'Failed to add item to room. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text('Failed to add item to room. Please check the details and try again.')
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text('An error occurred while adding the item to the room.')

    context.user_data['awaiting_item'] = False

# View items in a room
async def view_room_items_command(update, context, room_name: str):
    user_id = str(update.message.from_user.id)
    api_url = f"{API_URL}/room/getItemsOfRoom"
    
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json={'username': user_id, 'roomName': room_name}, headers=headers)

        if response.status_code == 200:
            items = response.json()
            if isinstance(items, list) and items:
                items_list = "\n".join(items)
                await update.message.reply_text(f"Items in {room_name}:\n{items_list}")
            else:
                await update.message.reply_text(f"No items found in {room_name}.")
        else:
            print(f'Failed to retrieve items. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text("Failed to retrieve items. Please try again.")
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text("An error occurred while retrieving items.")

# Edit item in room
async def edit_room_item_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_item_edit'] = True
    await update.message.reply_text('Please provide the room name, current item name, and the new item name in the format: room_name, current_item_name, new_item_name.')

async def handle_edit_room_item_message(update: Update, context: ContextTypes.DEFAULT_TYPE, room_name=None, old_item_name=None, new_item_name=None):
    if room_name is None or old_item_name is None or new_item_name is None:
        await update.message.reply_text('Please provide the room name, current item name, and the new item name.')
        return

    user_id = str(update.message.from_user.id)
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.patch(f'{API_URL}/room/editItem', json={'username': user_id, 'roomName': room_name, 'oldName': old_item_name, 'newName': new_item_name}, headers=headers)
        # payload for dubugging
        payload = {'username': user_id, 'roomName': room_name, 'oldName': old_item_name, 'newName': new_item_name}
        print(f'Sending payload: {payload}')

        if response.status_code == 200:
            await update.message.reply_text('Item updated successfully!')
        else:
            print(f'Failed to update item. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text('Failed to update item. Please check the details and try again.')
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text('An error occurred while updating the item.')

    context.user_data['awaiting_item_edit'] = False

# Delete item from room
async def delete_room_item_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['awaiting_item_deletion'] = True
    await update.message.reply_text('Please provide the room name and item name in the format: room_name, item_name.')

async def handle_delete_room_item_message(update: Update, context: ContextTypes.DEFAULT_TYPE, room_name=None, item_name=None):
    if room_name is None or item_name is None:
        await update.message.reply_text('Please provide both the room name and the item name.')
        return

    user_id = str(update.message.from_user.id)
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(f'{API_URL}/room/deleteItem', json={'username': user_id, 'roomName': room_name, 'itemName': item_name}, headers=headers)

        if response.status_code == 200:
            await update.message.reply_text('Item deleted successfully!')
        else:
            print(f'Failed to delete item. Status code: {response.status_code}, Response: {response.text}')
            await update.message.reply_text('Failed to delete item. Please check the details and try again.')
    except Exception as e:
        print(f'Exception occurred: {e}')
        await update.message.reply_text('An error occurred while deleting the item.')

    context.user_data['awaiting_item_deletion'] = False

# Extract intents and entities
def extract_intent_and_entities(text):
    doc = nlp(text)
    intent = None
    room_name = None
    item_name = None
    new_room_name = None
    new_item_name = None
    
    if 'add' in text.lower() and any(word in text.lower() for word in ['room', 'rooms']):
        intent = 'add_room'
    elif 'add' in text.lower() and 'item' in text.lower():
        intent = 'add_item_to_room'
    elif any(word in text.lower() for word in ['view', 'see']) and 'items' in text.lower() and any(word in text.lower() for word in ['room', 'rooms']):
        intent = 'view_room_items'
    elif any(word in text.lower() for word in ['view', 'see']) and any(word in text.lower() for word in ['room', 'rooms']):
        intent = 'view_rooms'
    elif 'delete' in text.lower() and 'item' in text.lower():
        intent = 'delete_room_item'
    elif 'delete' in text.lower() and any(word in text.lower() for word in ['room', 'rooms']):
        intent = 'delete_room'
    elif any(word in text.lower() for word in ['update', 'rename']):
        if 'item' in text.lower():
            intent = 'edit_room_item'
        else:
            intent = 'update_room'
    
    for ent in doc.ents:
        if ent.label_ in {'ORG', 'GPE', 'FACILITY', 'LOC'}:
            room_name = ent.text
        elif ent.label_ == 'PRODUCT':  # You may adjust the entity label based on your model
            item_name = ent.text
    
    tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]

    if not room_name or not item_name:
        tokens = [token.text for token in doc if not token.is_stop and not token.is_punct]
        
        if 'to' in tokens:
            to_index = tokens.index('to')
            
            if not room_name:
                room_name_candidates = tokens[to_index + 1:]
                room_name = " ".join(room_name_candidates) if room_name_candidates else None

            if not item_name:
                item_name_candidates = tokens[:to_index]
                item_name = " ".join(item_name_candidates) if item_name_candidates else None

        if not room_name and len(tokens) > 1:
            room_name = tokens[-1]  # Last token as the room name
        if not item_name and len(tokens) > 1:
            item_name = tokens[0]  # First token as the item name

    if intent == 'add_item_to_room':
        if 'to' in text.lower():
            parts = text.lower().split('to')
            item_name = parts[0].strip().split()[-1]
            room_name = parts[1].strip()

    if intent == 'edit_room_item':
        if 'to' in text.lower():
            parts = text.lower().split('to')
            remaining_text = parts[1].strip()
            if 'in' in remaining_text:
                in_parts = remaining_text.split('in')
                new_item_name = in_parts[0].strip()
                room_name = in_parts[1].strip()
            else:
                new_item_name = remaining_text.strip()
            item_name = parts[0].strip().split()[-1]
        elif ',' in text:
            parts = text.split(',')
            if len(parts) == 3:
                room_name = parts[0].strip()
                item_name = parts[1].strip()
                new_item_name = parts[2].strip()

    if intent == 'update_room':
        if 'to' in text.lower():
            parts = text.lower().split('to')
            room_name = parts[0].strip().split()[-1]
            new_room_name = parts[1].strip()
        elif ',' in text:
            parts = text.lower().split(',')
            room_name = parts[0].strip()
            new_room_name = parts[1].strip()

    return intent, room_name, new_room_name, item_name, new_item_name

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if context.user_data.get('awaiting_subspace'):
        await handle_add_subspace_message(update, context)
    elif context.user_data.get('awaiting_room'):
        await handle_add_room_message(update, context)
    elif context.user_data.get('awaiting_room_deletion'):
        await handle_delete_room_message(update, context)
    elif context.user_data.get('awaiting_update_room'):
        if ',' in text:
            old_name, new_name = map(str.strip, text.split(','))
        elif 'to' in text.lower():
            parts = text.lower().split('to')
            old_name = parts[0].strip().split()[-1]
            new_name = parts[1].strip()
        else:
            await update.message.reply_text('Please use the format: old_room_name, new_room_name or rename old_room_name to new_room_name.')
            return
        await handle_update_room_message(update, context, old_name=old_name, new_name=new_name)
    elif context.user_data.get('awaiting_item'):
        if ',' in text:
            room_name, item_name = map(str.strip, text.split(','))
            await handle_add_item_to_room_message(update, context, room_name=room_name, item_name=item_name)
        else:
            await update.message.reply_text('Please use the format: room_name, item_name.')
    elif context.user_data.get('awaiting_item_edit'):
        if ',' in text:
            room_name, old_item_name, new_item_name = map(str.strip, text.split(','))
            await handle_edit_room_item_message(update, context, room_name=room_name, old_item_name=old_item_name, new_item_name=new_item_name)
        else:
            await update.message.reply_text('Please use the format: room_name, current_item_name, new_item_name.')
    elif context.user_data.get('awaiting_item_deletion'):
        if ',' in text:
            room_name, item_name = map(str.strip, text.split(','))
            await handle_delete_room_item_message(update, context, room_name=room_name, item_name=item_name)
        else:
            await update.message.reply_text('Please use the format: room_name, item_name.')
    else:
        intent, room_name, new_room_name, item_name, new_item_name = extract_intent_and_entities(text)
        
        if intent == 'add_room' and room_name:
            await handle_add_room_message(update, context, room_name)
        elif intent == 'view_rooms':
            await view_rooms_command(update, context)
        elif intent == 'view_room_items' and room_name:
            await view_room_items_command(update, context, room_name)
        elif intent == 'delete_room' and room_name:
            await handle_delete_room_message(update, context, room_name)
        elif intent == 'update_room' and room_name and new_room_name:
            await handle_update_room_message(update, context, old_name=room_name, new_name=new_room_name)
        elif intent == 'add_item_to_room' and room_name and item_name:
            await handle_add_item_to_room_message(update, context, room_name=room_name, item_name=item_name)
        elif intent == 'edit_room_item' and room_name and item_name and new_item_name:
            await handle_edit_room_item_message(update, context, room_name=room_name, old_item_name=item_name, new_item_name=new_item_name)
        elif intent == 'delete_room_item' and room_name and item_name:
            await handle_delete_room_item_message(update, context, room_name=room_name, item_name=item_name)
        else:
            await update.message.reply_text("Sorry, I didn't understand that. Could you please clarify?")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# '__main__'
if __name__ == '__main__':
    print('Bot Starting...')
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add_room', add_room_command))
    app.add_handler(CommandHandler('view_rooms', view_rooms_command))
    app.add_handler(CommandHandler('delete_room', delete_room_command))
    app.add_handler(CommandHandler('update_room', update_room_command))
    app.add_handler(CommandHandler('add_item_to_room', add_item_to_room_command))
    app.add_handler(CommandHandler('view_room_items', view_room_items_command))
    app.add_handler(CommandHandler('edit_room_item', edit_room_item_command))
    app.add_handler(CommandHandler('delete_room_item', delete_room_item_command))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)