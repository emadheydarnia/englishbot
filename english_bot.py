#!/usr/bin/env python3
"""English Teaching Telegram Bot — Main Bot File"""

import logging
import os
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)
from exam_data import EXAMS, CATEGORIES

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TEACHER_ID = 70028156
EXAM_TIME_MINUTES = 30

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
all_scores = {}

# ── Keyboards ──────────────────────────────────────────────────────────────────

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 ارشد-دکتری", callback_data="cat_arshad")],
        [InlineKeyboardButton("🔤 A2Z English", callback_data="cat_a2z")],
    ])

def a2z_keyboard():
    rows = [[InlineKeyboardButton(cat["label"], callback_data="cat_" + k)] for k, cat in CATEGORIES.items()]
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="back_main")])
    return InlineKeyboardMarkup(rows)

def exam_list_keyboard(cat_key):
    cat = CATEGORIES[cat_key]
    rows = [[InlineKeyboardButton("📄 Exam " + str(i+1), callback_data="exam_" + ek)] for i, ek in enumerate(cat["exams"])]
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_a2z")])
    return InlineKeyboardMarkup(rows)

def back_main_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")]])

def results_keyboard(cat_key):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Try Again", callback_data="cat_" + cat_key)],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")],
    ])

# ── State helpers ──────────────────────────────────────────────────────────────

def get_state(context, user_id):
    key = "exam_" + str(user_id)
    if key not in context.bot_data:
        context.bot_data[key] = {}
    return context.bot_data[key]

def clear_state(context, user_id):
    context.bot_data["exam_" + str(user_id)] = {}

async def send_question(context, user_id, state):
    idx = state["current"]
    q = state["questions"][idx]
    total = len(state["questions"])
    elapsed = datetime.now() - state["start_time"]
    secs_left = max(0, int((timedelta(minutes=EXAM_TIME_MINUTES) - elapsed).total_seconds()))
    mins, secs = secs_left // 60, secs_left % 60
    hint = ("  " + q["hint"]) if q["hint"] else ""
    text = (
        "⏱ " + str(mins) + ":" + str(secs).zfill(2) +
        "  |  Q " + str(idx+1) + "/" + str(total) + "\n\n" +
        q["q"] + hint + "\n\n✏️ Type your answer:"
    )
    await context.bot.send_message(chat_id=user_id, text=text)

