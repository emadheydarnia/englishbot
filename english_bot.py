#!/usr/bin/env python3
"""English Teaching Telegram Bot — Main Bot File with AI Features"""

import logging
import os
import json
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)
from exam_data import EXAMS, CATEGORIES

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TEACHER_ID = int(os.environ.get("TEACHER_ID", "0"))
EXAM_TIME_MINUTES = int(os.environ.get("EXAM_TIME_MINUTES", "30"))
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)
all_scores = {}
ai_sessions = {}  # Store AI conversation history

# ── AI Topic Prompts ──────────────────────────────────────────────────────────

AI_TOPICS = {
    "present_simple_continuous": {
        "label": "📗 Present Simple vs Continuous",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Present Simple and Present Continuous tenses.
CRITICAL RULES:
- ALWAYS give sentences in PERSIAN and student must translate to ENGLISH
- NEVER give English sentences for student to translate to Persian
- Give exactly 20 PERSIAN sentences per session, one at a time
- Wait for student's English answer before giving next sentence
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain in PERSIAN which usage was tested:
Present Simple: regular, permanent, non-action verbs, time table future
Present Continuous: happening now, temporary, big now, changing/developing, planned future
At the end of each session give a daily report IN PERSIAN on student level, performance and progress.
At the end of each week give a weekly progress report IN PERSIAN.
Start by asking for student name and class number IN PERSIAN."""
    },
    "past_simple": {
        "label": "📘 Past Simple",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Past Simple tense.
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
Occasionally include review sentences from Present Simple and Present Continuous.
After each student answer, explain the usage in Persian.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "rather_prefer": {
        "label": "📙 Rather / Prefer",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice would rather, prefer, would sooner, would prefer.
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, question forms, past, present and future, same subject and different subjects.
Occasionally include review sentences from Present Simple, Present Continuous, Past Simple.
After each student answer, explain the usage in Persian.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "present_perfect": {
        "label": "📕 Present Perfect",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Present Perfect tense.
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain which usage was tested:
- past happening with present result
- past happening that continues till now (non-action verbs)
Occasionally include review sentences from Present Simple, Present Continuous, Past Simple, Rather/Prefer.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "present_perfect_continuous": {
        "label": "📓 Present Perfect Continuous",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Present Perfect Continuous tense.
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain the usage:
- past happening that continues till now (action verbs)
Occasionally include review sentences from Present Simple, Present Continuous, Past Simple, Rather/Prefer, Present Perfect.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "comparison": {
        "label": "📒 Comparison",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Comparison (comparative, superlative, as...as, adjectives and adverbs).
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain which comparison structure was used.
Occasionally include review sentences from all previous topics.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
SENTENCE RULES — VERY IMPORTANT:
- Sentences can be simple OR complex depending on the level — but must always sound NATURAL in Persian
- A real Iranian person should be able to say this sentence in real life
- Topics from daily life: food, school, family, friends, sports, weather, shopping, travel, work, hobbies
- NEVER combine unrelated ideas in one sentence just to make it longer — it sounds awkward
- NEVER use unusual or literary Persian vocabulary
- Example GOOD (simple): "این کیف از آن کیف سنگین‌تر است."
- Example GOOD (complex): "هوای تهران در زمستان خیلی سردتر از شیراز است."
- Example BAD: "او به کتاب‌های فانتزی علاقه‌مند است، اما من به آن‌ها ناتوانم." ← unnatural and awkward
Start by asking for student name and class number IN PERSIAN."""
    },
    "relative_clause": {
        "label": "📔 Relative Clause",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Relative Clauses (defining, non-defining, subjective, objective).
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain which type of relative clause was used.
Occasionally include review sentences from all previous topics.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "fanboys": {
        "label": "📃 Fanboys",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice FANBOYS conjunctions (For, And, Nor, But, Or, Yet, So).
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain which conjunction was used and why.
Occasionally include review sentences from all previous topics.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "contrast": {
        "label": "🔄 Contrast",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Contrast connectors (although, even though, despite, in spite of, however, nevertheless, etc.).
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain which contrast connector was used and why.
Occasionally include review sentences from all previous topics.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "grammar1": {
        "label": "📚 Grammar 1 (Mixed Review)",
        "prompt": """You are an English teacher helping Iranian students review all grammar topics covered so far:
Present Simple, Present Continuous, Past Simple, Rather/Prefer, Present Perfect, Present Perfect Continuous, Comparison, Relative Clause, Fanboys, Contrast.
Each day give exactly 20 mixed sentences in PERSIAN for the student to translate to English.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms from all topics.
After each student answer, explain which grammar point was tested.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "conditionals": {
        "label": "🔀 Conditionals",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Conditionals (Type 0, 1, 2, 3, mixed).
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms of all conditional types.
After each student answer, explain which type of conditional was used and why.
Occasionally include review sentences from all previous topics.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "passive": {
        "label": "🔃 Passive",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Passive Voice in all tenses.
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain the tense and passive structure used.
Occasionally include review sentences from all previous topics.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "causative": {
        "label": "⚙️ Causative",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Causative structures (have/get something done, make/let/help someone do).
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain the causative structure used.
Occasionally include review sentences from all previous topics.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "modals": {
        "label": "💬 Modals",
        "prompt": """You are a friendly, witty English teaching assistant for Emad Heydarnia (عماد حیدرنیا)'s language school.
If you mention the teacher's name in Persian, always write: عماد حیدرنیا — and refer to him as مدرس زبان (language instructor), never معلم.
Your personality: warm, encouraging, sometimes funny, uses Persian humor naturally.
Occasionally make light jokes related to English learning to keep students engaged.
Never be boring or robotic — be like a friendly tutor, not a machine.
You are helping Iranian students practice Modal verbs (can, could, may, might, must, shall, should, will, would, ought to, need to, have to, used to, etc.).
CRITICAL: Give sentences in PERSIAN, student must translate to ENGLISH. Never reverse this direction.
Give exactly 20 PERSIAN sentences per session, one at a time, wait for English answer before next sentence.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms.
After each student answer, explain which modal was used and its meaning.
Occasionally include review sentences from all previous topics.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "mixed": {
        "label": "🎯 Mixed (All Topics)",
        "prompt": """You are an English teacher helping Iranian students review ALL grammar topics:
Present Simple, Present Continuous, Past Simple, Rather/Prefer, Present Perfect, Present Perfect Continuous, Comparison, Relative Clause, Fanboys, Contrast, Conditionals, Passive, Causative, Modals.
Each day give exactly 20 mixed sentences in PERSIAN for the student to translate to English.
Day 1: A1 level, Day 2: A2 level, Days 3-4: B1 level, Days 5-6: B2 level.
Include positive, negative, and question forms from all topics.
After each student answer, explain which grammar point was tested.
At the end of each session give a daily report on student level, performance and progress.
At the end of each week give a weekly progress report.
All explanations and reports must be in PERSIAN. All practice sentences must be in PERSIAN for student to translate to ENGLISH.
Start by asking for student name and class number IN PERSIAN."""
    },
    "writing_task1": {
        "label": "✍️ Writing Task 1",
        "prompt": """You are a friendly IELTS Writing examiner and teacher at Emad Heydarnia (عماد حیدرنیا)'s language school.
Be encouraging, supportive and occasionally witty. Make feedback feel personal not robotic.
You are an IELTS Writing Task 1 examiner and teacher.
When a student starts, ask for their name and class number.
Then give them ONE IELTS Writing Task 1 question (can be any type: bar chart, line graph, pie chart, table, map, process diagram).
Give them 20 minutes to write their answer.
After they submit (or time is up), correct their writing and give:
- Band score (1-9) for: Task Achievement, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy
- Overall band score
- Detailed feedback on each criterion
- Corrected version of their writing
- Tips for improvement
Report the result to the teacher with student name, class, and scores.
Communicate all explanations in Persian but keep English writing in English."""
    },
    "writing_task2": {
        "label": "✍️ Writing Task 2",
        "prompt": """You are a friendly IELTS Writing examiner and teacher at Emad Heydarnia (عماد حیدرنیا)'s language school.
Be encouraging, supportive and occasionally witty. Make feedback feel personal not robotic.
You are an IELTS Writing Task 2 examiner and teacher.
When a student starts, ask for their name and class number.
Then give them ONE IELTS Writing Task 2 question (can be any type: opinion, discussion, problem-solution, advantages-disadvantages, double question).
Give them 40 minutes to write their answer.
After they submit (or time is up), correct their writing and give:
- Band score (1-9) for: Task Response, Coherence & Cohesion, Lexical Resource, Grammatical Range & Accuracy
- Overall band score
- Detailed feedback on each criterion
- Corrected version of their writing
- Tips for improvement
Report the result to the teacher with student name, class, and scores.
Communicate all explanations in Persian but keep English writing in English."""
    },
    "level_test": {
        "label": "🎯 Level Test",
        "prompt": """تو یک مدرس زبان انگلیسی شوخ‌طبع و صمیمی هستی که برای موسسه عماد حیدرنیا تعیین سطح می‌کنی.
شخصیت تو: گرم، دلسوز، گاهی شوخ و بامزه — مثل یه دوست که اتفاقاً خیلی هم بلده!
از شوخی‌های کوچیک فارسی استفاده کن تا آزمون ترسناک نباشه. مثلاً بعد از جواب اشتباه بگو "نگران نباش، اینشتین هم اول اشتباه می‌کرد! 😄"

زبان ارتباطی: تمام توضیحات، تشویق‌ها، بازخوردها و گزارش‌ها باید به فارسی باشن — فقط سوالات به انگلیسی.

با پرسیدن اسم دانش‌آموز به فارسی شروع کن.
بعد دقیقاً ۲۰ سوال یکی‌یکی بپرس و منتظر جواب بمون.

قوانین مهم:
- یک سوال بپرس، منتظر جواب بمون، بعد سوال بعدی
- جواب درست رو قبل از اتمام ۲۰ سوال لو نده
- سوالات به انگلیسی باشن
- ترکیب سوالات:
  * چهارگزینه‌ای (A/B/C/D) — 8 سوال
  * جای خالی — 6 سوال
  * ترجمه فارسی به انگلیسی — 4 سوال
  * پیدا کردن و تصحیح اشتباه — 2 سوال
- سوالات تدریجی سخت‌تر بشن
- شماره‌گذاری واضح: سوال ۱/۲۰، سوال ۲/۲۰، ...
- بعد از هر جواب (درست یا غلط) یه جمله کوتاه فارسی بگو — تشویق یا دلداری با کمی شوخ‌طبعی

توزیع سختی سوالات:
- سوال ۱-۴: A1 (فعل to be، حال ساده، اعداد، حروف تعریف)
- سوال ۵-۸: A2 (گذشته ساده، حال استمراری، واژگان پایه)
- سوال ۹-۱۲: B1 (حال کامل، مودال‌ها، حروف اضافه)
- سوال ۱۳-۱۶: B2 (شرطی، مجهول، جملات وصفی، واژگان پیشرفته)
- سوال ۱۷-۲۰: C1 (گرامر پیچیده، اصطلاحات، ساختارهای پیشرفته)

قوانین امتیازدهی — سخت‌گیرانه و واقع‌بینانه باش:
- فقط جواب کاملاً درست امتیاز داره — نیمه‌درست = اشتباه
- ۰ تا ۴ درست → A1
- ۵ تا ۸ درست → A2
- ۹ تا ۱۲ درست → B1
- ۱۳ تا ۱۶ درست → B2
- ۱۷ تا ۲۰ درست → C1
- اکثر زبان‌آموزان موسسه A2 یا B1 هستن — بدون دلیل کافی B2/C1 نده
- کسی که در زمان‌های پایه اشتباه داره نمی‌تونه B2 یا بالاتر باشه

بعد از ۲۰ سوال به فارسی:
- جواب‌های درست همه سوالات رو با توضیح کوتاه نشون بده
- نمره دقیق: X از ۲۰
- سطح رو بر اساس جدول بالا اعلام کن (مثال: "نمره شما ۱۱ از ۲۰ است — سطح B1")
- نقاط قوت
- نقاط ضعف
- توپیک‌های پیشنهادی برای تمرین
- نتیجه رو به مدرس (عماد حیدرنیا) گزارش بده با اسم دانش‌آموز، نمره و سطح"""
    },
}

# ── Score Storage ─────────────────────────────────────────────────────────────
all_scores = {}

# ── Keyboards ─────────────────────────────────────────────────────────────────

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 ارشد-دکتری", callback_data="cat_arshad")],
        [InlineKeyboardButton("🔤 A2Z English", callback_data="cat_a2z")],
        [InlineKeyboardButton("🎯 Level Test", callback_data="ai_topic_level_test")],
    ])

def a2z_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Exams", callback_data="cat_exams")],
        [InlineKeyboardButton("🤖 AI", callback_data="cat_ai")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")],
    ])

def exams_keyboard():
    rows = [[InlineKeyboardButton(cat["label"], callback_data="cat_" + k)] for k, cat in CATEGORIES.items()]
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_a2z")])
    return InlineKeyboardMarkup(rows)

def ai_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Grammar Practice", callback_data="ai_grammar")],
        [InlineKeyboardButton("✍️ Writing", callback_data="ai_writing")],
        [InlineKeyboardButton("🎯 Level Test", callback_data="ai_topic_level_test")],
        [InlineKeyboardButton("🔙 Back", callback_data="cat_a2z")],
    ])

