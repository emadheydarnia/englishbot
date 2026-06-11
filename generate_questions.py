#!/usr/bin/env python3
"""
generate_questions.py — تولید یک‌باره‌ی بانک سوالات Millionaire و ذخیره در PostgreSQL.

اجرا:
    python generate_questions.py            # فقط فصل‌هایی که هنوز ۱۰۰ سوال ندارن رو پر می‌کنه
    python generate_questions.py --level 0  # فقط فصل ۰ (اولین فصل)
    python generate_questions.py --reset    # کل بانک رو خالی و از نو می‌سازه

نیاز به env vars:  DATABASE_URL ، GEMINI_API_KEY
"""

import os
import sys
import json
import time
import argparse

import requests
import psycopg2

# ── همون تنظیمات bot ─────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-flash-latest",
]

# ترتیب لیگ — باید دقیقاً با MILLIONAIRE_LEAGUE داخل english_bot.py یکی باشه
MILLIONAIRE_LEAGUE = [
    ("present_simple_continuous", "Present Simple vs Continuous"),
    ("past_simple",               "Past Simple"),
    ("present_perfect",           "Present Perfect"),
    ("present_perfect_continuous","Present Perfect Continuous"),
    ("comparison",                "Comparison (comparatives & superlatives)"),
    ("rather_prefer",             "would rather / prefer / would sooner"),
    ("relative_clause",           "Relative Clauses"),
    ("fanboys",                   "FANBOYS coordinating conjunctions"),
    ("contrast",                  "Contrast linkers (although, despite, however...)"),
    ("conditionals",              "Conditionals (type 0,1,2,3 & mixed)"),
    ("passive",                   "Passive Voice"),
    ("causative",                 "Causative (have/get something done)"),
    ("modals",                    "Modal Verbs"),
]

# هر فصل ۱۰۰ سوال = ۲۵ تا در هر سطح CEFR
CEFR_LEVELS = ["A2", "B1", "B2", "C1"]
PER_CEFR = 25            # 25 × 4 = 100 per level
BATCH = 5               # تعداد سوال در هر call به Gemini


def get_db():
    return psycopg2.connect(os.environ["DATABASE_URL"], sslmode="require")


def call_gemini(prompt):
    messages = [{"role": "user", "content": prompt}]
    last_err = None
    for m in GEMINI_MODELS:
        payload = {"model": m, "messages": messages, "max_tokens": 4096, "temperature": 0.9}
        headers = {"Authorization": "Bearer " + GEMINI_API_KEY, "Content-Type": "application/json"}
        try:
            r = requests.post(GEMINI_URL, json=payload, headers=headers, timeout=90)
            if r.ok:
                return r.json()["choices"][0]["message"]["content"]
            if r.status_code in (429, 503, 529):
                print(f"   model {m} busy ({r.status_code}), waiting...")
                last_err = Exception(str(r.status_code))
                time.sleep(3)
                continue
            raise Exception(f"{r.status_code} {r.text[:150]}")
        except Exception as e:
            last_err = e
            print(f"   model {m} failed: {e}")
            continue
    raise last_err


def build_prompt(topic_label, cefr, n, review_labels):
    review_txt = ""
    if review_labels:
        review_txt = ("Some questions (about 30%) may also lightly review these earlier topics: "
                      + ", ".join(review_labels) + ".\n")
    return f"""You are writing questions for a 'Who Wants to Be a Millionaire' English GRAMMAR game.

MAIN TOPIC: {topic_label}
{review_txt}CEFR difficulty: {cefr}

Generate {n} DISTINCT multiple-choice grammar questions.

STRICT RULES for every question:
- Tests ENGLISH GRAMMAR (fill-in-the-blank or "choose the correct form"). One short English sentence.
- Exactly 4 options A,B,C,D. Exactly ONE correct. Wrong options reflect common learner errors.
- Vary the correct letter across questions (not always the same).
- A short PERSIAN (Farsi) explanation, max 2 sentences, why the answer is correct.
- Keep difficulty consistent with CEFR {cefr}.

Return ONLY a valid JSON array, no markdown, no commentary. Exactly this shape:
[
  {{"question":"...","options":{{"A":"...","B":"...","C":"...","D":"..."}},"correct":"A","explanation_fa":"..."}}
]"""


def parse_array(raw):
    txt = raw.strip().replace("```json", "").replace("```", "").strip()
    s = txt.find("[")
    e = txt.rfind("]")
    if s != -1 and e != -1:
        txt = txt[s:e+1]
    data = json.loads(txt)
    out = []
    for item in data:
        try:
            opts = item["options"]
            correct = str(item["correct"]).strip().upper()[:1]
            if correct not in ("A", "B", "C", "D"):
                continue
            if not all(L in opts for L in ("A", "B", "C", "D")):
                continue
            out.append({
                "question": str(item["question"]).strip(),
                "A": str(opts["A"]).strip(),
                "B": str(opts["B"]).strip(),
                "C": str(opts["C"]).strip(),
                "D": str(opts["D"]).strip(),
                "correct": correct,
                "explanation_fa": str(item.get("explanation_fa", "")).strip(),
            })
        except Exception:
            continue
    return out