async def finish_exam(context, user_id, state, timed_out=False):
    answers = state.get("answers", [])
    questions = state["questions"]
    name = state.get("student_name", "?")
    cls = state.get("student_class", "?")
    title = state.get("exam_title", "Exam")
    cat_key = state.get("cat_key", "psc")
    score = 0
    lines = []

    for i, q in enumerate(questions):
        given = answers[i].strip() if i < len(answers) else "(no answer)"
        correct = q["answer"]
        correct_opts = [c.strip().lower() for c in correct.split("/")]
        if given.lower() in correct_opts:
            score += 1
            lines.append("✅ Q" + str(i+1) + ": " + given)
        else:
            lines.append("❌ Q" + str(i+1) + ": You wrote: " + given + "\n    Correct: " + correct)

    total = len(questions)
    pct = int(score / total * 100)
    elapsed = datetime.now() - state["start_time"]
    m, s = int(elapsed.total_seconds()) // 60, int(elapsed.total_seconds()) % 60
    time_str = str(m) + ":" + str(s).zfill(2)

    if pct >= 90: grade = "🏆 Excellent!"
    elif pct >= 75: grade = "👍 Good job!"
    elif pct >= 50: grade = "📚 Keep practicing!"
    else: grade = "💪 Don't give up!"

    header = "⏰ Time is up!\n\n" if timed_out else "🎉 Exam Finished!\n\n"
    summary = (
        header +
        "📊 " + title + "\n" +
        "══════════════════\n" +
        "👤 " + name + "  |  🏫 " + cls + "\n" +
        "✅ Score: " + str(score) + "/" + str(total) + " (" + str(pct) + "%)\n" +
        "⏱ Time: " + time_str + "\n" +
        grade + "\n" +
        "══════════════════\n\n"
    )
    details = "\n".join(lines)
    full = summary + details
    kb = results_keyboard(cat_key)

    if len(full) > 4000:
        await context.bot.send_message(chat_id=user_id, text=summary)
        await context.bot.send_message(chat_id=user_id, text=details, reply_markup=kb)
    else:
        await context.bot.send_message(chat_id=user_id, text=full, reply_markup=kb)

    if user_id not in all_scores:
        all_scores[user_id] = []
    all_scores[user_id].append({
        "name": name, "class": cls, "exam": title,
        "score": str(score) + "/" + str(total), "pct": str(pct) + "%",
        "time": time_str, "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

    teacher_msg = (
        "📋 NEW RESULT\n══════════════════\n" +
        "👤 " + name + "  |  🏫 " + cls + "\n" +
        "📝 " + title + "\n" +
        "✅ " + str(score) + "/" + str(total) + " (" + str(pct) + "%)\n" +
        "⏱ " + time_str + "  |  📅 " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n" +
        "══════════════════"
    )
    try:
        await context.bot.send_message(chat_id=TEACHER_ID, text=teacher_msg)
    except Exception as e:
        logger.error("Teacher notify failed: " + str(e))

    clear_state(context, user_id)

async def timeout_job(context: ContextTypes.DEFAULT_TYPE):
    user_id = context.job.data["user_id"]
    state = get_state(context, user_id)
    if state.get("active"):
        state["active"] = False
        await context.bot.send_message(chat_id=user_id, text="⏰ Time is up! Submitting your exam...")
        await finish_exam(context, user_id, state, timed_out=True)

# ── Commands ───────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome, " + update.effective_user.first_name + "!\n\n"
        "I'm your English Learning Assistant. 🎓\n"
        "Please choose a category to get started:",
        reply_markup=main_menu_keyboard(),
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n/start — Main menu\n/help — This help\n"
        "/quit — Submit exam early\n/results — All scores (teacher only)"
    )

async def quit_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = get_state(context, user_id)
    if state.get("active"):
        state["active"] = False
        for j in context.job_queue.get_jobs_by_name("timer_" + str(user_id)):
            j.schedule_removal()
        await finish_exam(context, user_id, state)
    else:
        await update.message.reply_text("No active exam.", reply_markup=main_menu_keyboard())

async def results_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TEACHER_ID:
        await update.message.reply_text("⛔ Teacher only.")
        return
    if not all_scores:
        await update.message.reply_text("No results yet.")
        return
    lines = ["📊 ALL RESULTS\n══════════════════"]
    for uid, rs in all_scores.items():
        for r in rs:
            lines.append(
                "👤 " + r["name"] + "  🏫 " + r["class"] + "\n" +
                "📝 " + r["exam"] + "\n" +
                "✅ " + r["score"] + " (" + r["pct"] + ")  ⏱ " + r["time"] + "\n" +
                "📅 " + r["date"] + "\n──────────────────"
            )
    full = "\n".join(lines)
    for chunk in [full[i:i+4000] for i in range(0, len(full), 4000)]:
        await update.message.reply_text(chunk)

# ── Button handler ─────────────────────────────────────────────────────────────

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data == "back_main":
        state = get_state(context, user_id)
        if state.get("active"):
            state["active"] = False
            clear_state(context, user_id)
        await query.edit_message_text("Please choose a category:", reply_markup=main_menu_keyboard())

    elif data == "cat_arshad":
        await query.edit_message_text(
            "📚 ارشد-دکتری — Master's & PhD Prep\n\n"
            "Resources for:\n• Academic Reading & Vocabulary\n"
            "• Academic Writing\n• Listening comprehension\n"
            "• Advanced Grammar\n\n📌 Coming soon! 💪",
            reply_markup=back_main_keyboard()
        )

    elif data == "cat_a2z":
        await query.edit_message_text("🔤 A2Z English\n\nChoose a topic:", reply_markup=a2z_keyboard())

    elif data.startswith("cat_") and data not in ("cat_arshad", "cat_a2z"):
        cat_key = data[4:]
        if cat_key in CATEGORIES:
            cat = CATEGORIES[cat_key]
            await query.edit_message_text(
                cat["label"] + "\n\n" + str(len(cat["exams"])) + " exams available.\nChoose one:",
                reply_markup=exam_list_keyboard(cat_key)
            )

    elif data.startswith("exam_"):
        exam_key = data[5:]
        exam = EXAMS.get(exam_key)
        if not exam:
            await query.edit_message_text("Exam not found.", reply_markup=main_menu_keyboard())
            return
        cat_key = exam_key.rsplit("_", 1)[0]
        state = get_state(context, user_id)
        state["pending_exam_key"] = exam_key
        state["cat_key"] = cat_key
        state["step"] = "ask_name"
        await query.edit_message_text(
            "📝 " + exam["title"] + "\n\n"
            "ℹ️ " + exam["instruction"] + "\n\n"
            "Before we start:\n✏️ Please type your full name:"
        )

# ── Message handler ────────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = get_state(context, user_id)
    text = update.message.text.strip()

    if state.get("step") == "ask_name":
        state["student_name"] = text
        state["step"] = "ask_class"
        await update.message.reply_text("👋 Hello, " + text + "!\n\n🏫 Please type your class name or number:")
        return

    if state.get("step") == "ask_class":
        state["student_class"] = text
        exam = EXAMS[state["pending_exam_key"]]
        state.update({
            "step": "exam", "active": True, "current": 0,
            "answers": [], "questions": exam["questions"],
            "exam_title": exam["title"], "start_time": datetime.now(),
        })
        context.job_queue.run_once(
            timeout_job, when=EXAM_TIME_MINUTES * 60,
            data={"user_id": user_id}, name="timer_" + str(user_id),
        )
        await update.message.reply_text(
            "✅ Registered!\n👤 " + state["student_name"] + "  |  🏫 " + text + "\n\n" +
            "📝 " + exam["title"] + "\n" +
            "ℹ️ " + exam["instruction"] + "\n\n" +
            "⏱ Time: " + str(EXAM_TIME_MINUTES) + " min  |  📊 Questions: " + str(len(exam["questions"])) + "\n\n" +
            "✔️ After each answer you will see the correct answer immediately.\n\n" +
            "Good luck! 🍀  (Type /quit to submit early)"
        )
        await send_question(context, user_id, state)
        return

    if state.get("active"):
        elapsed = datetime.now() - state["start_time"]
        if elapsed > timedelta(minutes=EXAM_TIME_MINUTES):
            state["active"] = False
            await finish_exam(context, user_id, state, timed_out=True)
            return

        idx = state["current"]
        q = state["questions"][idx]
        correct_opts = [c.strip().lower() for c in q["answer"].split("/")]
        feedback = "✅ Correct!\n\n" if text.lower() in correct_opts else "❌ Wrong!\n✔️ Correct answer: " + q["answer"] + "\n\n"

        state["answers"].append(text)
        state["current"] += 1

        if state["current"] >= len(state["questions"]):
            await update.message.reply_text(feedback + "📊 Calculating your results...")
            state["active"] = False
            for j in context.job_queue.get_jobs_by_name("timer_" + str(user_id)):
                j.schedule_removal()
            await finish_exam(context, user_id, state)
        else:
            await update.message.reply_text(feedback)
            await send_question(context, user_id, state)
        return

    await update.message.reply_text("Please use /start to open the menu. 😊", reply_markup=main_menu_keyboard())

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("quit", quit_cmd))
    app.add_handler(CommandHandler("results", results_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
