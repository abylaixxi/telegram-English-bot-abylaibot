from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

ASK_GOAL, ASK_LEVEL, ASK_TIME = range(3)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Да", "Нет"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Здравствуйте! 👋 Рады видеть вас в нашей школе английского языка.\n"
        "Хотите записаться на пробное занятие?",
        reply_markup=reply_markup
    )
    return ASK_GOAL

async def ask_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.message.text.lower()
    if answer == "нет":
        await update.message.reply_text(
            "Хорошо, если появится интерес — будем рады вас видеть! 😊",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    context.user_data['goal'] = answer
    keyboard = [["A1", "A2", "B1"], ["B2", "C1", "C2"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Пробный урок длится 30 минут и проходит онлайн с преподавателем.\n"
        "Он поможет определить ваш уровень и познакомит с нашим подходом.\n"
        "Выберите ваш уровень английского:",
        reply_markup=reply_markup
    )
    return ASK_LEVEL

async def ask_level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['level'] = update.message.text
    keyboard = [["завтра в 18:00", "четверг в 15:30"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Отлично! 😊 Когда вам удобно провести занятие?",
        reply_markup=reply_markup
    )
    return ASK_TIME

async def ask_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['time'] = update.message.text
    await update.message.reply_text(
        f"Супер! Записала вас на пробный урок {context.user_data['time']}.\n"
        "За 10 минут до занятия пришлём ссылку на Zoom 💻\n"
        "Если возникнут вопросы — пишите, всегда на связи! Хорошего дня! 🌟",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Диалог отменён. Если передумаете — просто напишите /start.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token("8170972261:AAETqGFSpGeMUZ8Wq9diCwrgXm3jGnd42-s").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_goal)],
            ASK_LEVEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_level)],
            ASK_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_time)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
