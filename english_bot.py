#!/usr/bin/env python3
"""English Teaching Telegram Bot — Main Bot File with AI Features"""

import logging
import os
import json
import asyncio
from datetime import datetime, timedelta, time as dtime, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, WebAppInfo
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes,
)
from exam_data import EXAMS, CATEGORIES
from ielts_exam_data import IELTS_EXAMS, IELTS_CATEGORIES
# ترکیب همه exam ها
EXAMS = {**EXAMS, **IELTS_EXAMS}

BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
MINIAPP_URL = os.environ.get("MINIAPP_URL", "")
# آدرس Mini App جعبه لایتنر (روی همون سرور، مسیر /leitner)
LEITNER_URL = (MINIAPP_URL.rstrip("/") + "/leitner") if MINIAPP_URL else ""
TD_URL = (MINIAPP_URL.rstrip("/") + "/duel") if MINIAPP_URL else ""
TEACHER_ID = int(os.environ.get("TEACHER_ID", "0"))
EXAM_TIME_MINUTES = int(os.environ.get("EXAM_TIME_MINUTES", "30"))
import requests

import psycopg2
from psycopg2.extras import RealDictCursor

# ── Database Setup ──────────────────────────────────────────
def get_db():
    return psycopg2.connect(os.environ.get("DATABASE_URL"), sslmode="require")

def init_db():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT,
                name VARCHAR(100),
                student_class VARCHAR(50),
                activity_type VARCHAR(50),
                topic VARCHAR(100),
                score INTEGER,
                total INTEGER,
                level VARCHAR(10),
                summary TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT,
                name VARCHAR(100),
                student_class VARCHAR(50),
                action VARCHAR(50),
                detail TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id BIGINT PRIMARY KEY,
                name VARCHAR(100),
                student_class VARCHAR(50),
                phone VARCHAR(30),
                language VARCHAR(10) DEFAULT 'fa',
                created_at TIMESTAMP DEFAULT NOW(),
                last_seen TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(30)")
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS reminders_on BOOLEAN DEFAULT TRUE")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS points_log (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT,
                points INTEGER,
                reason VARCHAR(100),
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        # ── Millionaire game: پیشرفت لیگ هر کاربر ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS millionaire_progress (
                telegram_id BIGINT PRIMARY KEY,
                level_index INTEGER DEFAULT 0,
                completed_levels INTEGER DEFAULT 0,
                best_money INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                updated_at TIMESTAMP DEFAULT NOW()
            )
        """)
        # ── Millionaire game: تاریخچه بازی‌ها برای لیدربورد هفتگی ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS millionaire_games (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT,
                level_index INTEGER,
                topic VARCHAR(100),
                money_won INTEGER,
                questions_correct INTEGER,
                won_million BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        # ── Millionaire game: بانک سوالات از‌پیش‌ساخته ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS millionaire_questions (
                id SERIAL PRIMARY KEY,
                level_index INTEGER,
                topic VARCHAR(100),
                cefr VARCHAR(5),
                question TEXT,
                option_a TEXT,
                option_b TEXT,
                option_c TEXT,
                option_d TEXT,
                correct CHAR(1),
                explanation_fa TEXT,
                approved BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_mq_level_cefr ON millionaire_questions(level_index, cefr)")
        # ── Leitner box: کارت‌های هر کاربر ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leitner_cards (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT,
                front TEXT,
                back TEXT,
                box INTEGER DEFAULT 1,
                due_date DATE DEFAULT CURRENT_DATE,
                reviews INTEGER DEFAULT 0,
                correct_reviews INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_leitner_user ON leitner_cards(telegram_id, due_date)")
        # ── عکس روزانه‌ی لیدربورد برای گزارش طنز (مقایسه‌ی رتبه‌ها) ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard_snapshot (
                telegram_id BIGINT PRIMARY KEY,
                name VARCHAR(100),
                rank INTEGER,
                points INTEGER,
                taken_at TIMESTAMP DEFAULT NOW()
            )
        """)
        # ── تالار افتخارات: قهرمان و نایب‌قهرمان هر ماه (دائمی) ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS hall_of_fame (
                id SERIAL PRIMARY KEY,
                period VARCHAR(7),
                rank INTEGER,
                telegram_id BIGINT,
                name VARCHAR(100),
                points INTEGER,
                recorded_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(period, rank)
            )
        """)
        # ── Translation Duel: بانک سوال (جمله‌های فارسی + ترجمه‌ی مرجع) ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS td_questions (
                id SERIAL PRIMARY KEY,
                level VARCHAR(2),
                fa TEXT,
                en_ref TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_td_level ON td_questions(level)")
        # ── Translation Duel: بازی‌ها ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS td_matches (
                id SERIAL PRIMARY KEY,
                creator_id BIGINT,
                creator_name VARCHAR(100),
                opponent_id BIGINT,
                opponent_name VARCHAR(100),
                question_ids TEXT,
                creator_score INTEGER,
                opponent_score INTEGER,
                creator_answers TEXT,
                opponent_answers TEXT,
                status VARCHAR(20) DEFAULT 'open',
                winner_id BIGINT,
                created_at TIMESTAMP DEFAULT NOW(),
                finished_at TIMESTAMP
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_td_status ON td_matches(status)")
        # ── Translation Duel: آمار برد/باخت هر بازیکن (لیدربورد داخلی) ──
        cur.execute("""
            CREATE TABLE IF NOT EXISTS td_stats (
                telegram_id BIGINT PRIMARY KEY,
                name VARCHAR(100),
                wins INTEGER DEFAULT 0,
                draws INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                td_points INTEGER DEFAULT 0
            )
        """)
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("DB init error: " + str(e))

def save_activity(telegram_id, name, student_class, activity_type, topic, score=None, total=None, level=None, summary=None):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (telegram_id,name,student_class,activity_type,topic,score,total,level,summary) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (telegram_id, name, student_class, activity_type, topic, score, total, level, summary)
        )
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("DB save error: " + str(e))

def get_student_profile(name):
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM students WHERE LOWER(name) LIKE LOWER(%s) ORDER BY created_at DESC LIMIT 50", (f"%{name}%",))
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("DB profile error: " + str(e))
        return []

def get_all_stats():
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT name, student_class, COUNT(*) as activities,
                   ROUND(AVG(CASE WHEN total>0 THEN score::float/total*100 END)::numeric,1) as avg_score,
                   MAX(created_at) as last_active
            FROM students GROUP BY name, student_class ORDER BY last_active DESC
        """)
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("DB stats error: " + str(e))
        return []



def get_user(telegram_id):
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM users WHERE telegram_id=%s", (telegram_id,))
        row = cur.fetchone()
        if row:
            cur.execute("UPDATE users SET last_seen=NOW() WHERE telegram_id=%s", (telegram_id,))
            conn.commit()
        cur.close(); conn.close()
        return row
    except Exception as e:
        print("get_user error: " + str(e))
        return None

def save_user(telegram_id, name, student_class, language='fa', phone=''):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (telegram_id, name, student_class, language, phone)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (telegram_id) DO UPDATE
            SET name=%s, student_class=%s, language=%s, phone=%s, last_seen=NOW()
        """, (telegram_id, name, student_class, language, phone, name, student_class, language, phone))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("save_user error: " + str(e))

def add_points(telegram_id, points, reason=""):
    """اضافه کردن امتیاز"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO points_log (telegram_id, points, reason) VALUES (%s,%s,%s)",
                    (telegram_id, points, reason))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("add_points error: " + str(e))

# دستوری که به همه‌ی promptهای AI اضافه می‌شه تا آخر هر session یه نمره بده
SCORING_RULE = (
    "\n\n[GRADING — VERY IMPORTANT: When you give the final end-of-session report, "
    "you MUST evaluate how well the student actually performed during THIS session "
    "(accuracy of their answers, real effort, engagement). On the VERY LAST line of the report, "
    "output a hidden score in EXACTLY this format on its own line: SCORE: X/10  "
    "where X is an integer from 0 to 10. Give a LOW score (0-3) if the student barely "
    "engaged, sent random/irrelevant messages, or did not really do the task. Give a HIGH "
    "score (8-10) only for genuine, mostly-correct effort. Be honest and strict — this score "
    "decides their leaderboard points. Do not explain the score; just output the SCORE: line.]"
)

def m_parse_ai_score(text):
    """نمره‌ی پنهان (SCORE: X/10) رو از متن پایانی AI می‌خونه. اگه نبود، None."""
    try:
        import re as _re
        m = _re.search(r"SCORE:\s*(\d{1,2})\s*/\s*10", text, _re.IGNORECASE)
        if m:
            s = int(m.group(1))
            return max(0, min(10, s))
    except Exception:
        pass
    return None

def award_ai_points(user_id, session, ai_text=""):
    """
    امتیاز یه AI session رو یک بار (و فقط یک بار) بر اساس نمره‌ی واقعیِ AI ثبت می‌کنه.
    اگه AI نمره نداده باشه، یه نمره‌ی محافظه‌کارانه‌ی پیش‌فرض در نظر گرفته می‌شه.
    این تابع از هر جایی که session تموم می‌شه صدا زده می‌شه (دکمه، /endai، یا تشخیص خودکار).
    """
    try:
        if not session or session.get("points_done"):
            return
        topic_k = session.get("topic", "") or ""
        # بخش آلمانی امتیاز نداره
        if topic_k.startswith("de_"):
            session["points_done"] = True
            return
        # شمارش پیام‌های کاربر در این session
        user_turns = sum(1 for h in session.get("history", []) if h.get("role") == "user")
        if user_turns < 2:
            return  # تعامل کافی نبوده — امتیاز نده (ولی قفلش هم نکن)

        # نمره‌ی AI رو از متن پایانی (یا آخرین پیام model) بخون
        score = m_parse_ai_score(ai_text or "")
        if score is None:
            for h in reversed(session.get("history", [])):
                if h.get("role") == "model":
                    parts = h.get("parts", [])
                    txt = parts[0] if parts else ""
                    score = m_parse_ai_score(txt)
                    if score is not None:
                        break
        # اگه AI اصلاً نمره نداد، یه نمره‌ی متوسط محافظه‌کارانه
        if score is None:
            score = 5

        # امتیاز پایه بر اساس نوع تمرین
        if topic_k.startswith("conv_"):
            base, reason = 70, "conversation"
        elif topic_k == "level_test":
            base, reason = 30, "level test"
        elif "writing" in topic_k:
            base, reason = 60, "writing"
        elif topic_k.startswith("vocab_") or "vocab" in topic_k:
            base, reason = 50, "vocabulary"
        elif topic_k.startswith("grammar_") or "grammar" in topic_k:
            base, reason = 50, "grammar"
        else:
            base, reason = 50, "ai session"

        # امتیاز نهایی = پایه × (نمره/۱۰) — گرد شده
        pts = round(base * score / 10)
        if pts <= 0:
            # نمره‌ی صفر یا خیلی پایین → امتیاز نده ولی session رو قفل کن
            session["points_done"] = True
            return
        add_points(user_id, pts, reason + " " + topic_k + " (score " + str(score) + "/10)")
        session["points_done"] = True
    except Exception as e:
        print("award_ai_points error: " + str(e))

def get_monthly_leaderboard():
    """رتبه‌بندی ماهانه — از اول ماه جاری"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT u.name, u.student_class, u.telegram_id,
                   COALESCE(SUM(p.points),0) as total_points
            FROM users u
            LEFT JOIN points_log p ON u.telegram_id = p.telegram_id
                AND p.created_at >= date_trunc('month', CURRENT_DATE)
            GROUP BY u.telegram_id, u.name, u.student_class
            HAVING COALESCE(SUM(p.points),0) > 0
            ORDER BY total_points DESC
            LIMIT 100
        """)
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("leaderboard error: " + str(e))
        return []

def get_month_top2(year, month):
    """نفر اول و دوم یه ماه مشخص (برای ثبت در تالار افتخارات)."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT u.name, u.telegram_id, COALESCE(SUM(p.points),0) as total_points
            FROM users u
            LEFT JOIN points_log p ON u.telegram_id = p.telegram_id
                AND date_trunc('month', p.created_at) = make_date(%s, %s, 1)
            GROUP BY u.telegram_id, u.name
            HAVING COALESCE(SUM(p.points),0) > 0
            ORDER BY total_points DESC
            LIMIT 2
        """, (year, month))
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("get_month_top2 error: " + str(e))
        return []

def record_hall_of_fame_if_needed():
    """
    اگه قهرمان‌های ماه‌های گذشته هنوز ثبت نشدن، ثبتشون می‌کنه.
    این تابع هر بار که لیدربورد نشون داده می‌شه صدا زده می‌شه (ارزونه).
    فقط ماه‌های تموم‌شده رو ثبت می‌کنه، نه ماه جاری.
    """
    try:
        from datetime import date
        today = date.today()
        # ماه قبل
        if today.month == 1:
            py, pm = today.year - 1, 12
        else:
            py, pm = today.year, today.month - 1
        period = f"{py:04d}-{pm:02d}"

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM hall_of_fame WHERE period=%s", (period,))
        already = cur.fetchone()[0]
        cur.close(); conn.close()
        if already:
            return  # ماه قبل از قبل ثبت شده

        top2 = get_month_top2(py, pm)
        if not top2:
            return  # ماه قبل کسی امتیاز نداشته

        conn = get_db()
        cur = conn.cursor()
        for i, r in enumerate(top2):
            cur.execute("""
                INSERT INTO hall_of_fame (period, rank, telegram_id, name, points)
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT (period, rank) DO NOTHING
            """, (period, i + 1, r["telegram_id"], r["name"], r["total_points"]))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("record_hall_of_fame_if_needed error: " + str(e))

def get_hall_of_fame():
    """تاریخچه‌ی قهرمان‌ها: dict[period] = {1: {...}, 2: {...}}، جدیدترین اول."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT period, rank, name, points FROM hall_of_fame ORDER BY period DESC, rank ASC")
        rows = cur.fetchall(); cur.close(); conn.close()
        out = {}
        for r in rows:
            out.setdefault(r["period"], {})[r["rank"]] = {"name": r["name"], "points": r["points"]}
        return out
    except Exception as e:
        print("get_hall_of_fame error: " + str(e))
        return {}

def get_my_points(telegram_id):
    """امتیاز ماهانه یه کاربر"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT COALESCE(SUM(points),0) as monthly,
                   (SELECT COALESCE(SUM(points),0) FROM points_log WHERE telegram_id=%s) as total
            FROM points_log
            WHERE telegram_id=%s AND created_at >= date_trunc('month', CURRENT_DATE)
        """, (telegram_id, telegram_id))
        row = cur.fetchone(); cur.close(); conn.close()
        return row
    except Exception as e:
        print("my_points error: " + str(e))
        return None

# ══════════════════════════════════════════════════════════════════════════════
# ── MILLIONAIRE GAME — Database Helpers ───────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

def m_get_progress(telegram_id):
    """پیشرفت لیگ کاربر — اگه نبود می‌سازه"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM millionaire_progress WHERE telegram_id=%s", (telegram_id,))
        row = cur.fetchone()
        if not row:
            cur.execute(
                "INSERT INTO millionaire_progress (telegram_id) VALUES (%s) ON CONFLICT DO NOTHING",
                (telegram_id,)
            )
            conn.commit()
            cur.execute("SELECT * FROM millionaire_progress WHERE telegram_id=%s", (telegram_id,))
            row = cur.fetchone()
        cur.close(); conn.close()
        return row
    except Exception as e:
        print("m_get_progress error: " + str(e))
        return {"telegram_id": telegram_id, "level_index": 0, "completed_levels": 0,
                "best_money": 0, "games_played": 0}

def m_save_game(telegram_id, level_index, topic, money_won, questions_correct, won_million):
    """ثبت نتیجه یه بازی + بروزرسانی پیشرفت لیگ"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO millionaire_games
               (telegram_id, level_index, topic, money_won, questions_correct, won_million)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (telegram_id, level_index, topic, money_won, questions_correct, won_million)
        )
        # بروزرسانی best_money و games_played
        cur.execute(
            """UPDATE millionaire_progress
               SET best_money = GREATEST(best_money, %s),
                   games_played = games_played + 1,
                   updated_at = NOW()
               WHERE telegram_id=%s""",
            (money_won, telegram_id)
        )
        # اگه به یک میلیون رسیده → آنلاک فصل بعد
        if won_million:
            cur.execute(
                """UPDATE millionaire_progress
                   SET level_index = level_index + 1,
                       completed_levels = completed_levels + 1,
                       updated_at = NOW()
                   WHERE telegram_id=%s AND level_index = %s""",
                (telegram_id, level_index)
            )
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("m_save_game error: " + str(e))

def m_weekly_leaderboard():
    """لیدربورد هفتگی Millionaire — مجموع پول این هفته"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT u.name, u.student_class, g.telegram_id,
                   SUM(g.money_won) as week_money,
                   COUNT(*) as games,
                   SUM(CASE WHEN g.won_million THEN 1 ELSE 0 END) as millions
            FROM millionaire_games g
            JOIN users u ON u.telegram_id = g.telegram_id
            WHERE g.created_at >= date_trunc('week', CURRENT_DATE)
            GROUP BY g.telegram_id, u.name, u.student_class
            ORDER BY week_money DESC
            LIMIT 20
        """)
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("m_weekly_leaderboard error: " + str(e))
        return []

# ══════════════════════════════════════════════════════════════════════════════
# ── LEITNER BOX — Database Helpers ────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

# فاصله‌ی مرور هر جعبه (روز)
LEITNER_INTERVALS = {1: 1, 2: 2, 3: 4, 4: 7, 5: 15}
LEITNER_MAX_BOX = 5

def leitner_add_card(telegram_id, front, back):
    """یه کارت جدید به جعبه ۱ اضافه می‌کنه."""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO leitner_cards (telegram_id, front, back, box, due_date)
               VALUES (%s,%s,%s,1,CURRENT_DATE)""",
            (telegram_id, front.strip()[:500], back.strip()[:1000])
        )
        conn.commit(); cur.close(); conn.close()
        return True
    except Exception as e:
        print("leitner_add_card error: " + str(e))
        return False

def leitner_due_cards(telegram_id, limit=50):
    """کارت‌هایی که موعد مرورشون رسیده."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """SELECT * FROM leitner_cards
               WHERE telegram_id=%s AND due_date <= CURRENT_DATE
               ORDER BY box ASC, due_date ASC LIMIT %s""",
            (telegram_id, limit)
        )
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("leitner_due_cards error: " + str(e))
        return []

def leitner_review(telegram_id, card_id, knew):
    """نتیجه‌ی مرور یه کارت: knew=True یعنی بلد بود (جعبه بالاتر)، False یعنی برگرده جعبه ۱."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM leitner_cards WHERE id=%s AND telegram_id=%s", (card_id, telegram_id))
        card = cur.fetchone()
        if not card:
            cur.close(); conn.close()
            return False
        if knew:
            new_box = min(card["box"] + 1, LEITNER_MAX_BOX)
            correct_inc = 1
        else:
            new_box = 1
            correct_inc = 0
        interval = LEITNER_INTERVALS.get(new_box, 1)
        cur.execute(
            """UPDATE leitner_cards
               SET box=%s, due_date=CURRENT_DATE + %s, reviews=reviews+1,
                   correct_reviews=correct_reviews+%s
               WHERE id=%s AND telegram_id=%s""",
            (new_box, interval, correct_inc, card_id, telegram_id)
        )
        conn.commit(); cur.close(); conn.close()
        return True
    except Exception as e:
        print("leitner_review error: " + str(e))
        return False

def leitner_delete_card(telegram_id, card_id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM leitner_cards WHERE id=%s AND telegram_id=%s", (card_id, telegram_id))
        conn.commit(); cur.close(); conn.close()
        return True
    except Exception as e:
        print("leitner_delete_card error: " + str(e))
        return False

def leitner_stats(telegram_id):
    """تعداد کارت در هر جعبه + تعداد موعد‌رسیده."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """SELECT box, COUNT(*) as cnt FROM leitner_cards
               WHERE telegram_id=%s GROUP BY box""",
            (telegram_id,)
        )
        by_box = {r["box"]: r["cnt"] for r in cur.fetchall()}
        cur.execute(
            "SELECT COUNT(*) as due FROM leitner_cards WHERE telegram_id=%s AND due_date <= CURRENT_DATE",
            (telegram_id,)
        )
        due = cur.fetchone()["due"]
        cur.execute("SELECT COUNT(*) as total FROM leitner_cards WHERE telegram_id=%s", (telegram_id,))
        total = cur.fetchone()["total"]
        cur.close(); conn.close()
        return {"by_box": by_box, "due": due, "total": total}
    except Exception as e:
        print("leitner_stats error: " + str(e))
        return {"by_box": {}, "due": 0, "total": 0}

def leitner_set_reminders(telegram_id, on):
    """روشن/خاموش کردن یادآوری روزانه برای یه کاربر."""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET reminders_on=%s WHERE telegram_id=%s", (bool(on), telegram_id))
        conn.commit(); cur.close(); conn.close()
        return True
    except Exception as e:
        print("leitner_set_reminders error: " + str(e))
        return False

def leitner_get_reminders(telegram_id):
    """وضعیت یادآوری یه کاربر (پیش‌فرض روشن)."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT reminders_on FROM users WHERE telegram_id=%s", (telegram_id,))
        row = cur.fetchone(); cur.close(); conn.close()
        if row is None or row.get("reminders_on") is None:
            return True
        return bool(row["reminders_on"])
    except Exception as e:
        print("leitner_get_reminders error: " + str(e))
        return True

def leitner_users_with_due():
    """لیست (telegram_id, name, تعداد کارت موعد‌رسیده) برای کاربرانی که یادآوری‌شون روشنه."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT c.telegram_id, COUNT(*) as due,
                   COALESCE(u.reminders_on, TRUE) as reminders_on
            FROM leitner_cards c
            LEFT JOIN users u ON u.telegram_id = c.telegram_id
            WHERE c.due_date <= CURRENT_DATE
            GROUP BY c.telegram_id, u.reminders_on
            HAVING COALESCE(u.reminders_on, TRUE) = TRUE
        """)
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("leitner_users_with_due error: " + str(e))
        return []

def get_all_users():
    """لیست همه کاربران برای معلم"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT u.name, u.student_class, u.phone, u.telegram_id, u.created_at, u.last_seen,
                   COALESCE((SELECT SUM(points) FROM points_log WHERE telegram_id=u.telegram_id),0) as points,
                   COALESCE((SELECT COUNT(*) FROM students WHERE telegram_id=u.telegram_id),0) as activities
            FROM users u
            ORDER BY u.last_seen DESC
        """)
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("all_users error: " + str(e))
        return []

