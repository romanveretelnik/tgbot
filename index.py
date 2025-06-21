import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- НАЛАШТУВАННЯ ВАШОГО БОТА ---
# Замініть на ваш фактичний токен бота, отриманий від BotFather.
# Приклад: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
BOT_TOKEN = "7381506377:AAFYDWPBGKGqDCWbb-uWopBBLxl4yUSJ_4c"

# Замініть на URL вашого сайту з презентацією проекту.
# Приклад: "https://my-awesome-project.com/presentation"
PRESENTATION_URL = "https://msfirefly.my.canva.site/"

# Інформація про проект. Використовуйте Markdown для форматування (наприклад, *для жирного*).
PROJECT_INFO = """
🚀 *Назва проекту:* Мій Техно Табір Бот
✨ *Опис:*Табір для дітей віком 11-17 років,де будуть розваги та вивчення технологій з практикою.Учасники занурюються у світпрограмування та 3D-моделювання,працюють з фахівцями і розвивають різні здібності.
💡 *Основні функції:*
    - Надання посилання на презентацію
    - Інформація про проект та команду
"""

# Інформація про розробників. Використовуйте Markdown для форматування.
ABOUT_CREATORS = """
🧑‍💻 *Розробники:*
    - **Ім'я Учня 1:** (Роман) - Роль: Розробник логіки бота
    - **Ім'я Учня 2:** (Яна) - Роль: Дизайнер презентації
    - **Ім'я Учня 3:** (Олександр) - Роль: Тестувальник та ідейний натхненник
    - **Ім'я Учня 4:** (Тищенко Михайло) - Роль: Розробник декорацій
    - **Ім'я Учня 5:** (Родюк Назар) - Роль: Розробник декорацій
"""
# --- КІНЕЦЬ НАЛАШТУВАНЬ ---

# Включаємо логування, щоб бачити події бота в консолі.
# Це допомагає в налагодженні.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# Знижуємо рівень логування для бібліотеки httpx, щоб не перевантажувати консоль.
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє команду /start.
    Відправляє привітання та кнопки з посиланням на презентацію та інформацією.
    """
    # Створюємо кнопки для клавіатури.
    # InlineKeyboardButton("Текст кнопки", url="URL") - для зовнішніх посилань.
    # InlineKeyboardButton("Текст кнопки", callback_data="дані") - для кнопок, які повертають дані боту.
    keyboard = [
        [
            InlineKeyboardButton("🚀 Сайт", url=PRESENTATION_URL),
        ],
        [
            InlineKeyboardButton("💡 Про Проект", callback_data="about_project"),
            InlineKeyboardButton("🧑‍💻 Про Розробників", callback_data="about_creators"),
        ],
    ]
    # Створюємо розмітку клавіатури з кнопок.
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Відправляємо повідомлення користувачу разом з клавіатурою.
    await update.message.reply_text(
        "Привіт! Я твій бот для Техно Табору. Обирай, що тебе цікавить:",
        reply_markup=reply_markup,
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обробляє натискання на інлайн-кнопки (які мають callback_data).
    """
    # Отримуємо об'єкт CallbackQuery, який містить дані про натиснуту кнопку.
    query = update.callback_query
    # Обов'язково відповідаємо на callback-запит, щоб Telegram знав, що запит оброблено.
    # Це також прибирає "годинник" з кнопки.
    await query.answer()

    # Перевіряємо, які дані були прикріплені до натиснутої кнопки.
    if query.data == "about_project":
        # Редагуємо поточне повідомлення, щоб показати інформацію про проект.
        # parse_mode="Markdown" дозволяє використовувати розмітку Markdown у тексті.
        await query.edit_message_text(text=PROJECT_INFO, parse_mode="Markdown")
    elif query.data == "about_creators":
        # Редагуємо поточне повідомлення, щоб показати інформацію про розробників.
        await query.edit_message_text(text=ABOUT_CREATORS, parse_mode="Markdown")

def main() -> None:
    """
    Головна функція для запуску бота.
    """
    # Створюємо об'єкт Application, передаючи токен вашого бота.
    application = Application.builder().token(BOT_TOKEN).build()

    # Реєструємо обробники:
    # CommandHandler обробляє команди (наприклад, /start).
    application.add_handler(CommandHandler("start", start))
    # CallbackQueryHandler обробляє натискання на інлайн-кнопки.
    application.add_handler(CallbackQueryHandler(button))

    # Запускаємо бота в режимі постійного опитування (polling).
    # allowed_updates=Update.ALL_TYPES дозволяє боту отримувати всі типи оновлень.
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
