# -*- coding: utf-8 -*-
"""
بانک آزمون‌های کلاسی (Class Quiz).
هر آزمون: عنوان + مدت + لیست سوال‌ها. نمره‌ی نهایی همیشه از ۱۰۰ حساب می‌شه.
هر سوال: (qtype, question, answer, options, needs_ai, context)
- qtype: "fill" (جای خالی) یا "mc" (چندگزینه‌ای)
- options: برای mc لیست گزینه‌ها؛ برای fill خالی []
- answer: جواب درست. چند جواب جایگزین با / جدا می‌شه.
- needs_ai: اگه تصحیحش ظرافت داره و باید AI کمک کنه True
- context: متنی که بالای سوال نشون داده می‌شه (مثلاً بخش اولِ یک سوال دوبخشی).
"""

QUIZZES = {}

def _q(qtype, question, answer, options=None, needs_ai=False, context=""):
    return {"qtype": qtype, "question": question, "options": options or [],
            "answer": answer, "needs_ai": needs_ai, "context": context}

# ══════════════════════════════════════════════════════════════
# Exam 1 (present simple-continuous)
# ══════════════════════════════════════════════════════════════
QUIZZES["exam1"] = {
    "title": "Exam 1 (present simple-continuous)",
    "duration_min": 30,
    "questions": [
        _q("fill", "You can't see Jimmy now. He ____ a bath. (HAVE)",
           "is having/'s having"),
        _q("fill", "He ____ to the theatre. (NEVER GO)",
           "never goes"),
        _q("fill", "Anne ____ all her clothes herself. (MAKE)",
           "makes"),
        _q("fill", "At the moment she ____ a dress for a fancy dress party. (MAKE)",
           "is making/'s making",
           context="Anne makes all her clothes herself."),
        _q("fill", "He usually ____ coffee for breakfast. (HAVE)",
           "has"),
        _q("fill", "But today he ____ tea. (HAVE)",
           "is having/'s having",
           context="He usually has coffee for breakfast."),
        _q("fill", "I can't go home now because it ____ . (RAIN)",
           "is raining/'s raining"),
        _q("fill", "And I ____ an umbrella. (NOT HAVE)",
           "do not have/don't have/have not got/haven't got",
           context="I can't go home now because it's raining."),
        _q("fill", "In Britain women normally ____ hats. (NOT WEAR)",
           "do not wear/don't wear"),
        _q("fill", "The sun ____ in the east. (RISE)",
           "rises"),
        _q("fill", "And ____ in the west. (SET)",
           "sets",
           context="The sun rises in the east."),
        _q("fill", "Who ____ that terrible noise outside? (MAKE)",
           "is making/'s making"),
        _q("fill", "It's Dad. He ____ the lawn. (MOW)",
           "is mowing/'s mowing",
           context="Who is making that terrible noise outside?"),
        _q("fill", "I ____ this weekend near the coast. (SPEND)",
           "am spending/'m spending"),
        _q("fill", "I ____ there nearly every weekend. (GO)",
           "go",
           context="I'm spending this weekend near the coast."),
        _q("fill", "She ____ thirty cigarettes a day. (SMOKE)",
           "smokes"),
        _q("fill", "But at the moment she ____ to stop. (TRY)",
           "is trying/'s trying",
           context="She smokes thirty cigarettes a day."),
        _q("fill", "We ____ breakfast together every Sunday morning. (HAVE)",
           "have"),
        _q("fill", "What's that smell? It's in the kitchen. Something ____ . (BURN)",
           "is burning/'s burning"),
        _q("fill", "Who ____ to on the phone? – It's my friend Carry. (YOU SPEAK)",
           "are you speaking"),
        _q("fill", "I ____ overtime this month. (WORK)",
           "am working/'m working"),
        _q("fill", "Because I ____ up some money to buy a new car. (SAVE)",
           "am saving/'m saving",
           context="I am working overtime this month."),
        _q("fill", "The moon ____ around the earth. (GO)",
           "goes"),
        _q("fill", "She usually ____ languages very quickly. (LEARN)",
           "learns"),
        _q("fill", "But she ____ problems with Chinese. (HAVE)",
           "is having/'s having/has", needs_ai=True,
           context="She usually learns languages very quickly."),
        _q("fill", "____ TV every evening? (YOU WATCH)",
           "do you watch"),
        _q("fill", "He always ____ his bills on time. (PAY)",
           "pays"),
        _q("fill", "How long ____ you to get to the office? (IT TAKE)",
           "does it take"),
        _q("fill", "It ____ me about half an hour. (TAKE)",
           "takes",
           context="How long does it take you to get to the office?"),
        _q("fill", "The plane that ____ Heathrow at 9.15 is on schedule. (LEAVE)",
           "leaves"),
    ],
}