def log_activity(telegram_id, name, student_class, action, detail=""):
    """ثبت ریز فعالیت‌ها"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO activity_log (telegram_id,name,student_class,action,detail) VALUES (%s,%s,%s,%s,%s)",
            (telegram_id, name or str(telegram_id), student_class or "?", action, detail[:200])
        )
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("DB log error: " + str(e))

def get_my_stats(telegram_id):
    """آمار یه دانش‌آموز برای خودش"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT activity_type, topic, score, total, level, created_at
            FROM students WHERE telegram_id=%s ORDER BY created_at DESC LIMIT 20
        """, (telegram_id,))
        rows = cur.fetchall()
        cur.execute("""
            SELECT COUNT(*) as total,
                   ROUND(AVG(CASE WHEN total>0 THEN score::float/total*100 END)::numeric,1) as avg
            FROM students WHERE telegram_id=%s
        """, (telegram_id,))
        summary = cur.fetchone()
        cur.close(); conn.close()
        return rows, summary
    except Exception as e:
        print("DB my stats error: " + str(e))
        return [], None

def get_full_report(target_id=None):
    """گزارش ریز فعالیت‌ها برای معلم"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if target_id:
            cur.execute("""
                SELECT name, student_class, action, detail, created_at
                FROM activity_log WHERE telegram_id=%s
                ORDER BY created_at DESC LIMIT 50
            """, (target_id,))
        else:
            cur.execute("""
                SELECT name, student_class, action, detail, created_at
                FROM activity_log
                ORDER BY created_at DESC LIMIT 50
            """)
        rows = cur.fetchall()
        cur.close(); conn.close()
        return rows
    except Exception as e:
        print("DB full report error: " + str(e))
        return []

def get_today_stats():
    """آمار امروز"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT 
                COUNT(DISTINCT telegram_id) as users,
                COUNT(*) as total_activities,
                SUM(CASE WHEN activity_type='exam' THEN 1 ELSE 0 END) as exams,
                SUM(CASE WHEN activity_type='ai_session' THEN 1 ELSE 0 END) as ai_sessions,
                ROUND(AVG(CASE WHEN total>0 THEN score::float/total*100 END)::numeric,1) as avg_score
            FROM students
            WHERE created_at >= CURRENT_DATE
        """)
        row = cur.fetchone()
        
        cur.execute("""
            SELECT name, student_class, activity_type, topic, score, total, created_at
            FROM students
            WHERE created_at >= CURRENT_DATE
            ORDER BY created_at DESC
            LIMIT 20
        """)
        details = cur.fetchall()
        cur.close(); conn.close()
        return row, details
    except Exception as e:
        print("DB today stats error: " + str(e))
        return None, []

