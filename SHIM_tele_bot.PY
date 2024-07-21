
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
API_URL = 'https://smart-home-inventory-manager-4pzu2nxpd-w-zheng-jies-projects.vercel.app/'
API_KEY = 'BNArFb4gJ08pT6OYfgzr'

headers = {
    'x-api-key': API_KEY
}

# Commands
"""
start - Starts the bot
help - Provides help for SHIM Tele Bot

add_room - Adds a new room / space
add_SubSpace - Adds a new sub-space
additem - Adds a new item

view - Gets all spaces and subspaces
delete - Deletes a space or sub-space by ID
remove_item - Deletes an item by ID

get - Gets all items
"""

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am SHIM Bot! Select /help for more info!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Select /additem to add items, /add_room to add rooms, /add_SubSpace to add sub-spaces, /remove_item to remove items, or /view to see all spaces and subspaces!')

async def additem_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the item details in the format: sub_space_id, quantity, name, expiry_date')

async def add_room_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the room details in the format: room_name')

async def add_subspace_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the sub-space details in the format: space_id, sub_space_name')

async def handle_add_room_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    room_name = update.message.text.strip()
    user_id = update.message.from_user.id

    # Sending data to the API for adding a room
    try:
        response = requests.post(f'{API_URL}/spaces', json={'user_id': user_id, 'space_name': room_name}, headers=headers)

        if response.status_code == 201:
            await update.message.reply_text('Room added successfully!')
        else:
            await update.message.reply_text('Failed to add room. Please check the details and try again.')
    except Exception as e:
        await update.message.reply_text('An error occurred while adding the room.')

async def handle_add_subspace_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    details = update.message.text.split(',')
    if len(details) != 2:
        await update.message.reply_text('Invalid format. Please provide details in the format: sub_space_name, space_id')
        return
    
    sub_space_name, space_id = [detail.strip() for detail in details]
    
    # Sending data to the API for adding a sub-space
    try:
        response = requests.post(f'{API_URL}/sub_spaces', json={'space': space_id, 'sub_space_name': sub_space_name}, headers=headers)

        if response.status_code == 201:
            await update.message.reply_text('Sub-space added successfully!')
        else:
            await update.message.reply_text('Failed to add sub-space. Please check the details and try again.')
    except Exception as e:
        await update.message.reply_text('An error occurred while adding the sub-space.')

async def handle_add_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    details = update.message.text.split(',')
    if len(details) != 4:
        await update.message.reply_text('Invalid format. Please provide details in the format: sub_space_id, quantity, name, expiry_date (YYYY-MM-DD)')
        return
    
    item_name, sub_space_id, quantity, expiry_date = [detail.strip() for detail in details]
    
    # Sending data to the API for adding an item
    try:
        response = requests.post(f'{API_URL}/items', json={
            'sub_space_id': sub_space_id,
            'quantity': int(quantity),
            'item_name': item_name,
            'expiry_date': expiry_date
        }, headers=headers)
        
        if response.status_code == 201:
            await update.message.reply_text('Item added successfully!')
        else:
            await update.message.reply_text('Failed to add item. Please check the details and try again.')
    except Exception as e:
        await update.message.reply_text('An error occurred while adding the item.')

async def get_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f'{API_URL}/items', headers=headers)
    items = response.json()
    message = "Items in your inventory:\n"
    for item in items:
        message += f"{item['item_name']} (Quantity: {item['quantity']}, Expiry Date: {item['expiry_date']})\n"
    await update.message.reply_text(message)

async def remove_item_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the ID of the item you want to remove')

async def handle_remove_item_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item_id = update.message.text.strip()
    
    # Sending delete request to the API
    try:
        response = requests.delete(f'{API_URL}/items/{item_id}', headers=headers)
        
        if response.status_code == 200:
            await update.message.reply_text('Item removed successfully!')
        else:
            await update.message.reply_text('Failed to remove item. Please check the ID and try again.')
    except Exception as e:
        await update.message.reply_text('An error occurred while removing the item.')

async def view_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f'{API_URL}/spaces', headers=headers)
    spaces = response.json()
    message = "Spaces and Sub-spaces:\n"
    for space in spaces:
        message += f"Space: {space['space_name']}\n"
        if 'sub_spaces' in space:
            for sub_space in space['sub_spaces']:
                message += f"  - Sub-space: {sub_space['sub_space_name']}\n"
    await update.message.reply_text(message)

async def delete_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter the ID of the space or sub-space you want to delete.')

async def handle_delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    space_id = update.message.text.strip()
    
    # Sending delete request to the API
    try:
        response = requests.delete(f'{API_URL}/spaces/{space_id}', headers=headers)
        
        if response.status_code == 200:
            await update.message.reply_text('Space or sub-space deleted successfully!')
        else:
            await update.message.reply_text('Failed to delete space or sub-space. Please check the ID and try again.')
    except Exception as e:
        await update.message.reply_text('An error occurred while deleting the space or sub-space.')

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
    app.add_handler(CommandHandler('additem', additem_command))
    app.add_handler(CommandHandler('add_room', add_room_command))
    app.add_handler(CommandHandler('add_subspace', add_subspace_command))
    app.add_handler(CommandHandler('get', get_command))
    app.add_handler(CommandHandler('remove_item', remove_item_command))
    app.add_handler(CommandHandler('view', view_command))
    app.add_handler(CommandHandler('delete', delete_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex('add_room'), handle_add_room_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex('add_subspace'), handle_add_subspace_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex('additem'), handle_add_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex('remove_item'), handle_remove_item_message))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex('delete'), handle_delete_message))

    # Errors
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)