# ══════════════════════════════════════════════════════════════
# Exam 0 (Tenses structures) — ۱۲ زمان انگلیسی Active
# جمله‌های پایه: Sarah/study English ، They/build a house ، I/work on the project
# ══════════════════════════════════════════════════════════════
QUIZZES["exam0"] = {
    "title": "Exam 0 (Tenses structures)",
    "duration_min": 20,
    "questions": [
        _q("fill", "Sarah ____ English every single day. (Present Simple)",
           "studies",
           context="Base sentence: Sarah / study English"),
        _q("fill", "Sarah ____ English right now; she is resting. (Present Continuous - negative)",
           "is not studying/isn't studying",
           context="Base sentence: Sarah / study English"),
        _q("fill", "____ English before? (Present Perfect - question)",
           "Has Sarah studied/has studied", needs_ai=True,
           context="Base sentence: Sarah / study English   (e.g. Has Sarah studied ...?)"),
        _q("fill", "Sarah is tired because she ____ English for three hours. (Present Perfect Continuous)",
           "has been studying",
           context="Base sentence: Sarah / study English"),
        _q("fill", "They ____ a house last year; they didn't have enough money. (Past Simple - negative)",
           "did not build/didn't build",
           context="Base sentence: They / build a house"),
        _q("fill", "At this exact time yesterday they ____ a house. (Past Continuous)",
           "were building",
           context="Base sentence: They / build a house"),
        _q("fill", "____ the house before winter arrived? (Past Perfect - question)",
           "Had they built/had built", needs_ai=True,
           context="Base sentence: They / build a house   (e.g. Had they built ...?)"),
        _q("fill", "They ____ the house for months before the storm hit. (Past Perfect Continuous)",
           "had been building",
           context="Base sentence: They / build a house"),
        _q("fill", "I ____ on the project tomorrow because it's a holiday. (Future Simple - negative)",
           "will not work/won't work",
           context="Base sentence: I / work on the project"),
        _q("fill", "This time tomorrow evening I ____ on the project. (Future Continuous)",
           "will be working",
           context="Base sentence: I / work on the project"),
        _q("fill", "____ on the project by next Friday? (Future Perfect - question)",
           "Will I have worked/will have worked", needs_ai=True,
           context="Base sentence: I / work on the project   (e.g. Will I have worked ...?)"),
        _q("fill", "By next month I ____ on the project for half a year. (Future Perfect Continuous)",
           "will have been working",
           context="Base sentence: I / work on the project"),
    ],
}

QUIZZES["exam2"] = {
    "title": "Exam 2 (past simple/present simple/present continuous)",
    "duration_min": 30,
    "questions": [
        _q("fill", "Look! Steve ____ with another girl. (DANCE)", "is dancing/'s dancing"),
        _q("fill", "Joe said something funny and we all ____ . (LAUGH)", "laughed"),
        _q("fill", "Nick ____ from early morning until late at night every day. (WORK)", "works/worked"),
        _q("fill", "I was surprised that Allan ____ . (NOT WIN)", "did not win/didn't win"),
        _q("fill", "Alex was looking for the treasure, but he ____ it. (NOT FIND)", "did not find/didn't find"),
        _q("fill", "Richard ____ Kate something to drink, but she wasn't thirsty. (OFFER)", "offered"),
        _q("fill", "Tom is much shorter and ____ much less than Jack. (WEIGH)", "weighs"),
        _q("fill", "We ____ at home because it's raining. (STAY)", "are staying/'re staying"),
        _q("fill", "James ____ a love letter to Cindy. (WRITE)", "wrote"),
        _q("fill", "But he never ____ it to her. (GIVE)", "gave", context="James wrote a love letter to Cindy."),
        _q("fill", "When was the last time you ____ Christmas with your whole family? (CELEBRATE)", "celebrated"),
        _q("fill", "Bill typically ____ his work at 2:30. (FINISH)", "finishes"),
        _q("fill", "Roy ____ to come into the office on Mondays. (NOT NEED)", "does not need/doesn't need"),
        _q("fill", "In Japan, the new school year ____ in April. (BEGIN)", "begins"),
        _q("fill", "Could you please be quieter? David ____ . (SLEEP)", "is sleeping/'s sleeping"),
        _q("fill", "Neil can get there in ten minutes if he ____ fast. (DRIVE)", "drives"),
        _q("fill", "Why ____ to name your son Simon? (you DECIDE)", "did you decide", needs_ai=True),
        _q("fill", "Sam ____ his car at least once a week. (WASH)", "washes"),
        _q("fill", "____ the news on TV every day? (you WATCH)", "do you watch", needs_ai=True),
        _q("fill", "How often ____ at yourself in the mirror? (you LOOK)", "do you look", needs_ai=True),
        _q("fill", "Edward ____ that picture last summer. (PAINT)", "painted"),
        _q("fill", "The girl ____ to her feet. (JUMP)", "jumped"),
        _q("fill", "And she ____ the room. (LEAVE)", "left", context="The girl jumped to her feet."),
        _q("fill", "She feeds her dog the same thing that she ____ . (EAT)", "eats"),
        _q("fill", "Lisa ____ Randy every time she's in the United States. (VISIT)", "visits"),
        _q("fill", "Do you want to hear about what I ____ last summer? (DO)", "did"),
        _q("fill", "Alex ____ into bed. (GET)", "got"),
        _q("fill", "And he ____ the light. (TURN OFF)", "turned off", context="Alex got into bed."),
        _q("fill", "____ green or black tea? (you PREFER)", "do you prefer", needs_ai=True),
        _q("fill", "____ anybody who can teach my kids French? (you KNOW)", "do you know", needs_ai=True),
        _q("fill", "Look at the boy and the dog that ____ over there. (RUN)", "are running/'re running"),
        _q("fill", "Tom said that he hated the song we ____ last night. (SING)", "sang"),
        _q("fill", "The weather was cold and it ____ a lot. (RAIN)", "rained"),
    ],
}

if __name__ == "__main__":
    for k, v in QUIZZES.items():
        n = len(v['questions'])
        per = round(100 / n, 2)
        ai = sum(1 for q in v['questions'] if q['needs_ai'])
        ctx = sum(1 for q in v['questions'] if q['context'])
        print(f"{k}: {v['title']}")
        print(f"  {n} سوال × {per} نمره = 100 | {ai} سوال نیاز به AI | {ctx} سوال context دارن")