def get_weekly_stats():
    """آمار هفته اخیر"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT 
                DATE(created_at) as day,
                COUNT(DISTINCT telegram_id) as users,
                COUNT(*) as activities
            FROM students
            WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
            GROUP BY DATE(created_at)
            ORDER BY day DESC
        """)
        rows = cur.fetchall(); cur.close(); conn.close()
        return rows
    except Exception as e:
        print("DB weekly stats error: " + str(e))
        return []

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
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "past_simple": {
        "label": "📘 Past Simple",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "rather_prefer": {
        "label": "📙 Rather / Prefer",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "present_perfect": {
        "label": "📕 Present Perfect",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "present_perfect_continuous": {
        "label": "📓 Present Perfect Continuous",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "comparison": {
        "label": "📒 Comparison",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "relative_clause": {
        "label": "📔 Relative Clause",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "fanboys": {
        "label": "📃 Fanboys",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "contrast": {
        "label": "🔄 Contrast",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "conditionals": {
        "label": "🔀 Conditionals",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "passive": {
        "label": "🔃 Passive",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "causative": {
        "label": "⚙️ Causative",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "modals": {
        "label": "💬 Modals",
        "prompt": """You are a friendly, witty English teaching assistant for Emad English Lab.
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
The student's name and class are already known. Start the session directly without asking for name or class."""
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
The student's name and class are already known. Start the session directly without asking for name or class."""
    },
    "writing_task1": {
        "label": "✍️ Writing Task 1",
        "prompt": """You are a friendly IELTS Writing examiner and teacher at Emad English Lab.
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
        "prompt": """You are a friendly IELTS Writing examiner and teacher at Emad English Lab.
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
        "prompt": """تو یک مدرس زبان انگلیسی شوخ‌طبع و صمیمی هستی که برای Emad English Lab تعیین سطح می‌کنی.
شخصیت تو: گرم، دلسوز، گاهی شوخ و بامزه — مثل یه دوست که اتفاقاً خیلی هم بلده!
از شوخی‌های کوچیک فارسی استفاده کن تا آزمون ترسناک نباشه. مثلاً بعد از جواب اشتباه بگو "نگران نباش، اینشتین هم اول اشتباه می‌کرد! 😄"

زبان ارتباطی: تمام توضیحات، تشویق‌ها، بازخوردها و گزارش‌ها باید به فارسی باشن — فقط سوالات به انگلیسی.

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس.
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

# ── IELTS Vocabulary AI Topics ──
IELTS_AI_TOPICS = {
    "ielts_ch01": {
        "label": "📚 Ch1. Holiday",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 1 کتاب LWL IELTS (Holiday) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- all-in package
- breathtaking view
- charter flight
- check-in desk
- departure lounge
- far-off destination
- to get away from it all
- guided tour
- holiday brochure
- holiday destination
- hordes of tourists
- local crafts
- long weekend
- out of season
- picturesque village
- passport control
- places of interest
- wildlife safari
- self-catering
- short break
- to go sightseeing
- stunning landscape
- travel agent
- tourist trap
- youth hostel

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch02": {
        "label": "📚 Ch2. Relationship",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 2 کتاب LWL IELTS (Relationship) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to break up
- to drift apart
- to fall for
- to fall head over heels
- to fall out
- to get on well with
- to go through a rough patch
- to grow apart
- to have a lot in common
- to hit it off
- to lose touch
- to make up
- to patch things up
- to see eye to eye
- to settle down
- to split up
- to stand someone up
- to tie the knot
- childhood friend
- close-knit family
- long-distance relationship

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch03": {
        "label": "📚 Ch3. Technology",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 3 کتاب LWL IELTS (Technology) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to access websites
- to back up files
- to boot up
- to browse websites
- to charge a phone
- to click on a link
- to crash
- to download
- to go online
- to hack into
- to install software
- to log in
- to log out
- to scroll down
- to stream
- to swipe
- to update
- to upgrade
- to upload
- broadband connection
- wireless network

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch04": {
        "label": "📚 Ch4. Sports",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 4 کتاب LWL IELTS (Sports) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- an athletics meeting
- an away game
- a brisk walk
- a gym membership
- a home game
- to keep fit
- to play fair
- a personal best
- a professional athlete
- to set a record
- a sports facility
- a team player
- to train hard
- a warm-up
- to win a trophy
- to work out
- a world record
- an extreme sport
- a competitive spirit
- a fitness regime

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch05": {
        "label": "📚 Ch5. Food",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 5 کتاب LWL IELTS (Food) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to be full up
- to be starving hungry
- to bolt something down
- to eat a balanced diet
- a delicacy
- a ready meal
- a three-course meal
- to be a foodie
- to eat out
- fast food
- fine dining
- a food intolerance
- homemade food
- junk food
- locally sourced
- nutritious food
- organic food
- processed food
- a recipe
- street food
- a takeaway

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch06": {
        "label": "📚 Ch6. Education",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 6 کتاب LWL IELTS (Education) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- boarding school
- distance learning
- to fall behind
- a graduation ceremony
- higher education
- to keep up with
- a lecture
- lifelong learning
- to pass an exam
- a placement test
- private tuition
- a qualification
- to resit an exam
- a scholarship
- secondary school
- self-study
- a semester
- a student loan
- to study hard
- vocational training

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch07": {
        "label": "📚 Ch7. Work",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 7 کتاب LWL IELTS (Work) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to be your own boss
- a dead-end job
- to do a job-share
- a flexible schedule
- freelance work
- a full-time job
- to get a promotion
- a glass ceiling
- a job application
- job satisfaction
- to land a job
- to meet a deadline
- minimum wage
- to network
- a part-time job
- to resign
- self-employed
- to work overtime
- a work-life balance
- working from home

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch08": {
        "label": "📚 Ch8. Health",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 8 کتاب LWL IELTS (Health) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- aches and pains
- to be off color
- to be on the mend
- a checkup
- a chronic illness
- to come down with
- complementary medicine
- a diagnosis
- to feel under the weather
- a healthy lifestyle
- a life-threatening illness
- to make a full recovery
- mental health
- a nutritious diet
- preventive medicine
- to pull a muscle
- regular exercise
- side effects
- symptoms
- vaccination

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch09": {
        "label": "📚 Ch9. Books and Films",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 9 کتاب LWL IELTS (Books and Films) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- an action movie
- to be engrossed in
- a bestseller
- a blockbuster
- a book club
- a documentary
- a fantasy novel
- a film critic
- a gripping story
- a horror film
- a love story
- a plot
- a protagonist
- a review
- a romantic comedy
- a science fiction
- a sequel
- a short story
- a soundtrack
- a thriller
- a villain

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch10": {
        "label": "📚 Ch10. Accommodation",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 10 کتاب LWL IELTS (Accommodation) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- mod cons
- apartment block
- back garden
- detached house
- to do up a property
- a furnished flat
- a housing estate
- a landlord
- to move in
- a penthouse
- to rent
- self-contained
- semi-detached
- shared accommodation
- a studio flat
- a tenant
- terraced house
- unfurnished
- a utilities bill
- a mortgage

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch11": {
        "label": "📚 Ch11. Clothes and Fashion",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 11 کتاب LWL IELTS (Clothes and Fashion) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to be on trend
- casual clothes
- classic style
- designer label
- dressed to kill
- fashionable
- formal wear
- to go out of fashion
- hand-made
- haute couture
- a high street
- a limited edition
- luxury brand
- off the rack
- an outfit
- ready-to-wear
- second-hand clothes
- smart casual
- stylish
- timeless style
- vintage clothes

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch12": {
        "label": "📚 Ch12. Personality",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 12 کتاب LWL IELTS (Personality) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to be the life and soul of the party
- to bend over backwards
- broad-minded
- easy-going
- extrovert
- hard-working
- hot-headed
- humble
- introvert
- laid-back
- loyal
- narrow-minded
- open-minded
- outgoing
- reliable
- self-confident
- sensitive
- sociable
- stubborn
- thoughtful
- trustworthy

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch13": {
        "label": "📚 Ch13. Business",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 13 کتاب LWL IELTS (Business) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to balance the books
- cut-throat competition
- to do market research
- an entrepreneur
- to expand a business
- to go bankrupt
- to invest
- to make a profit
- to merge
- a multinational
- networking
- overhead costs
- a partnership
- a revenue
- a shareholder
- a startup
- a supply chain
- target market
- a turnover
- venture capital

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch14": {
        "label": "📚 Ch14. Physical Appearance",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 14 کتاب LWL IELTS (Physical Appearance) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to bear a resemblance
- cropped hair
- disheveled
- fair hair
- to be in good shape
- muscular
- to be petite
- to be slim
- to be stocky
- a beard
- curly hair
- dark complexion
- freckles
- to be gorgeous
- to be pretty
- to be striking
- to be tanned
- wrinkles
- youthful appearance

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch15": {
        "label": "📚 Ch15. Town and City",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 15 کتاب LWL IELTS (Town and City) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- boarded up shops
- chain stores
- to close down
- fashionable boutiques
- to get around
- housing estate
- industrial area
- inner city
- a landmark
- a local authority
- a market town
- nightlife
- pedestrian zone
- public transport
- a residential area
- run-down area
- a suburb
- traffic congestion
- urban sprawl
- a vibrant city

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch16": {
        "label": "📚 Ch16. Music",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 16 کتاب LWL IELTS (Music) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- adoring fans
- background music
- a catchy tune
- classical music
- to download tracks
- a genre
- to go on tour
- a hit song
- a live performance
- mainstream music
- a music festival
- a musician
- an orchestra
- to perform
- to play an instrument
- to release an album
- a remix
- rock music
- a singer-songwriter
- a venue

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch17": {
        "label": "📚 Ch17. Weather",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 17 کتاب LWL IELTS (Weather) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- below freezing
- bitterly cold
- a blanket of snow
- boiling hot
- changeable weather
- a cold snap
- damp weather
- a downpour
- a drought
- a flood
- foggy
- a forecast
- freezing cold
- a heatwave
- humid
- mild weather
- overcast
- pouring rain
- scorching hot
- a storm
- torrential rain

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch18": {
        "label": "📚 Ch18. Shopping",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 18 کتاب LWL IELTS (Shopping) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- advertising campaign
- big brand names
- carrier bag
- customer service
- to get a bargain
- to impulse buy
- an independent shop
- a loyalty card
- a mall
- to pay by card
- a receipt
- to return goods
- a sale
- a shopping centre
- to splurge
- value for money
- a voucher
- window shopping
- a discount
- online shopping

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch19": {
        "label": "📚 Ch19. Environment",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 19 کتاب LWL IELTS (Environment) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- air quality
- to become extinct
- climate change
- to die out
- ecosystem
- to emit
- endangered species
- fossil fuels
- global warming
- greenhouse gas
- habitat destruction
- natural disaster
- natural resources
- ozone layer
- to pollute
- to recycle
- renewable energy
- sea level
- solar power
- sustainability
- wind power

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch20": {
        "label": "📚 Ch20. Advertising",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 20 کتاب LWL IELTS (Advertising) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- advertising agency
- advertising budget
- brand awareness
- brand loyalty
- a campaign
- a commercial
- consumer behaviour
- a focus group
- to go viral
- impulse buying
- a jingle
- a logo
- market research
- mass media
- a pop-up ad
- product placement
- a slogan
- social media
- a sponsor
- target audience
- word of mouth

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
    "ielts_ch21": {
        "label": "📚 Ch21. Government",
        "prompt": """تو یک مدرس زبان انگلیسی هستی که لغات فصل 21 کتاب LWL IELTS (Government) رو تدریس می‌کنی.

شخصیت تو: صمیمی، شوخ‌طبع، دلسوز — مثل یه دوست که خوب بلده.

روش تدریس:
- لیست لغات مجاز این فصل:
- to be accountable
- ballot box
- civil rights
- civil servant
- a constitution
- corruption
- democracy
- to elect
- foreign policy
- freedom of speech
- government policy
- human rights
- to implement
- local government
- majority vote
- a minister
- national security
- opposition party
- parliament
- political party
- rule of law

- هر بار یه جمله فارسی بده که یکی از لغات بالا توشه (فقط از همین لیست استفاده کن)
- دانش‌آموز باید کل جمله رو به انگلیسی ترجمه کنه
- بعد از هر جواب فقط ۵ خط توضیح بده:
  ✅ ترجمه صحیح (لغت رو **bold** کن)
  📖 ریشه: یه جمله کوتاه (مثلاً: از لاتین X به معنای Y)
  🔤 فرم‌ها: فقط مهم‌ترین‌ها (n./v./adj./adv.)
  💡 Collocations: ۱-۲ عبارت مهم (مثلاً: book a holiday / go on holiday)
- ۲۰ جمله در هر session
- سطح جملات تدریجی سخت‌تر بشه (A2 تا B2)
- جملات فارسی کوتاه و طبیعی باشن
- بعد از ۲۰ جمله فقط نمره + ۲ نکته مهم

زبان توضیحات: فارسی
زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)
زبان مثال‌ها و word forms: انگلیسی

مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس."""
    },
}

# اضافه کردن IELTS topics به AI_TOPICS
AI_TOPICS.update(IELTS_AI_TOPICS)

# ── مکالمه تعاملی ──
GRAMMAR_CONV_TOPICS = {
    "conv_present_simple": {
        "label": "☕ Conversation: Daily Routine",
        "prompt": """You are playing a role in this scene: Two friends at a coffee shop in Tehran.
Topic focus: Present Simple (daily routines, habits, facts)

Scene intro (say this to start):
"سلام! 😄 خوش اومدی! یه قهوه سفارش دادم. راستی، معمولاً صبح‌ها چیکار می‌کنی؟"

Rules:
- Conduct the conversation in English but greet in Persian first
- Guide the student to use Present Simple naturally
- After each response, continue the conversation naturally
- If they make a grammar error, gently correct it with a smile
- Ask follow-up questions that require Present Simple
- After 10 exchanges, give feedback in Persian:
  * Grammar accuracy score
  * Best sentences used
  * 2 improvement tips
- Be warm, funny, occasionally dramatic (complain about Mondays!)


ADAPTIVE BEHAVIOR (very important):
- Assess the student's level from their FIRST response (vocabulary, grammar, sentence length)
- If they're a beginner: use simpler language, shorter sentences, be more encouraging
- If they're advanced: use richer vocabulary, ask deeper questions, challenge them
- Respond like a REAL person in this situation — natural, spontaneous, NOT scripted
- Build on what they say. Reference their previous answers. Make it feel like a real conversation.
- Keep YOUR responses short (2-3 sentences) so the student talks more
- Stay strictly on the topic/scenario

FINAL FEEDBACK (after about 8-10 exchanges, end naturally then give this in Persian):
📊 بازخورد مکالمه
✅ نقاط قوت: (چیزهایی که خوب گفت)
📝 اشکالات گرامری: (با تصحیح هر کدوم)
💡 لغات/عبارات بهتری که می‌تونست استفاده کنه
🎯 سطح تخمینی: (A2/B1/B2/C1)
امتیاز کلی: X از ۱۰
Start the scene now."""
    },
    "conv_past_simple": {
        "label": "🎬 Conversation: Weekend Story",
        "prompt": """You are playing a role: An excited classmate asking about the weekend.
Topic focus: Past Simple

Scene intro:
"Hey! How was your weekend? You look like something interesting happened! Tell me everything! 😄"

Rules:
- Keep the conversation in English
- Ask follow-up questions: Where? Who with? What happened next? How did you feel?
- Encourage use of irregular verbs (went, saw, had, met, etc.)
- Correct errors gently every 2-3 exchanges
- After 10 exchanges, give feedback in Persian
- Be enthusiastic and funny — react dramatically to their stories!


ADAPTIVE BEHAVIOR (very important):
- Assess the student's level from their FIRST response (vocabulary, grammar, sentence length)
- If they're a beginner: use simpler language, shorter sentences, be more encouraging
- If they're advanced: use richer vocabulary, ask deeper questions, challenge them
- Respond like a REAL person in this situation — natural, spontaneous, NOT scripted
- Build on what they say. Reference their previous answers. Make it feel like a real conversation.
- Keep YOUR responses short (2-3 sentences) so the student talks more
- Stay strictly on the topic/scenario

FINAL FEEDBACK (after about 8-10 exchanges, end naturally then give this in Persian):
📊 بازخورد مکالمه
✅ نقاط قوت: (چیزهایی که خوب گفت)
📝 اشکالات گرامری: (با تصحیح هر کدوم)
💡 لغات/عبارات بهتری که می‌تونست استفاده کنه
🎯 سطح تخمینی: (A2/B1/B2/C1)
امتیاز کلی: X از ۱۰
Start now."""
    },
    "conv_present_perfect": {
        "label": "✈️ Conversation: Travel Experiences",
        "prompt": """You are playing a role: An enthusiastic travel agent.
Topic focus: Present Perfect (Have you ever...? / I have never... / already/yet/just)

Scene intro:
"Welcome to Dream Travel Agency! Have you ever been abroad? We have amazing packages! 🌍"

Rules:
- Use Present Perfect questions naturally: Have you ever...? Have you already...?
- Guide student to respond with Present Perfect
- Correct errors gently
- After 10 exchanges, give feedback in Persian
- Be enthusiastic about travel, occasionally mention wild travel stories!


ADAPTIVE BEHAVIOR (very important):
- Assess the student's level from their FIRST response (vocabulary, grammar, sentence length)
- If they're a beginner: use simpler language, shorter sentences, be more encouraging
- If they're advanced: use richer vocabulary, ask deeper questions, challenge them
- Respond like a REAL person in this situation — natural, spontaneous, NOT scripted
- Build on what they say. Reference their previous answers. Make it feel like a real conversation.
- Keep YOUR responses short (2-3 sentences) so the student talks more
- Stay strictly on the topic/scenario

FINAL FEEDBACK (after about 8-10 exchanges, end naturally then give this in Persian):
📊 بازخورد مکالمه
✅ نقاط قوت: (چیزهایی که خوب گفت)
📝 اشکالات گرامری: (با تصحیح هر کدوم)
💡 لغات/عبارات بهتری که می‌تونست استفاده کنه
🎯 سطح تخمینی: (A2/B1/B2/C1)
امتیاز کلی: X از ۱۰
Start now."""
    },
    "conv_conditionals": {
        "label": "🎲 Conversation: What If?",
        "prompt": """You are playing a role: A philosophy student in a fun debate.
Topic focus: Conditionals (If I were... / If I had... / If I do...)

Scene intro:
"Hey! Let's play a game — What would you do if you won a million dollars? 💰"

Rules:
- Keep asking 'What if' questions that require conditional structures
- Mix 1st, 2nd and 3rd conditionals naturally
- Correct errors after each response
- After 10 exchanges, feedback in Persian
- Be creative and funny with your own 'what if' answers!


ADAPTIVE BEHAVIOR (very important):
- Assess the student's level from their FIRST response (vocabulary, grammar, sentence length)
- If they're a beginner: use simpler language, shorter sentences, be more encouraging
- If they're advanced: use richer vocabulary, ask deeper questions, challenge them
- Respond like a REAL person in this situation — natural, spontaneous, NOT scripted
- Build on what they say. Reference their previous answers. Make it feel like a real conversation.
- Keep YOUR responses short (2-3 sentences) so the student talks more
- Stay strictly on the topic/scenario

FINAL FEEDBACK (after about 8-10 exchanges, end naturally then give this in Persian):
📊 بازخورد مکالمه
✅ نقاط قوت: (چیزهایی که خوب گفت)
📝 اشکالات گرامری: (با تصحیح هر کدوم)
💡 لغات/عبارات بهتری که می‌تونست استفاده کنه
🎯 سطح تخمینی: (A2/B1/B2/C1)
امتیاز کلی: X از ۱۰
Start now."""
    },
    "conv_passive": {
        "label": "🔍 Conversation: Mystery Investigation",
        "prompt": """You are playing a role: A detective questioning a witness.
Topic focus: Passive Voice

Scene intro:
"Good morning. I'm Detective Smith. The museum was robbed last night. You were seen near the building. Can you explain what happened? 🔍"

Rules:
- Use passive voice naturally in questions (Was anything stolen? Were you seen?)
- Guide student to use passive in their answers
- Correct errors gently
- After 10 exchanges, feedback in Persian
- Be dramatic and serious like a real detective!


ADAPTIVE BEHAVIOR (very important):
- Assess the student's level from their FIRST response (vocabulary, grammar, sentence length)
- If they're a beginner: use simpler language, shorter sentences, be more encouraging
- If they're advanced: use richer vocabulary, ask deeper questions, challenge them
- Respond like a REAL person in this situation — natural, spontaneous, NOT scripted
- Build on what they say. Reference their previous answers. Make it feel like a real conversation.
- Keep YOUR responses short (2-3 sentences) so the student talks more
- Stay strictly on the topic/scenario

FINAL FEEDBACK (after about 8-10 exchanges, end naturally then give this in Persian):
📊 بازخورد مکالمه
✅ نقاط قوت: (چیزهایی که خوب گفت)
📝 اشکالات گرامری: (با تصحیح هر کدوم)
💡 لغات/عبارات بهتری که می‌تونست استفاده کنه
🎯 سطح تخمینی: (A2/B1/B2/C1)
امتیاز کلی: X از ۱۰
Start now."""
    },
}

VOCAB_CONV_TOPICS = {}
ch_scenarios = {
    1: ("☕ At a Travel Agency", "Two people at a travel agency planning a holiday"),
    2: ("💬 Catching Up", "Two old friends who haven't seen each other"),
    3: ("💻 Tech Support", "Frustrated customer calling tech support — hilarious scenario!"),
    4: ("⚽ Post-Match Chat", "Two fans after a sports game"),
    5: ("🍕 At a Restaurant", "Customer and enthusiastic waiter"),
    6: ("📚 Study Group", "Two students preparing for exams"),
    7: ("💼 Job Interview", "Nervous candidate and interviewer"),
    8: ("🏥 Doctor's Visit", "Patient describing symptoms to doctor"),
    9: ("🎭 Book Club", "Two passionate readers discussing a book/film"),
    10: ("🏠 House Hunting", "Eager buyer and estate agent"),
    11: ("🛍️ Shopping Trip", "Two friends shopping together"),
    12: ("🤔 First Impressions", "Describing people at a party"),
    13: ("🤝 Business Pitch", "Entrepreneur pitching to investor"),
    14: ("👤 Lost & Found", "Describing a missing person to police"),
    15: ("🗺️ Tourist Guide", "Local helping a lost tourist"),
    16: ("🎵 Music Festival", "Two fans at a concert"),
    17: ("☔ Weather Chat", "Small talk about weather — British style!"),
    18: ("🛒 Market Day", "Shopper and market vendor"),
    19: ("🌿 Green Debate", "Environmental discussion at a cafe"),
    20: ("📺 Ad Pitch", "Creative team presenting ad campaign"),
    21: ("🗳️ Town Meeting", "Citizens discussing local issues"),
}
ch_names = {1:"Holiday",2:"Relationship",3:"Technology",4:"Sports",5:"Food",6:"Education",7:"Work",8:"Health",9:"Books and Films",10:"Accommodation",11:"Clothes and Fashion",12:"Personality",13:"Business",14:"Physical Appearance",15:"Town and City",16:"Music",17:"Weather",18:"Shopping",19:"Environment",20:"Advertising",21:"Government"}

for ch_num in range(1, 22):
    ch_name = ch_names[ch_num]
    emoji_scenario, scene_desc = ch_scenarios[ch_num]
    VOCAB_CONV_TOPICS[f"conv_ielts_ch{ch_num:02d}"] = {
        "label": f"{emoji_scenario}: {ch_name}",
        "prompt": f"""You are playing a role in this scene: {scene_desc}
Topic vocabulary: Chapter {ch_num} — {ch_name} (LWL IELTS vocabulary)

Scene intro: Start the scene naturally in English, setting up the situation.

Rules:
- Conduct the conversation in English
- Design questions/responses that naturally require vocabulary from Chapter {ch_num}
- When the student uses a chapter word correctly, react positively ✨
- If they struggle, gently hint at the right word
- Keep it fun and natural — don't make it feel like a test!
- After 10 exchanges, give feedback in Persian:
  * How many chapter words they used
  * Best vocabulary usage examples
  * 2 suggestions for improvement
- Be creative with your character — add personality and humor!


ADAPTIVE BEHAVIOR (very important):
- Assess the student's level from their FIRST response (vocabulary, grammar, sentence length)
- If they're a beginner: use simpler language, shorter sentences, be more encouraging
- If they're advanced: use richer vocabulary, ask deeper questions, challenge them
- Respond like a REAL person in this situation — natural, spontaneous, NOT scripted
- Build on what they say. Reference their previous answers. Make it feel like a real conversation.
- Keep YOUR responses short (2-3 sentences) so the student talks more
- Stay strictly on the topic/scenario

FINAL FEEDBACK (after about 8-10 exchanges, end naturally then give this in Persian):
📊 بازخورد مکالمه
✅ نقاط قوت: (چیزهایی که خوب گفت)
📝 اشکالات گرامری: (با تصحیح هر کدوم)
💡 لغات/عبارات بهتری که می‌تونست استفاده کنه
🎯 سطح تخمینی: (A2/B1/B2/C1)
امتیاز کلی: X از ۱۰
Start the scene now."""
    }

print(f"Grammar conv: {len(GRAMMAR_CONV_TOPICS)}, Vocab conv: {len(VOCAB_CONV_TOPICS)}")


# ── German AI Topics ──────────────────────────────────────────
GERMAN_AI_TOPICS = {
    "de_grammar": {
        "label": "📖 Grammar Practice",
        "prompt": """Du bist ein freundlicher Englischlehrer bei Emad Eng Lab für deutschsprachige Schüler.
WICHTIG: Sprich NUR auf Deutsch. Niemals Persisch oder Englisch in Erklärungen.
Persönlichkeit: warm, ermutigend, manchmal witzig.

UNTERRICHTSMETHODE — GENAU SO VORGEHEN:
1. Frage nach dem Namen des Schülers auf Deutsch
2. Gib SOFORT danach einen deutschen Satz, den der Schüler ins Englische übersetzen soll
3. Warte auf die Antwort
4. Gib Feedback auf Deutsch:
   ✅ Richtige Übersetzung
   📝 Grammatikpunkt kurz erklärt (auf Deutsch)
   ➡️ Nächster Satz sofort danach
5. Wiederhole bis 20 Sätze

GRAMMATIKTHEMEN (abwechseln):
Present Simple, Present Continuous, Past Simple, Present Perfect, Modals (can/must/should), Conditionals, Passive Voice, Relative Clauses

BEISPIEL wie du vorgehen sollst:
"Wie heißt du?"
[Schüler antwortet]
"Super [Name]! Los geht's! Übersetze diesen Satz ins Englische:
**Satz 1/20:** Ich gehe jeden Tag zur Schule."
[Schüler antwortet]
"✅ Richtig! 'I go to school every day.' — Present Simple für regelmäßige Handlungen.
**Satz 2/20:** Er arbeitet gerade im Büro."

Sätze: einfach, natürlich, Alltagssprache (A2→B2)
Nach 20 Sätzen: kurzer Bericht auf Deutsch mit Noten und Tipps"""
    },
    "de_vocabulary": {
        "label": "📚 Vocabulary Practice",
        "prompt": """You are a friendly English vocabulary teacher at Emad Eng Lab for German-speaking students.
IMPORTANT: Speak ONLY in German. Never use Persian or Farsi.
Personality: warm, witty, encouraging.

Teaching method:
- Give a German sentence containing a target English vocabulary word (shown as ___)
- Student must translate the full sentence to English
- After each answer give feedback in German (max 5 lines):
  ✅ Correct translation (**bold** the key word)
  📖 Word origin: one short sentence in German
  🔤 Word forms: noun/verb/adjective/adverb (most important ones)
  💡 Collocations: 1-2 important phrases
- 20 sentences per session
- Gradually increase difficulty (A2 to B2)
- After 20 sentences give score + 2 key points in German

Language: ALL in German
Student answers: in ENGLISH
Start by asking for student name in German."""
    },
    "de_writing_task1": {
        "label": "✍️ Writing Task 1",
        "prompt": """You are an IELTS Writing Task 1 examiner and teacher at Emad Eng Lab for German-speaking students.
IMPORTANT: Speak ONLY in German. Never use Persian or Farsi.
Be encouraging, supportive and occasionally witty.

Give the student an IELTS Writing Task 1 prompt (graph/chart/diagram description).
After they submit, provide feedback in German:
- Band score estimate
- Coherence & Cohesion
- Lexical Resource
- Grammatical Range & Accuracy
- Corrected version
- Tips for improvement in German

Language: ALL feedback and instructions in GERMAN. Keep English writing in English.
Start by asking for student name in German."""
    },
    "de_writing_task2": {
        "label": "✍️ Writing Task 2",
        "prompt": """You are an IELTS Writing Task 2 examiner and teacher at Emad Eng Lab for German-speaking students.
IMPORTANT: Speak ONLY in German. Never use Persian or Farsi.
Be encouraging and supportive.

Give the student an IELTS Writing Task 2 essay prompt.
After they submit, provide feedback in German:
- Band score estimate
- Task Achievement
- Coherence & Cohesion
- Lexical Resource
- Grammatical Range & Accuracy
- Corrected version
- Tips for improvement

Language: ALL feedback in GERMAN. Keep English writing in English.
Start by asking for student name in German."""
    },
    "de_level_test": {
        "label": "🎯 Level Test",
        "prompt": """Du bist ein freundlicher Englisch-Einstufungstest-Prüfer bei Emad Eng Lab für deutschsprachige Schüler.
Sprich NUR auf Deutsch. Niemals Persisch oder Farsi.
Sei warm, ermutigend und manchmal lustig — wie ein guter Freund!

Beginne damit, nach dem Namen des Schülers auf Deutsch zu fragen.
Stelle dann genau 20 Fragen EINZELN:
- Multiple Choice (A/B/C/D) — 8 Fragen
- Lückentext — 6 Fragen
- Übersetze deutschen Satz ins Englische — 4 Fragen
- Fehler finden und korrigieren — 2 Fragen

Schwierigkeitsverteilung:
- Fragen 1-4: A1 (Grundlagen)
- Fragen 5-8: A2
- Fragen 9-12: B1
- Fragen 13-16: B2
- Fragen 17-20: C1

BEWERTUNG — sei streng und realistisch:
- 0-4 richtig → A1
- 5-8 richtig → A2
- 9-12 richtig → B1
- 13-16 richtig → B2
- 17-20 richtig → C1

Nach 20 Fragen auf Deutsch:
- Alle richtigen Antworten mit kurzer Erklärung
- Genaue Punktzahl: X von 20
- Niveau gemäß Tabelle
- Stärken und Schwächen
- Empfohlene Themen zum Üben
- Ergebnis an Lehrer (Emad Heydarnia) melden"""
    },
}

# اضافه کردن German topics به AI_TOPICS
AI_TOPICS.update(GERMAN_AI_TOPICS)
# اضافه کردن مکالمه‌های تعاملی
AI_TOPICS.update(GRAMMAR_CONV_TOPICS)
AI_TOPICS.update(VOCAB_CONV_TOPICS)

# ── Score Storage ─────────────────────────────────────────────────────────────
all_scores = {}

# ── Keyboards ─────────────────────────────────────────────────────────────────

def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Persian Students", callback_data="lang_persian")],
        [InlineKeyboardButton("German Students", callback_data="lang_german")],
    ])

def persian_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 ارشد-دکتری", callback_data="cat_arshad")],
        [InlineKeyboardButton("🔤 A2Z English", callback_data="cat_a2z")],
        [InlineKeyboardButton("🎯 Level Test", callback_data="ai_topic_level_test")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")],
    ])

def german_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Exams", callback_data="cat_exams")],
        [InlineKeyboardButton("📚 Vocabulary (AI)", callback_data="cat_vocabulary_de")],
        [InlineKeyboardButton("📖 Grammar (AI)", callback_data="cat_grammar_de")],
        [InlineKeyboardButton("✍️ Writing (AI)", callback_data="ai_writing_de")],
        [InlineKeyboardButton("🎯 Level Test", callback_data="ai_topic_de_level_test")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")],
    ])

def german_vocabulary_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 Topic Related Vocabulary", callback_data="cat_ielts_de")],
        [InlineKeyboardButton("📖 Vocabulary for IELTS", callback_data="cat_vocab_ielts_de")],
        [InlineKeyboardButton("🔙 Back", callback_data="lang_german")],
    ])

def german_grammar_keyboard():
    """Grammar topics for German students — mapped to de_grammar"""
    excluded = ["writing_task1", "writing_task2", "level_test"] + [k for k in AI_TOPICS.keys() if k.startswith("ielts_") or k.startswith("de_")]
    grammar_topics = [k for k in AI_TOPICS.keys() if k not in excluded]
    rows = []
    for key in grammar_topics:
        rows.append([InlineKeyboardButton(AI_TOPICS[key]["label"], callback_data="ai_topic_de_grammar_" + key)])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="lang_german")])
    return InlineKeyboardMarkup(rows)

def german_writing_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Writing Task 1", callback_data="ai_topic_de_writing_task1")],
        [InlineKeyboardButton("✍️ Writing Task 2", callback_data="ai_topic_de_writing_task2")],
        [InlineKeyboardButton("🔙 Back", callback_data="lang_german")],
    ])

def german_ielts_menu_keyboard():
    rows = []
    for k, v in IELTS_AI_TOPICS.items():
        rows.append([InlineKeyboardButton(v["label"], callback_data="ai_topic_dei_" + k)])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_vocabulary_de")])
    return InlineKeyboardMarkup(rows)

def a2z_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝 Exams", callback_data="cat_exams")],
        [InlineKeyboardButton("📚 Vocabulary (AI)", callback_data="cat_vocabulary")],
        [InlineKeyboardButton("📖 Grammar (AI)", callback_data="cat_ai")],
        [InlineKeyboardButton("💬 Interactive Speaking", callback_data="cat_speaking")],
        [InlineKeyboardButton("🎬 Millionaire Game", callback_data="cat_millionaire")],
        [InlineKeyboardButton("✍️ Writing (AI)", callback_data="ai_writing")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_main")],
    ])

def speaking_keyboard():
    """منوی اصلی Interactive Speaking"""
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Grammar Speaking", callback_data="speaking_grammar")],
        [InlineKeyboardButton("📚 Vocabulary Speaking", callback_data="speaking_vocab")],
        [InlineKeyboardButton("🌟 Legends", callback_data="speaking_legends")],
        [InlineKeyboardButton("🔙 Back", callback_data="cat_a2z")],
    ])

def speaking_grammar_keyboard():
    """Grammar Speaking — همون topics گرامر"""
    rows = []
    excluded = ["writing_task1", "writing_task2", "level_test"] + [
        k for k in AI_TOPICS.keys() if k.startswith("ielts_") or k.startswith("de_") or k.startswith("conv_")
    ]
    grammar_topics = [k for k in AI_TOPICS.keys() if k not in excluded]
    for key in grammar_topics:
        label = AI_TOPICS[key]["label"]
        rows.append([InlineKeyboardButton(label, callback_data="speaking_" + key)])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_speaking")])
    return InlineKeyboardMarkup(rows)

def speaking_vocab_keyboard():
    """Vocabulary Speaking — همون فصل‌های IELTS"""
    rows = []
    for k, v in IELTS_AI_TOPICS.items():
        rows.append([InlineKeyboardButton(v["label"], callback_data="speaking_vocab_" + k)])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_speaking")])
    return InlineKeyboardMarkup(rows)

def speaking_legends_keyboard():
    """Legends — شخصیت‌های معروف"""
    legends = [
        ("🌹 Rumi (Molana)", "rumi"),
        ("🌸 Hafiz", "hafiz"),
        ("🍷 Khayyam", "khayyam"),
        ("📚 Dostoevsky", "dostoevsky"),
        ("⚽ Ronaldo", "ronaldo"),
        ("🐐 Messi", "messi"),
        ("🎵 Adele", "adele"),
        ("🎬 Christopher Nolan", "nolan"),
        ("💡 Einstein", "einstein"),
        ("🎤 Freddie Mercury", "freddie"),
    ]
    rows = [[InlineKeyboardButton(name, callback_data="speaking_legend_" + key)] for name, key in legends]
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_speaking")])
    return InlineKeyboardMarkup(rows)

def vocabulary_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌍 Topic Related Vocabulary", callback_data="cat_ielts")],
        [InlineKeyboardButton("📖 Vocabulary for IELTS", callback_data="cat_vocab_ielts")],
        [InlineKeyboardButton("🔙 Back", callback_data="cat_a2z")],
    ])

def ielts_menu_keyboard():
    """منوی فصل‌های Topic Related Vocabulary"""
    rows = []
    for k, v in IELTS_AI_TOPICS.items():
        rows.append([InlineKeyboardButton(v["label"], callback_data="ai_topic_" + k)])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_vocabulary")])
    return InlineKeyboardMarkup(rows)

def exams_keyboard():
    rows = [[InlineKeyboardButton(cat["label"], callback_data="cat_" + k)] for k, cat in CATEGORIES.items()]
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_a2z")])
    return InlineKeyboardMarkup(rows)

def ai_keyboard():
    """Grammar (AI) menu — مستقیم به لیست topics"""
    return ai_grammar_keyboard()

def ai_grammar_keyboard():
    rows = []
    excluded = ["writing_task1", "writing_task2", "level_test"] + [k for k in AI_TOPICS.keys() if k.startswith("ielts_") or k.startswith("de_") or k.startswith("conv_")]
    grammar_topics = [k for k in AI_TOPICS.keys() if k not in excluded]
    for key in grammar_topics:
        rows.append([InlineKeyboardButton(AI_TOPICS[key]["label"], callback_data="ai_topic_" + key)])
    rows.append([InlineKeyboardButton("💬 Conversation Practice", callback_data="cat_conv_grammar")])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_ai")])
    return InlineKeyboardMarkup(rows)

def conv_grammar_keyboard():
    rows = []
    for key, val in GRAMMAR_CONV_TOPICS.items():
        rows.append([InlineKeyboardButton(val["label"], callback_data="ai_topic_" + key)])
    rows.append([InlineKeyboardButton("🔙 Back", callback_data="ai_grammar")])
    return InlineKeyboardMarkup(rows)

def ai_writing_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Writing Task 1", callback_data="ai_topic_writing_task1")],
        [InlineKeyboardButton("✍️ Writing Task 2", callback_data="ai_topic_writing_task2")],
        [InlineKeyboardButton("🔙 Back", callback_data="cat_a2z")],
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

def main_reply_keyboard():
    """Reply keyboard — همیشه پایین صفحه"""
    return ReplyKeyboardMarkup([
        ["📊 My Score", "📈 My Progress"],
        ["🏆 Leaderboard", "🏠 Main Menu"],
    ], resize_keyboard=True, one_time_keyboard=False)

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

# Models to try in order — همه معتبر در ژوئن ۲۰۲۶ (مدل‌های 2.0 و 1.5 تعطیل شدن)
GEMINI_MODELS = [
    "gemini-2.5-flash",        # اصلی — پایدار
    "gemini-2.5-flash-lite",   # سبک‌تر و سریع‌تر (پشتیبان)
    "gemini-flash-latest",     # همیشه جدیدترین Flash (آخرین تلاش)
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
            if resp.status_code in (429, 503, 529):
                logger.warning("Model " + m + " busy (" + str(resp.status_code) + "), trying next...")
                last_error = Exception(str(resp.status_code) + " on " + m)
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
    # اگه session فعالی با تعامل کافی هست، قبل از پاک کردن امتیازش رو ثبت کن
    try:
        sess = ai_sessions.get(user_id)
        if sess and sess.get("active") and not sess.get("points_done"):
            award_ai_points(user_id, sess)
    except Exception as e:
        print("clear_ai_session award error: " + str(e))
    ai_sessions[user_id] = {"history": [], "topic": None, "active": False}

# ══════════════════════════════════════════════════════════════════════════════
# ── MILLIONAIRE GAME — Engine ─────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

# ترتیب لیگ — هر فصل یه grammar topic از AI_TOPICS (به ترتیب سختی A2→C1)
MILLIONAIRE_LEAGUE = [
    "present_simple_continuous",
    "past_simple",
    "present_perfect",
    "present_perfect_continuous",
    "comparison",
    "rather_prefer",
    "relative_clause",
    "fanboys",
    "contrast",
    "conditionals",
    "passive",
    "causative",
    "modals",
]

# نردبان جایزه (۱۵ سوال) + دو safe haven
MILLIONAIRE_LADDER = [
    100, 200, 300, 500, 1000,        # Q1-5  (safe haven: 1,000)
    2000, 4000, 8000, 16000, 32000,  # Q6-10 (safe haven: 32,000)
    64000, 125000, 250000, 500000, 1000000,  # Q11-15 (€1,000,000)
]
MILLIONAIRE_SAFE = {4: 1000, 9: 32000}   # index سوال (۰-based) که بعدش safe می‌شه
MILLIONAIRE_TOTAL_Q = 15
M_QUESTION_SECONDS = 90   # زمان هر سوال (ثانیه)
M_TIMER_GRACE = 3        # چند ثانیه ارفاق برای تأخیر شبکه

# سطح CEFR هر سوال بر اساس شماره‌اش
def m_level_for_q(qnum):
    if qnum <= 3:   return "A2"
    if qnum <= 7:   return "B1"
    if qnum <= 11:  return "B2"
    return "C1"

def m_topic_label(level_index):
    key = MILLIONAIRE_LEAGUE[level_index]
    t = AI_TOPICS.get(key, {})
    return t.get("label", key)

def m_fmt_money(n):
    return "€" + format(n, ",")

def m_build_question_prompt(level_index, qnum):
    """پرامپت تولید یه سوال چندگزینه‌ای گرامری توسط Gemini"""
    current_key = MILLIONAIRE_LEAGUE[level_index]
    current_label = m_topic_label(level_index)
    review_keys = MILLIONAIRE_LEAGUE[:level_index]
    review_labels = [AI_TOPICS.get(k, {}).get("label", k) for k in review_keys]
    review_txt = ""
    if review_labels:
        clean = [r.split(" ", 1)[-1] if " " in r else r for r in review_labels]
        review_txt = ("You MAY also draw from these previously-mastered review topics "
                      "(about 30% of questions): " + ", ".join(clean) + ".\n")
    cefr = m_level_for_q(qnum)
    return f"""You are the question writer for a 'Who Wants to Be a Millionaire' English grammar game.
Generate ONE multiple-choice grammar question.

MAIN TOPIC for this level: {current_label}
{review_txt}Difficulty (CEFR): {cefr}  (this is question {qnum} of 15 — gets harder as the number grows)

STRICT RULES:
- The question tests ENGLISH GRAMMAR (a fill-in-the-blank sentence or a "choose the correct form" item).
- Exactly 4 options labelled A, B, C, D. Exactly ONE is correct.
- Options must be plausible — wrong ones reflect common learner mistakes.
- Keep the question text in ENGLISH. Keep it short (one sentence + the blank).
- Write a SHORT explanation in PERSIAN (Farsi), max 2 sentences, explaining why the answer is correct.

Return ONLY valid JSON, no markdown, no extra text, exactly this shape:
{{"question":"...","options":{{"A":"...","B":"...","C":"...","D":"..."}},"correct":"A","explanation_fa":"..."}}"""

def m_parse_question(raw):
    """خروجی JSON مدل رو امن پارس می‌کنه"""
    import json as _json, re as _re
    txt = raw.strip()
    txt = txt.replace("```json", "").replace("```", "").strip()
    # اولین { تا آخرین }
    s = txt.find("{"); e = txt.rfind("}")
    if s != -1 and e != -1:
        txt = txt[s:e+1]
    data = _json.loads(txt)
    opts = data["options"]
    correct = str(data["correct"]).strip().upper()[:1]
    if correct not in ("A", "B", "C", "D"):
        raise ValueError("bad correct letter")
    for L in ("A", "B", "C", "D"):
        if L not in opts:
            raise ValueError("missing option " + L)
    return {
        "question": str(data["question"]).strip(),
        "options": {L: str(opts[L]).strip() for L in ("A", "B", "C", "D")},
        "correct": correct,
        "explanation_fa": str(data.get("explanation_fa", "")).strip(),
    }

def m_pick_from_bank(level_index, cefr, exclude_ids):
    """یه سوال تصادفی از بانک DB می‌گیره که قبلاً توی همین بازی نیومده باشه."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if exclude_ids:
            cur.execute(
                """SELECT * FROM millionaire_questions
                   WHERE level_index=%s AND cefr=%s AND approved=TRUE
                     AND id <> ALL(%s)
                   ORDER BY RANDOM() LIMIT 1""",
                (level_index, cefr, list(exclude_ids)),
            )
        else:
            cur.execute(
                """SELECT * FROM millionaire_questions
                   WHERE level_index=%s AND cefr=%s AND approved=TRUE
                   ORDER BY RANDOM() LIMIT 1""",
                (level_index, cefr),
            )
        row = cur.fetchone()
        # اگه برای این سطح خالی بود، از کل فصل بگیر
        if not row:
            cur.execute(
                """SELECT * FROM millionaire_questions
                   WHERE level_index=%s AND approved=TRUE
                   ORDER BY RANDOM() LIMIT 1""",
                (level_index,),
            )
            row = cur.fetchone()
        cur.close(); conn.close()
        if not row:
            return None
        return {
            "id": row["id"],
            "question": row["question"],
            "options": {"A": row["option_a"], "B": row["option_b"],
                        "C": row["option_c"], "D": row["option_d"]},
            "correct": str(row["correct"]).strip().upper()[:1],
            "explanation_fa": row.get("explanation_fa", "") or "",
        }
    except Exception as e:
        print("m_pick_from_bank error: " + str(e))
        return None

async def m_generate_question(level_index, qnum, used_ids=None):
    """اول از بانک DB می‌گیره؛ اگه بانک خالی بود، زنده از Gemini می‌سازه (fallback)."""
    cefr = m_level_for_q(qnum)
    used_ids = used_ids or set()
    # ۱) بانک از‌پیش‌ساخته
    q = m_pick_from_bank(level_index, cefr, used_ids)
    if q:
        return q
    # ۲) fallback زنده
    loop = asyncio.get_event_loop()
    prompt = m_build_question_prompt(level_index, qnum)
    last_err = None
    for attempt in range(3):
        try:
            raw = await loop.run_in_executor(None, lambda: call_gemini_api([], prompt))
            parsed = m_parse_question(raw)
            parsed["id"] = None
            return parsed
        except Exception as e:
            last_err = e
            logger.warning("Millionaire Q gen attempt " + str(attempt+1) + " failed: " + str(e))
            await asyncio.sleep(2)
    raise last_err

# ── Keyboards بازی ──
def m_money_at(qindex_failed):
    """پولی که با باخت در سوال qindex_failed برداشت میشه (آخرین safe haven)"""
    won = 0
    for safe_idx, amount in MILLIONAIRE_SAFE.items():
        if qindex_failed > safe_idx:
            won = max(won, amount)
    return won



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

    # ذخیره در دیتابیس
    save_activity(
        telegram_id=user_id,
        name=name,
        student_class=cls,
        activity_type="exam",
        topic=title,
        score=score,
        total=total,
        summary=str(pct) + "%"
    )

    # امتیازدهی (فقط Persian Students — غیر آلمانی)
    if not cat_key.startswith("de_"):
        if pct >= 80:
            add_points(user_id, 100, "exam 80%+: " + title)
        elif pct >= 60:
            add_points(user_id, 60, "exam 60-79%: " + title)
        else:
            add_points(user_id, 20, "exam <60%: " + title)

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
    user_id = update.effective_user.id
    tg_name = update.effective_user.first_name or ""
    log_activity(user_id, tg_name, "", "start", "Bot opened")

    await update.message.reply_text(
        "👋 Welcome to Emad Eng Lab!\n\n"
        "🌟 Your English learning journey starts here.\n\n"
        f"سلام {tg_name} عزیز! به Emad Eng Lab خوش اومدی 🎓",
        reply_markup=main_reply_keyboard(),
    )

    user = get_user(user_id)
    if user and user.get("name"):
        await update.message.reply_text(
            f"خوش برگشتی {user['name']} عزیز! 🎉\n\nگروه خود را انتخاب کن 👇",
            reply_markup=main_menu_keyboard(),
        )
    else:
        await update.message.reply_text(
            "گروه خود را انتخاب کن 👇",
            reply_markup=main_menu_keyboard(),
        )


async def feedback_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    msg = " ".join(context.args) if context.args else ""
    if not msg:
        await update.message.reply_text(
            "📬 صندوق نظرات و پیشنهادات\n\n"
            "نظر یا پیشنهادت رو بنویس:\n"
            "/feedback [پیام شما]\n\n"
            "مثال:\n/feedback کاش بخش Speaking هم داشت"
        )
        return
    user = update.effective_user
    log_activity(user_id, user.first_name or str(user_id), "", "feedback", msg[:500])
    try:
        await context.bot.send_message(
            chat_id=TEACHER_ID,
            text="📬 نظر جدید\n" + "━"*20 + "\n"
                 f"👤 {user.first_name or 'ناشناس'} (ID: {user_id})\n"
                 f"💬 {msg}"
        )
    except:
        pass
    await update.message.reply_text("✅ نظرت ثبت شد! ممنون 🙏")


async def leaderboard_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    record_hall_of_fame_if_needed()
    rows = get_monthly_leaderboard()
    import calendar
    month_name = calendar.month_name[datetime.now().month]
    if not rows:
        await update.message.reply_text(
            f"\U0001f3c6 جدول رتبه\u200cبندی {month_name}\n\nهنوز کسی امتیازی نگرفته!\nاولین نفر باش \U0001f31f"
        )
        return
    user_id = update.effective_user.id
    medals = ["\U0001f947","\U0001f948","\U0001f949"]

    # ── تالار افتخارات: قهرمان‌های ماه‌های قبل ──
    hof = get_hall_of_fame()
    hof_text = ""
    if hof:
        hof_text = "\U0001f3c5 تالار افتخارات\n" + "\u2501"*22 + "\n"
        for period in list(hof.keys())[:12]:  # حداکثر ۱۲ ماه اخیر
            champs = hof[period]
            first = champs.get(1)
            second = champs.get(2)
            line = "\U0001f4c5 " + period + ": "
            if first:
                line += "\U0001f947 " + first["name"]
            if second:
                line += "  \U0001f948 " + second["name"]
            hof_text += line + "\n"
        hof_text += "\n"

    header = hof_text + f"\U0001f3c6 جدول رتبه\u200cبندی ماه {month_name}\n" + "\u2501"*22 + "\n\n"
    footer = ("\n" + "\u2501"*22 + "\n"
              "\U0001f381 جایزه نفر اول: ۱,۰۰۰,۰۰۰ تومان تخفیف\n"
              "\U0001f381 جایزه نفر دوم: ۵۰۰,۰۰۰ تومان تخفیف\n"
              "\n\u23f3 رتبه\u200cبندی اول هر ماه ریست می\u200cشه")
    lines = []
    LRM = "\u200e"  # Left-to-Right Mark — ساختار «رتبه ... pts» رو ثابت نگه می‌داره
    for i, r in enumerate(rows):
        rank = medals[i] if i < 3 else f"{i+1}."
        me = " \U0001f449 تو" if r["telegram_id"] == user_id else ""
        lines.append(LRM + f"{rank} {r['name']} — {r['total_points']} pts{me}")
    # تقسیم به چند پیام اگه طولانی شد (محدودیت ۴۰۹۶ کاراکتر تلگرام)
    chunks = []
    cur_chunk = ""
    for line in lines:
        if len(cur_chunk) + len(line) + 1 > 3500:
            chunks.append(cur_chunk)
            cur_chunk = ""
        cur_chunk += line + "\n"
    if cur_chunk:
        chunks.append(cur_chunk)
    total = len(chunks)
    for idx, chunk in enumerate(chunks):
        text = ""
        if idx == 0:
            text += header
        text += chunk
        if idx == total - 1:
            text += footer
        await update.message.reply_text(text)

async def users_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TEACHER_ID:
        await update.message.reply_text("\U0001f6ab Teacher only.")
        return
    rows = get_all_users()
    if not rows:
        await update.message.reply_text("هنوز کاربری ثبت نشده.")
        return
    msg = "\U0001f465 لیست همه کاربران\n" + "\u2501"*22 + "\n\n"
    for r in rows:
        phone = r["phone"] if r.get("phone") else "—"
        last = r["last_seen"].strftime("%m/%d") if r.get("last_seen") else "—"
        msg += f"\U0001f464 {r['name']} | کلاس {r['student_class']}\n"
        msg += f"   \U0001f4f1 {phone} | \u2b50 {r['points']} pts | \U0001f4dd {r['activities']} فعالیت | {last}\n\n"
        if len(msg) > 3500:
            msg += "...(ادامه دارد)"
            break
    await update.message.reply_text(msg)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Commands:\n/start — Main menu\n/help — This help\n"
        "/quit — Submit exam early\n/results — All scores (teacher only)\n"
        "/endai — End AI session\n/reminders — Turn daily Leitner reminders on/off\n"
        "/about — About Emad English Lab"
    )

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎓 Emad English Lab\n"
        "━━━━━━━━━━━━━━━━\n"
        "Learn English with exams, AI practice, the Millionaire game, and your own Leitner box.\n\n"
        "📢 Channel: https://t.me/emadenglishlab\n"
        "🤖 Bot: https://t.me/emadenglishbot\n"
        "📸 Instagram: https://instagram.com/emadheydarnia\n\n"
        "Made with ❤️ by Emad Heydarnia"
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
        award_ai_points(user_id, session)
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
        await query.edit_message_text("Please choose your group:", reply_markup=main_menu_keyboard())

    # ══════════════════════════════════════════════════════════════════
    # ── MILLIONAIRE — Mini App launcher ───────────────────────────────
    # ══════════════════════════════════════════════════════════════════
    elif data == "cat_millionaire":
        # بستن session های دیگه
        st = get_state(context, user_id)
        if st.get("active"):
            st["active"] = False
            for j in context.job_queue.get_jobs_by_name("timer_" + str(user_id)):
                j.schedule_removal()
            clear_state(context, user_id)
        clear_ai_session(user_id)
        prog = m_get_progress(user_id)
        li = min(prog["level_index"] if prog else 0, len(MILLIONAIRE_LEAGUE) - 1)
        intro = (
            "🎬 *WHO WANTS TO BE A MILLIONAIRE*\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "۱۵ سوال گرامری • از " + m_fmt_money(100) + " تا " + m_fmt_money(1000000) + "\n"
            "🔒 مرحله امن: " + m_fmt_money(1000) + " و " + m_fmt_money(32000) + "\n"
            "✂️ کمک‌ها: 50:50 و تعویض سوال\n\n"
            "📖 فصل فعلی: *" + m_topic_label(li) + "*\n"
            "🏅 فصل‌های فتح‌شده: " + str(prog["completed_levels"] if prog else 0) + "/" + str(len(MILLIONAIRE_LEAGUE)) + "\n"
            "💰 رکورد: " + m_fmt_money(prog["best_money"] if prog else 0) + "\n\n"
            "🎮 دکمه‌ی زیر رو بزن تا بازی گرافیکی باز بشه!"
        )
        rows = []
        if MINIAPP_URL:
            rows.append([InlineKeyboardButton("🎮 شروع بازی گرافیکی", web_app=WebAppInfo(url=MINIAPP_URL))])
        else:
            intro = ("🎬 *Millionaire*\n\n⚠️ آدرس Mini App هنوز تنظیم نشده.\n"
                     "متغیر `MINIAPP_URL` رو توی Railway تنظیم کن.")
        rows.append([InlineKeyboardButton("🔙 Back", callback_data="cat_a2z")])
        await query.edit_message_text(intro, reply_markup=InlineKeyboardMarkup(rows), parse_mode="Markdown")

    elif data == "lang_persian":
        # اگه هنوز ثبت‌نام نکرده، اول ثبت‌نام کنه
        u = get_user(user_id)
        if not (u and u.get("name")):
            context.user_data["awaiting_registration"] = True
            context.user_data["reg_step"] = "name"
            await query.edit_message_text("🎓 اول ثبت‌نامت کنیم!\n\nاسمت رو بنویس:")
            return
        await query.edit_message_text("Persian Students\n\nیه گزینه انتخاب کن:", reply_markup=persian_menu_keyboard())

    elif data == "lang_german":
        # علامت‌گذاری کاربر به‌عنوان آلمانی (برای محدود کردن بازی‌های فارسی‌محور)
        try:
            u = get_user(user_id)
            if u:
                save_user(user_id, u.get("name", ""), u.get("student_class", "German"), language="de", phone=u.get("phone", "") or "")
        except Exception:
            pass
        await query.edit_message_text("German Students\n\nBitte wähle eine Kategorie:", reply_markup=german_menu_keyboard())

    elif data == "cat_vocabulary_de":
        await query.edit_message_text("📚 Vocabulary (AI)\n\nBitte wähle eine Kategorie:", reply_markup=german_vocabulary_keyboard())

    elif data == "cat_grammar_de":
        await query.edit_message_text("📖 Grammar (AI)\n\nWähle ein Thema:", reply_markup=german_grammar_keyboard())

    elif data == "ai_writing_de":
        await query.edit_message_text("✍️ Writing (AI)\n\nChoose a task:", reply_markup=german_writing_keyboard())

    elif data == "cat_ielts_de":
        await query.edit_message_text("🌍 Topic Related Vocabulary\n\nWähle ein Kapitel:", reply_markup=german_ielts_menu_keyboard())

    elif data == "cat_vocab_ielts_de":
        await query.edit_message_text("📖 Vocabulary for IELTS\n\nKommt bald! 🔜", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="cat_vocabulary_de")]]))

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

    elif data == "cat_conv_grammar":
        await query.edit_message_text("💬 Conversation Practice\n\nیه موضوع انتخاب کن:", reply_markup=conv_grammar_keyboard())

    elif data == "cat_speaking":
        await query.edit_message_text(
            "💬 Interactive Speaking\n\n🎭 با AI به انگلیسی صحبت کن!\n📊 آخرش feedback کامل میگیری\n\nیه بخش انتخاب کن:",
            reply_markup=speaking_keyboard()
        )

    elif data == "speaking_grammar":
        try:
            kb = speaking_grammar_keyboard()
            await query.edit_message_text("📖 Grammar Speaking\n\nیه موضوع گرامری انتخاب کن:", reply_markup=kb)
        except Exception as e:
            await query.edit_message_text(f"خطا: {str(e)[:100]}", reply_markup=main_menu_keyboard())

    elif data == "speaking_vocab":
        await query.edit_message_text("📚 Vocabulary Speaking\n\nیه فصل انتخاب کن:", reply_markup=speaking_vocab_keyboard())

    elif data == "speaking_legends":
        await query.edit_message_text(
            "🌟 Legends\n\nبا یه شخصیت تاریخی یا مشهور به انگلیسی صحبت کن!\nAI شخصیت، جهان‌بینی و حتی شوخی‌هاشون رو شبیه‌سازی می‌کنه 🎭",
            reply_markup=speaking_legends_keyboard()
        )

    elif data.startswith("speaking_legend_"):
        legend_key = data[16:]
        legends_data = {
            "rumi": {
                "name": "Rumi (Molana) 🌹",
                "topic": "Sufism, love, poetry, and the search for the divine",
                "personality": """You are Jalal ad-Din Rumi (Molana), the 13th century Sufi poet and mystic.
You speak with deep wisdom, warmth, and occasional metaphorical language. You often use beautiful imagery from nature, love, and the soul.
You believe love is the greatest force in the universe. You're joyful, not somber — full of life and wonder.
Your worldview: The soul yearns to return to its origin (God/Truth). Music and dance (Sama) are paths to the divine. Love transcends all boundaries.
Famous quotes you might reference: "Out beyond ideas of wrongdoing and rightdoing, there is a field. I'll meet you there." / "The wound is the place where the Light enters you."
You speak in present tense about your philosophy as if it's timeless.
Occasionally share a brief poetic metaphor or image. Be warm, philosophical, and sometimes gently humorous."""
            },
            "hafiz": {
                "name": "Hafiz 🌸",
                "topic": "Poetry, wine (as metaphor), love, and mystical insight",
                "personality": """You are Hafiz (Khwaja Shams-ud-Din Muhammad Hafiz-e Shirazi), the 14th century Persian lyric poet.
You are witty, playful, and deeply spiritual — but you hide profound truths in playful language.
You love paradox: you talk about wine and the tavern, but mean divine love and the heart.
Your worldview: God is the beloved. Life is a beautiful mystery. The hypocrite who pretends piety is worse than the honest lover.
You're a bit mischievous — you enjoy teasing and wit. You quote your own ghazals naturally.
Be poetic, occasionally ironic, and always profound beneath the playfulness."""
            },
            "khayyam": {
                "name": "Omar Khayyam 🍷",
                "topic": "Philosophy, the brevity of life, mathematics, and carpe diem",
                "personality": """You are Omar Khayyam, the 11th/12th century Persian mathematician, astronomer, and poet.
You are philosophical, slightly melancholic, but with a deep acceptance of life's mystery.
Your worldview: Life is short. Nobody knows what happens after death. Enjoy the present moment — a cup of wine (joy), a friend, a beautiful day. Don't waste life on empty promises of paradise or fear of hell.
You are also scientifically minded — you solved cubic equations, reformed the Persian calendar.
Famous Rubaiyat themes: the potter and the clay, the moving finger, the caravan of life.
Be thoughtful, a touch wistful, occasionally darkly humorous, and always honest."""
            },
            "dostoevsky": {
                "name": "Fyodor Dostoevsky 📚",
                "topic": "Literature, suffering, redemption, human psychology, and his novels",
                "personality": """You are Fyodor Dostoevsky, the great Russian novelist (1821-1881).
You are intense, passionate, deeply empathetic about human suffering, and obsessed with the question of God and free will.
Your worldview: Suffering is transformative. The poor and downtrodden deserve dignity. Without God, everything is permitted. Love and compassion can redeem even the most fallen soul.
You may reference your novels: Crime and Punishment, The Brothers Karamazov, The Idiot, Notes from Underground.
You experienced imprisonment in Siberia — it deepened your humanity.
Be intense but warm, psychologically probing, occasionally dramatic, and deeply human."""
            },
            "ronaldo": {
                "name": "Cristiano Ronaldo ⚽",
                "topic": "Football, discipline, success, and the pursuit of greatness",
                "personality": """You are Cristiano Ronaldo (CR7), one of the greatest footballers of all time.
You are confident, driven, and competitive — but also warm and appreciative of your fans.
Your worldview: Hard work beats talent. You were NOT born great — you became great through sacrifice, discipline, and obsession with improvement. 5am training sessions. Perfect diet. Mental strength.
You love your family deeply. You're proud of your humble origins in Madeira. 
Talk about: your records (goals, trophies), rivalry with Messi (respectfully competitive), training secrets, what drives you.
Be charismatic, slightly boastful but self-aware, motivational, and occasionally funny about football rivalries."""
            },
            "messi": {
                "name": "Lionel Messi 🐐",
                "topic": "Football, natural talent, teamwork, and quiet greatness",
                "personality": """You are Lionel Messi, widely considered the greatest footballer of all time.
You are humble, quiet, and let your football do the talking — but in conversation you open up warmly.
Your worldview: Football is joy. Team is everything. You don't chase records — they come naturally when you love the game. Family keeps you grounded.
Talk about: the World Cup 2022 being your greatest moment, Barcelona years, the rivalry with Ronaldo (respectful), what makes football beautiful.
Be humble, thoughtful, occasionally surprised by your own achievements, and warm when discussing family and Argentina."""
            },
            "adele": {
                "name": "Adele 🎵",
                "topic": "Music, emotions, songwriting, and being authentic",
                "personality": """You are Adele, the British singer-songwriter known for emotional, powerful vocals.
You are warm, funny, self-deprecating, and deeply honest about your emotions.
Your worldview: Music should make people feel less alone. Songs come from real pain and real love. You don't follow trends — you follow your heart.
Talk about: your albums (19, 21, 25, 30), the stories behind songs like Someone Like You, Hello, Easy On Me. Your love of tea. Being a mum. Being body-positive.
Be funny (you have great British humor!), emotionally open, occasionally a bit dramatic, and very real."""
            },
            "nolan": {
                "name": "Christopher Nolan 🎬",
                "topic": "Cinema, storytelling, time, and the nature of reality",
                "personality": """You are Christopher Nolan, director of Inception, Interstellar, The Dark Knight, Oppenheimer.
You are cerebral, passionate about practical filmmaking, and fascinated by time and subjective reality.
Your worldview: Cinema is the most powerful art form. Practical effects > CGI. Stories should challenge audiences. Time is not linear — our perception of it shapes our reality.
Talk about: the ideas behind your films, shooting on IMAX, why you don't use phones on set, the concept of temporal manipulation in storytelling.
Be thoughtful, slightly intense, genuinely excited about ideas, and passionate about the craft of filmmaking."""
            },
            "einstein": {
                "name": "Albert Einstein 💡",
                "topic": "Science, curiosity, imagination, and the universe",
                "personality": """You are Albert Einstein, theoretical physicist (1879-1955).
You are playful, curious, and deeply philosophical about science and humanity.
Your worldview: Imagination is more important than knowledge. God does not play dice (though quantum mechanics challenged this!). Science without religion is lame, religion without science is blind. The most beautiful thing we can experience is the mysterious.
Talk about: relativity, the photoelectric effect, your thought experiments, your violin playing, your pacifism, fleeing Nazi Germany.
Be warm, playful, occasionally self-deprecating, and always enthusiastic about ideas. Use thought experiments naturally."""
            },
            "freddie": {
                "name": "Freddie Mercury 🎤",
                "topic": "Music, performance, creativity, and living life fully",
                "personality": """You are Freddie Mercury, lead vocalist of Queen (1946-1991).
You are flamboyant, theatrical, deeply musical, and warmly generous with your affection for fans.
Your worldview: Live life fully, love deeply, perform as if it's your last show. Music transcends all barriers. The show must go on.
Talk about: writing Bohemian Rhapsody, Live Aid 1985, your love of opera, Zanzibar and your heritage, what it means to truly perform.
Be dramatic, warm, witty, occasionally camp and theatrical, and deeply passionate about music and life."""
            },
        }
        
        legend = legends_data.get(legend_key)
        if not legend:
            await query.edit_message_text("شخصیت پیدا نشد!", reply_markup=main_menu_keyboard())
            return
        
        u = get_user(user_id)
        student_name = u["name"] if u and u.get("name") else "friend"
        
        prompt = f"""You are {legend['name']}, in conversation with a student learning English named {student_name}.

{legend['personality']}

CONVERSATION RULES:
- Stay completely in character throughout — think, speak, and react as {legend['name']} would
- The student is learning English — speak naturally but not too complex
- Keep YOUR turns to 2-4 sentences so the student has room to respond
- Ask questions that fit your character naturally
- If the student makes grammar errors, note them mentally but NEVER break character to correct mid-conversation
- React authentically to what they say — be surprised, amused, thoughtful, as the real person would be
- After 8-10 natural exchanges, wrap up in character, then step OUT of character briefly to give feedback in Persian:

📊 بازخورد مکالمه با {legend['name']}
✅ نقاط قوت در مکالمه:
📝 اشکالات گرامری: (هر اشتباه + تصحیح)
💡 عبارات بهتر که می‌تونست بگه:
🎯 سطح تخمینی: (A2/B1/B2/C1)
⭐ امتیاز: X از ۱۰

Now begin: introduce yourself as {legend['name']} and start the conversation naturally."""

        topic_label = "🌟 " + legend["name"]
        topic = {"label": topic_label, "prompt": prompt}
        
        clear_ai_session(user_id)
        session = get_ai_session(user_id)
        session["topic"] = "legend_" + legend_key
        session["active"] = True
        session["system_prompt"] = prompt
        log_activity(user_id, "", "", "ai_start", "legend_" + legend_key)
        
        session_msg = f"🌟 {legend['name']}\n\nMic is on! 🎙️\nType /endai to end.\n\n⏳ Please wait..."
        await query.edit_message_text(session_msg)
        
        try:
            loop = asyncio.get_event_loop()
            def call_g():
                return call_gemini_api([], prompt)
            resp = await loop.run_in_executor(None, call_g)
            await context.bot.send_message(chat_id=user_id, text=resp)
        except Exception as e:
            await context.bot.send_message(chat_id=user_id, text="⚠️ Connection error. Please try again.")
        return

    elif data.startswith("speaking_vocab_"):
        # Vocabulary speaking — همون IELTS vocab ولی با مکالمه
        ielts_key = data[15:]
        base_topic = IELTS_AI_TOPICS.get(ielts_key)
        if not base_topic:
            await query.edit_message_text("Topic not found.", reply_markup=main_menu_keyboard())
            return
        
        u = get_user(user_id)
        student_name = u["name"] if u and u.get("name") else "friend"
        ch_name = base_topic["label"].replace("📚 ", "")
        
        prompt = f"""You are a friendly, engaging English conversation partner.
Topic: Vocabulary from Chapter — {ch_name}

Your role: Choose a natural scenario that fits this vocabulary topic and start a real conversation.
For example: if the topic is "Holiday", you might be a travel agent, or a friend planning a trip together.

RULES:
- Have a NATURAL conversation — not a lesson, not a test
- Naturally use words from the {ch_name} vocabulary list in your own sentences
- When the student uses a vocabulary word correctly, react naturally (✨ or a positive reaction)  
- Keep YOUR turns short (2-3 sentences) — let the student talk more
- If they can't find a word, give a subtle hint without breaking the conversation flow
- Adapt to their level
- After 8-10 exchanges, end naturally then give feedback in Persian:

📊 بازخورد — {ch_name} Vocabulary
✅ لغاتی که درست استفاده کرد:
📝 اشکالات: (لغت اشتباه + تصحیح)
💡 لغاتی که می‌تونست بیشتر استفاده کنه:
🎯 سطح تخمینی: (A2/B1/B2/C1)
⭐ امتیاز: X از ۱۰

Student's name: {student_name}. Start the scenario now."""

        clear_ai_session(user_id)
        session = get_ai_session(user_id)
        session["topic"] = "speaking_vocab_" + ielts_key
        session["active"] = True
        session["system_prompt"] = prompt
        log_activity(user_id, "", "", "ai_start", "speaking_vocab_" + ielts_key)
        
        session_msg = f"📚 Vocabulary Speaking: {ch_name}\n\nMic is on! 🎙️\nType /endai to end.\n\n⏳ Please wait..."
        await query.edit_message_text(session_msg)
        
        try:
            loop = asyncio.get_event_loop()
            def call_g():
                return call_gemini_api([], prompt)
            resp = await loop.run_in_executor(None, call_g)
            await context.bot.send_message(chat_id=user_id, text=resp)
        except Exception as e:
            await context.bot.send_message(chat_id=user_id, text="⚠️ Connection error. Please try again.")
        return

    elif data.startswith("speaking_"):
        # جلوگیری از conflict با legend و vocab handlers
        if data.startswith("speaking_legend_") or data.startswith("speaking_vocab_"):
            # اینا قبلاً handle شدن — اگه اینجا رسیدیم یعنی بالاتر پیدا نشدن
            await query.edit_message_text("در حال بارگذاری...", reply_markup=main_menu_keyboard())
            return

        # grammar topic با speaking prompt
        grammar_key = data[9:]
        base_topic = AI_TOPICS.get(grammar_key)
        if not base_topic:
            await query.edit_message_text("Topic not found.", reply_markup=main_menu_keyboard())
            return

        # ساختن speaking prompt براساس grammar topic
        grammar_label = base_topic["label"]
        speaking_prompt = f"""You are playing a role in a natural conversation scenario.
Grammar focus: {grammar_label}

Your role: Choose a fun, realistic character (e.g., a barista, a travel agent, a friend, a colleague, a doctor) that fits naturally with using {grammar_label} structures.

Introduce yourself and the scene briefly (1-2 sentences), then start the conversation naturally.

CONVERSATION RULES:
- Speak naturally as your character — NOT like a teacher
- Keep YOUR turns SHORT (1-3 sentences) so the student talks more
- Ask questions that naturally require {grammar_label} to answer correctly
- Adapt to the student's level — if they struggle, simplify; if they're good, go deeper
- If they make a grammar error, note it mentally but DON'T stop the conversation — correct at the end
- Build on what they say — reference their previous responses
- After 8-10 natural exchanges, wrap up the conversation naturally, then give feedback in Persian:

📊 بازخورد مکالمه — {grammar_label}
✅ نقاط قوت:
📝 اشکالات گرامری: (هر اشتباه + تصحیح)
💡 عبارات بهتر:
🎯 سطح تخمینی:
⭐ امتیاز: X از ۱۰

Start the scene now — introduce your character and setting briefly, then begin."""

        short_label = grammar_label.split(' ', 1)[-1] if ' ' in grammar_label else grammar_label
        topic = {"label": "💬 Speaking: " + short_label, "prompt": speaking_prompt}

        u = get_user(user_id)
        student_name = u["name"] if u and u.get("name") else ""
        if student_name:
            topic["prompt"] += f"\n\n[Student's name is {student_name}. Use their name naturally in conversation.]"

        clear_ai_session(user_id)
        session = get_ai_session(user_id)
        session["topic"] = "conv_" + grammar_key
        session["active"] = True
        session["system_prompt"] = topic["prompt"]
        log_activity(user_id, "", "", "ai_start", "speaking_" + grammar_key)

        session_msg = "💬 " + topic["label"] + "\n\nMic is on! 🎙️\nType /endai to end.\n\n⏳ Please wait..."
        await query.edit_message_text(session_msg)

        try:
            loop = asyncio.get_event_loop()
            start_p = topic["prompt"] + SCORING_RULE
            def call_g():
                return call_gemini_api([], start_p)
            resp = await loop.run_in_executor(None, call_g)
            await context.bot.send_message(chat_id=user_id, text=resp)
        except Exception as e:
            await context.bot.send_message(chat_id=user_id, text="⚠️ Connection error. Please try again.")
        return

    elif data == "cat_vocabulary":
        await query.edit_message_text("📚 Vocabulary (AI)\n\nیه دسته انتخاب کن:", reply_markup=vocabulary_keyboard())

    elif data == "cat_vocab_ielts":
        await query.edit_message_text("📖 Vocabulary for IELTS\n\nبه زودی محتوا اضافه می‌شه. 🔜", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="cat_vocabulary")]]))

    elif data == "cat_ielts":
        await query.edit_message_text("🌍 Topic Related Vocabulary\n\nیه فصل انتخاب کن:", reply_markup=ielts_menu_keyboard())



    elif data == "cat_ai":
        await query.edit_message_text("🤖 AI Assistant\n\nChoose a section:", reply_markup=ai_keyboard())

    elif data == "ai_grammar":
        await query.edit_message_text("📖 Grammar Practice\n\nChoose a topic:", reply_markup=ai_grammar_keyboard())

    elif data == "ai_writing":
        await query.edit_message_text("✍️ Writing\n\nChoose a task:", reply_markup=ai_writing_keyboard())

    elif data.startswith("ai_topic_"):
        topic_key = data[9:]

        # بررسی German grammar topics (de_grammar_TOPICKEY)
        if topic_key.startswith("de_grammar_"):
            persian_key = topic_key[11:]  # حذف "de_grammar_"
            base_topic = AI_TOPICS.get(persian_key)
            if base_topic:
                de_prompt = """Du bist ein freundlicher Englischlehrer bei Emad Eng Lab für deutschsprachige Schüler.
WICHTIG: Sprich NUR auf Deutsch. Niemals Persisch.
Gib deutsche Sätze, die der Schüler ins Englische übersetzen soll.
Nach jeder Antwort: kurzes Feedback auf Deutsch (richtige Übersetzung + Grammatikpunkt).
20 Sätze pro Session, dann kurzer Bericht.
Starte mit: Wie heißt du?

Grammatikthema: """ + base_topic["label"]
                topic = {"label": base_topic["label"], "prompt": de_prompt}
                is_german_override = True
            else:
                topic = None
        # بررسی German topics
        elif topic_key.startswith("de_"):
            topic = GERMAN_AI_TOPICS.get(topic_key)
        elif topic_key.startswith("dei_"):
            # IELTS برای آلمانی — همون prompt ولی زبان آلمانی
            ielts_key = topic_key[4:]  # حذف "dei_"
            base_topic = IELTS_AI_TOPICS.get(ielts_key)
            if base_topic:
                de_prompt = base_topic["prompt"]
                de_prompt = de_prompt.replace("زبان توضیحات: فارسی", "Sprache der Erklärungen: DEUTSCH")
                de_prompt = de_prompt.replace("زبان جملات تمرینی: فارسی (برای ترجمه به انگلیسی)", "Übungssätze: Deutsche Sätze zum Übersetzen ins Englische")
                de_prompt = de_prompt.replace("زبان مثال‌ها و word forms: انگلیسی", "Beispiele und Wortformen: Englisch")
                de_prompt = de_prompt.replace("مستقیم شروع کن — اسم دانش‌آموز از قبل مشخصه، دوباره نپرس.", "Starte direkt — der Name des Schülers ist bereits bekannt.")
                de_prompt = de_prompt.replace("جای خالی را با لغت مناسب انگلیسی پر کنید.", "Übersetze den deutschen Satz ins Englische.")
                de_prompt = de_prompt.replace("تمام توضیحات، بازخوردها و گزارش‌ها باید به فارسی باشن", "Alle Erklärungen und Berichte auf Deutsch")
                # دستور قوی در ابتدا اضافه کن
                de_prompt = """CRITICAL INSTRUCTION: You are teaching German-speaking students. 
ALL sentences you give for translation must be in GERMAN. 
NEVER give Persian/Farsi sentences. 
ALL explanations, feedback, and reports must be in GERMAN.
Student translates German sentences into English.

""" + de_prompt
                topic = {
                    "label": base_topic["label"],
                    "prompt": de_prompt
                }
            else:
                topic = None
        else:
            topic = AI_TOPICS.get(topic_key)

        if not topic:
            await query.edit_message_text("Topic not found.", reply_markup=main_menu_keyboard())
            return

        clear_ai_session(user_id)
        session = get_ai_session(user_id)
        session["topic"] = topic_key
        session["active"] = True
        session["system_prompt"] = topic["prompt"]
        log_activity(user_id, "", "", "ai_start", topic_key)

        # گرفتن اسم کاربر تا AI دوباره نپرسه
        u = get_user(user_id)
        student_name = u["name"] if u and u.get("name") else ""
        name_inject = ""
        if student_name:
            name_inject = f"\n\n[IMPORTANT: The student's name is {student_name}. Do NOT ask for their name. Address them as {student_name} and start the activity directly.]"

        is_german = topic_key.startswith("de_") or topic_key.startswith("dei_") or locals().get("is_german_override", False)
        if is_german:
            session_msg = "🤖 " + topic["label"] + "\n\nKI-Sitzung gestartet!\nTippe /endai zum Beenden.\n\n⏳ Bitte warten..."
            start_prompt = topic["prompt"] + name_inject + SCORING_RULE + "\n\nBitte starte die Sitzung jetzt auf Deutsch. Gib KEINE persischen Saetze."
        else:
            session_msg = "🤖 " + topic["label"] + "\n\nAI session started!\nType /endai to end the session.\n\n⏳ Please wait..."
            start_prompt = topic["prompt"] + name_inject + SCORING_RULE + "\n\nPlease start the session now."
        await query.edit_message_text(session_msg)

        try:
            loop = asyncio.get_event_loop()
            def call_gemini():
                return call_gemini_api([], start_prompt)
            
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
                        # تشخیص زبان بر اساس topic
                        if session.get("topic", "").startswith("de_") or session.get("topic", "").startswith("dei_"):
                            wait_msg = "⏳ Server ist beschäftigt, bitte " + str(wait) + " Sekunden warten... (Versuch " + str(attempt+2) + "/4)"
                        else:
                            wait_msg = "⏳ سرور شلوغه، " + str(wait) + " ثانیه صبر کن... (تلاش " + str(attempt+2) + "/4)"
                        await context.bot.send_message(chat_id=user_id, text=wait_msg)
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

    # ثبت‌نام کاربر جدید
    if context.user_data.get("awaiting_registration"):
        # کلیدهای پایین صفحه نباید به عنوان جواب ثبت‌نام ثبت بشن
        reserved_buttons = ["📊 My Score", "📈 My Progress", "🏆 Leaderboard", "🏠 Main Menu"]
        if text in reserved_buttons:
            await update.message.reply_text("لطفاً اول ثبت‌نامت رو کامل کن 🙏")
            return
        step = context.user_data.get("reg_step", "name")
        if step == "name":
            context.user_data["reg_name"] = text
            context.user_data["reg_step"] = "class"
            await update.message.reply_text(f"سلام {text}!\n\nشماره کلاست چنده؟")
            return
        elif step == "class":
            context.user_data["reg_class"] = text
            context.user_data["reg_step"] = "phone"
            await update.message.reply_text(
                "\U0001f4f1 شماره تلفنت رو بفرست (اختیاری)\n\nاگه نمی\u200cخوای، بنویس: رد"
            )
            return
        elif step == "phone":
            name = context.user_data.get("reg_name", "")
            student_class = context.user_data.get("reg_class", "")
            phone = "" if text.strip() in ("رد", "skip", "Skip", "-") else text.strip()
            save_user(user_id, name, student_class, phone=phone)
            context.user_data["awaiting_registration"] = False
            context.user_data.pop("reg_step", None)
            context.user_data.pop("reg_name", None)
            context.user_data.pop("reg_class", None)
            await update.message.reply_text(
                f"\u2705 ثبت\u200cنام کامل شد!\n\nخوش اومدی {name} از کلاس {student_class}! \U0001f389",
                reply_markup=main_reply_keyboard()
            )
            await update.message.reply_text(
                "Persian Students\n\nیه گزینه انتخاب کن 👇",
                reply_markup=persian_menu_keyboard()
            )
            return

    # Note: AI session is checked AFTER all exam checks below

    # شناسایی دکمه‌های reply keyboard پایین صفحه
    # کلید Main Menu — همه session ها رو می‌بنده و برمیگرده
    if text == "📊 My Score":
        await myscore_cmd(update, context)
        return

    if text == "📈 My Progress":
        await myprogress_cmd(update, context)
        return

    if text == "🏆 Leaderboard":
        await leaderboard_cmd(update, context)
        return

    if text == "🏠 Main Menu":
        # اگه exam فعاله
        if state.get("active"):
            state["active"] = False
            for j in context.job_queue.get_jobs_by_name("timer_" + str(user_id)):
                j.schedule_removal()
            clear_state(context, user_id)
        # اگه AI session فعاله
        clear_ai_session(user_id)
        await update.message.reply_text(
            "Please select your group / گروه خود را انتخاب کنید 👇",
            reply_markup=main_menu_keyboard()
        )
        return

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

            is_end = any(word in resp_text.lower() for word in ["band score", "overall:", "level:", "سطح:", "نمره:", "weekly report", "گزارش هفتگی", "بازخورد مکالمه", "امتیاز کلی", "سطح تخمینی"])
            # وجود خط SCORE: X/10 هم نشونه‌ی پایان session ـه
            if m_parse_ai_score(resp_text) is not None:
                is_end = True

            # خط نمره‌ی پنهان رو از متنی که به دانش‌آموز نشون داده می‌شه حذف کن
            import re as _re_score
            display_text = _re_score.sub(r"\n?\s*SCORE:\s*\d{1,2}\s*/\s*10\s*", "", resp_text).strip()

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

            if len(display_text) > 4000:
                chunks = [display_text[i:i+4000] for i in range(0, len(display_text), 4000)]
                for i, chunk in enumerate(chunks):
                    if i == len(chunks) - 1:
                        await update.message.reply_text(chunk)
                    else:
                        await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(display_text)

            if is_end:
                log_activity(user_id, ai_state.get("student_name","?"), ai_state.get("student_class","?"), "ai_end", session.get("topic",""))
                # ذخیره session AI در دیتابیس
                ai_state = get_state(context, user_id)
                save_activity(
                    telegram_id=user_id,
                    name=ai_state.get("student_name", str(user_id)),
                    student_class=ai_state.get("student_class", "?"),
                    activity_type="ai_session",
                    topic=session.get("topic", "unknown"),
                    level=next((w for w in ["A1","A2","B1","B2","C1"] if w in resp_text), None),
                    summary=resp_text[:200]
                )
                # امتیازدهی AI session بر اساس نمره‌ی واقعی AI (یک‌بار)
                award_ai_points(user_id, session, resp_text)
                clear_ai_session(user_id)
                await update.message.reply_text(
                    "🏠 منو اصلی:",
                    reply_markup=main_reply_keyboard()
                )

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

async def myscore_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمرات خود دانش‌آموز"""
    user_id = update.effective_user.id
    rows, summary = get_my_stats(user_id)
    if not rows:
        await update.message.reply_text("هنوز هیچ فعالیتی ثبت نشده. برو یه exam بده! 💪")
        return

    name = rows[0].get("name", "") if rows else ""
    exams = [r for r in rows if r["activity_type"] == "exam" and r["score"] is not None]
    ai_sess = [r for r in rows if r["activity_type"] == "ai_session"]

    msg = "📊 نتایج من\n" + "━" * 28 + "\n"
    if summary and summary["avg"]:
        msg += "📈 میانگین کلی: " + str(summary["avg"]) + "%\n\n"

    if exams:
        msg += "📝 Exam ها:\n"
        for r in exams[:10]:
            pct = round(r["score"] / r["total"] * 100) if r["total"] else 0
            emoji = "✅" if pct >= 70 else "⚠️" if pct >= 50 else "❌"
            days_ago = (datetime.now() - r["created_at"]).days
            date_str = "امروز" if days_ago == 0 else "دیروز" if days_ago == 1 else str(days_ago) + " روز پیش"
            msg += "  " + emoji + " " + str(r["topic"])[:30] + " — " + str(r["score"]) + "/" + str(r["total"]) + " (" + str(pct) + "%) | " + date_str + "\n"

    if ai_sess:
        msg += "\n🤖 AI Sessions:\n"
        for r in ai_sess[:5]:
            days_ago = (datetime.now() - r["created_at"]).days
            date_str = "امروز" if days_ago == 0 else "دیروز" if days_ago == 1 else str(days_ago) + " روز پیش"
            level = " | " + r["level"] if r["level"] else ""
            msg += "  🔹 " + str(r["topic"])[:30] + level + " | " + date_str + "\n"

    await update.message.reply_text(msg)

async def myprogress_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """پیشرفت دانش‌آموز"""
    user_id = update.effective_user.id
    rows, summary = get_my_stats(user_id)
    if not rows:
        await update.message.reply_text("هنوز فعالیتی ثبت نشده! 🎯\nبرو یه exam بده یا AI رو امتحان کن.")
        return

    exams = [r for r in rows if r["activity_type"] == "exam" and r["score"] is not None]
    ai_sess = [r for r in rows if r["activity_type"] == "ai_session"]
    level_tests = [r for r in rows if r["level"]]

    msg = "📈 پیشرفت من\n" + "━" * 28 + "\n"

    # سطح فعلی
    if level_tests:
        msg += "🎓 سطح فعلی: " + str(level_tests[0]["level"]) + "\n\n"

    # آمار exam ها
    if exams:
        scores = [r["score"] / r["total"] * 100 for r in exams if r["total"]]
        msg += "📝 Exams (" + str(len(exams)) + " عدد):\n"
        for r in exams[:5]:
            pct = round(r["score"] / r["total"] * 100) if r["total"] else 0
            emoji = "✅" if pct >= 70 else "⚠️" if pct >= 50 else "❌"
            days_ago = (datetime.now() - r["created_at"]).days
            date_str = "امروز" if days_ago == 0 else "دیروز" if days_ago == 1 else str(days_ago) + " روز پیش"
            msg += "  " + emoji + " " + str(r["topic"])[:25] + " — " + str(pct) + "% | " + date_str + "\n"

        if scores:
            msg += "\n🎯 بهترین نمره: " + str(round(max(scores))) + "%\n"
            msg += "📊 میانگین کلی: " + str(round(sum(scores)/len(scores))) + "%\n"
            if len(scores) >= 2:
                trend = scores[0] - scores[-1]
                if trend > 5:
                    msg += "📈 روند: در حال پیشرفت! 🌟\n"
                elif trend < -5:
                    msg += "📉 روند: نیاز به تمرین بیشتر 💪\n"
                else:
                    msg += "➡️ روند: ثابت\n"

            # ضعیف‌ترین topic
            topic_scores = {}
            for r in exams:
                if r["total"]:
                    pct = r["score"] / r["total"] * 100
                    t = str(r["topic"])[:25]
                    if t not in topic_scores:
                        topic_scores[t] = []
                    topic_scores[t].append(pct)
            if topic_scores:
                worst = min(topic_scores, key=lambda t: sum(topic_scores[t])/len(topic_scores[t]))
                msg += "💪 ضعیف‌ترین topic: " + worst + "\n"

    # AI sessions
    if ai_sess:
        msg += "\n🤖 AI Sessions: " + str(len(ai_sess)) + " جلسه\n"

    await update.message.reply_text(msg)

async def report_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """گزارش ریز فعالیت‌ها — فقط معلم"""
    if update.effective_user.id != TEACHER_ID:
        await update.message.reply_text("🚫 Teacher only.")
        return
    arg = " ".join(context.args) if context.args else ""
    rows = get_full_report()
    if not rows:
        await update.message.reply_text("هیچ فعالیتی ثبت نشده.")
        return
    msg = "📋 گزارش ریز فعالیت‌ها\n" + "━" * 28 + "\n"
    for r in rows:
        time = r["created_at"].strftime("%m/%d %H:%M")
        detail = " | " + str(r["detail"]) if r["detail"] else ""
        msg += time + " — " + str(r["name"]) + " | " + str(r["action"]) + detail + "\n"
        if len(msg) > 3500:
            msg += "...\n(بقیه نتایج ادامه دارد)"
            break
    await update.message.reply_text(msg)

async def profile_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TEACHER_ID:
        await update.message.reply_text("🚫 Teacher only.")
        return
    name = " ".join(context.args) if context.args else ""
    if not name:
        await update.message.reply_text("استفاده: /profile [اسم دانش‌آموز]")
        return
    rows = get_student_profile(name)
    if not rows:
        await update.message.reply_text(f"❌ دانش‌آموزی با اسم '{name}' پیدا نشد.")
        return
    msg = "📋 پرونده: " + rows[0]["name"] + " — کلاس " + str(rows[0]["student_class"]) + "\n"
    msg += "━" * 30 + "\n"
    for r in rows:
        date = r["created_at"].strftime("%Y/%m/%d")
        if r["score"] is not None:
            msg += "📝 " + str(r["topic"]) + " | نمره: " + str(r["score"]) + "/" + str(r["total"]) + " | " + date + "\n"
        elif r["level"]:
            msg += "🤖 " + str(r["topic"]) + " | سطح: " + str(r["level"]) + " | " + date + "\n"
        else:
            msg += "✅ " + str(r["topic"]) + " | " + date + "\n"
    await update.message.reply_text(msg)

async def stats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TEACHER_ID:
        await update.message.reply_text("🚫 Teacher only.")
        return
    
    arg = context.args[0] if context.args else "today"
    
    if arg == "all":
        # آمار همه دانش‌آموزان
        rows = get_all_stats()
        if not rows:
            await update.message.reply_text("هنوز اطلاعاتی ثبت نشده.")
            return
        msg = "📊 آمار کلی همه دانش‌آموزان\n" + "━" * 30 + "\n"
        for r in rows:
            avg = str(r['avg_score']) + "%" if r['avg_score'] else "—"
            last = r['last_active'].strftime("%m/%d") if r['last_active'] else "—"
            msg += "👤 " + str(r["name"]) + " | " + str(r["activities"]) + " فعالیت | میانگین: " + avg + " | آخرین: " + last + "\n"
        await update.message.reply_text(msg)

    elif arg == "week":
        # آمار هفتگی
        rows = get_weekly_stats()
        if not rows:
            await update.message.reply_text("اطلاعاتی برای هفته گذشته نیست.")
            return
        msg = "📅 آمار ۷ روز گذشته\n" + "━" * 30 + "\n"
        for r in rows:
            msg += str(r['day'].strftime("%Y/%m/%d")) + " — " + str(r['users']) + " نفر | " + str(r['activities']) + " فعالیت\n"
        await update.message.reply_text(msg)

    else:
        # آمار امروز (پیش‌فرض)
        today, details = get_today_stats()
        if not today or today['total_activities'] == 0:
            await update.message.reply_text("امروز هنوز هیچ فعالیتی ثبت نشده.")
            return
        msg = "📊 آمار امروز\n" + "━" * 30 + "\n"
        msg += "👥 کاربر فعال: " + str(today['users']) + "\n"
        msg += "📝 Exam: " + str(today['exams'] or 0) + "\n"
        msg += "🤖 AI Session: " + str(today['ai_sessions'] or 0) + "\n"
        if today['avg_score']:
            msg += "📈 میانگین نمره: " + str(today['avg_score']) + "%\n"
        msg += "\n🕐 آخرین فعالیت‌ها:\n"
        for d in details[:10]:
            time = d['created_at'].strftime("%H:%M")
            score_str = " | " + str(d['score']) + "/" + str(d['total']) if d['score'] else ""
            msg += time + " — " + str(d['name']) + " | " + str(d['topic']) + score_str + "\n"
        await update.message.reply_text(msg)

def m_bank_count_by_level():
    """تعداد سوال هر فصل توی بانک"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT level_index, COUNT(*) FROM millionaire_questions GROUP BY level_index")
        d = {li: c for li, c in cur.fetchall()}
        cur.close(); conn.close()
        return d
    except Exception as e:
        print("m_bank_count error: " + str(e))
        return {}

# ══════════════════════════════════════════════════════════════════════════════
# ── TRANSLATION DUEL — Question Bank ──────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

# ساختار هر مسابقه: ۱۲ جمله به این ترتیب سطح‌بندی
TD_STRUCTURE = ["A1", "A2", "A2", "A2", "B1", "B1", "B2", "B2", "C1", "C1", "C2", "C2"]
TD_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]
TD_TARGET_PER_LEVEL = 200

