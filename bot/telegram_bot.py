import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

load_dotenv()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to TeleStudentAssistant!\n\n"
        "I can help you with:\n\n"
        "📚 Subjects\n"
        "📝 Assignments\n"
        "📅 Exams\n"
        "🤖 AI explanations\n"
        "📖 Study plans\n"
        "🧠 Quizzes\n"
        "📊 Progress\n"
        "📄 PDF summaries\n\n"
        "Try:\n"
        "subjects\n"
        "study plan\n"
        "quiz Python\n"
        "explain normalization\n\n"
        "📄 You can also upload a PDF directly."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 TeleStudentAssistant Commands\n\n"
        "📚 Academic\n"
        "• subjects\n"
        "• add subject Python\n"
        "• study plan\n"
        "• explain normalization\n"
        "• quiz Python\n\n"
        "📝 Assignments\n"
        "• assignments\n"
        '• add assignment "Python Project" "2026-09-20"\n\n'
        "📅 Exams\n"
        "• exams\n"
        '• add exam "DBMS" "2026-09-25"\n\n'
        "📊 Progress\n"
        "• progress\n\n"
        "📄 PDF\n"
        "• Upload a PDF directly to the chat\n\n"
        "❓ Type your question normally."
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    text = update.message.text.strip()

    try:
        frontend_agent = context.application.bot_data["frontend_agent"]

        response = frontend_agent.handle(text)

        await update.message.reply_text(response)

    except Exception as e:
        print(f"Text processing error: {e}")

        await update.message.reply_text(
            "❌ Sorry, I could not process your request."
        )


async def handle_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Receives a PDF from Telegram, downloads it locally,
    and sends it through the existing agent system.
    """

    if not update.message or not update.message.document:
        return

    document = update.message.document

    # Check file extension
    file_name = document.file_name or "uploaded_file.pdf"

    if not file_name.lower().endswith(".pdf"):
        await update.message.reply_text(
            "❌ Please upload a PDF file only."
        )
        return

    await update.message.reply_text(
        "📄 PDF received.\n\n"
        "⏳ Downloading and analyzing the document..."
    )

    try:
        # Get Telegram file
        telegram_file = await document.get_file()

        # Create upload directory
        upload_dir = Path("data") / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)

        # Safe filename
        safe_name = Path(file_name).name
        file_path = upload_dir / safe_name

        # Download PDF
        await telegram_file.download_to_drive(
            custom_path=str(file_path)
        )

        print(f"PDF downloaded: {file_path}")

        # Get frontend agent
        frontend_agent = context.application.bot_data["frontend_agent"]

        # Send PDF path into existing backend flow
        command = f'summarize_pdf "{file_path}"'

        response = frontend_agent.handle(command)

        await update.message.reply_text(
            "📖 PDF Summary\n\n" + response
        )

    except Exception as e:
        print(f"PDF processing error: {e}")

        await update.message.reply_text(
            "❌ I could not process this PDF.\n\n"
            "Please make sure the PDF contains selectable text."
        )


def create_telegram_app(frontend_agent):

    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is missing from .env"
        )

    application = Application.builder().token(token).build()

    # Store frontend agent
    application.bot_data["frontend_agent"] = frontend_agent

    # Commands
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    # PDF handler
    application.add_handler(
        MessageHandler(
            filters.Document.PDF,
            handle_pdf
        )
    )

    # Text handler
    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_text
        )
    )

    return application


def run_telegram(frontend_agent):

    application = create_telegram_app(frontend_agent)

    print("Telegram bot started...")

    application.run_polling()