def ai_grammar_keyboard():
    rows = []
    grammar_topics = [k for k in AI_TOPICS.keys() if k not in ["writing_task1", "writing_task2", "level_test"]]
    for key in grammar_topics:
        rows.append([InlineKeyboardButton(AI_TOPICS[key]["label"], callback_data="ai_topic_" + key)])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_ai")])
    return InlineKeyboardMarkup(rows)

def ai_writing_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Writing Task 1", callback_data="ai_topic_writing_task1")],
        [InlineKeyboardButton("✍️ Writing Task 2", callback_data="ai_topic_writing_task2")],
        [InlineKeyboardButton("🔙 Back", callback_data="cat_ai")],
    ])

def exam_list_keyboard(cat_key):
    cat = CATEGORIES[cat_key]
    rows = [[InlineKeyboardButton("📄 Exam " + str(i+1), callback_data="exam_" + ek)] for i, ek in enumerate(cat["exams"])]
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_exams")])
    return InlineKeyboardMarkup(rows)

def back_main_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")]])

def results_keyboard(cat_key):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Try Again", callback_data="cat_" + cat_key)],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")],
    ])

def ai_end_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 New Session", callback_data="cat_ai")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")],
    ])

def ai_active_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 بازگشت به منو اصلی", callback_data="back_main")],
    ])