def td_bank_count_by_level():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT level, COUNT(*) FROM td_questions GROUP BY level")
        out = {lv: 0 for lv in TD_LEVELS}
        for lv, c in cur.fetchall():
            out[lv] = c
        cur.close(); conn.close()
        return out
    except Exception as e:
        print("td_bank_count error: " + str(e))
        return {lv: 0 for lv in TD_LEVELS}

def td_pick_questions():
    """۱۲ سوال بر اساس TD_STRUCTURE انتخاب می‌کنه (تصادفی از هر سطح). خروجی: لیست rowها."""
    import random as _r
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        picked = []
        for lv in TD_STRUCTURE:
            cur.execute(
                "SELECT id, level, fa, en_ref FROM td_questions WHERE level=%s ORDER BY RANDOM() LIMIT 1",
                (lv,)
            )
            row = cur.fetchone()
            if row:
                picked.append(dict(row))
        cur.close(); conn.close()
        return picked
    except Exception as e:
        print("td_pick_questions error: " + str(e))
        return []

def td_get_questions_by_ids(ids):
    """سوال‌ها رو با ترتیب دقیق idها برمی‌گردونه (برای نفر دوم که همون سوال‌ها رو بگیره)."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, level, fa, en_ref FROM td_questions WHERE id = ANY(%s)", (ids,))
        by_id = {r["id"]: dict(r) for r in cur.fetchall()}
        cur.close(); conn.close()
        return [by_id[i] for i in ids if i in by_id]
    except Exception as e:
        print("td_get_questions_by_ids error: " + str(e))
        return []

def td_score_answers(questions, answers):
    """
    جواب‌های کاربر رو با AI تصحیح می‌کنه (انعطاف‌پذیر — ترجمه‌ی درستِ متفاوت هم قبول).
    questions: لیست dict با fa و en_ref
    answers: لیست رشته (جواب کاربر، به ترتیب)
    خروجی: (score, details) که details لیست dict هست با درست/غلط هر سوال.
    """
    import json as _json
    # ساخت متن سوال‌ها و جواب‌ها برای AI
    items = []
    for i, q in enumerate(questions):
        ua = answers[i] if i < len(answers) else ""
        items.append({
            "n": i + 1,
            "persian": q.get("fa", ""),
            "reference": q.get("en_ref", ""),
            "student": (ua or "").strip()
        })
    prompt = (
        "You are grading a Persian-to-English translation quiz. For each item, decide if the "
        "student's English translation correctly conveys the meaning of the Persian sentence.\n"
        "BE FLEXIBLE: accept any correct translation even if wording differs from the reference. "
        "Minor typos or small grammar slips that don't change meaning are still CORRECT. "
        "Empty or meaningless or wrong-meaning answers are INCORRECT.\n\n"
        "Return ONLY a JSON array, one object per item, in order:\n"
        '{"n": 1, "correct": true/false}\n\n'
        "Items:\n" + _json.dumps(items, ensure_ascii=False)
    )
    try:
        resp = call_gemini_api([], prompt)
    except Exception as e:
        print("td_score_answers gemini error: " + str(e))
        resp = None
    details = []
    score = 0
    if resp:
        txt = resp.strip()
        if "```" in txt:
            parts = txt.split("```")
            if len(parts) >= 2:
                txt = parts[1].replace("json", "", 1).strip()
        try:
            s = txt.find("["); e = txt.rfind("]")
            arr = _json.loads(txt[s:e+1]) if s >= 0 and e > s else []
        except Exception:
            arr = []
        # نگاشت n → correct
        cmap = {}
        for o in arr:
            try:
                cmap[int(o.get("n"))] = bool(o.get("correct"))
            except Exception:
                pass
        for i in range(len(questions)):
            ok = cmap.get(i + 1, False)
            if ok:
                score += 1
            details.append({"correct": ok})
    else:
        # اگه AI کار نکرد، همه رو غلط حساب نکن — یه fallback ساده‌ی تطبیق متن
        for i, q in enumerate(questions):
            ua = (answers[i] if i < len(answers) else "").strip().lower()
            ref = (q.get("en_ref", "") or "").strip().lower()
            ok = bool(ua) and (ua == ref)
            if ok:
                score += 1
            details.append({"correct": ok})
    return score, details

def td_generate_feedback(questions, creator_answers, opponent_answers, creator_name, opponent_name):
    """فیدبک کوتاه و آموزشی نهایی (بعد از اینکه هر دو بازی کردن)."""
    import json as _json
    items = []
    for i, q in enumerate(questions):
        items.append({
            "persian": q.get("fa", ""),
            "reference": q.get("en_ref", ""),
            creator_name: (creator_answers[i] if i < len(creator_answers) else ""),
            opponent_name: (opponent_answers[i] if i < len(opponent_answers) else ""),
        })
    prompt = (
        "تو یه معلم زبان انگلیسی هستی. این یه مسابقه‌ی ترجمه‌ی فارسی به انگلیسی بین دو نفر بوده.\n"
        "برای هر جمله، ترجمه‌ی مرجع رو بده و اگه اشتباه مهمی توی جواب‌ها بود کوتاه توضیح بده.\n"
        "فیدبک باید کوتاه، آموزشی و دوستانه باشه (فارسی بنویس). برای هر جمله حداکثر ۱-۲ خط.\n"
        "خیلی طولانی ننویس. اول هر جمله شماره بذار.\n\n"
        "جمله‌ها و جواب‌ها:\n" + _json.dumps(items, ensure_ascii=False)
    )
    try:
        resp = call_gemini_api([], prompt)
        return resp.strip() if resp else ""
    except Exception as e:
        print("td_generate_feedback error: " + str(e))
        return ""

def td_create_match(creator_id, creator_name, question_ids, creator_score, creator_answers):
    """
    یه بازی جدید می‌سازه (نفر اول مسابقه رو داده). برمی‌گردونه match_id.
    وضعیت اولیه: waiting (منتظر حریف).
    """
    import json as _json
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO td_matches
            (creator_id, creator_name, question_ids, creator_score, creator_answers, status)
            VALUES (%s,%s,%s,%s,%s,'waiting') RETURNING id
        """, (creator_id, creator_name, _json.dumps(question_ids),
              creator_score, _json.dumps(creator_answers, ensure_ascii=False)))
        mid = cur.fetchone()[0]
        conn.commit(); cur.close(); conn.close()
        return mid
    except Exception as e:
        print("td_create_match error: " + str(e))
        return None

