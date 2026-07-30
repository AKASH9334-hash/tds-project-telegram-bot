from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from dotenv import load_dotenv
import os
import json

from agent import solve_question
from logger import save_log


load_dotenv()


TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Data Analyst Bot Ready"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    question = update.message.text


    # Get answer from Ollama
    answer = solve_question(question)


    # Save log
    save_log(
        question,
        answer
    )


    try:
        # Convert model JSON text into Python dictionary
        answer_json = json.loads(answer)

    except:
        # If model gives non-JSON text
        answer_json = {
            "result": answer
        }


    # Final format required by assignment
    final_response = {
        "answer": answer_json,
        "log_url": "https://your-host/run.jsonl"
    }


    await update.message.reply_text(
        json.dumps(final_response)
    )



app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


app.add_handler(
    MessageHandler(
        filters.TEXT,
        handle_message
    )
)


print("Bot running...")


app.run_polling()