def exam_active_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Submit Exam", callback_data="exam_submit")],
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

# Models to try in order — powerful first, fast as fallback
GEMINI_MODELS = [
    "gemini-2.5-flash-preview-05-20",  # جدیدترین و سریع‌ترین
    "gemini-2.5-flash",                 # پشتیبان
]

def call_gemini_api(history, new_message, model=None):
    """Call Google Gemini API (OpenAI-compatible endpoint)."""
    messages = []
    for item in history:
        role = "user" if item["role"] == "user" else "assistant"
        messages.append({"role": role, "content": item["parts"][0]})
    messages.append({"role": "user", "content": new_message})

    models_to_try = [model] if model else GEMINI_MODELS
    last_error = None

    for m in models_to_try:
        payload = {
            "model": m,
            "messages": messages,
            "max_tokens": 2048,
            "temperature": 0.7,
        }
        headers = {
            "Authorization": "Bearer " + GEMINI_API_KEY,
            "Content-Type": "application/json"
        }
        try:
            resp = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=60)
            if resp.ok:
                return resp.json()["choices"][0]["message"]["content"]
            if resp.status_code == 429:
                logger.warning("Rate limit on " + m + ", trying next model...")
                last_error = Exception("429 rate limit on " + m)
                import time; time.sleep(2)
                continue
            raise Exception(str(resp.status_code) + " " + resp.text[:200])
        except Exception as e:
            last_error = e
            logger.warning("Model " + m + " failed: " + str(e))
            continue

    raise last_error