def td_list_open_matches(exclude_id=None):
    """لیست بازی‌های منتظرِ حریف (waiting) که حریفشون پر نشده و مال خود کاربر نیست."""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT id, creator_id, creator_name, created_at
            FROM td_matches WHERE status='waiting'
            ORDER BY created_at DESC LIMIT 50
        """)
        rows = cur.fetchall(); cur.close(); conn.close()
        out = []
        for r in rows:
            if exclude_id and r["creator_id"] == exclude_id:
                continue  # نمی‌تونی به بازی خودت join شی
            out.append(dict(r))
        return out
    except Exception as e:
        print("td_list_open_matches error: " + str(e))
        return []

def td_get_match(match_id):
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM td_matches WHERE id=%s", (match_id,))
        row = cur.fetchone(); cur.close(); conn.close()
        return dict(row) if row else None
    except Exception as e:
        print("td_get_match error: " + str(e))
        return None

def td_claim_match(match_id, opponent_id, opponent_name):
    """
    حریف یه بازی waiting رو می‌گیره (atomic — جلوی join همزمانِ دو نفر رو می‌گیره).
    وضعیت می‌شه 'playing'. برمی‌گردونه True اگه موفق شد.
    """
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE td_matches SET opponent_id=%s, opponent_name=%s, status='playing'
            WHERE id=%s AND status='waiting' AND creator_id != %s
        """, (opponent_id, opponent_name, match_id, opponent_id))
        ok = cur.rowcount > 0
        conn.commit(); cur.close(); conn.close()
        return ok
    except Exception as e:
        print("td_claim_match error: " + str(e))
        return False

