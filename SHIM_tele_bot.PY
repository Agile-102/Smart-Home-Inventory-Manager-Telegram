"""
Smart-Home-Inventory-Manager / SHIM Telegram Bot
Binded to Telegram User: WZJ99
Telegram: https://t.me/WZJ99
"""
# make sure to pip install python-telegram-bot



from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = '7056035301:AAGfskXNZ6JxZjxOt0yjcDvaegZ3zcUMO9Q'
BOT_USERNAME: Final = '@SHIM_Tele_Bot'


# Commands
"""
start - Starts the bot
help - Provides help for SHIM Tele Bot
"""
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # message on start
    await update.message.reply_text('Hello! I am SHIM Bot! Select /help for more info!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Select /add to start adding things to your inventory!')


# Responses

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'test' in processed:
        return 'Test good!'
    
    if 'test2' in processed:
        return 'Test 2 also good!'
    
    return 'I do not understand what you wrote'


# Messages

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This informs us if it is a grp chat or private chat
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Debugging print statement
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    # Debugging print statement
    print('Bot:', response)
    await update.messae.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused eror {context.error}')



if __name__ == '__main__':
    print(f'Bot Starting...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)

    print(f'Polling...')
    app.run_polling(poll_interval=3)