def get_ai_session(user_id):
    if user_id not in ai_sessions:
        ai_sessions[user_id] = {"history": [], "topic": None, "active": False}
    return ai_sessions[user_id]

def clear_ai_session(user_id):
    ai_sessions[user_id] = {"history": [], "topic": None, "active": False}

async def chat_with_gemini(user_id, user_message, system_prompt=None):
    session = get_ai_session(user_id)
    if system_prompt and not session["history"]:
        session["history"].append({"role": "user", "parts": [system_prompt + "\n\nStudent: " + user_message]})
    else:
        session["history"].append({"role": "user", "parts": [user_message]})
    
    chat = gemini_model.start_chat(history=session["history"][:-1])
    response = chat.send_message(session["history"][-1]["parts"][0])
    
    session["history"].append({"role": "model", "parts": [response.text]})
    return response.text

# ── Exam helpers ───────────────────────────────────────────────────────────────

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
    await context.bot.send_message(chat_id=user_id, text=text, reply_markup=exam_active_keyboard())

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
        "╔══════════════════╗\n" +
        "║   " + title[:16].center(16) + "   ║\n" +
        "╚══════════════════╝\n\n" +
        "👤 " + name + "  |  🏫 " + cls + "\n" +
        "✅ Score: " + str(score) + "/" + str(total) + " (" + str(pct) + "%)\n" +
        "▓" * int(pct/10) + "░" * (10 - int(pct/10)) + " " + str(pct) + "%\n" +
        "⏱ Time: " + time_str + "\n" +
        grade + "\n\n"
    )
    details = "\n".join(lines)
    full = summary + details
    kb = results_keyboard(cat_key)

    if len(full) > 4000:
        await context.bot.send_message(chat_id=user_id, text=summary)
        await context.bot.send_message(chat_id=user_id, text=details, reply_markup=kb)
    else:
        await context.bot.send_message(chat_id=user_id, text=full, reply_markup=kb)

    if user_id not in context.bot_data.get("all_scores", {}):
        if "all_scores" not in context.bot_data:
            context.bot_data["all_scores"] = {}
        context.bot_data["all_scores"][user_id] = []
    context.bot_data["all_scores"][user_id].append({
        "name": name, "class": cls, "exam": title,
        "score": str(score) + "/" + str(total), "pct": str(pct) + "%",
        "time": time_str, "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

    teacher_msg = (
        "📋 NEW EXAM RESULT\n" +
        "══════════════════\n" +
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

    clear_ai_session(user_id)
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
        "سلام " + update.effective_user.first_name + " عزیز! 👋\n\n"
        "من دستیار عماد حیدرنیا، مدرس زبان انگلیسی هستم 🎓\n"
        "اینجا یاد میگیری، تمرین میکنی و پیشرفت میکنی 💪\n\n"
        "بریم شروع کنیم؟ 😊",
        reply_markup=main_menu_keyboard(),
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n/start — Main menu\n/help — This help\n"
        "/quit — Submit exam early\n/results — All scores (teacher only)\n"
        "/endai — End AI session"
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

async def endai_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    session = get_ai_session(user_id)
    if session["active"]:
        clear_ai_session(user_id)
        await update.message.reply_text(
            "✅ AI session ended.\n\nSee you next time! 😊",
            reply_markup=main_menu_keyboard()
        )
    else:
        await update.message.reply_text("No active AI session.", reply_markup=main_menu_keyboard())

async def results_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != TEACHER_ID:
        await update.message.reply_text("⛔ Teacher only.")
        return
    
    scores = context.bot_data.get("all_scores", {})
    if not scores:
        await update.message.reply_text("📊 No results yet.")
        return
    
    lines = ["📊 ALL RESULTS\n══════════════════"]
    for uid, rs in scores.items():
        for r in rs:
            lines.append(
                "👤 " + r["name"] + "  🏫 " + r.get("class", "?") + "\n" +
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

    if data == "exam_submit":
        state = get_state(context, user_id)
        if state.get("active"):
            state["active"] = False
            for j in context.job_queue.get_jobs_by_name("timer_" + str(user_id)):
                j.schedule_removal()
            await query.answer("✅ Submitting your exam...")
            await finish_exam(context, user_id, state)
        else:
            await query.answer("No active exam.")
        return

    if data == "back_main":
        state = get_state(context, user_id)
        if state.get("active"):
            state["active"] = False
            for j in context.job_queue.get_jobs_by_name("timer_" + str(user_id)):
                j.schedule_removal()
            clear_state(context, user_id)
        clear_ai_session(user_id)
        await query.edit_message_text("Please choose a category:", reply_markup=main_menu_keyboard())

    elif data == "cat_arshad":
        await query.edit_message_text(
            "📚 ارشد-دکتری — Master's & PhD Prep\n\n"
            "📌 Coming soon! 💪",
            reply_markup=back_main_keyboard()
        )

    elif data == "cat_a2z":
        await query.edit_message_text("🔤 A2Z English\n\nChoose a topic:", reply_markup=a2z_keyboard())

    elif data == "cat_exams":
        await query.edit_message_text("📝 Exams\n\nChoose a category:", reply_markup=exams_keyboard())

    elif data == "cat_ai":
        await query.edit_message_text("🤖 AI Assistant\n\nChoose a section:", reply_markup=ai_keyboard())

    elif data == "ai_grammar":
        await query.edit_message_text("📖 Grammar Practice\n\nChoose a topic:", reply_markup=ai_grammar_keyboard())

    elif data == "ai_writing":
        await query.edit_message_text("✍️ Writing\n\nChoose a task:", reply_markup=ai_writing_keyboard())

    elif data.startswith("ai_topic_"):
        topic_key = data[9:]
        topic = AI_TOPICS.get(topic_key)
        if not topic:
            await query.edit_message_text("Topic not found.", reply_markup=main_menu_keyboard())
            return

        clear_ai_session(user_id)
        session = get_ai_session(user_id)
        session["topic"] = topic_key
        session["active"] = True
        session["system_prompt"] = topic["prompt"]

        await query.edit_message_text(
            "🤖 " + topic["label"] + "\n\n"
            "AI session started!\n"
            "Type /endai to end the session.\n\n"
            "⏳ Please wait..."
        )

        try:
            loop = asyncio.get_event_loop()
            def call_gemini():
                return call_gemini_api([], topic["prompt"] + "\n\nPlease start the session now.")
            
            # Try up to 4 times with increasing delay
            resp_text = None
            last_error = None
            delays = [3, 8, 15]
            for attempt in range(4):
                try:
                    resp_text = await loop.run_in_executor(None, call_gemini)
                    break
                except Exception as e:
                    last_error = e
                    logger.warning("Groq start attempt " + str(attempt+1) + " failed: " + str(e))
                    if attempt < 3:
                        wait = delays[min(attempt, len(delays)-1)]
                        await context.bot.send_message(
                            chat_id=user_id,
                            text="⏳ سرور شلوغه، " + str(wait) + " ثانیه صبر کن... (تلاش " + str(attempt+2) + "/4)"
                        )
                        await asyncio.sleep(wait)

            if resp_text is None:
                raise last_error
                
            session["history"] = [
                {"role": "user", "parts": [topic["prompt"] + "\n\nPlease start the session now."]},
                {"role": "model", "parts": [resp_text]},
            ]
            if len(resp_text) > 4000:
                for chunk in [resp_text[i:i+4000] for i in range(0, len(resp_text), 4000)]:
                    await context.bot.send_message(chat_id=user_id, text=chunk)
            else:
                await context.bot.send_message(chat_id=user_id, text=resp_text)
        except Exception as e:
            logger.error("Groq error on start: " + str(e))
            session["active"] = False
            clear_ai_session(user_id)
            await context.bot.send_message(
                chat_id=user_id,
                text="☕ سرور رفته چایی بخوره! شماهم یه چایی بخوری بیای سرش خلوت میشه 😄\nچند دقیقه دیگه دوباره امتحان کن",
                reply_markup=main_menu_keyboard()
            )

    elif data.startswith("cat_") and data not in ("cat_arshad", "cat_a2z", "cat_ai"):
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
            "🆕 New Exam Starting!\n\n"
            "📝 " + exam["title"] + "\n\n"
            "ℹ️ " + exam["instruction"] + "\n\n"
            "✏️ Please type your full name:"
        )

# ── Message handler ────────────────────────────────────────────────────────────

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state = get_state(context, user_id)
    text = update.message.text.strip()
    # Note: AI session is checked AFTER all exam checks below

    # ── Exam registration — MUST be checked first ──
    if state.get("step") == "ask_name":
        # Clear any active AI session
        clear_ai_session(user_id)
        pending_key = state.get("pending_exam_key")
        if not pending_key or pending_key not in EXAMS:
            await update.message.reply_text(
                "⚠️ سشن منقضی شده. لطفاً از منو دوباره شروع کن.",
                reply_markup=main_menu_keyboard()
            )
            clear_state(context, user_id)
            return
        state["student_name"] = text
        state["step"] = "ask_class"
        await update.message.reply_text("👋 Hello, " + text + "!\n\n🏫 Please type your class name or number:")
        return

    if state.get("step") == "ask_class":
        # Clear any active AI session
        clear_ai_session(user_id)
        state["student_class"] = text
        pending_key = state.get("pending_exam_key")
        if not pending_key or pending_key not in EXAMS:
            await update.message.reply_text(
                "⚠️ مشکلی پیش اومد. لطفاً از منو دوباره امتحان رو شروع کن.",
                reply_markup=main_menu_keyboard()
            )
            clear_state(context, user_id)
            return
        exam = EXAMS[pending_key]
        clear_ai_session(user_id)  # ensure AI is off during exam
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
            "🆕 New Exam Starting!\n\n" +
            "╔══════════════════╗\n" +
            "║   EXAM DETAILS   ║\n" +
            "╚══════════════════╝\n\n" +
            "👤 " + state["student_name"] + "  |  🏫 " + text + "\n" +
            "📝 " + exam["title"] + "\n" +
            "ℹ️ " + exam["instruction"] + "\n\n" +
            "⏱ Time: " + str(EXAM_TIME_MINUTES) + " min  |  📊 Questions: " + str(len(exam["questions"])) + "\n\n" +
            "✔️ You will see correct answer after each question.\n\n" +
            "Good luck! 🍀  (Type /quit to submit early)"
        )
        await send_question(context, user_id, state)
        return

    # ── Exam in progress ──
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

    # ── AI session in progress ──
    session = get_ai_session(user_id)
    if session.get("active"):
        # Check cooldown
        last_msg_time = session.get("last_msg_time", 0)
        current_time = datetime.now().timestamp()
        if current_time - last_msg_time < 5:
            await update.message.reply_text("⏳ یه لحظه صبر کن... 😊")
            return
        session["last_msg_time"] = current_time

        try:
            await context.bot.send_chat_action(chat_id=user_id, action="typing")
            history = session["history"]
            
            def call_gemini_msg():
                return call_gemini_api(history, text)

            loop = asyncio.get_event_loop()

            # Try up to 4 times with increasing delay
            resp_text = None
            last_error = None
            delays = [5, 10, 20]
            for attempt in range(4):
                try:
                    resp_text = await loop.run_in_executor(None, call_gemini_msg)
                    break
                except Exception as e:
                    last_error = e
                    logger.warning("Groq msg attempt " + str(attempt+1) + " failed: " + str(e))
                    if attempt < 3:
                        wait = delays[min(attempt, len(delays)-1)]
                        await update.message.reply_text(
                            "⏳ سرور شلوغه، " + str(wait) + " ثانیه دیگه امتحان می‌کنم... (تلاش " + str(attempt+2) + "/4)"
                        )
                        await asyncio.sleep(wait)
            if resp_text is None:
                raise last_error

            session["history"].append({"role": "user", "parts": [text]})
            session["history"].append({"role": "model", "parts": [resp_text]})

            is_end = any(word in resp_text.lower() for word in ["band score", "overall:", "level:", "سطح:", "نمره:", "weekly report", "گزارش هفتگی"])

            if is_end:
                try:
                    teacher_msg = (
                        "📋 AI SESSION REPORT\n══════════════════\n" +
                        "📝 Topic: " + str(session.get("topic", "unknown")) + "\n" +
                        "📅 " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n" +
                        "══════════════════\n" +
                        resp_text[:500]
                    )
                    await context.bot.send_message(chat_id=TEACHER_ID, text=teacher_msg)
                except:
                    pass

            kb = ai_end_keyboard() if is_end else ai_active_keyboard()

            if len(resp_text) > 4000:
                chunks = [resp_text[i:i+4000] for i in range(0, len(resp_text), 4000)]
                for i, chunk in enumerate(chunks):
                    if i == len(chunks) - 1:
                        await update.message.reply_text(chunk, reply_markup=kb)
                    else:
                        await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(resp_text, reply_markup=kb)

            if is_end:
                clear_ai_session(user_id)

        except Exception as e:
            logger.error("Groq error: " + str(e))
            await update.message.reply_text(
                "☕ سرور شلوغه، یه لحظه صبر کن و دوباره بفرست 😊"
            )
        return

    # ── Default ──
    await update.message.reply_text(
        "Please use /start to open the menu. 😊",
        reply_markup=main_menu_keyboard()
    )

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("quit", quit_cmd))
    app.add_handler(CommandHandler("endai", endai_cmd))
    app.add_handler(CommandHandler("results", results_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