def td_finalize_match(match_id, opponent_score, opponent_answers):
    """
    وقتی نفر دوم بازی رو تموم کرد: برنده رو مشخص می‌کنه، امتیاز لیدربورد اصلی رو اعمال می‌کنه،
    آمار داخلی رو آپدیت می‌کنه. خروجی: dict نتیجه‌ی نهایی.
    """
    import json as _json
    m = td_get_match(match_id)
    if not m or m["status"] != "playing":
        return None
    cs = m["creator_score"] or 0
    os_ = opponent_score
    # تعیین برنده
    if cs > os_:
        winner_id = m["creator_id"]
    elif os_ > cs:
        winner_id = m["opponent_id"]
    else:
        winner_id = None  # مساوی

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            UPDATE td_matches SET opponent_score=%s, opponent_answers=%s,
                   status='finished', winner_id=%s, finished_at=NOW()
            WHERE id=%s
        """, (os_, _json.dumps(opponent_answers, ensure_ascii=False), winner_id, match_id))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("td_finalize update error: " + str(e))

    # امتیاز لیدربورد اصلی: برنده +۴۰، بازنده −۱۰، مساوی هیچی
    if winner_id:
        loser_id = m["opponent_id"] if winner_id == m["creator_id"] else m["creator_id"]
        add_points(winner_id, 40, "Translation Duel win")
        add_points(loser_id, -10, "Translation Duel loss")

    # آمار داخلی (برد=۳، مساوی=۱)
    if winner_id is None:
        td_update_stats(m["creator_id"], m["creator_name"], "draw")
        td_update_stats(m["opponent_id"], m["opponent_name"], "draw")
    else:
        loser_id = m["opponent_id"] if winner_id == m["creator_id"] else m["creator_id"]
        win_name = m["creator_name"] if winner_id == m["creator_id"] else m["opponent_name"]
        lose_name = m["opponent_name"] if winner_id == m["creator_id"] else m["creator_name"]
        td_update_stats(winner_id, win_name, "win")
        td_update_stats(loser_id, lose_name, "loss")

    return {
        "creator_name": m["creator_name"], "opponent_name": m["opponent_name"],
        "creator_score": cs, "opponent_score": os_,
        "winner_id": winner_id,
        "is_draw": winner_id is None,
    }

def td_update_stats(uid, name, result):
    """آمار داخلی یه بازیکن رو آپدیت می‌کنه. result: win/draw/loss"""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO td_stats (telegram_id, name, wins, draws, losses, td_points)
            VALUES (%s,%s,0,0,0,0)
            ON CONFLICT (telegram_id) DO UPDATE SET name=EXCLUDED.name
        """, (uid, name))
        if result == "win":
            cur.execute("UPDATE td_stats SET wins=wins+1, td_points=td_points+3 WHERE telegram_id=%s", (uid,))
        elif result == "draw":
            cur.execute("UPDATE td_stats SET draws=draws+1, td_points=td_points+1 WHERE telegram_id=%s", (uid,))
        else:
            cur.execute("UPDATE td_stats SET losses=losses+1 WHERE telegram_id=%s", (uid,))
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("td_update_stats error: " + str(e))

def td_internal_leaderboard():
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT name, wins, draws, losses, td_points
            FROM td_stats ORDER BY td_points DESC, wins DESC LIMIT 50
        """)
        rows = cur.fetchall(); cur.close(); conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print("td_internal_leaderboard error: " + str(e))
        return []

def td_recent_results(limit=30):
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT creator_name, opponent_name, creator_score, opponent_score, winner_id,
                   creator_id, opponent_id, finished_at
            FROM td_matches WHERE status='finished'
            ORDER BY finished_at DESC LIMIT %s
        """, (limit,))
        rows = cur.fetchall(); cur.close(); conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        print("td_recent_results error: " + str(e))
        return []

def td_bootstrap_bank(max_seconds=0):
    """
    یک‌بار بانک ۱۲۰۰ جمله‌ای (۶ سطح × ۲۰۰) رو با AI می‌سازه.
    blocking است و موقع startup صدا زده می‌شه (با متغیر TD_BOOTSTRAP=true).
    """
    import time as _t, json as _json
    start = _t.time()
    counts = td_bank_count_by_level()
    total_now = sum(counts.values())
    if total_now >= TD_TARGET_PER_LEVEL * len(TD_LEVELS):
        logger.info("TD bank already full (%d). Skipping." % total_now)
        return
    logger.info("TD bank bootstrap starting (have %d)..." % total_now)

    try:
        conn = get_db()
    except Exception as e:
        logger.error("td bootstrap: DB connect failed: " + str(e))
        return

    level_desc = {
        "A1": "very basic everyday sentences (greetings, simple present, basic nouns)",
        "A2": "simple past/future, daily routines, simple connectors",
        "B1": "opinions, experiences, common phrasal verbs, moderate complexity",
        "B2": "abstract topics, passive voice, conditionals, richer vocabulary",
        "C1": "complex ideas, nuanced expressions, advanced structures",
        "C2": "idiomatic, sophisticated, near-native complexity",
    }

    for lv in TD_LEVELS:
        cur = conn.cursor()
        cur.execute("SELECT LOWER(fa) FROM td_questions WHERE level=%s", (lv,))
        seen = set(r[0] for r in cur.fetchall())
        cur.execute("SELECT COUNT(*) FROM td_questions WHERE level=%s", (lv,))
        have = cur.fetchone()[0]; cur.close()
        need = TD_TARGET_PER_LEVEL - have
        attempts = 0
        consecutive_fails = 0
        while need > 0 and attempts < 120:
            if max_seconds and (_t.time() - start) > max_seconds:
                logger.warning("td bootstrap: time budget reached.")
                conn.close(); return
            attempts += 1
            ask = min(8, need + 2)
            prompt = (
                "You are creating content for a Persian-to-English translation game.\n"
                "CEFR level: " + lv + " — " + level_desc[lv] + "\n\n"
                "Generate " + str(ask) + " DISTINCT Persian sentences appropriate for this level, "
                "each with a correct, natural English reference translation.\n"
                "Rules:\n"
                "- The Persian sentence is what the student sees and must translate to English.\n"
                "- Keep sentences level-appropriate (A1 easiest, C2 hardest).\n"
                "- Natural, real-life sentences. Avoid duplicates.\n"
                "- Output ONLY a JSON array, no extra text. Each item: "
                '{"fa": "جمله فارسی", "en": "English reference translation"}\n'
            )
            resp = None
            try:
                resp = call_gemini_api([], prompt)
            except Exception as e:
                logger.error("td bootstrap gemini error (continuing): " + str(e))
                resp = None
            if not resp:
                consecutive_fails += 1
                if consecutive_fails >= 8:
                    logger.warning("td bootstrap: too many fails on %s, moving on." % lv)
                    break
                _t.sleep(2)
                continue
            consecutive_fails = 0
            # استخراج JSON
            txt = resp.strip()
            if "```" in txt:
                txt = txt.split("```")[1] if txt.count("```") >= 2 else txt
                txt = txt.replace("json", "", 1).strip() if txt.lower().startswith("json") else txt
            try:
                s = txt.find("["); e = txt.rfind("]")
                items = _json.loads(txt[s:e+1]) if s >= 0 and e > s else []
            except Exception:
                items = []
            cur = conn.cursor()
            added = 0
            for it in items:
                fa = str(it.get("fa", "")).strip()
                en = str(it.get("en", "")).strip()
                if not fa or not en or fa.lower() in seen:
                    continue
                seen.add(fa.lower())
                cur.execute("INSERT INTO td_questions (level, fa, en_ref) VALUES (%s,%s,%s)", (lv, fa, en))
                added += 1
                need -= 1
            conn.commit(); cur.close()
            logger.info("TD %s: +%d (need %d more)" % (lv, added, max(0, need)))
            _t.sleep(1.5)
    conn.close()
    logger.info("TD bank bootstrap finished.")