def count_existing(cur, level_index, cefr):
    cur.execute(
        "SELECT COUNT(*) FROM millionaire_questions WHERE level_index=%s AND cefr=%s",
        (level_index, cefr),
    )
    return cur.fetchone()[0]


def existing_questions_set(cur, level_index):
    cur.execute(
        "SELECT LOWER(question) FROM millionaire_questions WHERE level_index=%s",
        (level_index,),
    )
    return set(r[0] for r in cur.fetchall())


def insert_questions(cur, level_index, topic_key, cefr, items):
    for it in items:
        cur.execute(
            """INSERT INTO millionaire_questions
               (level_index, topic, cefr, question, option_a, option_b, option_c, option_d, correct, explanation_fa)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (level_index, topic_key, cefr, it["question"],
             it["A"], it["B"], it["C"], it["D"], it["correct"], it["explanation_fa"]),
        )


def generate_for_level(conn, level_index):
    topic_key, topic_label = MILLIONAIRE_LEAGUE[level_index]
    review_labels = [lbl for _, lbl in MILLIONAIRE_LEAGUE[:level_index]][-4:]  # حداکثر ۴ تای آخر
    cur = conn.cursor()
    seen = existing_questions_set(cur, level_index)
    print(f"\n=== فصل {level_index+1}/{len(MILLIONAIRE_LEAGUE)}: {topic_label} ===")

    for cefr in CEFR_LEVELS:
        have = count_existing(cur, level_index, cefr)
        need = PER_CEFR - have
        if need <= 0:
            print(f"  [{cefr}] کامله ({have}/{PER_CEFR}) — رد شد")
            continue
        print(f"  [{cefr}] نیاز به {need} سوال جدید...")
        attempts = 0
        while need > 0 and attempts < 12:
            attempts += 1
            ask = min(BATCH, need + 2)  # کمی بیشتر بخواه چون بعضیا dup یا نامعتبرن
            try:
                raw = call_gemini(build_prompt(topic_label, cefr, ask, review_labels))
                items = parse_array(raw)
            except Exception as e:
                print(f"    تلاش {attempts} خطا: {e}")
                time.sleep(3)
                continue
            fresh = []
            for it in items:
                key = it["question"].lower()
                if key in seen:
                    continue
                seen.add(key)
                fresh.append(it)
                if len(fresh) >= need:
                    break
            if fresh:
                insert_questions(cur, level_index, topic_key, cefr, fresh)
                conn.commit()
                need -= len(fresh)
                print(f"    +{len(fresh)} ثبت شد (باقی‌مونده: {need})")
            time.sleep(1)
        if need > 0:
            print(f"  ⚠️ [{cefr}] فقط تا اینجا رسید، {need} تا کم موند")
    cur.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", type=int, default=None, help="فقط همین فصل (۰-based)")
    ap.add_argument("--reset", action="store_true", help="خالی کردن کل بانک")
    args = ap.parse_args()

    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY تنظیم نشده."); sys.exit(1)
    if not os.environ.get("DATABASE_URL"):
        print("❌ DATABASE_URL تنظیم نشده."); sys.exit(1)

    conn = get_db()
    # مطمئن شو جدول هست (اگه bot هنوز init نکرده)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS millionaire_questions (
            id SERIAL PRIMARY KEY, level_index INTEGER, topic VARCHAR(100),
            cefr VARCHAR(5), question TEXT, option_a TEXT, option_b TEXT,
            option_c TEXT, option_d TEXT, correct CHAR(1), explanation_fa TEXT,
            approved BOOLEAN DEFAULT TRUE, created_at TIMESTAMP DEFAULT NOW()
        )""")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_mq_level_cefr ON millionaire_questions(level_index, cefr)")
    if args.reset:
        cur.execute("DELETE FROM millionaire_questions")
        print("🗑 کل بانک سوالات پاک شد.")
    conn.commit(); cur.close()

    if args.level is not None:
        generate_for_level(conn, args.level)
    else:
        for i in range(len(MILLIONAIRE_LEAGUE)):
            generate_for_level(conn, i)

    # گزارش نهایی
    cur = conn.cursor()
    cur.execute("SELECT level_index, COUNT(*) FROM millionaire_questions GROUP BY level_index ORDER BY level_index")
    print("\n📊 جمع‌بندی بانک سوالات:")
    total = 0
    for li, c in cur.fetchall():
        total += c
        print(f"   فصل {li+1}: {c} سوال")
    print(f"   ──────────\n   مجموع: {total} سوال")
    cur.close(); conn.close()
    print("\n✅ تمام شد.")


if __name__ == "__main__":
    main()
