from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from flask import Flask, request
import logging
from typing import DefaultDict

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
user_notifs = DefaultDict(bool)
user_ids = {}

logger = logging.getLogger(__name__)
logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.WARNING)

server = Flask(__name__)


@server.route('/webhook', methods=['POST'])
def webhook() -> str:
    data = request.json
    request_id = data["id"]

    user_id = user_ids[request_id]
    if user_notifs[user_id]:
        logger.info(f"Notification sent for {user_id}")
        send_reminder(user_id, data['event'])
    return "ok"


async def send_reminder(user_id, msg):
    await app.sendMessage(chat_id=user_id, text=msg)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    user_notifs[user_id] = True

    if (len(context.args) > 1):
        await update.message.reply_text("Specify only one ID")
        return
    
    if (len(context.args) == 1):
        requests_id = context.args[0]
        user_notifs[user_id] = requests_id
    
    await update.message.reply_text(f'Pushing notifications for {update.effective_user.first_name}!')

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    user_notifs[user_id] = False
    
    await update.message.reply_text(f'Stopping notifications for {update.effective_user.first_name}!')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id
    
    if user_notifs[user_id]:
        await update.message.reply_text(f'Notifs for {update.effective_user.first_name} are on!')
    else:
        await update.message.reply_text(f'Reminders for {update.effective_user.first_name} are off!')

async def setId(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.chat_id

    if (len(context.args) > 1):
        await update.message.reply_text("Specify only one ID")
        return

    requests_id = context.args[0]
    user_notifs[user_id] = requests_id
    
    await update.message.reply_text(f'Telegram ID {update.effective_user.username} associated with Request ID {requests_id}')

    
app = ApplicationBuilder().token(telegram_bot_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("stop", stop))
app.add_handler(CommandHandler("status", status))
app.add_handler(CommandHandler("setId", setId))

server.run(port=5000)
app.run_polling()