def m_bootstrap_bank(target_per_level=100, max_seconds=0):
    """
    اگه بانک سوالات خالی/ناقصه، یک بار پُرش می‌کنه. این تابع blocking است و
    موقع startup قبل از run_polling صدا زده می‌شه. هر فصل ۲۵ سوال در هر CEFR.
    max_seconds=0 یعنی بدون محدودیت زمانی.
    """
    import time as _t
    cefr_levels = ["A2", "B1", "B2", "C1"]
    per_cefr = max(1, target_per_level // len(cefr_levels))
    start = _t.time()

    counts = m_bank_count_by_level()
    total_now = sum(counts.values())
    if total_now >= target_per_level * len(MILLIONAIRE_LEAGUE):
        logger.info("Millionaire bank already full (%d). Skipping bootstrap." % total_now)
        return
    logger.info("Millionaire bank bootstrap starting (have %d questions)..." % total_now)

    try:
        conn = get_db()
    except Exception as e:
        logger.error("bootstrap: DB connect failed: " + str(e))
        return

    for level_index in range(len(MILLIONAIRE_LEAGUE)):
        topic_key = MILLIONAIRE_LEAGUE[level_index]
        topic_label = m_topic_label(level_index)
        review = [m_topic_label(i) for i in range(level_index)][-4:]
        review_txt = ("Some questions (~30%) may lightly review: " + ", ".join(review) + ".\n") if review else ""

        cur = conn.cursor()
        cur.execute("SELECT LOWER(question) FROM millionaire_questions WHERE level_index=%s", (level_index,))
        seen = set(r[0] for r in cur.fetchall())
        cur.close()

        for cefr in cefr_levels:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM millionaire_questions WHERE level_index=%s AND cefr=%s",
                        (level_index, cefr))
            have = cur.fetchone()[0]; cur.close()
            need = per_cefr - have
            attempts = 0
            while need > 0 and attempts < 12:
                if max_seconds and (_t.time() - start) > max_seconds:
                    logger.warning("bootstrap: time budget reached, stopping.")
                    conn.close(); return
                attempts += 1
                ask = min(5, need + 2)
                prompt = (
                    "You are writing questions for a 'Who Wants to Be a Millionaire' English GRAMMAR game.\n"
                    "MAIN TOPIC: " + topic_label + "\n" + review_txt +
                    "CEFR difficulty: " + cefr + "\n\n"
                    "Generate " + str(ask) + " DISTINCT multiple-choice grammar questions.\n"
                    "Rules: one short English sentence (fill-in-the-blank or choose correct form); "
                    "exactly 4 options A,B,C,D; exactly ONE correct; vary the correct letter; "
                    "wrong options reflect common learner mistakes; a SHORT Persian (Farsi) explanation (max 2 sentences).\n"
                    'Return ONLY a valid JSON array, no markdown: '
                    '[{"question":"...","options":{"A":"...","B":"...","C":"...","D":"..."},"correct":"A","explanation_fa":"..."}]'
                )
                try:
                    raw = call_gemini_api([], prompt)
                except Exception as e:
                    logger.warning("bootstrap gen error L%d %s: %s" % (level_index, cefr, str(e)))
                    _t.sleep(3); continue
                # parse array
                import json as _j
                txt = raw.strip().replace("```json", "").replace("```", "").strip()
                a = txt.find("["); b = txt.rfind("]")
                if a != -1 and b != -1:
                    txt = txt[a:b+1]
                try:
                    items = _j.loads(txt)
                except Exception:
                    continue
                fresh = []
                for it in items:
                    try:
                        opts = it["options"]
                        cc = str(it["correct"]).strip().upper()[:1]
                        if cc not in ("A", "B", "C", "D"):
                            continue
                        if not all(L in opts for L in ("A", "B", "C", "D")):
                            continue
                        qk = str(it["question"]).strip().lower()
                        if qk in seen:
                            continue
                        seen.add(qk)
                        fresh.append((level_index, topic_key, cefr, str(it["question"]).strip(),
                                      str(opts["A"]).strip(), str(opts["B"]).strip(),
                                      str(opts["C"]).strip(), str(opts["D"]).strip(),
                                      cc, str(it.get("explanation_fa", "")).strip()))
                        if len(fresh) >= need:
                            break
                    except Exception:
                        continue
                if fresh:
                    cur2 = conn.cursor()
                    cur2.executemany(
                        """INSERT INTO millionaire_questions
                           (level_index, topic, cefr, question, option_a, option_b, option_c, option_d, correct, explanation_fa)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        fresh)
                    conn.commit(); cur2.close()
                    need -= len(fresh)
                _t.sleep(1)
        logger.info("bootstrap: level %d (%s) done." % (level_index + 1, topic_label))

    conn.close()
    final = m_bank_count_by_level()
    logger.info("Millionaire bank bootstrap finished. Total: %d" % sum(final.values()))

async def mqstats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """آمار بانک سوالات Millionaire — فقط معلم"""
    if update.effective_user.id != TEACHER_ID:
        await update.message.reply_text("🚫 Teacher only.")
        return
    counts = m_bank_count_by_level()
    if not counts:
        await update.message.reply_text("بانک سوالات خالیه. هنوز چیزی تولید نشده.")
        return
    msg = "🎬 بانک سوالات Millionaire\n" + "━" * 22 + "\n"
    total = 0
    for i in range(len(MILLIONAIRE_LEAGUE)):
        c = counts.get(i, 0); total += c
        bar = "✅" if c >= 100 else ("🟡" if c > 0 else "⬜")
        msg += f"{bar} فصل {i+1}: {c}/100 — {m_topic_label(i)}\n"
    msg += "━" * 22 + f"\nمجموع: {total} سوال"
    await update.message.reply_text(msg)


# ══════════════════════════════════════════════════════════════════════════════
# ── MINI APP — Backend API (aiohttp) ──────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════
# این بخش یه وب‌سرور سبک کنار خود bot اجرا می‌شه و به Mini App (وب‌اپ تلگرام)
# سوال می‌ده، جواب رو اعتبارسنجی می‌کنه و نتیجه/لیدربورد رو برمی‌گردونه.
# امنیت: همه‌ی requestها با initData تلگرام (امضای HMAC با BOT_TOKEN) احراز هویت می‌شن.
# وضعیت بازی روی سرور نگه‌داری می‌شه تا کاربر نتونه با دستکاری فرانت تقلب کنه.

import hashlib
import hmac
from urllib.parse import parse_qsl

# وضعیت بازی‌های فعال Mini App در حافظه — کلید: telegram_id
M_API_GAMES = {}

def m_verify_init_data(init_data, max_age=0):
    """
    اعتبارسنجی initData تلگرام طبق مستندات رسمی.
    خروجی: dict اطلاعات کاربر اگه معتبر بود، وگرنه None.
    max_age=0 یعنی بررسی انقضای زمانی غیرفعاله (جلوگیری از auth_failed بی‌مورد).
    """
    if not init_data or not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return None
    try:
        pairs = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = pairs.pop("hash", None)
        if not received_hash:
            return None
        # رشته‌ی بررسی داده‌ها (الفبایی، با \n)
        data_check = "\n".join(f"{k}={v}" for k, v in sorted(pairs.items()))
        secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
        calc_hash = hmac.new(secret_key, data_check.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(calc_hash, received_hash):
            return None
        # بررسی تازگی (جلوگیری از replay قدیمی)
        auth_date = int(pairs.get("auth_date", "0"))
        if max_age and auth_date:
            import time as _t
            if _t.time() - auth_date > max_age:
                return None
        user_json = pairs.get("user")
        if not user_json:
            return None
        return json.loads(user_json)
    except Exception as e:
        logger.warning("initData verify failed: " + str(e))
        return None

def m_api_user_from_request(data):
    """از بدنه‌ی request، کاربر احراز هویت‌شده رو برمی‌گردونه (یا None)."""
    init_data = data.get("initData", "")
    if not init_data:
        logger.warning("auth: initData is EMPTY (Mini App did not send it)")
        return None
    user = m_verify_init_data(init_data)
    if not user:
        logger.warning("auth: initData present but verification FAILED (len=" + str(len(init_data)) + ")")
        return None
    return user

def m_api_public_question(q):
    """نسخه‌ی امن سوال برای فرانت — بدون حرف درست و توضیح."""
    return {
        "id": q.get("id"),
        "question": q["question"],
        "options": q["options"],
    }

def m_api_ladder():
    out = []
    for i in range(MILLIONAIRE_TOTAL_Q):
        out.append({
            "step": i + 1,
            "money": MILLIONAIRE_LADDER[i],
            "safe": i in MILLIONAIRE_SAFE,
            "top": i == MILLIONAIRE_TOTAL_Q - 1,
        })
    return out

def m_api_progress_payload(telegram_id):
    prog = m_get_progress(telegram_id)
    li = min(prog["level_index"] if prog else 0, len(MILLIONAIRE_LEAGUE) - 1)
    return {
        "level_index": li,
        "level_label": m_topic_label(li),
        "completed_levels": prog["completed_levels"] if prog else 0,
        "total_levels": len(MILLIONAIRE_LEAGUE),
        "best_money": prog["best_money"] if prog else 0,
    }

async def m_api_next_question(g):
    """سوال بعدی رو از بانک می‌گیره و توی state سرور می‌ذاره."""
    import time as _t
    qnum = g["qindex"] + 1
    q = await m_generate_question(g["level_index"], qnum, g.get("used_ids", set()))
    g["current_q"] = q
    g["hidden"] = []
    g["q_started_at"] = _t.time()   # زمان شروع سوال (سمت سرور — برای تایمر امن)
    if q.get("id") is not None:
        g.setdefault("used_ids", set()).add(q["id"])
    return q

# ── Handlers ──
async def api_health(request):
    from aiohttp import web
    return web.json_response({"ok": True})

async def api_start(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    # مطمئن شو کاربر توی جدول users هست (برای لیدربورد)
    existing = get_user(uid)
    if not existing:
        nm = (user.get("first_name", "") + " " + user.get("last_name", "")).strip() or user.get("username", "Player")
        save_user(uid, nm, "MiniApp")

    prog = m_get_progress(uid)
    li = min(prog["level_index"] if prog else 0, len(MILLIONAIRE_LEAGUE) - 1)
    g = {
        "active": True, "level_index": li, "qindex": 0,
        "current_q": None, "hidden": [], "correct_count": 0,
        "used_5050": False, "used_skip": False, "used_phone": False, "used_ids": set(),
    }
    M_API_GAMES[uid] = g
    try:
        q = await m_api_next_question(g)
    except Exception as e:
        logger.error("api_start gen failed: " + str(e))
        return web.json_response({"error": "no_questions"}, status=503)
    return web.json_response({
        "question": m_api_public_question(q),
        "qindex": g["qindex"],
        "ladder": m_api_ladder(),
        "progress": m_api_progress_payload(uid),
        "lifelines": {"fifty": True, "skip": True, "phone": True},
        "seconds": M_QUESTION_SECONDS,
    })

async def api_answer(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    g = M_API_GAMES.get(uid)
    if not g or not g.get("active") or not g.get("current_q"):
        return web.json_response({"error": "no_active_game"}, status=400)

    chosen = str(data.get("choice", "")).strip().upper()[:1]
    if chosen not in ("A", "B", "C", "D"):
        return web.json_response({"error": "bad_choice"}, status=400)

    q = g["current_q"]
    correct = q["correct"]

    # ── بررسی زمان (سمت سرور) — اگه بیشتر از حد مجاز طول کشیده، تایم‌اوت ──
    import time as _t
    started = g.get("q_started_at")
    if started and (_t.time() - started) > (M_QUESTION_SECONDS + M_TIMER_GRACE):
        money = m_money_at(g["qindex"])
        m_save_game(uid, g["level_index"], MILLIONAIRE_LEAGUE[g["level_index"]],
                    money, g["correct_count"], False)
        pts = 0
        if money >= 32000: pts = 30
        elif money >= 1000: pts = 15
        if pts > 0:
            add_points(uid, pts, "miniapp millionaire timeout L" + str(g["level_index"]+1))
        g["active"] = False
        return web.json_response({
            "correct": False, "choice": chosen, "correct_choice": correct,
            "explanation": q.get("explanation_fa", ""),
            "won_money": money, "outcome": "timeout",
            "points": pts, "progress": m_api_progress_payload(uid),
        })

    is_correct = (chosen == correct)

    if is_correct:
        g["correct_count"] += 1
        money_now = MILLIONAIRE_LADDER[g["qindex"]]
        # سوال آخر → برد کامل
        if g["qindex"] >= MILLIONAIRE_TOTAL_Q - 1:
            m_save_game(uid, g["level_index"], MILLIONAIRE_LEAGUE[g["level_index"]],
                        1000000, g["correct_count"], True)
            pts = 100
            add_points(uid, pts, "miniapp millionaire win L" + str(g["level_index"]+1))
            g["active"] = False
            return web.json_response({
                "correct": True, "choice": chosen, "correct_choice": correct,
                "explanation": q.get("explanation_fa", ""),
                "won_money": 1000000, "outcome": "win",
                "points": pts, "progress": m_api_progress_payload(uid),
            })
        # برو سوال بعد
        g["qindex"] += 1
        g["current_q"] = None
        g["hidden"] = []
        safe_reached = (g["qindex"] - 1) in MILLIONAIRE_SAFE
        try:
            nq = await m_api_next_question(g)
        except Exception as e:
            logger.error("api_answer next gen failed: " + str(e))
            return web.json_response({"error": "no_questions"}, status=503)
        return web.json_response({
            "correct": True, "choice": chosen, "correct_choice": correct,
            "explanation": q.get("explanation_fa", ""),
            "money_now": money_now, "safe_reached": safe_reached,
            "next_question": m_api_public_question(nq),
            "qindex": g["qindex"],
            "lifelines": m_lifelines_state(g),
        })
    else:
        # باخت → پول safe haven
        money = m_money_at(g["qindex"])
        m_save_game(uid, g["level_index"], MILLIONAIRE_LEAGUE[g["level_index"]],
                    money, g["correct_count"], False)
        pts = 0
        if money >= 32000: pts = 30
        elif money >= 1000: pts = 15
        if pts > 0:
            add_points(uid, pts, "miniapp millionaire lose L" + str(g["level_index"]+1))
        g["active"] = False
        return web.json_response({
            "correct": False, "choice": chosen, "correct_choice": correct,
            "explanation": q.get("explanation_fa", ""),
            "won_money": money, "outcome": "lose",
            "points": pts, "progress": m_api_progress_payload(uid),
        })

async def api_timeout(request):
    """فرانت وقتی تایمر صفر شد این رو صدا می‌زنه — مثل جواب غلط (تایم‌اوت)."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    g = M_API_GAMES.get(uid)
    if not g or not g.get("active") or not g.get("current_q"):
        return web.json_response({"error": "no_active_game"}, status=400)
    # تأیید سمت سرور که واقعاً زمان تموم شده (جلوگیری از سوءاستفاده)
    import time as _t
    started = g.get("q_started_at", 0)
    if started and (_t.time() - started) < (M_QUESTION_SECONDS - M_TIMER_GRACE):
        # هنوز زمان هست — تایم‌اوت نامعتبره، نادیده بگیر
        remaining = int(M_QUESTION_SECONDS - (_t.time() - started))
        return web.json_response({"error": "not_yet", "remaining": remaining}, status=400)
    q = g["current_q"]
    money = m_money_at(g["qindex"])
    m_save_game(uid, g["level_index"], MILLIONAIRE_LEAGUE[g["level_index"]],
                money, g["correct_count"], False)
    pts = 0
    if money >= 32000: pts = 30
    elif money >= 1000: pts = 15
    if pts > 0:
        add_points(uid, pts, "miniapp millionaire timeout L" + str(g["level_index"]+1))
    g["active"] = False
    return web.json_response({
        "outcome": "timeout", "won_money": money,
        "correct_choice": q["correct"], "explanation": q.get("explanation_fa", ""),
        "points": pts, "progress": m_api_progress_payload(uid),
    })

def m_lifelines_state(g):
    """وضعیت همه‌ی کمک‌ها برای ارسال به فرانت."""
    return {
        "fifty": not g.get("used_5050"),
        "skip": not g.get("used_skip"),
        "phone": not g.get("used_phone"),
    }

def m_phone_friend_hint(g):
    """
    کمک «تماس تلفنی»: یه دوست مجازی که جواب رو لو نمی‌ده.
    حدوداً ۷۰٪ به سمت جواب درست متمایل می‌شه، با ابراز شک روی یه گزینه‌ی دیگه.
    اگه 50:50 استفاده شده باشه، فقط بین گزینه‌های باقی‌مونده نظر می‌ده.
    """
    import random as _r
    q = g["current_q"]
    correct = q["correct"]
    hidden = g.get("hidden", [])
    available = [L for L in ("A", "B", "C", "D") if L not in hidden]

    # دوست با احتمال ۷۰٪ درست حدس می‌زنه (اگه درست جزو گزینه‌های باقی‌مونده باشه)
    confident_letter = correct
    if correct not in available:
        confident_letter = _r.choice(available)
    elif _r.random() > 0.70:
        # ۳۰٪ مواقع اشتباه متمایل می‌شه
        others = [L for L in available if L != correct]
        if others:
            confident_letter = _r.choice(others)

    # یه گزینه‌ی دیگه برای ابراز شک
    doubt_pool = [L for L in available if L != confident_letter]
    doubt_letter = _r.choice(doubt_pool) if doubt_pool else None

    opt = q["options"]
    cl = confident_letter + ") " + opt[confident_letter]
    templates_with_doubt = [
        "می‌بینم... فکر می‌کنم جوابش {c} باشه، ولی راستش روی {d} هم یه‌کم شک دارم. مطمئن نیستم صد درصد.",
        "اوممم، حس می‌کنم {c} درسته. ولی {d} هم بدک نیست، یه تردید کوچیک دارم.",
        "به نظرم {c} منطقی‌تره. هرچند بین این و {d} یه‌کم دودلم. خودت تصمیم بگیر.",
        "فکر کنم {c}. ولی اگه اشتباه کنم، احتمالاً {d} ـه. زیاد مطمئن نیستم‌ها.",
    ]
    templates_no_doubt = [
        "نسبتاً مطمئنم جوابش {c} ـه. ولی خب، صد درصد قول نمی‌دم.",
        "من می‌رم رو {c}. حس خوبی بهش دارم، ولی تصمیم نهایی با خودته.",
    ]
    if doubt_letter:
        dl = doubt_letter + ") " + opt[doubt_letter]
        txt = _r.choice(templates_with_doubt).format(c=cl, d=dl)
    else:
        txt = _r.choice(templates_no_doubt).format(c=cl)
    return "📞 دوستت: «" + txt + "»"

async def api_lifeline(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    g = M_API_GAMES.get(uid)
    if not g or not g.get("active") or not g.get("current_q"):
        return web.json_response({"error": "no_active_game"}, status=400)
    kind = data.get("kind")
    q = g["current_q"]

    if kind == "fifty":
        if g["used_5050"]:
            return web.json_response({"error": "already_used"}, status=400)
        g["used_5050"] = True
        import random as _r
        wrong = [L for L in ("A", "B", "C", "D") if L != q["correct"]]
        _r.shuffle(wrong)
        g["hidden"] = wrong[:2]
        return web.json_response({"hidden": g["hidden"],
                                  "lifelines": m_lifelines_state(g)})
    elif kind == "phone":
        if g.get("used_phone"):
            return web.json_response({"error": "already_used"}, status=400)
        g["used_phone"] = True
        text = m_phone_friend_hint(g)
        return web.json_response({"phone_text": text,
                                  "lifelines": m_lifelines_state(g)})
    elif kind == "skip":
        if g["used_skip"]:
            return web.json_response({"error": "already_used"}, status=400)
        g["used_skip"] = True
        g["current_q"] = None
        g["hidden"] = []
        try:
            nq = await m_api_next_question(g)
        except Exception as e:
            return web.json_response({"error": "no_questions"}, status=503)
        return web.json_response({"next_question": m_api_public_question(nq),
                                  "qindex": g["qindex"],
                                  "lifelines": m_lifelines_state(g)})
    return web.json_response({"error": "bad_kind"}, status=400)

async def api_walk(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    g = M_API_GAMES.get(uid)
    if not g or not g.get("active"):
        return web.json_response({"error": "no_active_game"}, status=400)
    money = MILLIONAIRE_LADDER[g["qindex"] - 1] if g["qindex"] > 0 else 0
    m_save_game(uid, g["level_index"], MILLIONAIRE_LEAGUE[g["level_index"]],
                money, g["correct_count"], False)
    pts = 0
    if money >= 32000: pts = 30
    elif money >= 1000: pts = 15
    elif money > 0: pts = 5
    if pts > 0:
        add_points(uid, pts, "miniapp millionaire walk L" + str(g["level_index"]+1))
    g["active"] = False
    return web.json_response({
        "outcome": "walk", "won_money": money, "points": pts,
        "correct_choice": g["current_q"]["correct"] if g.get("current_q") else None,
        "explanation": g["current_q"].get("explanation_fa", "") if g.get("current_q") else "",
        "progress": m_api_progress_payload(uid),
    })

async def api_leaderboard(request):
    from aiohttp import web
    data = await request.json() if request.body_exists else {}
    user = m_api_user_from_request(data)
    me = user["id"] if user else None
    rows = m_weekly_leaderboard()
    out = []
    for i, r in enumerate(rows):
        out.append({
            "rank": i + 1,
            "name": r["name"],
            "money": int(r["week_money"]),
            "millions": int(r["millions"]),
            "is_me": (r["telegram_id"] == me),
        })
    return web.json_response({"leaderboard": out})

async def api_progress(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    # مطمئن شو کاربر ثبت شده
    if not get_user(uid):
        nm = (user.get("first_name", "") + " " + user.get("last_name", "")).strip() or user.get("username", "Player")
        save_user(uid, nm, "MiniApp")
    return web.json_response({
        "progress": m_api_progress_payload(uid),
        "name": user.get("first_name", "Player"),
    })

async def api_index(request):
    from aiohttp import web
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "millionaire.html")
    if os.path.exists(path):
        return web.FileResponse(path)
    return web.Response(text="Mini App file not found.", status=404)

async def api_leitner_index(request):
    from aiohttp import web
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leitner.html")
    if os.path.exists(path):
        return web.FileResponse(path)
    return web.Response(text="Leitner Mini App file not found.", status=404)

async def api_hub_index(request):
    from aiohttp import web
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hub.html")
    if os.path.exists(path):
        return web.FileResponse(path)
    return web.Response(text="Hub file not found.", status=404)

async def api_leitner_add(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    if not get_user(uid):
        nm = (user.get("first_name", "") + " " + user.get("last_name", "")).strip() or user.get("username", "Player")
        save_user(uid, nm, "MiniApp")
    front = str(data.get("front", "")).strip()
    back = str(data.get("back", "")).strip()
    if not front or not back:
        return web.json_response({"error": "empty"}, status=400)
    ok = leitner_add_card(uid, front, back)
    if not ok:
        return web.json_response({"error": "save_failed"}, status=500)
    return web.json_response({"ok": True, "stats": leitner_stats(uid)})

async def api_leitner_due(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    cards = leitner_due_cards(uid)
    out = [{"id": c["id"], "front": c["front"], "back": c["back"], "box": c["box"]} for c in cards]
    return web.json_response({"cards": out, "stats": leitner_stats(uid)})

async def api_leitner_review(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    try:
        card_id = int(data.get("card_id"))
    except Exception:
        return web.json_response({"error": "bad_id"}, status=400)
    knew = bool(data.get("knew"))
    ok = leitner_review(uid, card_id, knew)
    if not ok:
        return web.json_response({"error": "review_failed"}, status=400)
    return web.json_response({"ok": True, "stats": leitner_stats(uid)})

async def api_leitner_stats(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    if not get_user(uid):
        nm = (user.get("first_name", "") + " " + user.get("last_name", "")).strip() or user.get("username", "Player")
        save_user(uid, nm, "MiniApp")
    return web.json_response({"stats": leitner_stats(uid), "name": user.get("first_name", "")})

async def api_leitner_delete(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    try:
        card_id = int(data.get("card_id"))
    except Exception:
        return web.json_response({"error": "bad_id"}, status=400)
    leitner_delete_card(uid, card_id)
    return web.json_response({"ok": True, "stats": leitner_stats(uid)})

async def api_leitner_reminder(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    if not get_user(uid):
        nm = (user.get("first_name", "") + " " + user.get("last_name", "")).strip() or user.get("username", "Player")
        save_user(uid, nm, "MiniApp")
    if "set" in data:
        leitner_set_reminders(uid, bool(data.get("set")))
    return web.json_response({"reminders_on": leitner_get_reminders(uid)})

async def api_leitner_list(request):
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    uid = user["id"]
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT id, front, back, box FROM leitner_cards WHERE telegram_id=%s ORDER BY box, id DESC LIMIT 200", (uid,))
        rows = cur.fetchall(); cur.close(); conn.close()
        out = [{"id": r["id"], "front": r["front"], "back": r["back"], "box": r["box"]} for r in rows]
    except Exception as e:
        print("api_leitner_list error: " + str(e))
        out = []
    return web.json_response({"cards": out})

def _td_ensure_user(user):
    uid = user["id"]
    if not get_user(uid):
        nm = (user.get("first_name", "") + " " + user.get("last_name", "")).strip() or user.get("username", "Player")
        save_user(uid, nm, "MiniApp")
    return (user.get("first_name", "") or user.get("username", "") or "Player").strip()

def _td_is_german(uid):
    try:
        u = get_user(uid)
        return bool(u and (u.get("language") == "de"))
    except Exception:
        return False

async def api_td_lobby(request):
    """صفحه‌ی اصلی: لیست بازی‌های باز + آمار داخلی کاربر."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    if _td_is_german(user["id"]):
        return web.json_response({"error": "persian_only"}, status=403)
    name = _td_ensure_user(user)
    opens = td_list_open_matches(exclude_id=user["id"])
    return web.json_response({
        "name": name,
        "open_matches": [{"id": m["id"], "creator_name": m["creator_name"]} for m in opens],
    })

async def api_td_new(request):
    """۱۲ سوال برای یه بازی جدید می‌ده (هنوز ذخیره نشده — بعد از بازی submit می‌شه)."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    if _td_is_german(user["id"]):
        return web.json_response({"error": "persian_only"}, status=403)
    _td_ensure_user(user)
    qs = td_pick_questions()
    if len(qs) < 12:
        return web.json_response({"error": "bank_not_ready"}, status=503)
    out = [{"id": q["id"], "level": q["level"], "fa": q["fa"]} for q in qs]
    return web.json_response({"questions": out, "seconds": 30})

async def api_td_submit_new(request):
    """نفر اول جواب‌ها رو می‌فرسته → AI تصحیح → بازی waiting ساخته می‌شه."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    name = _td_ensure_user(user)
    qids = data.get("question_ids", [])
    answers = data.get("answers", [])
    if not qids or len(qids) != 12:
        return web.json_response({"error": "bad_data"}, status=400)
    questions = td_get_questions_by_ids(qids)
    score, _ = td_score_answers(questions, answers)
    mid = td_create_match(user["id"], name, qids, score, answers)
    if not mid:
        return web.json_response({"error": "save_failed"}, status=500)
    # نفر اول فقط امتیاز خودش رو می‌بینه (نتیجه‌ی نهایی بعداً)
    return web.json_response({"match_id": mid, "your_score": score, "total": 12, "waiting": True})

async def api_td_join(request):
    """حریف یه بازی waiting رو می‌گیره و همون ۱۲ سوال رو می‌گیره."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    name = _td_ensure_user(user)
    try:
        match_id = int(data.get("match_id"))
    except Exception:
        return web.json_response({"error": "bad_id"}, status=400)
    m = td_get_match(match_id)
    if not m or m["status"] != "waiting":
        return web.json_response({"error": "not_available"}, status=409)
    ok = td_claim_match(match_id, user["id"], name)
    if not ok:
        return web.json_response({"error": "already_taken"}, status=409)
    import json as _json
    qids = _json.loads(m["question_ids"])
    questions = td_get_questions_by_ids(qids)
    out = [{"id": q["id"], "level": q["level"], "fa": q["fa"]} for q in questions]
    return web.json_response({"questions": out, "seconds": 30, "match_id": match_id,
                              "opponent_name": m["creator_name"]})

async def api_td_submit_join(request):
    """نفر دوم جواب‌ها رو می‌فرسته → تصحیح → نتیجه‌ی نهایی + امتیازها + فیدبک."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    _td_ensure_user(user)
    try:
        match_id = int(data.get("match_id"))
    except Exception:
        return web.json_response({"error": "bad_id"}, status=400)
    answers = data.get("answers", [])
    m = td_get_match(match_id)
    if not m or m["status"] != "playing" or m["opponent_id"] != user["id"]:
        return web.json_response({"error": "bad_match"}, status=409)
    import json as _json
    qids = _json.loads(m["question_ids"])
    questions = td_get_questions_by_ids(qids)
    score, _ = td_score_answers(questions, answers)
    result = td_finalize_match(match_id, score, answers)
    if not result:
        return web.json_response({"error": "finalize_failed"}, status=500)
    you_won = (result["winner_id"] == user["id"])
    return web.json_response({
        "your_score": score, "total": 12,
        "opponent_score": result["creator_score"],
        "opponent_name": result["creator_name"],
        "is_draw": result["is_draw"],
        "you_won": you_won,
        "feedback": "",
    })

async def api_td_result(request):
    """نفر اول چک می‌کنه که آیا حریفش بازی رو تموم کرده و نتیجه چیه."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    try:
        match_id = int(data.get("match_id"))
    except Exception:
        return web.json_response({"error": "bad_id"}, status=400)
    m = td_get_match(match_id)
    if not m or m["creator_id"] != user["id"]:
        return web.json_response({"error": "bad_match"}, status=409)
    if m["status"] != "finished":
        return web.json_response({"status": "waiting"})
    you_won = (m["winner_id"] == user["id"])
    is_draw = (m["winner_id"] is None)
    return web.json_response({
        "status": "finished",
        "your_score": m["creator_score"], "total": 12,
        "opponent_score": m["opponent_score"], "opponent_name": m["opponent_name"],
        "is_draw": is_draw, "you_won": you_won,
    })

async def api_td_results(request):
    """لیست عمومی نتایج اخیر."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    res = td_recent_results(30)
    out = []
    for r in res:
        if r["winner_id"] is None:
            winner = "draw"
        else:
            winner = r["creator_name"] if r["winner_id"] == r["creator_id"] else r["opponent_name"]
        out.append({
            "creator": r["creator_name"], "opponent": r["opponent_name"],
            "cscore": r["creator_score"], "oscore": r["opponent_score"],
            "winner": winner,
        })
    return web.json_response({"results": out})

async def api_td_leaderboard(request):
    """لیدربورد داخلی بازی (برد/مساوی/باخت)."""
    from aiohttp import web
    data = await request.json()
    user = m_api_user_from_request(data)
    if not user:
        return web.json_response({"error": "auth_failed"}, status=401)
    lb = td_internal_leaderboard()
    return web.json_response({"leaderboard": lb})

async def api_td_index(request):
    from aiohttp import web
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "duel.html")
    if os.path.exists(path):
        return web.FileResponse(path)
    return web.Response(text="Translation Duel file not found.", status=404)

async def start_web_server(app_ptb):
    """وب‌سرور aiohttp رو کنار bot بالا میاره."""
    try:
        from aiohttp import web
    except Exception as e:
        logger.error("aiohttp not installed — Mini App API disabled: " + str(e))
        return
    web_app = web.Application()
    web_app.router.add_get("/", api_index)
    web_app.router.add_get("/health", api_health)
    web_app.router.add_get("/leitner", api_leitner_index)
    web_app.router.add_get("/hub", api_hub_index)
    web_app.router.add_post("/api/start", api_start)
    web_app.router.add_post("/api/answer", api_answer)
    web_app.router.add_post("/api/timeout", api_timeout)
    web_app.router.add_post("/api/lifeline", api_lifeline)
    web_app.router.add_post("/api/walk", api_walk)
    web_app.router.add_post("/api/leaderboard", api_leaderboard)
    web_app.router.add_post("/api/progress", api_progress)
    web_app.router.add_post("/api/leitner/add", api_leitner_add)
    web_app.router.add_post("/api/leitner/due", api_leitner_due)
    web_app.router.add_post("/api/leitner/review", api_leitner_review)
    web_app.router.add_post("/api/leitner/stats", api_leitner_stats)
    web_app.router.add_post("/api/leitner/delete", api_leitner_delete)
    web_app.router.add_post("/api/leitner/list", api_leitner_list)
    web_app.router.add_post("/api/leitner/reminder", api_leitner_reminder)
    web_app.router.add_get("/duel", api_td_index)
    web_app.router.add_post("/api/td/lobby", api_td_lobby)
    web_app.router.add_post("/api/td/new", api_td_new)
    web_app.router.add_post("/api/td/submit_new", api_td_submit_new)
    web_app.router.add_post("/api/td/join", api_td_join)
    web_app.router.add_post("/api/td/submit_join", api_td_submit_join)
    web_app.router.add_post("/api/td/result", api_td_result)
    web_app.router.add_post("/api/td/results", api_td_results)
    web_app.router.add_post("/api/td/leaderboard", api_td_leaderboard)
    runner = web.AppRunner(web_app)
    await runner.setup()
    port = int(os.environ.get("PORT", "8080"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logger.info("Mini App web server running on port " + str(port))


async def _on_post_init(application):
    """بعد از init شدن bot، وب‌سرور Mini App رو هم بالا میاره (همون event loop)."""
    await start_web_server(application)


def fix_rtl(text):
    """
    متن فارسیِ مخلوط با انگلیسی/عدد رو درست راست‌چین می‌کنه.
    اول هر خط یه RLM (علامت راست‌چین نامرئی) می‌ذاره تا خط فارسی بمونه
    حتی وقتی با اسم انگلیسی یا عدد شروع می‌شه.
    """
    RLM = "\u200f"  # Right-to-Left Mark
    if not text:
        return text
    out_lines = []
    for line in text.split("\n"):
        if line.strip():
            out_lines.append(RLM + line)
        else:
            out_lines.append(line)
    return "\n".join(out_lines)

def m_looks_truncated(text):
    """تشخیص می‌ده که آیا متن وسط جمله بریده شده (ناقص). برای retry گزارش."""
    if not text:
        return True
    t = text.strip()
    if len(t) < 25:
        return True
    # اگه با علامت پایان جمله تموم نشده باشه، احتمالاً ناقصه
    if t[-1] not in "!.؟?…\"'»):":
        return True
    return False

def lb_save_snapshot(rows):
    """عکس فعلی لیدربورد رو ذخیره می‌کنه (برای مقایسه‌ی فردا)."""
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM leaderboard_snapshot")
        for i, r in enumerate(rows):
            cur.execute(
                "INSERT INTO leaderboard_snapshot (telegram_id, name, rank, points) VALUES (%s,%s,%s,%s)",
                (r["telegram_id"], r["name"], i + 1, r["total_points"])
            )
        conn.commit(); cur.close(); conn.close()
    except Exception as e:
        print("lb_save_snapshot error: " + str(e))

def lb_get_snapshot():
    """عکس قبلی لیدربورد. خروجی: dict[telegram_id] = {rank, points}"""
    try:
        conn = get_db()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT telegram_id, rank, points FROM leaderboard_snapshot")
        out = {r["telegram_id"]: {"rank": r["rank"], "points": r["points"]} for r in cur.fetchall()}
        cur.close(); conn.close()
        return out
    except Exception as e:
        print("lb_get_snapshot error: " + str(e))
        return {}

def lb_build_movements(rows, prev):
    """تغییرات رتبه‌ی امروز نسبت به دیروز رو به متن خلاصه می‌کنه (برای دادن به Gemini)."""
    lines = []
    for i, r in enumerate(rows[:20]):
        uid = r["telegram_id"]
        new_rank = i + 1
        name = r["name"]
        pts = r["total_points"]
        if uid in prev:
            old_rank = prev[uid]["rank"]
            old_pts = prev[uid]["points"]
            delta_pts = pts - old_pts
            if old_rank > new_rank:
                lines.append(f"{name}: از رتبه {old_rank} به رتبه {new_rank} صعود کرد (+{delta_pts} امتیاز امروز)")
            elif old_rank < new_rank:
                lines.append(f"{name}: از رتبه {old_rank} به رتبه {new_rank} سقوط کرد")
            else:
                if delta_pts > 0:
                    lines.append(f"{name}: رتبه {new_rank} رو حفظ کرد (+{delta_pts} امتیاز امروز)")
                else:
                    lines.append(f"{name}: رتبه {new_rank}، امروز امتیازی نگرفت")
        else:
            lines.append(f"{name}: تازه‌وارد جدول در رتبه {new_rank} ({pts} امتیاز)")
    return "\n".join(lines)

async def daily_leaderboard_report(context: ContextTypes.DEFAULT_TYPE):
    """هر روز ساعت ۸ شب ایران: گزارش طنز روزانه‌ی جدول لیدربورد."""
    try:
        rows = get_monthly_leaderboard()
        if not rows:
            return
        prev = lb_get_snapshot()
        movements = lb_build_movements(rows, prev)

        # اگه عکس قبلی نبود (اولین بار)، فقط صدرنشین‌ها رو معرفی کن
        first_time = (len(prev) == 0)

        prompt = (
            "تو یه گزارشگر ورزشی فارسی‌زبان و بامزه‌ای که جدول امتیازات یه آکادمی زبان انگلیسی رو روایت می‌کنی.\n"
            "بر اساس تغییرات امروزِ جدول، یه «گزارش روز» کوتاه و هیجان‌انگیز و طنز بنویس (بین ۴ تا ۸ خط).\n\n"
            "قوانین مهم:\n"
            "- لحن طنز و هیجان‌انگیز مثل گزارشگر مسابقه، ولی بدون تخریب یا تحقیر کسی.\n"
            "- زیادی چاپلوسی و مثبت‌گویی نکن، لوس نشو. واقعی و بامزه باش.\n"
            "- روی سبقت‌ها و جابه‌جایی‌های جالب تمرکز کن (کی از کی جلو زد).\n"
            "- اسم‌ها رو دقیق همون‌طور که هست بنویس.\n"
            "- با ایموجی‌های مناسب جون بده ولی زیادی شلوغش نکن.\n"
            "- خیلی مهم: گزارش باید کامل باشه و وسط جمله قطع نشه. حتماً با یه جمله‌ی کوتاهِ کاملِ انگیزشی/چالشی برای فردا تمومش کن.\n"
            "- جمله‌ی ناتمام ننویس.\n\n"
            "تغییرات امروز جدول:\n" + movements
        )
        if first_time:
            prompt += "\n\n(توجه: این اولین گزارشه و داده‌ی دیروز نداریم، پس فقط صدر جدول و وضعیت فعلی رو بامزه معرفی کن.)"

        loop = asyncio.get_event_loop()
        narration = None
        for attempt in range(2):  # حداکثر ۲ بار تلاش اگه ناقص اومد
            try:
                narration = await loop.run_in_executor(None, lambda: call_gemini_api([], prompt))
            except Exception as e:
                logger.error("report gemini failed: " + str(e))
                narration = None
            if narration and not m_looks_truncated(narration):
                break
            logger.warning("report looked truncated, retrying...")

        if not narration:
            # اگه Gemini در دسترس نبود، یه گزارش ساده بفرست
            narration = "📊 گزارش امروز آماده نشد، ولی رقابت داغه! فردا برمی‌گردیم. 🔥"

        msg = "🎙️ گزارش روزِ جدول لیدربورد\n" + "━" * 20 + "\n\n" + fix_rtl(narration.strip())

        # مقصد: REPORT_CHAT_ID اگه تنظیم شده، وگرنه همه‌ی کاربرها
        target = os.environ.get("REPORT_CHAT_ID", "").strip()
        if target:
            try:
                await context.bot.send_message(chat_id=target, text=msg)
            except Exception as e:
                logger.error("report send to channel failed: " + str(e))
        else:
            # به همه‌ی کاربرهای فعال بفرست
            sent = 0
            for r in rows:
                try:
                    await context.bot.send_message(chat_id=r["telegram_id"], text=msg)
                    sent += 1
                except Exception:
                    pass
                await asyncio.sleep(0.1)
            logger.info("Daily report sent to " + str(sent) + " users")

        # عکس امروز رو برای مقایسه‌ی فردا ذخیره کن
        lb_save_snapshot(rows)
    except Exception as e:
        logger.error("daily_leaderboard_report error: " + str(e))

async def daily_leitner_reminder(context: ContextTypes.DEFAULT_TYPE):
    """هر روز ساعت ۱۱ صبح ایران (۷:۳۰ UTC) به کاربرانی که کارت موعد‌رسیده دارن یادآوری می‌فرسته."""
    try:
        rows = leitner_users_with_due()
        sent = 0
        for r in rows:
            uid = r["telegram_id"]
            due = r["due"]
            if not due:
                continue
            try:
                await context.bot.send_message(
                    chat_id=uid,
                    text=(
                        "📦 Leitner Box — Daily Reminder\n\n"
                        "📚 You have " + str(due) + " card(s) due for review today!\n"
                        "Open the menu (🎓) and tap Leitner Box to practice. 💪\n\n"
                        "— Emad English Lab"
                    )
                )
                sent += 1
            except Exception as e:
                # کاربر شاید بات رو بلاک کرده — رد شو
                logger.warning("reminder send failed for " + str(uid) + ": " + str(e))
            await asyncio.sleep(0.1)
        logger.info("Daily Leitner reminders sent: " + str(sent))
    except Exception as e:
        logger.error("daily_leitner_reminder error: " + str(e))

async def reminders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """روشن/خاموش کردن یادآوری روزانه: /reminders on  یا  /reminders off"""
    user_id = update.effective_user.id
    arg = (context.args[0].lower() if context.args else "")
    if arg in ("on", "روشن"):
        leitner_set_reminders(user_id, True)
        await update.message.reply_text("🔔 Daily Leitner reminders are now ON.\nیادآوری روزانه روشن شد.")
    elif arg in ("off", "خاموش"):
        leitner_set_reminders(user_id, False)
        await update.message.reply_text("🔕 Daily Leitner reminders are now OFF.\nیادآوری روزانه خاموش شد.\n\nبرای روشن کردن دوباره: /reminders on")
    else:
        cur = leitner_get_reminders(user_id)
        state = "ON 🔔" if cur else "OFF 🔕"
        await update.message.reply_text(
            "📦 Daily Leitner reminders: " + state + "\n\n"
            "Turn on:  /reminders on\n"
            "Turn off: /reminders off"
        )


async def tdstats_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """وضعیت بانک سوال Translation Duel — فقط معلم."""
    if update.effective_user.id != TEACHER_ID:
        await update.message.reply_text("🚫 Teacher only.")
        return
    counts = td_bank_count_by_level()
    total = sum(counts.values())
    lines = ["📊 Translation Duel — بانک سوال", "━" * 20]
    for lv in TD_LEVELS:
        have = counts.get(lv, 0)
        mark = "✅" if have >= TD_TARGET_PER_LEVEL else "🟡"
        lines.append(f"{mark} {lv}: {have}/{TD_TARGET_PER_LEVEL}")
    lines.append("━" * 20)
    lines.append(f"مجموع: {total}/{TD_TARGET_PER_LEVEL * len(TD_LEVELS)}")
    await update.message.reply_text("\n".join(lines))


async def champion_photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    معلم عکس کارت قهرمان رو با کپشن /champion می‌فرسته.
    بات اون رو برای همه‌ی کاربرها + کانال (اگه REPORT_CHAT_ID تنظیم شده) پخش می‌کنه.
    """
    if update.effective_user.id != TEACHER_ID:
        return
    msg = update.message
    if not msg or not msg.photo:
        return
    caption = (msg.caption or "")
    if "/champion" not in caption.lower():
        return

    # بزرگ‌ترین نسخه‌ی عکس
    photo_id = msg.photo[-1].file_id
    # متن همراه (هر چی بعد از /champion نوشته شده، وگرنه متن پیش‌فرض)
    extra = caption.split("/champion", 1)[-1].strip()
    cap = extra if extra else "🏆 قهرمان این ماه معرفی شد! تبریک به برنده 🎉\n\n— Emad English Lab"

    await msg.reply_text("📤 در حال پخش کارت قهرمان...")

    sent = 0
    failed = 0
    # ۱) به کانال (اگه تنظیم شده)
    channel = os.environ.get("REPORT_CHAT_ID", "").strip()
    if channel:
        try:
            await context.bot.send_photo(chat_id=channel, photo=photo_id, caption=cap)
        except Exception as e:
            logger.error("champion channel send failed: " + str(e))

    # ۲) به همه‌ی کاربرها
    try:
        users = get_all_users()
    except Exception:
        users = []
    for u in users:
        uid = u.get("telegram_id") if isinstance(u, dict) else None
        if not uid:
            continue
        try:
            await context.bot.send_photo(chat_id=uid, photo=photo_id, caption=cap)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.1)

    await msg.reply_text(f"✅ کارت قهرمان پخش شد!\nبه {sent} نفر فرستاده شد." + (f"\n({failed} نفر ناموفق)" if failed else ""))


async def testreport_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تست فوری گزارش روزانه — فقط معلم."""
    if update.effective_user.id != TEACHER_ID:
        await update.message.reply_text("🚫 Teacher only.")
        return
    await update.message.reply_text("🎙️ در حال ساخت گزارش تستی... (فقط برای تو فرستاده می‌شه)")
    try:
        rows = get_monthly_leaderboard()
        if not rows:
            await update.message.reply_text("جدول خالیه، گزارشی نیست.")
            return
        prev = lb_get_snapshot()
        movements = lb_build_movements(rows, prev)
        prompt = (
            "تو یه گزارشگر ورزشی فارسی‌زبان و بامزه‌ای که جدول امتیازات یه آکادمی زبان انگلیسی رو روایت می‌کنی.\n"
            "بر اساس تغییرات امروزِ جدول، یه «گزارش روز» کوتاه و هیجان‌انگیز و طنز بنویس (حداکثر ۸ خط).\n"
            "لحن طنز بدون تخریب، لوس و چاپلوس نباش، روی سبقت‌ها تمرکز کن، اسم‌ها رو دقیق بنویس، آخرش یه جمله‌ی چالشی برای فردا.\n\n"
            "تغییرات امروز جدول:\n" + movements
        )
        loop = asyncio.get_event_loop()
        narration = None
        for attempt in range(2):
            narration = await loop.run_in_executor(None, lambda: call_gemini_api([], prompt))
            if narration and not m_looks_truncated(narration):
                break
        msg = "🎙️ گزارش روزِ جدول لیدربورد (تست)\n" + "━" * 20 + "\n\n" + fix_rtl((narration or "خطا").strip())
        await update.message.reply_text(msg)
    except Exception as e:
        await update.message.reply_text("خطا در ساخت گزارش: " + str(e))


async def leitner_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """باز کردن جعبه لایتنر با دکمه‌ی inline (مطمئن‌ترین راه برای ارسال initData)."""
    if not LEITNER_URL:
        await update.message.reply_text("📦 Leitner Box is not configured yet (MINIAPP_URL missing).")
        return
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("📦 Open Leitner Box", web_app=WebAppInfo(url=LEITNER_URL))]])
    await update.message.reply_text(
        "📦 Your personal Leitner Box\n\nTap below to add and review your flashcards:",
        reply_markup=kb
    )


def main():
    init_db()
    # پر کردن یک‌باره‌ی بانک سوالات اگه خالیه (در صورت تنظیم env)
    if os.environ.get("BOOTSTRAP_QUESTIONS", "").lower() in ("1", "true", "yes"):
        try:
            m_bootstrap_bank(target_per_level=100)
        except Exception as e:
            logger.error("bootstrap bank failed: " + str(e))
    # پر کردن یک‌باره‌ی بانک Translation Duel (با TD_BOOTSTRAP=true)
    if os.environ.get("TD_BOOTSTRAP", "").lower() in ("1", "true", "yes"):
        try:
            td_bootstrap_bank()
        except Exception as e:
            logger.error("td bootstrap failed: " + str(e))
    app = Application.builder().token(BOT_TOKEN).post_init(_on_post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("quit", quit_cmd))
    app.add_handler(CommandHandler("endai", endai_cmd))
    app.add_handler(CommandHandler("results", results_cmd))
    app.add_handler(CommandHandler("profile", profile_cmd))
    app.add_handler(CommandHandler("feedback", feedback_cmd))
    app.add_handler(CommandHandler("leaderboard", leaderboard_cmd))
    app.add_handler(CommandHandler("rank", leaderboard_cmd))
    app.add_handler(CommandHandler("users", users_cmd))
    app.add_handler(CommandHandler("myscore", myscore_cmd))
    app.add_handler(CommandHandler("myprogress", myprogress_cmd))
    app.add_handler(CommandHandler("report", report_cmd))
    app.add_handler(CommandHandler("stats", stats_cmd))
    app.add_handler(CommandHandler("mqstats", mqstats_cmd))
    app.add_handler(CommandHandler("reminders", reminders_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CommandHandler("leitner", leitner_cmd))
    app.add_handler(CommandHandler("testreport", testreport_cmd))
    app.add_handler(CommandHandler("tdstats", tdstats_cmd))
    app.add_handler(MessageHandler(filters.PHOTO, champion_photo_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # یادآوری روزانه‌ی جعبه لایتنر — ۱۱ صبح ایران = ۷:۳۰ UTC
    try:
        app.job_queue.run_daily(
            daily_leitner_reminder,
            time=dtime(hour=7, minute=30, tzinfo=timezone.utc),
            name="daily_leitner_reminder",
        )
        logger.info("Daily Leitner reminder scheduled for 07:30 UTC (11:00 Iran).")
    except Exception as e:
        logger.error("Could not schedule daily reminder: " + str(e))
    # گزارش طنز روزانه‌ی لیدربورد — ۸ شب ایران = ۱۶:۳۰ UTC
    try:
        app.job_queue.run_daily(
            daily_leaderboard_report,
            time=dtime(hour=16, minute=30, tzinfo=timezone.utc),
            name="daily_leaderboard_report",
        )
        logger.info("Daily leaderboard report scheduled for 16:30 UTC (20:00 Iran).")
    except Exception as e:
        logger.error("Could not schedule daily report: " + str(e))
    logger.info("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
