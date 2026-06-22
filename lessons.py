# -*- coding: utf-8 -*-
"""
Pre-authored lessons for the German bot.

Key:   (level, topic_key)   e.g. ("A1", "greeting")
Value: {"note": <grammar/vocab lesson in English>, "questions": [{"en":..., "de":...}, ...]}

Lessons that are NOT listed here automatically fall back to AI generation in the bot,
so the bot keeps working while these are filled in lesson by lesson.
"""

LESSONS = {
    ("A1", "greeting"): {
        "note": (
            "📖 Greeting — A1\n\n"
            "German greetings change with the time of day and how formal you are.\n\n"
            "GREETINGS\n"
            "• Hallo — Hello (anytime)\n"
            "• Guten Morgen — Good morning\n"
            "• Guten Tag — Good day / Hello (daytime)\n"
            "• Guten Abend — Good evening\n"
            "• Gute Nacht — Good night (before bed)\n"
            "• Tschüss — Bye (informal)\n"
            "• Auf Wiedersehen — Goodbye (formal)\n"
            "• Bis bald / Bis später — See you soon / later\n\n"
            "FORMAL vs INFORMAL — \"du\" and \"Sie\"\n"
            "German has two words for \"you\":\n"
            "• du — informal (friends, family)\n"
            "• Sie — formal (strangers, officials); always capitalized.\n"
            "\"How are you?\" → Wie geht es dir? (informal) · Wie geht es Ihnen? (formal) · Wie geht's? (casual)\n\n"
            "INTRODUCING YOURSELF\n"
            "• Ich heiße Anna. — My name is Anna. (heißen = to be called)\n"
            "• Ich bin Anna. — I am Anna.\n"
            "• Mein Name ist Anna. — My name is Anna.\n"
            "• Wie heißt du? / Wie heißen Sie? — What's your name?\n"
            "• Freut mich. — Nice to meet you.\n\n"
            "SHORT ANSWERS\n"
            "• Mir geht es gut. — I'm fine.   • Es geht. — So-so.   • Und dir? — And you?\n\n"
            "GRAMMAR FOCUS — sein & heißen (present tense)\n"
            "sein (to be): ich bin · du bist · er/sie ist · wir sind · ihr seid · sie/Sie sind\n"
            "heißen (to be called): ich heiße · du heißt · er/sie heißt · sie/Sie heißen\n"
            "Word order: the verb is in second position — \"Ich heiße Anna.\"\n"
            "In a question with a question word: question word + verb + subject — \"Wie heißt du?\"\n\n"
            "Tap Start and translate 40 short sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "Hello!", "de": "Hallo!"},
            {"en": "Good morning!", "de": "Guten Morgen!"},
            {"en": "Good day!", "de": "Guten Tag!"},
            {"en": "Good evening!", "de": "Guten Abend!"},
            {"en": "Good night!", "de": "Gute Nacht!"},
            {"en": "Bye!", "de": "Tschüss!"},
            {"en": "Goodbye!", "de": "Auf Wiedersehen!"},
            {"en": "See you soon!", "de": "Bis bald!"},
            {"en": "See you later!", "de": "Bis später!"},
            {"en": "Thank you!", "de": "Danke!"},
            {"en": "Yes, please.", "de": "Ja, bitte."},
            {"en": "No, thank you.", "de": "Nein, danke."},
            {"en": "How are you?", "de": "Wie geht es dir?"},
            {"en": "How are you? (formal)", "de": "Wie geht es Ihnen?"},
            {"en": "I am fine.", "de": "Mir geht es gut."},
            {"en": "Very well, thanks.", "de": "Sehr gut, danke."},
            {"en": "So-so.", "de": "Es geht."},
            {"en": "And you?", "de": "Und dir?"},
            {"en": "What is your name?", "de": "Wie heißt du?"},
            {"en": "What is your name? (formal)", "de": "Wie heißen Sie?"},
            {"en": "My name is Anna.", "de": "Ich heiße Anna."},
            {"en": "I am Thomas.", "de": "Ich bin Thomas."},
            {"en": "My name is Peter.", "de": "Mein Name ist Peter."},
            {"en": "Nice to meet you.", "de": "Freut mich."},
            {"en": "Welcome!", "de": "Willkommen!"},
            {"en": "Where are you from?", "de": "Woher kommst du?"},
            {"en": "I am from Berlin.", "de": "Ich komme aus Berlin."},
            {"en": "I am from Iran.", "de": "Ich komme aus dem Iran."},
            {"en": "Do you speak German?", "de": "Sprichst du Deutsch?"},
            {"en": "I speak a little German.", "de": "Ich spreche ein bisschen Deutsch."},
            {"en": "I don't understand.", "de": "Ich verstehe nicht."},
            {"en": "Please repeat that.", "de": "Wiederhole das bitte."},
            {"en": "How are you today?", "de": "Wie geht es dir heute?"},
            {"en": "I am very happy.", "de": "Ich bin sehr glücklich."},
            {"en": "Have a nice day!", "de": "Schönen Tag noch!"},
            {"en": "This is my friend Lena.", "de": "Das ist meine Freundin Lena."},
            {"en": "How old are you?", "de": "Wie alt bist du?"},
            {"en": "I am twenty years old.", "de": "Ich bin zwanzig Jahre alt."},
            {"en": "Where do you live?", "de": "Wo wohnst du?"},
            {"en": "It was nice to meet you.", "de": "Es war schön, dich kennenzulernen."},
        ],
    },

    ("A1", "holiday"): {
        "note": (
            "📖 Holiday — A1\n\n"
            "The present tense (Präsens) is used for now, habits and the near future. "
            "Most verbs are regular: take the stem and add the endings.\n\n"
            "REGULAR PRESENT ENDINGS (machen = to do/make)\n"
            "ich mache · du machst · er/sie/es macht · wir machen · ihr macht · sie/Sie machen\n\n"
            "USEFUL TRAVEL VERBS\n"
            "reisen (travel) · fliegen (fly) · fahren (go/drive) · besuchen (visit) · "
            "buchen (book) · packen (pack) · bleiben (stay) · schwimmen (swim)\n\n"
            "A few verbs change their stem vowel in du/er forms:\n"
            "fahren → du fährst, er fährt   ·   sehen → du siehst, er sieht\n\n"
            "WORD ORDER — verb in position 2\n"
            "Ich fahre im Sommer nach Italien.  ·  Im Sommer fahre ich nach Italien. (verb still 2nd)\n"
            "Question word + verb + subject: Wohin fährst du?\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I travel a lot.", "de": "Ich reise viel."},
            {"en": "We fly to Spain.", "de": "Wir fliegen nach Spanien."},
            {"en": "She books a hotel.", "de": "Sie bucht ein Hotel."},
            {"en": "I pack my suitcase.", "de": "Ich packe meinen Koffer."},
            {"en": "They visit Berlin.", "de": "Sie besuchen Berlin."},
            {"en": "He swims in the sea.", "de": "Er schwimmt im Meer."},
            {"en": "We stay for one week.", "de": "Wir bleiben eine Woche."},
            {"en": "I take many photos.", "de": "Ich mache viele Fotos."},
            {"en": "Where are you going?", "de": "Wohin fährst du?"},
            {"en": "I am going to Italy.", "de": "Ich fahre nach Italien."},
            {"en": "The holiday begins tomorrow.", "de": "Der Urlaub beginnt morgen."},
            {"en": "We travel by train.", "de": "Wir fahren mit dem Zug."},
            {"en": "She flies to Paris.", "de": "Sie fliegt nach Paris."},
            {"en": "Do you visit your family?", "de": "Besuchst du deine Familie?"},
            {"en": "I book a flight.", "de": "Ich buche einen Flug."},
            {"en": "The children swim every day.", "de": "Die Kinder schwimmen jeden Tag."},
            {"en": "We stay overnight at the hotel.", "de": "Wir übernachten im Hotel."},
            {"en": "In summer we travel to Greece.", "de": "Im Sommer reisen wir nach Griechenland."},
            {"en": "He visits a museum.", "de": "Er besucht ein Museum."},
            {"en": "I buy souvenirs.", "de": "Ich kaufe Souvenirs."},
            {"en": "When does the train leave?", "de": "Wann fährt der Zug?"},
            {"en": "We go to the beach.", "de": "Wir gehen an den Strand."},
            {"en": "She sends a postcard.", "de": "Sie schickt eine Postkarte."},
            {"en": "I drink coffee at the airport.", "de": "Ich trinke Kaffee am Flughafen."},
            {"en": "Do you fly often?", "de": "Fliegst du oft?"},
            {"en": "They book a tour.", "de": "Sie buchen eine Tour."},
            {"en": "We visit our grandparents.", "de": "Wir besuchen unsere Großeltern."},
            {"en": "The plane lands at six.", "de": "Das Flugzeug landet um sechs."},
            {"en": "I am looking for my passport.", "de": "Ich suche meinen Pass."},
            {"en": "He drives to the mountains.", "de": "Er fährt in die Berge."},
            {"en": "We spend two weeks in Spain.", "de": "Wir verbringen zwei Wochen in Spanien."},
            {"en": "She takes a lot of photos.", "de": "Sie macht viele Fotos."},
            {"en": "I always travel in summer.", "de": "Ich reise immer im Sommer."},
            {"en": "Do you stay at home?", "de": "Bleibst du zu Hause?"},
            {"en": "The hotel is very nice.", "de": "Das Hotel ist sehr schön."},
            {"en": "We fly home on Sunday.", "de": "Wir fliegen am Sonntag nach Hause."},
            {"en": "He visits a new country every year.", "de": "Er besucht jedes Jahr ein neues Land."},
            {"en": "I love the sea.", "de": "Ich liebe das Meer."},
            {"en": "Where do you spend your holidays?", "de": "Wo verbringst du deinen Urlaub?"},
            {"en": "In winter we go skiing in Austria.", "de": "Im Winter fahren wir in Österreich Ski."},
        ],
    },

    ("A1", "relationship"): {
        "note": (
            "📖 Relationship — A1\n\n"
            "PERSONAL PRONOUNS (subject form — nominative)\n"
            "ich (I) · du (you, informal) · er (he) · sie (she) · es (it)\n"
            "wir (we) · ihr (you, plural) · sie (they) · Sie (you, formal)\n\n"
            "THE VERB haben (to have) — irregular and very common\n"
            "ich habe · du hast · er/sie/es hat · wir haben · ihr habt · sie/Sie haben\n\n"
            "We use haben for family and possessions, and it takes the Akkusativ "
            "(einen/eine/ein):\n"
            "Ich habe einen Bruder.  ·  Sie hat eine große Familie.\n\n"
            "FAMILY VOCAB\n"
            "die Mutter, der Vater, die Eltern, die Schwester, der Bruder, die Tochter, der Sohn, "
            "die Großmutter (Oma), der Großvater (Opa), der Mann, die Frau, das Kind, "
            "der Freund / die Freundin.\n\n"
            "Remember: the verb stays in position 2.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I have a sister.", "de": "Ich habe eine Schwester."},
            {"en": "He has two brothers.", "de": "Er hat zwei Brüder."},
            {"en": "We have a big family.", "de": "Wir haben eine große Familie."},
            {"en": "She has a daughter and a son.", "de": "Sie hat eine Tochter und einen Sohn."},
            {"en": "Do you have children?", "de": "Hast du Kinder?"},
            {"en": "They have a dog.", "de": "Sie haben einen Hund."},
            {"en": "My mother is very nice.", "de": "Meine Mutter ist sehr nett."},
            {"en": "My father is a teacher.", "de": "Mein Vater ist Lehrer."},
            {"en": "I have a brother.", "de": "Ich habe einen Bruder."},
            {"en": "My sister is twelve years old.", "de": "Meine Schwester ist zwölf Jahre alt."},
            {"en": "We have grandparents in Italy.", "de": "Wir haben Großeltern in Italien."},
            {"en": "He has a wife and two children.", "de": "Er hat eine Frau und zwei Kinder."},
            {"en": "Do you have a sister?", "de": "Hast du eine Schwester?"},
            {"en": "She is my friend.", "de": "Sie ist meine Freundin."},
            {"en": "My parents live in Berlin.", "de": "Meine Eltern wohnen in Berlin."},
            {"en": "I love my family.", "de": "Ich liebe meine Familie."},
            {"en": "He has many friends.", "de": "Er hat viele Freunde."},
            {"en": "My grandmother is eighty.", "de": "Meine Großmutter ist achtzig."},
            {"en": "We have a small house.", "de": "Wir haben ein kleines Haus."},
            {"en": "Do you have a brother or a sister?", "de": "Hast du einen Bruder oder eine Schwester?"},
            {"en": "My uncle lives in Austria.", "de": "Mein Onkel wohnt in Österreich."},
            {"en": "She has a cat.", "de": "Sie hat eine Katze."},
            {"en": "My name is Sara and I have one child.", "de": "Ich heiße Sara und ich habe ein Kind."},
            {"en": "They are my cousins.", "de": "Sie sind meine Cousins."},
            {"en": "My brother is married.", "de": "Mein Bruder ist verheiratet."},
            {"en": "I have no children.", "de": "Ich habe keine Kinder."},
            {"en": "Her husband is from Spain.", "de": "Ihr Mann kommt aus Spanien."},
            {"en": "We have a big garden.", "de": "Wir haben einen großen Garten."},
            {"en": "My aunt is very funny.", "de": "Meine Tante ist sehr lustig."},
            {"en": "Do you have a pet?", "de": "Hast du ein Haustier?"},
            {"en": "My son goes to school.", "de": "Mein Sohn geht zur Schule."},
            {"en": "I have two sisters and one brother.", "de": "Ich habe zwei Schwestern und einen Bruder."},
            {"en": "His sister is a doctor.", "de": "Seine Schwester ist Ärztin."},
            {"en": "We often visit our grandparents.", "de": "Wir besuchen oft unsere Großeltern."},
            {"en": "My daughter likes animals.", "de": "Meine Tochter mag Tiere."},
            {"en": "Are you married?", "de": "Bist du verheiratet?"},
            {"en": "My family is very important.", "de": "Meine Familie ist sehr wichtig."},
            {"en": "He has a little brother.", "de": "Er hat einen kleinen Bruder."},
            {"en": "My grandparents have a farm.", "de": "Meine Großeltern haben einen Bauernhof."},
            {"en": "I live with my family.", "de": "Ich wohne bei meiner Familie."},
        ],
    },

    ("A1", "technology"): {
        "note": (
            "📖 Technology — A1\n\n"
            "Every German noun has a gender: masculine (der), feminine (die) or neuter (das). "
            "Always learn the article with the noun.\n\n"
            "DEFINITE ARTICLE (the) — nominative\n"
            "der (m): der Computer, der Drucker · die (f): die Maus, die Kamera · "
            "das (n): das Handy, das Internet\n"
            "Plural is always die: die Computer, die Handys.\n\n"
            "INDEFINITE ARTICLE (a/an)\n"
            "ein (m/n): ein Computer, ein Handy · eine (f): eine Maus, eine Kamera\n"
            "Negative: kein/keine — Das ist kein Drucker.\n\n"
            "NOMINATIVE = the subject (who/what does the action):\n"
            "Der Computer ist neu.  ·  Das ist ein Handy.\n\n"
            "TECH VOCAB\n"
            "der Computer, der Bildschirm, der Drucker, der Akku, das Handy, das Laptop, das Tablet, "
            "das Internet, das Passwort, die Tastatur, die Maus, die App, die E-Mail, die Kamera.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "The computer is new.", "de": "Der Computer ist neu."},
            {"en": "That is a mobile phone.", "de": "Das ist ein Handy."},
            {"en": "The screen is big.", "de": "Der Bildschirm ist groß."},
            {"en": "I have a tablet.", "de": "Ich habe ein Tablet."},
            {"en": "The mouse is small.", "de": "Die Maus ist klein."},
            {"en": "Is that a printer?", "de": "Ist das ein Drucker?"},
            {"en": "No, that is not a printer.", "de": "Nein, das ist kein Drucker."},
            {"en": "The phone is expensive.", "de": "Das Handy ist teuer."},
            {"en": "My computer is slow.", "de": "Mein Computer ist langsam."},
            {"en": "The internet is fast.", "de": "Das Internet ist schnell."},
            {"en": "I need a password.", "de": "Ich brauche ein Passwort."},
            {"en": "The camera takes good photos.", "de": "Die Kamera macht gute Fotos."},
            {"en": "Where is the keyboard?", "de": "Wo ist die Tastatur?"},
            {"en": "The app is free.", "de": "Die App ist kostenlos."},
            {"en": "I write an email.", "de": "Ich schreibe eine E-Mail."},
            {"en": "The battery is empty.", "de": "Der Akku ist leer."},
            {"en": "This is my new phone.", "de": "Das ist mein neues Handy."},
            {"en": "The laptop does not work.", "de": "Das Laptop funktioniert nicht."},
            {"en": "Do you have a charger?", "de": "Hast du ein Ladegerät?"},
            {"en": "The screen is broken.", "de": "Der Bildschirm ist kaputt."},
            {"en": "I install an app.", "de": "Ich installiere eine App."},
            {"en": "The printer is old.", "de": "Der Drucker ist alt."},
            {"en": "My password is secret.", "de": "Mein Passwort ist geheim."},
            {"en": "The mobile phone is on the table.", "de": "Das Handy ist auf dem Tisch."},
            {"en": "I have no internet.", "de": "Ich habe kein Internet."},
            {"en": "The computer is in the office.", "de": "Der Computer ist im Büro."},
            {"en": "Is the wifi free?", "de": "Ist das WLAN kostenlos?"},
            {"en": "The camera is very good.", "de": "Die Kamera ist sehr gut."},
            {"en": "I need a new charger.", "de": "Ich brauche ein neues Ladegerät."},
            {"en": "The smartphone is modern.", "de": "Das Smartphone ist modern."},
            {"en": "Where is my phone?", "de": "Wo ist mein Handy?"},
            {"en": "The keyboard is dirty.", "de": "Die Tastatur ist schmutzig."},
            {"en": "The app is very useful.", "de": "Die App ist sehr nützlich."},
            {"en": "The screen is too small.", "de": "Der Bildschirm ist zu klein."},
            {"en": "I buy a new computer.", "de": "Ich kaufe einen neuen Computer."},
            {"en": "The email is important.", "de": "Die E-Mail ist wichtig."},
            {"en": "My laptop is fast.", "de": "Mein Laptop ist schnell."},
            {"en": "That is not my phone.", "de": "Das ist nicht mein Handy."},
            {"en": "The photos are beautiful.", "de": "Die Fotos sind schön."},
            {"en": "Technology is very important today.", "de": "Technik ist heute sehr wichtig."},
        ],
    },

    ("A1", "sports"): {
        "note": (
            "📖 Sports — A1\n\n"
            "THE ACCUSATIVE CASE (Akkusativ) — the direct object (what receives the action).\n"
            "Only the MASCULINE article changes; die / das / plural stay the same.\n"
            "  der → den    ·    ein → einen\n"
            "  die → die     ·    eine → eine\n"
            "  das → das     ·    ein → ein\n\n"
            "• Wir gewinnen das Spiel.  ·  Ich kaufe einen Ball.\n"
            "• Most sports/games take NO article: Ich spiele Fußball. · Ich mache Sport.\n\n"
            "USEFUL VERBS\n"
            "spielen (play) · machen (do) · trainieren (train) · laufen (run) · "
            "gewinnen (win) · verlieren (lose) · schwimmen (swim)\n\n"
            "VOCAB: der Fußball, der Ball, der Sport, das Spiel, die Mannschaft (team), "
            "das Schwimmbad, das Stadion, das Tor (goal), der Trainer, der Spieler.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I play football.", "de": "Ich spiele Fußball."},
            {"en": "We play tennis.", "de": "Wir spielen Tennis."},
            {"en": "He plays basketball.", "de": "Er spielt Basketball."},
            {"en": "I do sport every day.", "de": "Ich mache jeden Tag Sport."},
            {"en": "She swims very fast.", "de": "Sie schwimmt sehr schnell."},
            {"en": "They train on Mondays.", "de": "Sie trainieren montags."},
            {"en": "I buy a ball.", "de": "Ich kaufe einen Ball."},
            {"en": "We win the game.", "de": "Wir gewinnen das Spiel."},
            {"en": "The team is very good.", "de": "Die Mannschaft ist sehr gut."},
            {"en": "I run in the park.", "de": "Ich laufe im Park."},
            {"en": "Do you play tennis?", "de": "Spielst du Tennis?"},
            {"en": "He has a new trainer.", "de": "Er hat einen neuen Trainer."},
            {"en": "We lose the game.", "de": "Wir verlieren das Spiel."},
            {"en": "I need new shoes.", "de": "Ich brauche neue Schuhe."},
            {"en": "She plays volleyball.", "de": "Sie spielt Volleyball."},
            {"en": "The match starts at three.", "de": "Das Spiel beginnt um drei."},
            {"en": "I watch the game.", "de": "Ich sehe das Spiel."},
            {"en": "We go to the stadium.", "de": "Wir gehen ins Stadion."},
            {"en": "He scores a goal.", "de": "Er schießt ein Tor."},
            {"en": "My brother plays handball.", "de": "Mein Bruder spielt Handball."},
            {"en": "I like sport.", "de": "Ich mag Sport."},
            {"en": "The pool is closed today.", "de": "Das Schwimmbad ist heute geschlossen."},
            {"en": "We train hard.", "de": "Wir trainieren hart."},
            {"en": "She wins the race.", "de": "Sie gewinnt das Rennen."},
            {"en": "Do you do yoga?", "de": "Machst du Yoga?"},
            {"en": "I play football with my friends.", "de": "Ich spiele Fußball mit meinen Freunden."},
            {"en": "The team has a good trainer.", "de": "Die Mannschaft hat einen guten Trainer."},
            {"en": "He runs ten kilometers.", "de": "Er läuft zehn Kilometer."},
            {"en": "We play a game.", "de": "Wir spielen ein Spiel."},
            {"en": "I take my ball.", "de": "Ich nehme meinen Ball."},
            {"en": "They have a big stadium.", "de": "Sie haben ein großes Stadion."},
            {"en": "She trains every evening.", "de": "Sie trainiert jeden Abend."},
            {"en": "I love football.", "de": "Ich liebe Fußball."},
            {"en": "Our team wins often.", "de": "Unsere Mannschaft gewinnt oft."},
            {"en": "He is a good player.", "de": "Er ist ein guter Spieler."},
            {"en": "I play tennis on Sundays.", "de": "Ich spiele sonntags Tennis."},
            {"en": "We need a new ball.", "de": "Wir brauchen einen neuen Ball."},
            {"en": "The game is very exciting.", "de": "Das Spiel ist sehr spannend."},
            {"en": "Do you watch football?", "de": "Schaust du Fußball?"},
            {"en": "Sport keeps me healthy.", "de": "Sport hält mich gesund."},
        ],
    },

    ("A1", "food"): {
        "note": (
            "📖 Food — A1\n\n"
            "Talking about food uses the Akkusativ (the thing you eat / buy / want). "
            "Only masculine changes: der→den, ein→einen.\n\n"
            "KEY VERBS\n"
            "essen: ich esse, du isst, er isst · trinken: ich trinke, du trinkst\n"
            "nehmen: ich nehme, du nimmst, er nimmt · "
            "möchten (would like): ich möchte, du möchtest · mögen (like): ich mag, du magst\n\n"
            "• Ich esse einen Apfel.  ·  Ich trinke einen Kaffee.\n"
            "• Ich möchte ein Wasser, bitte.  ·  Ich mag Schokolade.\n"
            "With möchten, the main verb goes to the end: Ich möchte einen Tee trinken.\n\n"
            "VOCAB: das Brot, der Apfel, der Käse, das Ei, der Reis, die Suppe, das Fleisch, "
            "der Fisch, das Wasser, der Kaffee, der Tee, der Saft, die Milch, das Gemüse, das Obst.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I eat an apple.", "de": "Ich esse einen Apfel."},
            {"en": "I drink water.", "de": "Ich trinke Wasser."},
            {"en": "She eats bread.", "de": "Sie isst Brot."},
            {"en": "We drink coffee.", "de": "Wir trinken Kaffee."},
            {"en": "I would like a tea.", "de": "Ich möchte einen Tee."},
            {"en": "He eats fish.", "de": "Er isst Fisch."},
            {"en": "I like cheese.", "de": "Ich mag Käse."},
            {"en": "Do you eat meat?", "de": "Isst du Fleisch?"},
            {"en": "I would like a water, please.", "de": "Ich möchte ein Wasser, bitte."},
            {"en": "We eat rice.", "de": "Wir essen Reis."},
            {"en": "She drinks milk.", "de": "Sie trinkt Milch."},
            {"en": "I take a coffee.", "de": "Ich nehme einen Kaffee."},
            {"en": "The soup is hot.", "de": "Die Suppe ist heiß."},
            {"en": "Do you like chocolate?", "de": "Magst du Schokolade?"},
            {"en": "I eat vegetables every day.", "de": "Ich esse jeden Tag Gemüse."},
            {"en": "He drinks a juice.", "de": "Er trinkt einen Saft."},
            {"en": "I would like an apple.", "de": "Ich möchte einen Apfel."},
            {"en": "We buy bread and cheese.", "de": "Wir kaufen Brot und Käse."},
            {"en": "She doesn't eat meat.", "de": "Sie isst kein Fleisch."},
            {"en": "I am hungry.", "de": "Ich habe Hunger."},
            {"en": "I am thirsty.", "de": "Ich habe Durst."},
            {"en": "The bread is fresh.", "de": "Das Brot ist frisch."},
            {"en": "Do you want a tea or a coffee?", "de": "Möchtest du einen Tee oder einen Kaffee?"},
            {"en": "I eat an egg in the morning.", "de": "Ich esse morgens ein Ei."},
            {"en": "We like fruit.", "de": "Wir mögen Obst."},
            {"en": "He takes the fish.", "de": "Er nimmt den Fisch."},
            {"en": "The coffee is too hot.", "de": "Der Kaffee ist zu heiß."},
            {"en": "I would like to drink a water.", "de": "Ich möchte ein Wasser trinken."},
            {"en": "She eats a lot of vegetables.", "de": "Sie isst viel Gemüse."},
            {"en": "We cook a soup.", "de": "Wir kochen eine Suppe."},
            {"en": "Do you like fish?", "de": "Magst du Fisch?"},
            {"en": "I drink tea without sugar.", "de": "Ich trinke Tee ohne Zucker."},
            {"en": "The meal is delicious.", "de": "Das Essen ist lecker."},
            {"en": "I buy fruit at the market.", "de": "Ich kaufe Obst auf dem Markt."},
            {"en": "He eats too much chocolate.", "de": "Er isst zu viel Schokolade."},
            {"en": "We would like the menu, please.", "de": "Wir möchten die Speisekarte, bitte."},
            {"en": "I don't drink coffee.", "de": "Ich trinke keinen Kaffee."},
            {"en": "She likes apples and bananas.", "de": "Sie mag Äpfel und Bananen."},
            {"en": "The restaurant is very good.", "de": "Das Restaurant ist sehr gut."},
            {"en": "I would like to order a pizza.", "de": "Ich möchte eine Pizza bestellen."},
        ],
    },

    ("A1", "education"): {
        "note": (
            "📖 Education — A1\n\n"
            "MODAL VERB können (can / to be able to).\n"
            "A modal needs a second verb in the INFINITIVE, which goes to the END.\n"
            "ich kann · du kannst · er/sie kann · wir können · ihr könnt · sie/Sie können\n\n"
            "• Ich kann Deutsch sprechen.  → I can speak German.\n"
            "• Kannst du mir helfen?  → Can you help me?\n"
            "The modal is in position 2; the main verb is last.\n\n"
            "VOCAB: die Schule, die Universität, der Lehrer/die Lehrerin, der Schüler, "
            "der Student, das Fach (subject), die Prüfung (exam), die Hausaufgaben (homework), "
            "lernen, verstehen, lesen, schreiben.\n"
            "SUBJECTS: Mathe, Deutsch, Englisch, Biologie, Geschichte, Kunst, Sport, Musik.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I can speak German.", "de": "Ich kann Deutsch sprechen."},
            {"en": "Can you help me?", "de": "Kannst du mir helfen?"},
            {"en": "She can read well.", "de": "Sie kann gut lesen."},
            {"en": "We learn English at school.", "de": "Wir lernen Englisch in der Schule."},
            {"en": "He can write fast.", "de": "Er kann schnell schreiben."},
            {"en": "I study every evening.", "de": "Ich lerne jeden Abend."},
            {"en": "Can you understand me?", "de": "Kannst du mich verstehen?"},
            {"en": "The teacher is very nice.", "de": "Der Lehrer ist sehr nett."},
            {"en": "I have homework today.", "de": "Ich habe heute Hausaufgaben."},
            {"en": "We can ask a question.", "de": "Wir können eine Frage stellen."},
            {"en": "She studies at the university.", "de": "Sie studiert an der Universität."},
            {"en": "Can I open the window?", "de": "Kann ich das Fenster öffnen?"},
            {"en": "My favorite subject is math.", "de": "Mein Lieblingsfach ist Mathe."},
            {"en": "The exam is on Monday.", "de": "Die Prüfung ist am Montag."},
            {"en": "He cannot come today.", "de": "Er kann heute nicht kommen."},
            {"en": "I want to learn German.", "de": "Ich möchte Deutsch lernen."},
            {"en": "Can you repeat that, please?", "de": "Kannst du das bitte wiederholen?"},
            {"en": "We read a book in class.", "de": "Wir lesen ein Buch im Unterricht."},
            {"en": "She can speak three languages.", "de": "Sie kann drei Sprachen sprechen."},
            {"en": "The students are in the classroom.", "de": "Die Schüler sind im Klassenzimmer."},
            {"en": "I don't understand the question.", "de": "Ich verstehe die Frage nicht."},
            {"en": "Can we work together?", "de": "Können wir zusammenarbeiten?"},
            {"en": "He learns very quickly.", "de": "Er lernt sehr schnell."},
            {"en": "I write the answer.", "de": "Ich schreibe die Antwort."},
            {"en": "Can you explain that?", "de": "Kannst du das erklären?"},
            {"en": "The lesson begins at eight.", "de": "Der Unterricht beginnt um acht."},
            {"en": "I have an exam tomorrow.", "de": "Ich habe morgen eine Prüfung."},
            {"en": "She can help you.", "de": "Sie kann dir helfen."},
            {"en": "We learn a lot.", "de": "Wir lernen viel."},
            {"en": "Can I ask something?", "de": "Kann ich etwas fragen?"},
            {"en": "My teacher speaks English.", "de": "Mein Lehrer spricht Englisch."},
            {"en": "He does his homework.", "de": "Er macht seine Hausaufgaben."},
            {"en": "I cannot find my book.", "de": "Ich kann mein Buch nicht finden."},
            {"en": "Can you read this word?", "de": "Kannst du dieses Wort lesen?"},
            {"en": "The university is very big.", "de": "Die Universität ist sehr groß."},
            {"en": "We study together.", "de": "Wir lernen zusammen."},
            {"en": "She wants to become a teacher.", "de": "Sie möchte Lehrerin werden."},
            {"en": "I can answer the question.", "de": "Ich kann die Frage beantworten."},
            {"en": "The book is very interesting.", "de": "Das Buch ist sehr interessant."},
            {"en": "Education is very important.", "de": "Bildung ist sehr wichtig."},
        ],
    },

    ("A1", "work"): {
        "note": (
            "📖 Work — A1\n\n"
            "MORE MODAL VERBS (second verb → infinitive at the end).\n"
            "müssen (must / have to): ich muss · du musst · er muss · wir müssen · ihr müsst · sie müssen\n"
            "wollen (want to): ich will · du willst · er will · wir wollen · ihr wollt · sie wollen\n\n"
            "• Ich muss um acht arbeiten.  ·  Ich will Geld verdienen.\n\n"
            "TELLING THE TIME\n"
            "Wie spät ist es? — What time is it? · Es ist acht Uhr. · um neun Uhr · halb zehn (9:30).\n\n"
            "VOCAB: die Arbeit, der Job, der Beruf, das Büro, der Chef, der Kollege, die Firma, "
            "arbeiten, verdienen (earn), pünktlich (on time).\n"
            "JOBS: der Arzt/die Ärztin, der Lehrer, der Ingenieur, die Verkäuferin, der Koch.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I work in an office.", "de": "Ich arbeite in einem Büro."},
            {"en": "She is a doctor.", "de": "Sie ist Ärztin."},
            {"en": "I have to work today.", "de": "Ich muss heute arbeiten."},
            {"en": "He wants to earn money.", "de": "Er will Geld verdienen."},
            {"en": "What time is it?", "de": "Wie spät ist es?"},
            {"en": "It is eight o'clock.", "de": "Es ist acht Uhr."},
            {"en": "I start at nine.", "de": "Ich beginne um neun."},
            {"en": "My boss is very nice.", "de": "Mein Chef ist sehr nett."},
            {"en": "We have to work a lot.", "de": "Wir müssen viel arbeiten."},
            {"en": "She wants to be a teacher.", "de": "Sie will Lehrerin werden."},
            {"en": "I work from nine to five.", "de": "Ich arbeite von neun bis fünf."},
            {"en": "He works in a factory.", "de": "Er arbeitet in einer Fabrik."},
            {"en": "Do you have to work tomorrow?", "de": "Musst du morgen arbeiten?"},
            {"en": "I want to find a new job.", "de": "Ich will einen neuen Job finden."},
            {"en": "My colleague is friendly.", "de": "Mein Kollege ist freundlich."},
            {"en": "The meeting starts at ten.", "de": "Das Meeting beginnt um zehn."},
            {"en": "I must call the boss.", "de": "Ich muss den Chef anrufen."},
            {"en": "She works as a nurse.", "de": "Sie arbeitet als Krankenschwester."},
            {"en": "We want to work together.", "de": "Wir wollen zusammenarbeiten."},
            {"en": "I have to go now.", "de": "Ich muss jetzt gehen."},
            {"en": "He earns a lot of money.", "de": "Er verdient viel Geld."},
            {"en": "My job is very interesting.", "de": "Mein Job ist sehr interessant."},
            {"en": "I work every day.", "de": "Ich arbeite jeden Tag."},
            {"en": "She has to write an email.", "de": "Sie muss eine E-Mail schreiben."},
            {"en": "What is your job?", "de": "Was bist du von Beruf?"},
            {"en": "I am an engineer.", "de": "Ich bin Ingenieur."},
            {"en": "We want to start a company.", "de": "Wir wollen eine Firma gründen."},
            {"en": "The office is in the city.", "de": "Das Büro ist in der Stadt."},
            {"en": "He has to work on Saturday.", "de": "Er muss am Samstag arbeiten."},
            {"en": "I want to learn a lot.", "de": "Ich will viel lernen."},
            {"en": "My salary is good.", "de": "Mein Gehalt ist gut."},
            {"en": "She works at a bank.", "de": "Sie arbeitet bei einer Bank."},
            {"en": "I have to be on time.", "de": "Ich muss pünktlich sein."},
            {"en": "Do you want to work here?", "de": "Willst du hier arbeiten?"},
            {"en": "He is a good cook.", "de": "Er ist ein guter Koch."},
            {"en": "We are done at six.", "de": "Wir sind um sechs fertig."},
            {"en": "I want to help my colleagues.", "de": "Ich will meinen Kollegen helfen."},
            {"en": "The work is very hard.", "de": "Die Arbeit ist sehr schwer."},
            {"en": "She must learn German for her job.", "de": "Sie muss für ihren Job Deutsch lernen."},
            {"en": "I want to be successful.", "de": "Ich will erfolgreich sein."},
        ],
    },

    ("A1", "health"): {
        "note": (
            "📖 Health — A1\n\n"
            "TWO WAYS TO SAY \"NO / NOT\"\n"
            "1) kein/keine — negates a NOUN (replaces ein/eine or no article):\n"
            "   Ich habe Zeit. → Ich habe keine Zeit.   ·   Ich trinke keinen Alkohol.\n"
            "2) nicht — negates a verb, adjective or the whole sentence:\n"
            "   Ich komme nicht.   ·   Das ist nicht gut.   ·   Ich bin nicht müde.\n"
            "Rule: kein with nouns, nicht for everything else.\n\n"
            "FEELING / HEALTH\n"
            "Ich bin krank / gesund / müde.   ·   Ich habe Kopfschmerzen.\n"
            "Mir tut der Kopf weh. (My head hurts.)   ·   Ich brauche einen Arzt.\n\n"
            "VOCAB: der Kopf, der Bauch, der Hals, der Arm, das Bein, der Rücken, der Zahn, "
            "krank, gesund, müde, der Arzt, die Apotheke, die Medizin.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I am tired.", "de": "Ich bin müde."},
            {"en": "I am not tired.", "de": "Ich bin nicht müde."},
            {"en": "He is ill.", "de": "Er ist krank."},
            {"en": "She is healthy.", "de": "Sie ist gesund."},
            {"en": "I have a headache.", "de": "Ich habe Kopfschmerzen."},
            {"en": "I have no time.", "de": "Ich habe keine Zeit."},
            {"en": "I don't drink alcohol.", "de": "Ich trinke keinen Alkohol."},
            {"en": "My head hurts.", "de": "Mir tut der Kopf weh."},
            {"en": "I need a doctor.", "de": "Ich brauche einen Arzt."},
            {"en": "He is not here.", "de": "Er ist nicht hier."},
            {"en": "I am not hungry.", "de": "Ich habe keinen Hunger."},
            {"en": "My stomach hurts.", "de": "Mir tut der Bauch weh."},
            {"en": "She has a cold.", "de": "Sie hat eine Erkältung."},
            {"en": "I do not feel well.", "de": "Ich fühle mich nicht gut."},
            {"en": "The medicine is in the bag.", "de": "Die Medizin ist in der Tasche."},
            {"en": "I have no money for the doctor.", "de": "Ich habe kein Geld für den Arzt."},
            {"en": "My back hurts.", "de": "Mir tut der Rücken weh."},
            {"en": "He cannot sleep.", "de": "Er kann nicht schlafen."},
            {"en": "I am not sick.", "de": "Ich bin nicht krank."},
            {"en": "Where is the pharmacy?", "de": "Wo ist die Apotheke?"},
            {"en": "I have a sore throat.", "de": "Ich habe Halsschmerzen."},
            {"en": "She doesn't have a fever.", "de": "Sie hat kein Fieber."},
            {"en": "I drink a lot of water.", "de": "Ich trinke viel Wasser."},
            {"en": "My tooth hurts.", "de": "Mir tut der Zahn weh."},
            {"en": "He is very healthy.", "de": "Er ist sehr gesund."},
            {"en": "I am not afraid.", "de": "Ich habe keine Angst."},
            {"en": "The doctor is not here today.", "de": "Der Arzt ist heute nicht hier."},
            {"en": "I need medicine.", "de": "Ich brauche Medizin."},
            {"en": "She is feeling better.", "de": "Es geht ihr besser."},
            {"en": "My leg hurts.", "de": "Mir tut das Bein weh."},
            {"en": "I do not smoke.", "de": "Ich rauche nicht."},
            {"en": "He has no appetite.", "de": "Er hat keinen Appetit."},
            {"en": "I sleep eight hours.", "de": "Ich schlafe acht Stunden."},
            {"en": "Are you ill?", "de": "Bist du krank?"},
            {"en": "I am not well today.", "de": "Mir geht es heute nicht gut."},
            {"en": "She takes the medicine.", "de": "Sie nimmt die Medizin."},
            {"en": "My arm hurts.", "de": "Mir tut der Arm weh."},
            {"en": "I have no pain.", "de": "Ich habe keine Schmerzen."},
            {"en": "He goes to the doctor.", "de": "Er geht zum Arzt."},
            {"en": "Health is the most important thing.", "de": "Gesundheit ist das Wichtigste."},
        ],
    },

    ("A1", "books_films"): {
        "note": (
            "📖 Books and Films — A1\n\n"
            "NOUN PLURALS — irregular, learn them with the noun. Common patterns:\n"
            "• -e (often + umlaut): der Film → die Filme, das Buch → die Bücher\n"
            "• -n/-en: die Geschichte → die Geschichten\n"
            "• -er: das Kind → die Kinder\n"
            "• -s: das Auto → die Autos, das Kino → die Kinos\n"
            "• no change: der Computer → die Computer\n"
            "The plural article is always die.\n\n"
            "SAYING WHAT YOU LIKE — gern (after the verb)\n"
            "Ich lese gern. (I like reading.)  ·  Ich sehe gern Filme.  ·  "
            "Ich spiele nicht gern Karten.\n"
            "lieber = prefer: Ich lese lieber Bücher.\n\n"
            "VOCAB: das Buch/die Bücher, der Film/die Filme, das Kino, die Geschichte, "
            "der Autor, die Serie, lesen, sehen, langweilig, spannend, lustig, traurig.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I like reading.", "de": "Ich lese gern."},
            {"en": "I read a book.", "de": "Ich lese ein Buch."},
            {"en": "I have many books.", "de": "Ich habe viele Bücher."},
            {"en": "We watch a film.", "de": "Wir sehen einen Film."},
            {"en": "I like watching films.", "de": "Ich sehe gern Filme."},
            {"en": "The film is exciting.", "de": "Der Film ist spannend."},
            {"en": "She reads two books a week.", "de": "Sie liest zwei Bücher pro Woche."},
            {"en": "The book is boring.", "de": "Das Buch ist langweilig."},
            {"en": "We go to the cinema.", "de": "Wir gehen ins Kino."},
            {"en": "I don't like horror films.", "de": "Ich sehe nicht gern Horrorfilme."},
            {"en": "He reads a newspaper.", "de": "Er liest eine Zeitung."},
            {"en": "The films are very long.", "de": "Die Filme sind sehr lang."},
            {"en": "I prefer comedies.", "de": "Ich mag lieber Komödien."},
            {"en": "This story is funny.", "de": "Diese Geschichte ist lustig."},
            {"en": "Do you like reading?", "de": "Liest du gern?"},
            {"en": "The children watch a cartoon.", "de": "Die Kinder sehen einen Zeichentrickfilm."},
            {"en": "I read every evening.", "de": "Ich lese jeden Abend."},
            {"en": "She likes romantic films.", "de": "Sie sieht gern Liebesfilme."},
            {"en": "The author is famous.", "de": "Der Autor ist berühmt."},
            {"en": "We watch a series.", "de": "Wir sehen eine Serie."},
            {"en": "I have no time to read.", "de": "Ich habe keine Zeit zum Lesen."},
            {"en": "The cinema is new.", "de": "Das Kino ist neu."},
            {"en": "He reads science fiction.", "de": "Er liest Science-Fiction."},
            {"en": "The book is very interesting.", "de": "Das Buch ist sehr interessant."},
            {"en": "I watch films in German.", "de": "Ich sehe Filme auf Deutsch."},
            {"en": "She tells a story.", "de": "Sie erzählt eine Geschichte."},
            {"en": "We like the same films.", "de": "Wir mögen die gleichen Filme."},
            {"en": "The story is sad.", "de": "Die Geschichte ist traurig."},
            {"en": "I buy two tickets.", "de": "Ich kaufe zwei Karten."},
            {"en": "The film starts at eight.", "de": "Der Film beginnt um acht."},
            {"en": "He doesn't read much.", "de": "Er liest nicht viel."},
            {"en": "I love good books.", "de": "Ich liebe gute Bücher."},
            {"en": "The series has many episodes.", "de": "Die Serie hat viele Folgen."},
            {"en": "Do you watch films often?", "de": "Siehst du oft Filme?"},
            {"en": "I read the book twice.", "de": "Ich lese das Buch zweimal."},
            {"en": "My sister likes comics.", "de": "Meine Schwester mag Comics."},
            {"en": "The actor is very good.", "de": "Der Schauspieler ist sehr gut."},
            {"en": "We watch a film together.", "de": "Wir sehen zusammen einen Film."},
            {"en": "I prefer reading.", "de": "Ich lese lieber."},
            {"en": "Books are my hobby.", "de": "Bücher sind mein Hobby."},
        ],
    },

    ("A1", "accommodation"): {
        "note": (
            "📖 Accommodation — A1\n\n"
            "WHERE THINGS ARE — prepositions + Dativ (location, with \"wo?\")\n"
            "in, an (at/on a wall), auf (on top), unter (under), neben (next to), "
            "vor (in front of), hinter (behind), zwischen (between), über (above).\n"
            "Dativ articles: der/das → dem, die → der, plural → den (+n).\n"
            "Contractions: in dem → im, an dem → am.\n"
            "• Das Buch ist auf dem Tisch.  ·  Die Lampe ist neben dem Bett.  ·  Ich bin im Wohnzimmer.\n\n"
            "es gibt = there is / there are (+ Akkusativ):\n"
            "• Es gibt einen Balkon.  ·  Es gibt zwei Schlafzimmer.\n\n"
            "VOCAB: die Wohnung, das Haus, das Zimmer, die Küche, das Bad, das Wohnzimmer, "
            "das Schlafzimmer, der Tisch, der Stuhl, das Bett, das Sofa, der Schrank, die Lampe.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "The book is on the table.", "de": "Das Buch ist auf dem Tisch."},
            {"en": "I am in the kitchen.", "de": "Ich bin in der Küche."},
            {"en": "The lamp is next to the bed.", "de": "Die Lampe ist neben dem Bett."},
            {"en": "We live in a flat.", "de": "Wir wohnen in einer Wohnung."},
            {"en": "There is a balcony.", "de": "Es gibt einen Balkon."},
            {"en": "The chair is in front of the table.", "de": "Der Stuhl ist vor dem Tisch."},
            {"en": "My room is very small.", "de": "Mein Zimmer ist sehr klein."},
            {"en": "The cat is under the sofa.", "de": "Die Katze ist unter dem Sofa."},
            {"en": "There are two bedrooms.", "de": "Es gibt zwei Schlafzimmer."},
            {"en": "The kitchen is big.", "de": "Die Küche ist groß."},
            {"en": "The picture is on the wall.", "de": "Das Bild ist an der Wand."},
            {"en": "I sit on the sofa.", "de": "Ich sitze auf dem Sofa."},
            {"en": "The bathroom is next to the bedroom.", "de": "Das Bad ist neben dem Schlafzimmer."},
            {"en": "We have a garden.", "de": "Wir haben einen Garten."},
            {"en": "The keys are on the table.", "de": "Die Schlüssel sind auf dem Tisch."},
            {"en": "There is no elevator.", "de": "Es gibt keinen Aufzug."},
            {"en": "The flat is on the third floor.", "de": "Die Wohnung ist im dritten Stock."},
            {"en": "My bed is by the window.", "de": "Mein Bett ist am Fenster."},
            {"en": "The wardrobe is in the bedroom.", "de": "Der Schrank ist im Schlafzimmer."},
            {"en": "We are in the living room.", "de": "Wir sind im Wohnzimmer."},
            {"en": "The car is in front of the house.", "de": "Das Auto ist vor dem Haus."},
            {"en": "There is a big kitchen.", "de": "Es gibt eine große Küche."},
            {"en": "The dog sleeps under the table.", "de": "Der Hund schläft unter dem Tisch."},
            {"en": "My flat has three rooms.", "de": "Meine Wohnung hat drei Zimmer."},
            {"en": "The lamp is over the table.", "de": "Die Lampe ist über dem Tisch."},
            {"en": "The bag is behind the door.", "de": "Die Tasche ist hinter der Tür."},
            {"en": "We need a new sofa.", "de": "Wir brauchen ein neues Sofa."},
            {"en": "The kitchen is between the rooms.", "de": "Die Küche ist zwischen den Zimmern."},
            {"en": "There is a small bathroom.", "de": "Es gibt ein kleines Bad."},
            {"en": "The flat is very bright.", "de": "Die Wohnung ist sehr hell."},
            {"en": "My desk is by the window.", "de": "Mein Schreibtisch ist am Fenster."},
            {"en": "The plant is on the floor.", "de": "Die Pflanze ist auf dem Boden."},
            {"en": "There are many windows.", "de": "Es gibt viele Fenster."},
            {"en": "The rent is too high.", "de": "Die Miete ist zu hoch."},
            {"en": "We live on the ground floor.", "de": "Wir wohnen im Erdgeschoss."},
            {"en": "The chairs are in the kitchen.", "de": "Die Stühle sind in der Küche."},
            {"en": "There is a garage.", "de": "Es gibt eine Garage."},
            {"en": "My room is on the left.", "de": "Mein Zimmer ist links."},
            {"en": "The house has a garden.", "de": "Das Haus hat einen Garten."},
            {"en": "I am looking for a new flat.", "de": "Ich suche eine neue Wohnung."},
        ],
    },

    ("A1", "clothes_fashion"): {
        "note": (
            "📖 Clothes & Fashion — A1\n\n"
            "ADJECTIVES AFTER THE VERB (predicative) — NO ending!\n"
            "After sein / werden / bleiben, the adjective never changes:\n"
            "• Die Jacke ist neu.  ·  Die Schuhe sind teuer.  ·  Das Kleid ist schön.\n"
            "(Endings before a noun come later, at A2.)\n\n"
            "COLOURS: rot, blau, grün, gelb, schwarz, weiß, braun, grau, orange, rosa.\n"
            "• Der Pullover ist blau.  ·  Meine Schuhe sind schwarz.\n\n"
            "CLOTHES VOCAB\n"
            "die Jacke, die Hose, das Hemd, das T-Shirt, der Pullover, das Kleid, der Rock, "
            "die Schuhe, die Mütze, der Schal, die Socken, der Mantel.\n"
            "tragen (to wear): ich trage, du trägst, er trägt.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "The jacket is new.", "de": "Die Jacke ist neu."},
            {"en": "The shoes are black.", "de": "Die Schuhe sind schwarz."},
            {"en": "My shirt is white.", "de": "Mein Hemd ist weiß."},
            {"en": "The dress is beautiful.", "de": "Das Kleid ist schön."},
            {"en": "I wear a jacket.", "de": "Ich trage eine Jacke."},
            {"en": "The trousers are too big.", "de": "Die Hose ist zu groß."},
            {"en": "The T-shirt is red.", "de": "Das T-Shirt ist rot."},
            {"en": "My socks are green.", "de": "Meine Socken sind grün."},
            {"en": "Do you wear a hat?", "de": "Trägst du eine Mütze?"},
            {"en": "The coat is very warm.", "de": "Der Mantel ist sehr warm."},
            {"en": "The skirt is too short.", "de": "Der Rock ist zu kurz."},
            {"en": "Her dress is yellow.", "de": "Ihr Kleid ist gelb."},
            {"en": "I wear a scarf in winter.", "de": "Ich trage im Winter einen Schal."},
            {"en": "The shoes are expensive.", "de": "Die Schuhe sind teuer."},
            {"en": "My jacket is brown.", "de": "Meine Jacke ist braun."},
            {"en": "The shirt is dirty.", "de": "Das Hemd ist schmutzig."},
            {"en": "His coat is black.", "de": "Sein Mantel ist schwarz."},
            {"en": "The pullover is too small.", "de": "Der Pullover ist zu klein."},
            {"en": "I like the colour blue.", "de": "Ich mag die Farbe Blau."},
            {"en": "The clothes are cheap.", "de": "Die Kleidung ist billig."},
            {"en": "My shoes are new.", "de": "Meine Schuhe sind neu."},
            {"en": "The hat is grey.", "de": "Die Mütze ist grau."},
            {"en": "She wears a dress.", "de": "Sie trägt ein Kleid."},
            {"en": "The trousers are black.", "de": "Die Hose ist schwarz."},
            {"en": "This jacket is too expensive.", "de": "Diese Jacke ist zu teuer."},
            {"en": "My T-shirt is orange.", "de": "Mein T-Shirt ist orange."},
            {"en": "He wears glasses.", "de": "Er trägt eine Brille."},
            {"en": "The socks are white.", "de": "Die Socken sind weiß."},
            {"en": "The skirt is pink.", "de": "Der Rock ist rosa."},
            {"en": "I need new shoes.", "de": "Ich brauche neue Schuhe."},
            {"en": "The coat is long.", "de": "Der Mantel ist lang."},
            {"en": "Her shirt is light blue.", "de": "Ihr Hemd ist hellblau."},
            {"en": "The clothes are comfortable.", "de": "Die Kleidung ist bequem."},
            {"en": "The colour is very nice.", "de": "Die Farbe ist sehr schön."},
            {"en": "My jacket is too big.", "de": "Meine Jacke ist zu groß."},
            {"en": "The dress is green.", "de": "Das Kleid ist grün."},
            {"en": "I buy a shirt.", "de": "Ich kaufe ein Hemd."},
            {"en": "The shoes are very comfortable.", "de": "Die Schuhe sind sehr bequem."},
            {"en": "What are you wearing today?", "de": "Was trägst du heute?"},
            {"en": "Red is my favorite color.", "de": "Rot ist meine Lieblingsfarbe."},
        ],
    },

    ("A1", "personality"): {
        "note": (
            "📖 Personality — A1\n\n"
            "DESCRIBING PEOPLE — sein + adjective (predicative, no ending)\n"
            "• Er ist freundlich.  ·  Sie ist sehr nett.  ·  Wir sind glücklich.\n\n"
            "INTENSIFIERS (placed before the adjective)\n"
            "sehr (very) · ziemlich (quite) · total (totally) · wirklich (really) · "
            "ein bisschen (a bit) · nicht so (not so) · zu (too).\n"
            "• Sie ist ziemlich ruhig.  ·  Er ist ein bisschen schüchtern.  ·  Das ist nicht so wichtig.\n\n"
            "PERSONALITY ADJECTIVES\n"
            "nett, freundlich, ruhig, laut, lustig, ernst (serious), fleißig (hard-working), "
            "faul (lazy), höflich (polite), ehrlich (honest), geduldig (patient), "
            "nervös, schüchtern (shy), offen (open).\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "He is friendly.", "de": "Er ist freundlich."},
            {"en": "She is very nice.", "de": "Sie ist sehr nett."},
            {"en": "I am happy.", "de": "Ich bin glücklich."},
            {"en": "He is quite quiet.", "de": "Er ist ziemlich ruhig."},
            {"en": "She is funny.", "de": "Sie ist lustig."},
            {"en": "We are very patient.", "de": "Wir sind sehr geduldig."},
            {"en": "He is a bit shy.", "de": "Er ist ein bisschen schüchtern."},
            {"en": "My friend is honest.", "de": "Mein Freund ist ehrlich."},
            {"en": "She is hard-working.", "de": "Sie ist fleißig."},
            {"en": "He is sometimes lazy.", "de": "Er ist manchmal faul."},
            {"en": "You are very polite.", "de": "Du bist sehr höflich."},
            {"en": "The teacher is strict.", "de": "Der Lehrer ist streng."},
            {"en": "I am a little nervous.", "de": "Ich bin ein bisschen nervös."},
            {"en": "She is really friendly.", "de": "Sie ist wirklich freundlich."},
            {"en": "He is not so serious.", "de": "Er ist nicht so ernst."},
            {"en": "My sister is very loud.", "de": "Meine Schwester ist sehr laut."},
            {"en": "They are very kind.", "de": "Sie sind sehr freundlich."},
            {"en": "He is always happy.", "de": "Er ist immer glücklich."},
            {"en": "She is quite open.", "de": "Sie ist ziemlich offen."},
            {"en": "My boss is impatient.", "de": "Mein Chef ist ungeduldig."},
            {"en": "I am calm.", "de": "Ich bin ruhig."},
            {"en": "He is reliable.", "de": "Er ist zuverlässig."},
            {"en": "She is totally relaxed.", "de": "Sie ist total entspannt."},
            {"en": "You are too serious.", "de": "Du bist zu ernst."},
            {"en": "My brother is funny.", "de": "Mein Bruder ist lustig."},
            {"en": "The child is shy.", "de": "Das Kind ist schüchtern."},
            {"en": "She is very intelligent.", "de": "Sie ist sehr intelligent."},
            {"en": "He is friendly and polite.", "de": "Er ist freundlich und höflich."},
            {"en": "I am not lazy.", "de": "Ich bin nicht faul."},
            {"en": "She is always honest.", "de": "Sie ist immer ehrlich."},
            {"en": "My colleague is helpful.", "de": "Mein Kollege ist hilfsbereit."},
            {"en": "He is quite serious today.", "de": "Er ist heute ziemlich ernst."},
            {"en": "They are very hard-working.", "de": "Sie sind sehr fleißig."},
            {"en": "She is a bit nervous.", "de": "Sie ist ein bisschen nervös."},
            {"en": "You are very kind.", "de": "Du bist sehr nett."},
            {"en": "He is rarely angry.", "de": "Er ist selten wütend."},
            {"en": "My mother is patient.", "de": "Meine Mutter ist geduldig."},
            {"en": "The man is unfriendly.", "de": "Der Mann ist unfreundlich."},
            {"en": "She is really funny.", "de": "Sie ist wirklich lustig."},
            {"en": "I am proud of you.", "de": "Ich bin stolz auf dich."},
        ],
    },

    ("A1", "business"): {
        "note": (
            "📖 Business and Money — A1\n\n"
            "NUMBERS\n"
            "0 null · 1 eins · 2 zwei · 3 drei · 4 vier · 5 fünf · 6 sechs · 7 sieben · "
            "8 acht · 9 neun · 10 zehn · 11 elf · 12 zwölf · 20 zwanzig · "
            "21 einundzwanzig · 30 dreißig · 100 hundert · 1000 tausend.\n"
            "Order: 21 = ein-und-zwanzig (one-and-twenty).\n\n"
            "MONEY & PRICES\n"
            "der Euro, der Cent, das Geld, der Preis, kosten, bezahlen, kaufen, verkaufen, billig, teuer.\n"
            "• Was kostet das? — How much is that?\n"
            "• Das kostet zehn Euro.  ·  Das ist zu teuer.  ·  Ich bezahle mit Karte.\n\n"
            "VOCAB: die Bank, das Konto, die Rechnung (bill), das Bargeld (cash), "
            "die Karte (card), günstig (good value), das Angebot (offer).\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "How much is that?", "de": "Was kostet das?"},
            {"en": "That costs ten euros.", "de": "Das kostet zehn Euro."},
            {"en": "It is too expensive.", "de": "Das ist zu teuer."},
            {"en": "I pay with card.", "de": "Ich bezahle mit Karte."},
            {"en": "I have no cash.", "de": "Ich habe kein Bargeld."},
            {"en": "The book costs twelve euros.", "de": "Das Buch kostet zwölf Euro."},
            {"en": "That is very cheap.", "de": "Das ist sehr billig."},
            {"en": "I would like to pay.", "de": "Ich möchte bezahlen."},
            {"en": "The price is good.", "de": "Der Preis ist gut."},
            {"en": "I buy a ticket.", "de": "Ich kaufe eine Karte."},
            {"en": "We sell our car.", "de": "Wir verkaufen unser Auto."},
            {"en": "The bill is twenty euros.", "de": "Die Rechnung ist zwanzig Euro."},
            {"en": "Do you have change?", "de": "Hast du Kleingeld?"},
            {"en": "The coffee costs three euros.", "de": "Der Kaffee kostet drei Euro."},
            {"en": "I have one hundred euros.", "de": "Ich habe hundert Euro."},
            {"en": "The offer is good.", "de": "Das Angebot ist gut."},
            {"en": "The shoes cost fifty euros.", "de": "Die Schuhe kosten fünfzig Euro."},
            {"en": "I need money.", "de": "Ich brauche Geld."},
            {"en": "Can I pay here?", "de": "Kann ich hier bezahlen?"},
            {"en": "The bank is closed.", "de": "Die Bank ist geschlossen."},
            {"en": "It costs twenty-one euros.", "de": "Es kostet einundzwanzig Euro."},
            {"en": "We have no money.", "de": "Wir haben kein Geld."},
            {"en": "The price is too high.", "de": "Der Preis ist zu hoch."},
            {"en": "I buy two tickets.", "de": "Ich kaufe zwei Karten."},
            {"en": "That is good value.", "de": "Das ist günstig."},
            {"en": "The phone costs three hundred euros.", "de": "Das Handy kostet dreihundert Euro."},
            {"en": "I pay in cash.", "de": "Ich bezahle bar."},
            {"en": "How much does the bag cost?", "de": "Was kostet die Tasche?"},
            {"en": "The hotel is expensive.", "de": "Das Hotel ist teuer."},
            {"en": "I have a bank account.", "de": "Ich habe ein Konto."},
            {"en": "The rent is eight hundred euros.", "de": "Die Miete ist achthundert Euro."},
            {"en": "We pay the bill.", "de": "Wir bezahlen die Rechnung."},
            {"en": "The price is fair.", "de": "Der Preis ist fair."},
            {"en": "I save my money.", "de": "Ich spare mein Geld."},
            {"en": "The ticket costs nine euros.", "de": "Die Karte kostet neun Euro."},
            {"en": "Do you accept cards?", "de": "Nehmt ihr Karten?"},
            {"en": "It is on offer.", "de": "Es ist im Angebot."},
            {"en": "I earn enough money.", "de": "Ich verdiene genug Geld."},
            {"en": "The shop is cheap.", "de": "Der Laden ist billig."},
            {"en": "Time is money.", "de": "Zeit ist Geld."},
        ],
    },

    ("A1", "physical_appearance"): {
        "note": (
            "📖 Physical Appearance — A1\n\n"
            "DESCRIBING HOW SOMEONE LOOKS — two easy patterns:\n"
            "1) sein + adjective (predicative, no ending):\n"
            "   Er ist groß.  ·  Sie ist klein.  ·  Er ist jung.  ·  Sie ist schlank.\n"
            "2) haben + a feature:\n"
            "   Er hat eine Brille.  ·  Sie hat lange Haare.  ·  Er hat einen Bart.\n"
            "Also: Seine Augen sind blau.  ·  Ihre Haare sind kurz.\n\n"
            "VOCAB: groß (tall), klein (short), jung (young), alt (old), schlank (slim), "
            "die Haare (hair), die Augen (eyes), der Bart (beard), die Brille (glasses), "
            "blond, dunkel (dark), kurz (short), lang (long), schön, hübsch (pretty).\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "He is tall.", "de": "Er ist groß."},
            {"en": "She is small.", "de": "Sie ist klein."},
            {"en": "He is young.", "de": "Er ist jung."},
            {"en": "She is old.", "de": "Sie ist alt."},
            {"en": "He wears glasses.", "de": "Er trägt eine Brille."},
            {"en": "Her hair is long.", "de": "Ihre Haare sind lang."},
            {"en": "His eyes are blue.", "de": "Seine Augen sind blau."},
            {"en": "She is very pretty.", "de": "Sie ist sehr hübsch."},
            {"en": "He has a beard.", "de": "Er hat einen Bart."},
            {"en": "My brother is slim.", "de": "Mein Bruder ist schlank."},
            {"en": "Her hair is short.", "de": "Ihre Haare sind kurz."},
            {"en": "He is quite tall.", "de": "Er ist ziemlich groß."},
            {"en": "She has blonde hair.", "de": "Sie hat blonde Haare."},
            {"en": "His eyes are dark.", "de": "Seine Augen sind dunkel."},
            {"en": "The man is old.", "de": "Der Mann ist alt."},
            {"en": "She is beautiful.", "de": "Sie ist schön."},
            {"en": "He is not very tall.", "de": "Er ist nicht sehr groß."},
            {"en": "My sister is young.", "de": "Meine Schwester ist jung."},
            {"en": "He has short hair.", "de": "Er hat kurze Haare."},
            {"en": "Her eyes are green.", "de": "Ihre Augen sind grün."},
            {"en": "She wears glasses.", "de": "Sie trägt eine Brille."},
            {"en": "He is strong.", "de": "Er ist stark."},
            {"en": "The child is small.", "de": "Das Kind ist klein."},
            {"en": "She has long hair.", "de": "Sie hat lange Haare."},
            {"en": "His hair is dark.", "de": "Seine Haare sind dunkel."},
            {"en": "He looks young.", "de": "Er sieht jung aus."},
            {"en": "She is a little older.", "de": "Sie ist ein bisschen älter."},
            {"en": "My father has a beard.", "de": "Mein Vater hat einen Bart."},
            {"en": "He is tall and slim.", "de": "Er ist groß und schlank."},
            {"en": "Her hair is blonde.", "de": "Ihre Haare sind blond."},
            {"en": "The woman is pretty.", "de": "Die Frau ist hübsch."},
            {"en": "He has brown eyes.", "de": "Er hat braune Augen."},
            {"en": "She is taller than me.", "de": "Sie ist größer als ich."},
            {"en": "My grandmother is old.", "de": "Meine Großmutter ist alt."},
            {"en": "He looks tired.", "de": "Er sieht müde aus."},
            {"en": "She has beautiful eyes.", "de": "Sie hat schöne Augen."},
            {"en": "He is handsome.", "de": "Er ist gutaussehend."},
            {"en": "Her smile is beautiful.", "de": "Ihr Lächeln ist schön."},
            {"en": "His beard is long.", "de": "Sein Bart ist lang."},
            {"en": "She looks like her mother.", "de": "Sie sieht wie ihre Mutter aus."},
        ],
    },

    ("A1", "town_city"): {
        "note": (
            "📖 Town and City — A1\n\n"
            "SEPARABLE VERBS\n"
            "Some verbs have a prefix that SPLITS OFF and jumps to the END in a main clause.\n"
            "Infinitive: ankommen → Der Zug kommt um acht an.\n"
            "Common ones: aufstehen (get up), einkaufen (shop), abfahren (depart), "
            "ankommen (arrive), anrufen (call), aufmachen (open), zumachen (close), "
            "mitkommen (come along), aussteigen (get off), umsteigen (change/transfer).\n"
            "• Ich stehe um sieben auf.  ·  Wir kaufen im Supermarkt ein.  ·  Der Bus fährt gleich ab.\n"
            "After a modal it stays together: Ich muss früh aufstehen.\n\n"
            "VOCAB: die Stadt, das Dorf, die Straße, der Platz, der Bahnhof, die Haltestelle, "
            "der Bus, die U-Bahn, der Zug, das Rathaus, der Markt, die Brücke, "
            "links, rechts, geradeaus.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I get up at seven.", "de": "Ich stehe um sieben auf."},
            {"en": "The train arrives at eight.", "de": "Der Zug kommt um acht an."},
            {"en": "We shop at the supermarket.", "de": "Wir kaufen im Supermarkt ein."},
            {"en": "The bus departs soon.", "de": "Der Bus fährt gleich ab."},
            {"en": "I call my friend.", "de": "Ich rufe meinen Freund an."},
            {"en": "Do you come along?", "de": "Kommst du mit?"},
            {"en": "The shop opens at nine.", "de": "Der Laden macht um neun auf."},
            {"en": "I get off at the station.", "de": "Ich steige am Bahnhof aus."},
            {"en": "The city is very big.", "de": "Die Stadt ist sehr groß."},
            {"en": "We change at the next stop.", "de": "Wir steigen an der nächsten Haltestelle um."},
            {"en": "Go straight ahead.", "de": "Gehen Sie geradeaus."},
            {"en": "The bus stop is on the left.", "de": "Die Haltestelle ist links."},
            {"en": "I get up early.", "de": "Ich stehe früh auf."},
            {"en": "She calls the doctor.", "de": "Sie ruft den Arzt an."},
            {"en": "The train leaves at ten.", "de": "Der Zug fährt um zehn ab."},
            {"en": "We go shopping today.", "de": "Wir kaufen heute ein."},
            {"en": "The town hall is in the centre.", "de": "Das Rathaus ist im Zentrum."},
            {"en": "Turn right at the bridge.", "de": "Biegen Sie an der Brücke rechts ab."},
            {"en": "I have to get up early.", "de": "Ich muss früh aufstehen."},
            {"en": "The museum opens at ten.", "de": "Das Museum macht um zehn auf."},
            {"en": "Where is the station?", "de": "Wo ist der Bahnhof?"},
            {"en": "The market is on the square.", "de": "Der Markt ist auf dem Platz."},
            {"en": "We arrive in the evening.", "de": "Wir kommen am Abend an."},
            {"en": "He closes the window.", "de": "Er macht das Fenster zu."},
            {"en": "I take the subway.", "de": "Ich nehme die U-Bahn."},
            {"en": "The street is very long.", "de": "Die Straße ist sehr lang."},
            {"en": "Do you want to come along?", "de": "Willst du mitkommen?"},
            {"en": "The bus arrives late.", "de": "Der Bus kommt spät an."},
            {"en": "She gets off here.", "de": "Sie steigt hier aus."},
            {"en": "We buy fruit at the market.", "de": "Wir kaufen Obst auf dem Markt."},
            {"en": "The train departs from platform two.", "de": "Der Zug fährt von Gleis zwei ab."},
            {"en": "I get up at six every day.", "de": "Ich stehe jeden Tag um sechs auf."},
            {"en": "The bridge is very old.", "de": "Die Brücke ist sehr alt."},
            {"en": "Please open the door.", "de": "Machen Sie bitte die Tür auf."},
            {"en": "The city has a beautiful park.", "de": "Die Stadt hat einen schönen Park."},
            {"en": "We change trains in Berlin.", "de": "Wir steigen in Berlin um."},
            {"en": "The bank is next to the post office.", "de": "Die Bank ist neben der Post."},
            {"en": "I call you tomorrow.", "de": "Ich rufe dich morgen an."},
            {"en": "The supermarket closes at eight.", "de": "Der Supermarkt macht um acht zu."},
            {"en": "The village is small and quiet.", "de": "Das Dorf ist klein und ruhig."},
        ],
    },

    ("A1", "music"): {
        "note": (
            "📖 Music — A1\n\n"
            "COORDINATING CONJUNCTIONS — they join two main clauses WITHOUT changing word "
            "order. The verb still stays in position 2.\n"
            "und (and) · aber (but) · oder (or) · denn (because).\n"
            "• Ich höre Musik und ich tanze.\n"
            "• Ich spiele Gitarre, aber ich singe nicht.\n"
            "• Magst du Rock oder magst du Pop?\n"
            "• Ich bleibe zu Hause, denn ich bin müde.\n"
            "With und/oder you can drop the repeated subject: Ich singe und tanze.\n\n"
            "VOCAB: die Musik, das Lied (song), die Band, das Konzert, das Instrument, "
            "die Gitarre, das Klavier (piano), die Geige (violin), das Schlagzeug (drums), "
            "singen, spielen, hören, tanzen, laut, leise (quiet).\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I listen to music.", "de": "Ich höre Musik."},
            {"en": "I sing and I dance.", "de": "Ich singe und ich tanze."},
            {"en": "I play guitar.", "de": "Ich spiele Gitarre."},
            {"en": "She sings well.", "de": "Sie singt gut."},
            {"en": "I like rock, but I don't like jazz.", "de": "Ich mag Rock, aber ich mag keinen Jazz."},
            {"en": "Do you play piano or guitar?", "de": "Spielst du Klavier oder Gitarre?"},
            {"en": "We go to a concert.", "de": "Wir gehen zu einem Konzert."},
            {"en": "The music is too loud.", "de": "Die Musik ist zu laut."},
            {"en": "I stay home because I am tired.", "de": "Ich bleibe zu Hause, denn ich bin müde."},
            {"en": "He plays the violin.", "de": "Er spielt Geige."},
            {"en": "I sing and dance.", "de": "Ich singe und tanze."},
            {"en": "She listens to music and reads a book.", "de": "Sie hört Musik und liest ein Buch."},
            {"en": "I like pop, but he likes rock.", "de": "Ich mag Pop, aber er mag Rock."},
            {"en": "The band is very famous.", "de": "Die Band ist sehr berühmt."},
            {"en": "Do you sing or do you play an instrument?", "de": "Singst du oder spielst du ein Instrument?"},
            {"en": "I learn the piano.", "de": "Ich lerne Klavier."},
            {"en": "The song is beautiful.", "de": "Das Lied ist schön."},
            {"en": "We dance because the music is good.", "de": "Wir tanzen, denn die Musik ist gut."},
            {"en": "He plays drums in a band.", "de": "Er spielt Schlagzeug in einer Band."},
            {"en": "I like the song, but it is too long.", "de": "Ich mag das Lied, aber es ist zu lang."},
            {"en": "She sings in a choir.", "de": "Sie singt in einem Chor."},
            {"en": "Do you listen to the radio or to CDs?", "de": "Hörst du Radio oder CDs?"},
            {"en": "The concert starts at eight.", "de": "Das Konzert beginnt um acht."},
            {"en": "I play guitar and he sings.", "de": "Ich spiele Gitarre und er singt."},
            {"en": "I am happy because I love music.", "de": "Ich bin glücklich, denn ich liebe Musik."},
            {"en": "The music is quiet.", "de": "Die Musik ist leise."},
            {"en": "She has a beautiful voice.", "de": "Sie hat eine schöne Stimme."},
            {"en": "We sing together.", "de": "Wir singen zusammen."},
            {"en": "I don't dance, but I sing.", "de": "Ich tanze nicht, aber ich singe."},
            {"en": "He buys a new guitar.", "de": "Er kauft eine neue Gitarre."},
            {"en": "The concert is sold out.", "de": "Das Konzert ist ausverkauft."},
            {"en": "I listen to music every day.", "de": "Ich höre jeden Tag Musik."},
            {"en": "Do you like classical music?", "de": "Magst du klassische Musik?"},
            {"en": "She plays piano and guitar.", "de": "Sie spielt Klavier und Gitarre."},
            {"en": "The song is on the radio.", "de": "Das Lied läuft im Radio."},
            {"en": "I sing because I am happy.", "de": "Ich singe, denn ich bin glücklich."},
            {"en": "The musicians are very good.", "de": "Die Musiker sind sehr gut."},
            {"en": "I like the melody, but not the lyrics.", "de": "Ich mag die Melodie, aber nicht den Text."},
            {"en": "We listen to music and relax.", "de": "Wir hören Musik und entspannen uns."},
            {"en": "Music makes me happy.", "de": "Musik macht mich glücklich."},
        ],
    },

    ("A1", "weather"): {
        "note": (
            "📖 Weather — A1\n\n"
            "THE IMPERSONAL \"es\"\n"
            "German weather uses es (\"it\") as a dummy subject, like English \"it is raining\".\n"
            "• Es regnet.  ·  Es schneit.  ·  Es ist kalt / warm / heiß / sonnig / windig.\n"
            "• Es gibt ein Gewitter. (There is a storm.)\n"
            "The verb stays in position 2: Heute ist es kalt.  ·  Im Sommer ist es heiß.\n\n"
            "ASKING\n"
            "Wie ist das Wetter? — What is the weather like?\n\n"
            "VOCAB: das Wetter, die Sonne, der Regen, der Schnee, der Wind, die Wolke, "
            "der Himmel, das Gewitter (storm), der Nebel (fog), das Grad (degree), "
            "sonnig, bewölkt (cloudy), kalt, warm, heiß.\n"
            "SEASONS: der Frühling, der Sommer, der Herbst, der Winter.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "It is raining.", "de": "Es regnet."},
            {"en": "It is cold.", "de": "Es ist kalt."},
            {"en": "It is warm today.", "de": "Heute ist es warm."},
            {"en": "It is snowing.", "de": "Es schneit."},
            {"en": "The sun is shining.", "de": "Die Sonne scheint."},
            {"en": "It is very hot.", "de": "Es ist sehr heiß."},
            {"en": "What is the weather like?", "de": "Wie ist das Wetter?"},
            {"en": "It is windy.", "de": "Es ist windig."},
            {"en": "The sky is blue.", "de": "Der Himmel ist blau."},
            {"en": "It is cloudy.", "de": "Es ist bewölkt."},
            {"en": "It rains a lot in autumn.", "de": "Im Herbst regnet es viel."},
            {"en": "It is sunny.", "de": "Es ist sonnig."},
            {"en": "It is ten degrees.", "de": "Es ist zehn Grad."},
            {"en": "It is foggy.", "de": "Es ist neblig."},
            {"en": "In summer it is hot.", "de": "Im Sommer ist es heiß."},
            {"en": "It is snowing in the mountains.", "de": "In den Bergen schneit es."},
            {"en": "There is a storm.", "de": "Es gibt ein Gewitter."},
            {"en": "The weather is nice.", "de": "Das Wetter ist schön."},
            {"en": "It is raining again.", "de": "Es regnet wieder."},
            {"en": "In winter it is very cold.", "de": "Im Winter ist es sehr kalt."},
            {"en": "The wind is strong.", "de": "Der Wind ist stark."},
            {"en": "It is too hot for me.", "de": "Es ist mir zu heiß."},
            {"en": "The weather is bad.", "de": "Das Wetter ist schlecht."},
            {"en": "It is getting dark.", "de": "Es wird dunkel."},
            {"en": "The sun is warm.", "de": "Die Sonne ist warm."},
            {"en": "It is cold outside.", "de": "Draußen ist es kalt."},
            {"en": "In spring the weather is nice.", "de": "Im Frühling ist das Wetter schön."},
            {"en": "It is twenty degrees today.", "de": "Heute ist es zwanzig Grad."},
            {"en": "It often rains here.", "de": "Hier regnet es oft."},
            {"en": "The clouds are grey.", "de": "Die Wolken sind grau."},
            {"en": "It is freezing.", "de": "Es friert."},
            {"en": "The weather is changing.", "de": "Das Wetter ändert sich."},
            {"en": "It is warm in the house.", "de": "Im Haus ist es warm."},
            {"en": "It is a beautiful day.", "de": "Es ist ein schöner Tag."},
            {"en": "The rain is cold.", "de": "Der Regen ist kalt."},
            {"en": "It will rain tomorrow.", "de": "Morgen regnet es."},
            {"en": "The summer is hot.", "de": "Der Sommer ist heiß."},
            {"en": "It is snowing all day.", "de": "Es schneit den ganzen Tag."},
            {"en": "I like the autumn.", "de": "Ich mag den Herbst."},
            {"en": "The weather is warm and sunny.", "de": "Das Wetter ist warm und sonnig."},
        ],
    },

    ("A1", "shopping"): {
        "note": (
            "📖 Shopping — A1\n\n"
            "THE IMPERATIVE (instructions / requests)\n"
            "du-form: take the du-form, drop -st and \"du\": du nimmst → Nimm! · du kaufst → Kauf!\n"
            "Sie-form (polite): verb + Sie: Nehmen Sie! · Kommen Sie! · Warten Sie!\n"
            "Add bitte to soften: Warten Sie bitte einen Moment.\n\n"
            "dieser / diese / dieses = this (follows the der/die/das pattern):\n"
            "  dieser Mantel (m) · diese Jacke (f) · dieses Hemd (n) · diese Schuhe (pl).\n"
            "Masculine Akkusativ → diesen: Ich nehme diesen Mantel.\n\n"
            "VOCAB: das Geschäft / der Laden (shop), der Supermarkt, die Kasse (checkout), "
            "die Größe (size), die Tüte (bag), kaufen, nehmen, brauchen, suchen, zahlen.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I buy bread.", "de": "Ich kaufe Brot."},
            {"en": "Take this jacket.", "de": "Nimm diese Jacke."},
            {"en": "How much does this cost?", "de": "Was kostet das?"},
            {"en": "I need a bag.", "de": "Ich brauche eine Tüte."},
            {"en": "Come in, please.", "de": "Kommen Sie bitte herein."},
            {"en": "I take this shirt.", "de": "Ich nehme dieses Hemd."},
            {"en": "Where is the checkout?", "de": "Wo ist die Kasse?"},
            {"en": "This dress is beautiful.", "de": "Dieses Kleid ist schön."},
            {"en": "Wait a moment, please.", "de": "Warten Sie bitte einen Moment."},
            {"en": "I am looking for shoes.", "de": "Ich suche Schuhe."},
            {"en": "Buy the apples.", "de": "Kauf die Äpfel."},
            {"en": "This coat is too expensive.", "de": "Dieser Mantel ist zu teuer."},
            {"en": "What size do you need?", "de": "Welche Größe brauchst du?"},
            {"en": "Give me the receipt, please.", "de": "Geben Sie mir bitte den Kassenbon."},
            {"en": "I pay at the checkout.", "de": "Ich zahle an der Kasse."},
            {"en": "These shoes are cheap.", "de": "Diese Schuhe sind billig."},
            {"en": "Take this one.", "de": "Nimm diesen."},
            {"en": "The shop is open.", "de": "Das Geschäft ist offen."},
            {"en": "I would like this jacket.", "de": "Ich möchte diese Jacke."},
            {"en": "Try the pullover on.", "de": "Probier den Pullover an."},
            {"en": "Do you have this in blue?", "de": "Haben Sie das in Blau?"},
            {"en": "I buy two bottles of water.", "de": "Ich kaufe zwei Flaschen Wasser."},
            {"en": "This is on offer.", "de": "Das ist im Angebot."},
            {"en": "Pay at the counter.", "de": "Zahlen Sie an der Kasse."},
            {"en": "I need a new bag.", "de": "Ich brauche eine neue Tasche."},
            {"en": "This T-shirt is too small.", "de": "Dieses T-Shirt ist zu klein."},
            {"en": "Show me the menu, please.", "de": "Zeigen Sie mir bitte die Karte."},
            {"en": "We go shopping.", "de": "Wir gehen einkaufen."},
            {"en": "Take this jacket, it is cheap.", "de": "Nimm diese Jacke, sie ist billig."},
            {"en": "The supermarket is closed.", "de": "Der Supermarkt ist geschlossen."},
            {"en": "I look for a present.", "de": "Ich suche ein Geschenk."},
            {"en": "Give me two, please.", "de": "Geben Sie mir bitte zwei."},
            {"en": "This bag is very practical.", "de": "Diese Tasche ist sehr praktisch."},
            {"en": "Do you need a bag?", "de": "Brauchen Sie eine Tüte?"},
            {"en": "I buy this coat.", "de": "Ich kaufe diesen Mantel."},
            {"en": "The price is good.", "de": "Der Preis ist gut."},
            {"en": "Come to the shop.", "de": "Komm in den Laden."},
            {"en": "This shop is new.", "de": "Dieser Laden ist neu."},
            {"en": "I take these shoes.", "de": "Ich nehme diese Schuhe."},
            {"en": "Have a nice day!", "de": "Schönen Tag noch!"},
        ],
    },

    ("A1", "environment"): {
        "note": (
            "📖 Environment — A1 (review + sollen / dürfen)\n\n"
            "This lesson reviews negation (kein / nicht) and adds two more modals.\n"
            "sollen (should): ich soll, du sollst, er soll, wir sollen …\n"
            "dürfen (be allowed to): ich darf, du darfst, er darf, wir dürfen …\n"
            "The second verb goes to the END, like all modals.\n"
            "• Wir sollen Energie sparen.  ·  Man darf hier nicht parken.\n"
            "\"man\" = \"one / you in general\" — very common in rules.\n\n"
            "NEGATION REVIEW: kein + noun (Es gibt keine Lösung) · nicht + rest (Das ist nicht gut).\n\n"
            "VOCAB: die Umwelt, die Natur, der Müll (rubbish), das Wasser, die Luft (air), "
            "der Baum, das Plastik, recyceln, sparen (save), schützen (protect), "
            "sauber (clean), schmutzig (dirty), wichtig.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "We should save water.", "de": "Wir sollen Wasser sparen."},
            {"en": "You are not allowed to park here.", "de": "Man darf hier nicht parken."},
            {"en": "We protect the environment.", "de": "Wir schützen die Umwelt."},
            {"en": "I don't throw rubbish on the floor.", "de": "Ich werfe keinen Müll auf den Boden."},
            {"en": "The air is clean.", "de": "Die Luft ist sauber."},
            {"en": "We should recycle plastic.", "de": "Wir sollen Plastik recyceln."},
            {"en": "The water is dirty.", "de": "Das Wasser ist schmutzig."},
            {"en": "You may not smoke here.", "de": "Hier darf man nicht rauchen."},
            {"en": "Nature is beautiful.", "de": "Die Natur ist schön."},
            {"en": "We have no time to lose.", "de": "Wir haben keine Zeit zu verlieren."},
            {"en": "The environment is important.", "de": "Die Umwelt ist wichtig."},
            {"en": "We should use less plastic.", "de": "Wir sollen weniger Plastik benutzen."},
            {"en": "The river is not clean.", "de": "Der Fluss ist nicht sauber."},
            {"en": "You are allowed to swim here.", "de": "Hier darf man schwimmen."},
            {"en": "I separate the rubbish.", "de": "Ich trenne den Müll."},
            {"en": "We must protect the trees.", "de": "Wir müssen die Bäume schützen."},
            {"en": "There is too much rubbish.", "de": "Es gibt zu viel Müll."},
            {"en": "We should switch off the light.", "de": "Wir sollen das Licht ausschalten."},
            {"en": "The air is not good.", "de": "Die Luft ist nicht gut."},
            {"en": "You should save energy.", "de": "Du sollst Energie sparen."},
            {"en": "We don't use plastic bags.", "de": "Wir benutzen keine Plastiktüten."},
            {"en": "The forest is very big.", "de": "Der Wald ist sehr groß."},
            {"en": "We should drink tap water.", "de": "Wir sollen Leitungswasser trinken."},
            {"en": "You may not feed the animals.", "de": "Man darf die Tiere nicht füttern."},
            {"en": "Recycling is important.", "de": "Recycling ist wichtig."},
            {"en": "The beach is clean.", "de": "Der Strand ist sauber."},
            {"en": "We have no clean water.", "de": "Wir haben kein sauberes Wasser."},
            {"en": "We should ride a bike.", "de": "Wir sollen Fahrrad fahren."},
            {"en": "The city is dirty.", "de": "Die Stadt ist schmutzig."},
            {"en": "You are not allowed to make noise.", "de": "Man darf keinen Lärm machen."},
            {"en": "We plant a tree.", "de": "Wir pflanzen einen Baum."},
            {"en": "The sea is not clean.", "de": "Das Meer ist nicht sauber."},
            {"en": "We should waste less.", "de": "Wir sollen weniger verschwenden."},
            {"en": "Plastic is a big problem.", "de": "Plastik ist ein großes Problem."},
            {"en": "We can save energy.", "de": "Wir können Energie sparen."},
            {"en": "There is no rubbish here.", "de": "Hier gibt es keinen Müll."},
            {"en": "We should walk more.", "de": "Wir sollen mehr zu Fuß gehen."},
            {"en": "The environment needs our help.", "de": "Die Umwelt braucht unsere Hilfe."},
            {"en": "We don't have much time.", "de": "Wir haben nicht viel Zeit."},
            {"en": "Every person can help.", "de": "Jeder Mensch kann helfen."},
        ],
    },

    ("A1", "advertising"): {
        "note": (
            "📖 Advertising — A1\n\n"
            "POSSESSIVE ARTICLES (my, your, his, her, our …) — same endings as ein/kein.\n"
            "  ich → mein     ·  wir → unser\n"
            "  du → dein      ·  ihr → euer\n"
            "  er → sein      ·  sie (they) → ihr\n"
            "  sie (she) → ihr ·  Sie (formal) → Ihr\n"
            "Endings: + e for feminine/plural; + en for masculine Akkusativ.\n"
            "• Das ist mein Auto. (n)  ·  meine Firma (f)  ·  Ich liebe meinen Job. (m, Akk)\n"
            "• Kaufen Sie unser Produkt!  ·  Entdecken Sie Ihre Vorteile!\n\n"
            "VOCAB: die Werbung (advertising), das Produkt, das Angebot, der Preis, "
            "die Marke (brand), der Kunde (customer), neu, günstig, kostenlos (free), "
            "das Geschenk, kaufen, sparen.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "This is my car.", "de": "Das ist mein Auto."},
            {"en": "Buy our product!", "de": "Kaufen Sie unser Produkt!"},
            {"en": "I love my job.", "de": "Ich liebe meinen Job."},
            {"en": "Where is your bag?", "de": "Wo ist deine Tasche?"},
            {"en": "Our prices are low.", "de": "Unsere Preise sind niedrig."},
            {"en": "Discover your advantages!", "de": "Entdecken Sie Ihre Vorteile!"},
            {"en": "Her idea is good.", "de": "Ihre Idee ist gut."},
            {"en": "His product is new.", "de": "Sein Produkt ist neu."},
            {"en": "Try our new offer!", "de": "Probieren Sie unser neues Angebot!"},
            {"en": "My brand is famous.", "de": "Meine Marke ist berühmt."},
            {"en": "Your shoes are nice.", "de": "Deine Schuhe sind schön."},
            {"en": "We love our customers.", "de": "Wir lieben unsere Kunden."},
            {"en": "This is his money.", "de": "Das ist sein Geld."},
            {"en": "Save with our offer!", "de": "Sparen Sie mit unserem Angebot!"},
            {"en": "Your gift is free.", "de": "Ihr Geschenk ist kostenlos."},
            {"en": "My phone is new.", "de": "Mein Handy ist neu."},
            {"en": "Their house is big.", "de": "Ihr Haus ist groß."},
            {"en": "I like your idea.", "de": "Ich mag deine Idee."},
            {"en": "Our shop is open.", "de": "Unser Geschäft ist offen."},
            {"en": "Buy your ticket now!", "de": "Kaufen Sie jetzt Ihre Karte!"},
            {"en": "Her car is red.", "de": "Ihr Auto ist rot."},
            {"en": "My family is small.", "de": "Meine Familie ist klein."},
            {"en": "His job is interesting.", "de": "Sein Job ist interessant."},
            {"en": "Visit our website!", "de": "Besuchen Sie unsere Webseite!"},
            {"en": "Your order is ready.", "de": "Ihre Bestellung ist fertig."},
            {"en": "We protect your data.", "de": "Wir schützen Ihre Daten."},
            {"en": "My favorite brand is here.", "de": "Meine Lieblingsmarke ist hier."},
            {"en": "Their products are cheap.", "de": "Ihre Produkte sind günstig."},
            {"en": "Our team is the best.", "de": "Unser Team ist das beste."},
            {"en": "I take my coffee with me.", "de": "Ich nehme meinen Kaffee mit."},
            {"en": "Your opinion is important.", "de": "Deine Meinung ist wichtig."},
            {"en": "His company is new.", "de": "Seine Firma ist neu."},
            {"en": "We need your help.", "de": "Wir brauchen Ihre Hilfe."},
            {"en": "My answer is clear.", "de": "Meine Antwort ist klar."},
            {"en": "Their offer is good.", "de": "Ihr Angebot ist gut."},
            {"en": "Choose your gift!", "de": "Wählen Sie Ihr Geschenk!"},
            {"en": "Our service is free.", "de": "Unser Service ist kostenlos."},
            {"en": "Your time is valuable.", "de": "Ihre Zeit ist wertvoll."},
            {"en": "I love my city.", "de": "Ich liebe meine Stadt."},
            {"en": "Discover our world!", "de": "Entdecken Sie unsere Welt!"},
        ],
    },

    ("A1", "government"): {
        "note": (
            "📖 Government and Society — A1 (consolidation)\n\n"
            "This final A1 lesson brings everything together, focusing on QUESTION WORDS "
            "(W-Fragen) and the formal Sie.\n\n"
            "W-QUESTIONS (verb in position 2)\n"
            "wer (who) · was (what) · wo (where) · wohin (where to) · woher (where from) · "
            "wann (when) · warum (why) · wie (how) · wie viel / wie viele (how much/many) · "
            "welcher/welche/welches (which).\n"
            "• Woher kommen Sie?  ·  Wo wohnen Sie?  ·  Was machen Sie beruflich?\n"
            "Yes/No questions put the verb first: Sprechen Sie Deutsch?\n"
            "The formal Sie is used with officials, on forms, and with strangers.\n\n"
            "VOCAB: der Staat, die Regierung (government), das Land, der Bürger (citizen), "
            "der Pass (passport), das Amt (office), das Formular (form), die Steuer (tax), "
            "wählen (vote/choose), wohnen, anmelden (register).\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "Where do you live?", "de": "Wo wohnen Sie?"},
            {"en": "Where do you come from?", "de": "Woher kommen Sie?"},
            {"en": "What is your name?", "de": "Wie heißen Sie?"},
            {"en": "Do you speak German?", "de": "Sprechen Sie Deutsch?"},
            {"en": "When does the office open?", "de": "Wann öffnet das Amt?"},
            {"en": "I need a passport.", "de": "Ich brauche einen Pass."},
            {"en": "Why do you need the form?", "de": "Warum brauchen Sie das Formular?"},
            {"en": "Who is the chancellor?", "de": "Wer ist der Kanzler?"},
            {"en": "How can I help you?", "de": "Wie kann ich Ihnen helfen?"},
            {"en": "Where is the office?", "de": "Wo ist das Amt?"},
            {"en": "I want to register.", "de": "Ich möchte mich anmelden."},
            {"en": "Which form do I need?", "de": "Welches Formular brauche ich?"},
            {"en": "How much does it cost?", "de": "Wie viel kostet es?"},
            {"en": "Please fill out the form.", "de": "Füllen Sie bitte das Formular aus."},
            {"en": "Where do I have to sign?", "de": "Wo muss ich unterschreiben?"},
            {"en": "Citizens pay taxes.", "de": "Bürger zahlen Steuern."},
            {"en": "When is the election?", "de": "Wann ist die Wahl?"},
            {"en": "I live in Germany.", "de": "Ich wohne in Deutschland."},
            {"en": "What do you do for a living?", "de": "Was machen Sie beruflich?"},
            {"en": "Do you have an appointment?", "de": "Haben Sie einen Termin?"},
            {"en": "The government is in Berlin.", "de": "Die Regierung ist in Berlin."},
            {"en": "How many people live here?", "de": "Wie viele Menschen wohnen hier?"},
            {"en": "Please wait here.", "de": "Warten Sie bitte hier."},
            {"en": "I have an appointment at ten.", "de": "Ich habe um zehn einen Termin."},
            {"en": "Where can I vote?", "de": "Wo kann ich wählen?"},
            {"en": "Show me your passport, please.", "de": "Zeigen Sie mir bitte Ihren Pass."},
            {"en": "The country is very big.", "de": "Das Land ist sehr groß."},
            {"en": "What time does the office close?", "de": "Wann schließt das Amt?"},
            {"en": "I don't understand the form.", "de": "Ich verstehe das Formular nicht."},
            {"en": "Can you help me, please?", "de": "Können Sie mir bitte helfen?"},
            {"en": "Every citizen can vote.", "de": "Jeder Bürger kann wählen."},
            {"en": "Where is the town hall?", "de": "Wo ist das Rathaus?"},
            {"en": "I would like to apply for a visa.", "de": "Ich möchte ein Visum beantragen."},
            {"en": "What is your address?", "de": "Wie ist Ihre Adresse?"},
            {"en": "The taxes are high.", "de": "Die Steuern sind hoch."},
            {"en": "Please come tomorrow.", "de": "Kommen Sie bitte morgen."},
            {"en": "Who is responsible?", "de": "Wer ist verantwortlich?"},
            {"en": "I have all the documents.", "de": "Ich habe alle Dokumente."},
            {"en": "Where do I have to go?", "de": "Wohin muss ich gehen?"},
            {"en": "Thank you for your help.", "de": "Danke für Ihre Hilfe."},
        ],
    },

    ("A2", "greeting"): {
        "note": (
            "📖 Greeting — A2\n\n"
            "THE PERFECT TENSE (Perfekt) — the spoken past. It has TWO parts:\n"
            "  haben (conjugated, position 2)  +  past participle (at the END)\n"
            "Regular (weak) verbs: ge + stem + t →\n"
            "  machen → gemacht · lernen → gelernt · arbeiten → gearbeitet\n"
            "Verbs in -ieren and most with be-/ver- take NO ge-:\n"
            "  studieren → studiert · besuchen → besucht\n"
            "• Ich habe Deutsch gelernt.  → I learned German.\n"
            "• Was hast du gestern gemacht?\n\n"
            "TIME WORDS: gestern (yesterday), letzte Woche, schon (already), "
            "noch nicht (not yet), gerade (just now).\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I learned German.", "de": "Ich habe Deutsch gelernt."},
            {"en": "What did you do yesterday?", "de": "Was hast du gestern gemacht?"},
            {"en": "We worked a lot.", "de": "Wir haben viel gearbeitet."},
            {"en": "She asked a question.", "de": "Sie hat eine Frage gestellt."},
            {"en": "I said hello.", "de": "Ich habe Hallo gesagt."},
            {"en": "He played football.", "de": "Er hat Fußball gespielt."},
            {"en": "Have you already had breakfast?", "de": "Hast du schon gefrühstückt?"},
            {"en": "I listened to music.", "de": "Ich habe Musik gehört."},
            {"en": "We learned a lot.", "de": "Wir haben viel gelernt."},
            {"en": "She lived in Berlin.", "de": "Sie hat in Berlin gewohnt."},
            {"en": "I bought bread.", "de": "Ich habe Brot gekauft."},
            {"en": "Did you work yesterday?", "de": "Hast du gestern gearbeitet?"},
            {"en": "He cooked dinner.", "de": "Er hat das Abendessen gekocht."},
            {"en": "They danced all night.", "de": "Sie haben die ganze Nacht getanzt."},
            {"en": "I made tea.", "de": "Ich habe Tee gemacht."},
            {"en": "She studied medicine.", "de": "Sie hat Medizin studiert."},
            {"en": "We visited a museum.", "de": "Wir haben ein Museum besucht."},
            {"en": "I already paid.", "de": "Ich habe schon bezahlt."},
            {"en": "He answered the email.", "de": "Er hat die E-Mail beantwortet."},
            {"en": "Did you hear that?", "de": "Hast du das gehört?"},
            {"en": "I waited an hour.", "de": "Ich habe eine Stunde gewartet."},
            {"en": "We celebrated her birthday.", "de": "Wir haben ihren Geburtstag gefeiert."},
            {"en": "She greeted the guests.", "de": "Sie hat die Gäste begrüßt."},
            {"en": "I learned the words.", "de": "Ich habe die Wörter gelernt."},
            {"en": "He showed me the photos.", "de": "Er hat mir die Fotos gezeigt."},
            {"en": "We talked for hours.", "de": "Wir haben stundenlang geredet."},
            {"en": "I cooked yesterday.", "de": "Ich habe gestern gekocht."},
            {"en": "Did she say something?", "de": "Hat sie etwas gesagt?"},
            {"en": "They lived here for ten years.", "de": "Sie haben zehn Jahre hier gewohnt."},
            {"en": "I have not paid yet.", "de": "Ich habe noch nicht bezahlt."},
            {"en": "We laughed a lot.", "de": "Wir haben viel gelacht."},
            {"en": "He worked at a bank.", "de": "Er hat bei einer Bank gearbeitet."},
            {"en": "I packed my bag.", "de": "Ich habe meine Tasche gepackt."},
            {"en": "She practiced the piano.", "de": "Sie hat Klavier geübt."},
            {"en": "Did you buy the tickets?", "de": "Hast du die Karten gekauft?"},
            {"en": "I just made a coffee.", "de": "Ich habe gerade einen Kaffee gemacht."},
            {"en": "They thanked me.", "de": "Sie haben mir gedankt."},
            {"en": "I learned a new word today.", "de": "Ich habe heute ein neues Wort gelernt."},
            {"en": "He greeted me kindly.", "de": "Er hat mich freundlich begrüßt."},
            {"en": "We have learned so much.", "de": "Wir haben so viel gelernt."},
        ],
    },

    ("A2", "holiday"): {
        "note": (
            "📖 Holiday — A2\n\n"
            "PERFECT TENSE with sein\n"
            "Some verbs use sein (not haben) in the Perfekt. Mostly:\n"
            "• MOTION (A → B): gehen → gegangen, fahren → gefahren, fliegen → geflogen, "
            "kommen → gekommen, reisen → gereist\n"
            "• CHANGE OF STATE: aufstehen → aufgestanden, einschlafen → eingeschlafen\n"
            "• sein → gewesen, bleiben → geblieben, werden → geworden\n"
            "Structure: sein (position 2) + participle (END).\n"
            "• Ich bin nach Italien gefahren.  → I went to Italy.\n"
            "• Wir sind am Meer geblieben.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I went to Italy.", "de": "Ich bin nach Italien gefahren."},
            {"en": "We flew to Spain.", "de": "Wir sind nach Spanien geflogen."},
            {"en": "She went home.", "de": "Sie ist nach Hause gegangen."},
            {"en": "They stayed at the sea.", "de": "Sie sind am Meer geblieben."},
            {"en": "I traveled a lot.", "de": "Ich bin viel gereist."},
            {"en": "He came late.", "de": "Er ist spät gekommen."},
            {"en": "We drove to the mountains.", "de": "Wir sind in die Berge gefahren."},
            {"en": "I got up early.", "de": "Ich bin früh aufgestanden."},
            {"en": "The holiday was great.", "de": "Der Urlaub ist toll gewesen."},
            {"en": "She flew to Berlin yesterday.", "de": "Sie ist gestern nach Berlin geflogen."},
            {"en": "We went to the beach.", "de": "Wir sind an den Strand gegangen."},
            {"en": "I stayed at home.", "de": "Ich bin zu Hause geblieben."},
            {"en": "They traveled through Europe.", "de": "Sie sind durch Europa gereist."},
            {"en": "He went swimming.", "de": "Er ist schwimmen gegangen."},
            {"en": "We came back on Sunday.", "de": "Wir sind am Sonntag zurückgekommen."},
            {"en": "I fell asleep on the train.", "de": "Ich bin im Zug eingeschlafen."},
            {"en": "She went on holiday.", "de": "Sie ist in den Urlaub gefahren."},
            {"en": "The flight was long.", "de": "Der Flug ist lang gewesen."},
            {"en": "We walked to the hotel.", "de": "Wir sind zum Hotel gegangen."},
            {"en": "I have never been to Paris.", "de": "Ich bin noch nie in Paris gewesen."},
            {"en": "He drove to the airport.", "de": "Er ist zum Flughafen gefahren."},
            {"en": "They flew home.", "de": "Sie sind nach Hause geflogen."},
            {"en": "We arrived in the evening.", "de": "Wir sind am Abend angekommen."},
            {"en": "I went out yesterday.", "de": "Ich bin gestern ausgegangen."},
            {"en": "She stayed one week.", "de": "Sie ist eine Woche geblieben."},
            {"en": "The children ran to the sea.", "de": "Die Kinder sind ans Meer gelaufen."},
            {"en": "We traveled by train.", "de": "Wir sind mit dem Zug gefahren."},
            {"en": "He has gone already.", "de": "Er ist schon gegangen."},
            {"en": "I flew for the first time.", "de": "Ich bin zum ersten Mal geflogen."},
            {"en": "We went into the city.", "de": "Wir sind in die Stadt gegangen."},
            {"en": "She came to the party.", "de": "Sie ist zur Party gekommen."},
            {"en": "They drove home late.", "de": "Sie sind spät nach Hause gefahren."},
            {"en": "I have been to Greece.", "de": "Ich bin in Griechenland gewesen."},
            {"en": "We got up at six.", "de": "Wir sind um sechs aufgestanden."},
            {"en": "He traveled alone.", "de": "Er ist allein gereist."},
            {"en": "The bus arrived on time.", "de": "Der Bus ist pünktlich angekommen."},
            {"en": "We stayed in a hotel.", "de": "Wir sind in einem Hotel geblieben."},
            {"en": "She flew to New York.", "de": "Sie ist nach New York geflogen."},
            {"en": "I came back yesterday.", "de": "Ich bin gestern zurückgekommen."},
            {"en": "The holiday went by quickly.", "de": "Der Urlaub ist schnell vergangen."},
        ],
    },

    ("A2", "relationship"): {
        "note": (
            "📖 Relationship — A2\n\n"
            "THE DATIVE OBJECT (Dativ) — usually the person who receives something.\n"
            "Articles: der→dem, das→dem, die→der, plural→den (+n).\n"
            "Pronouns: ich→mir, du→dir, er→ihm, sie→ihr, wir→uns, ihr→euch, sie→ihnen, Sie→Ihnen.\n"
            "• Ich gebe meinem Bruder ein Buch.  ·  Kannst du mir helfen?\n\n"
            "DATIVE VERBS (take a dative object):\n"
            "helfen, danken, gefallen (to please), gehören (belong to), gratulieren, "
            "antworten, glauben, vertrauen.\n"
            "• Das Geschenk gefällt mir.  ·  Das Auto gehört meinem Vater.\n"
            "Word order: subject – verb – DATIVE – ACCUSATIVE.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "Can you help me?", "de": "Kannst du mir helfen?"},
            {"en": "I help my friend.", "de": "Ich helfe meinem Freund."},
            {"en": "The present pleases me.", "de": "Das Geschenk gefällt mir."},
            {"en": "The car belongs to my father.", "de": "Das Auto gehört meinem Vater."},
            {"en": "I give my brother a book.", "de": "Ich gebe meinem Bruder ein Buch."},
            {"en": "She thanks her teacher.", "de": "Sie dankt ihrer Lehrerin."},
            {"en": "I believe you.", "de": "Ich glaube dir."},
            {"en": "He gives her flowers.", "de": "Er gibt ihr Blumen."},
            {"en": "Can you answer me?", "de": "Kannst du mir antworten?"},
            {"en": "The book belongs to him.", "de": "Das Buch gehört ihm."},
            {"en": "I congratulate you.", "de": "Ich gratuliere dir."},
            {"en": "The city pleases us.", "de": "Die Stadt gefällt uns."},
            {"en": "I show my friend the photos.", "de": "Ich zeige meinem Freund die Fotos."},
            {"en": "She helps her mother.", "de": "Sie hilft ihrer Mutter."},
            {"en": "We thank you.", "de": "Wir danken euch."},
            {"en": "The jacket belongs to me.", "de": "Die Jacke gehört mir."},
            {"en": "He tells me a story.", "de": "Er erzählt mir eine Geschichte."},
            {"en": "I give my sister a gift.", "de": "Ich gebe meiner Schwester ein Geschenk."},
            {"en": "Does the film please you?", "de": "Gefällt dir der Film?"},
            {"en": "I write him a letter.", "de": "Ich schreibe ihm einen Brief."},
            {"en": "She helps the children.", "de": "Sie hilft den Kindern."},
            {"en": "The house belongs to my parents.", "de": "Das Haus gehört meinen Eltern."},
            {"en": "Can I help you?", "de": "Kann ich Ihnen helfen?"},
            {"en": "He gives the dog food.", "de": "Er gibt dem Hund Futter."},
            {"en": "I thank my friends.", "de": "Ich danke meinen Freunden."},
            {"en": "The idea pleases me.", "de": "Die Idee gefällt mir."},
            {"en": "She answers her boss.", "de": "Sie antwortet ihrem Chef."},
            {"en": "We give the guests coffee.", "de": "Wir geben den Gästen Kaffee."},
            {"en": "I believe my sister.", "de": "Ich glaube meiner Schwester."},
            {"en": "The colour suits you.", "de": "Die Farbe steht dir."},
            {"en": "He brings me a coffee.", "de": "Er bringt mir einen Kaffee."},
            {"en": "I trust you.", "de": "Ich vertraue dir."},
            {"en": "The shoes belong to her.", "de": "Die Schuhe gehören ihr."},
            {"en": "She gives her son money.", "de": "Sie gibt ihrem Sohn Geld."},
            {"en": "Can you lend me the book?", "de": "Kannst du mir das Buch leihen?"},
            {"en": "We congratulate the couple.", "de": "Wir gratulieren dem Paar."},
            {"en": "The food pleases the children.", "de": "Das Essen gefällt den Kindern."},
            {"en": "I send my grandmother a card.", "de": "Ich schicke meiner Großmutter eine Karte."},
            {"en": "He helps me every day.", "de": "Er hilft mir jeden Tag."},
            {"en": "Family is important to me.", "de": "Familie ist mir wichtig."},
        ],
    },

    ("A2", "technology"): {
        "note": (
            "📖 Technology — A2\n\n"
            "PERFECT with STRONG (irregular) verbs\n"
            "Strong verbs form the participle with ge- … -en, often with a vowel change. "
            "Learn them as a set:\n"
            "  schreiben → geschrieben · lesen → gelesen · sehen → gesehen · "
            "sprechen → gesprochen · nehmen → genommen · finden → gefunden · "
            "geben → gegeben · halten → gehalten\n"
            "No ge- with be-/ver-: bekommen → bekommen · verstehen → verstanden.\n"
            "Most take haben.\n"
            "• Ich habe eine E-Mail geschrieben.  ·  Hast du die Nachricht gelesen?\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I wrote an email.", "de": "Ich habe eine E-Mail geschrieben."},
            {"en": "Have you read the message?", "de": "Hast du die Nachricht gelesen?"},
            {"en": "I saw the video.", "de": "Ich habe das Video gesehen."},
            {"en": "We spoke on the phone.", "de": "Wir haben am Telefon gesprochen."},
            {"en": "He found the file.", "de": "Er hat die Datei gefunden."},
            {"en": "I took the phone.", "de": "Ich habe das Handy genommen."},
            {"en": "She got a new laptop.", "de": "Sie hat einen neuen Laptop bekommen."},
            {"en": "I did not understand the question.", "de": "Ich habe die Frage nicht verstanden."},
            {"en": "We watched a film.", "de": "Wir haben einen Film gesehen."},
            {"en": "He wrote a program.", "de": "Er hat ein Programm geschrieben."},
            {"en": "I read the news online.", "de": "Ich habe die Nachrichten online gelesen."},
            {"en": "Have you seen my message?", "de": "Hast du meine Nachricht gesehen?"},
            {"en": "She gave me her number.", "de": "Sie hat mir ihre Nummer gegeben."},
            {"en": "We found a good app.", "de": "Wir haben eine gute App gefunden."},
            {"en": "I spoke with the technician.", "de": "Ich habe mit dem Techniker gesprochen."},
            {"en": "He took my charger.", "de": "Er hat mein Ladegerät genommen."},
            {"en": "I have already read the email.", "de": "Ich habe die E-Mail schon gelesen."},
            {"en": "They understood the problem.", "de": "Sie haben das Problem verstanden."},
            {"en": "She wrote a long text.", "de": "Sie hat einen langen Text geschrieben."},
            {"en": "I saw your photos.", "de": "Ich habe deine Fotos gesehen."},
            {"en": "We received the file.", "de": "Wir haben die Datei bekommen."},
            {"en": "He read the instructions.", "de": "Er hat die Anleitung gelesen."},
            {"en": "I gave him my password.", "de": "Ich habe ihm mein Passwort gegeben."},
            {"en": "Have you spoken to her?", "de": "Hast du mit ihr gesprochen?"},
            {"en": "She found the mistake.", "de": "Sie hat den Fehler gefunden."},
            {"en": "I have not seen the film.", "de": "Ich habe den Film nicht gesehen."},
            {"en": "We wrote the report together.", "de": "Wir haben den Bericht zusammen geschrieben."},
            {"en": "He read a lot.", "de": "Er hat viel gelesen."},
            {"en": "I understood you well.", "de": "Ich habe dich gut verstanden."},
            {"en": "She gave a presentation.", "de": "Sie hat eine Präsentation gehalten."},
            {"en": "We saw each other yesterday.", "de": "Wir haben uns gestern gesehen."},
            {"en": "I read your message twice.", "de": "Ich habe deine Nachricht zweimal gelesen."},
            {"en": "He got an answer.", "de": "Er hat eine Antwort bekommen."},
            {"en": "They spoke about the project.", "de": "Sie haben über das Projekt gesprochen."},
            {"en": "I found your email.", "de": "Ich habe deine E-Mail gefunden."},
            {"en": "She wrote to me.", "de": "Sie hat mir geschrieben."},
            {"en": "We understood the lesson.", "de": "Wir haben die Lektion verstanden."},
            {"en": "He has seen this before.", "de": "Er hat das schon einmal gesehen."},
            {"en": "I gave her the laptop.", "de": "Ich habe ihr den Laptop gegeben."},
            {"en": "Technology has changed our lives.", "de": "Die Technik hat unser Leben verändert."},
        ],
    },

    ("A2", "sports"): {
        "note": (
            "📖 Sports — A2\n\n"
            "PERFECT of SEPARABLE & INSEPARABLE verbs\n"
            "SEPARABLE verbs put -ge- BETWEEN prefix and participle:\n"
            "  einkaufen → eingekauft · anrufen → angerufen · anfangen → angefangen · "
            "teilnehmen → teilgenommen · fernsehen → ferngesehen\n"
            "INSEPARABLE prefixes (be-, ver-, er-, ent-, ge-) take NO ge-:\n"
            "  besuchen → besucht · verlieren → verloren · gewinnen → gewonnen · "
            "erreichen → erreicht · beginnen → begonnen\n"
            "• Ich habe gestern trainiert und gewonnen.\n"
            "• Wir haben am Turnier teilgenommen.\n"
            "(Motion/sein verbs still take sein: aufstehen → ist aufgestanden.)\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "We won the game.", "de": "Wir haben das Spiel gewonnen."},
            {"en": "They lost the match.", "de": "Sie haben das Spiel verloren."},
            {"en": "I trained yesterday.", "de": "Ich habe gestern trainiert."},
            {"en": "He called the trainer.", "de": "Er hat den Trainer angerufen."},
            {"en": "We took part in the tournament.", "de": "Wir haben am Turnier teilgenommen."},
            {"en": "She bought new shoes.", "de": "Sie hat neue Schuhe gekauft."},
            {"en": "I watched the game on TV.", "de": "Ich habe das Spiel im Fernsehen gesehen."},
            {"en": "The team won again.", "de": "Die Mannschaft hat wieder gewonnen."},
            {"en": "We started at six.", "de": "Wir haben um sechs angefangen."},
            {"en": "He scored two goals.", "de": "Er hat zwei Tore geschossen."},
            {"en": "I got up early for training.", "de": "Ich bin früh zum Training aufgestanden."},
            {"en": "She joined in.", "de": "Sie hat mitgemacht."},
            {"en": "We played for two hours.", "de": "Wir haben zwei Stunden gespielt."},
            {"en": "He won the race.", "de": "Er hat das Rennen gewonnen."},
            {"en": "The match started late.", "de": "Das Spiel hat spät angefangen."},
            {"en": "I forgot my sports bag.", "de": "Ich habe meine Sporttasche vergessen."},
            {"en": "We met at the stadium.", "de": "Wir haben uns am Stadion getroffen."},
            {"en": "She called me after the game.", "de": "Sie hat mich nach dem Spiel angerufen."},
            {"en": "They reached the final.", "de": "Sie haben das Finale erreicht."},
            {"en": "I took part too.", "de": "Ich habe auch mitgemacht."},
            {"en": "He lost his keys.", "de": "Er hat seine Schlüssel verloren."},
            {"en": "We watched TV after sport.", "de": "Wir haben nach dem Sport ferngesehen."},
            {"en": "The coach explained the rules.", "de": "Der Trainer hat die Regeln erklärt."},
            {"en": "I signed up for the course.", "de": "Ich habe mich für den Kurs angemeldet."},
            {"en": "She won a medal.", "de": "Sie hat eine Medaille gewonnen."},
            {"en": "We invited the other team.", "de": "Wir haben das andere Team eingeladen."},
            {"en": "He prepared everything.", "de": "Er hat alles vorbereitet."},
            {"en": "I bought a ticket for the game.", "de": "Ich habe eine Karte für das Spiel gekauft."},
            {"en": "They started the season well.", "de": "Sie haben die Saison gut begonnen."},
            {"en": "We lost in the end.", "de": "Wir haben am Ende verloren."},
            {"en": "She has already left.", "de": "Sie ist schon weggegangen."},
            {"en": "He picked me up.", "de": "Er hat mich abgeholt."},
            {"en": "I called the doctor after the injury.", "de": "Ich habe nach der Verletzung den Arzt angerufen."},
            {"en": "We celebrated the victory.", "de": "Wir haben den Sieg gefeiert."},
            {"en": "The game has finished.", "de": "Das Spiel ist zu Ende gegangen."},
            {"en": "He missed the training.", "de": "Er hat das Training verpasst."},
            {"en": "I have understood the rules.", "de": "Ich habe die Regeln verstanden."},
            {"en": "They booked the field.", "de": "Sie haben den Platz reserviert."},
            {"en": "She has come back.", "de": "Sie ist zurückgekommen."},
            {"en": "We have won the championship.", "de": "Wir haben die Meisterschaft gewonnen."},
        ],
    },

    ("A2", "food"): {
        "note": (
            "📖 Food — A2\n\n"
            "COMPARATIVE & SUPERLATIVE\n"
            "Comparative: adjective + -er … als (than)\n"
            "  billig → billiger · schnell → schneller →  Pizza ist billiger als Sushi.\n"
            "Superlative (predicative): am + adjective + -sten\n"
            "  Das ist am billigsten.  ·  Kaffee schmeckt am besten.\n"
            "Short adjectives often add an umlaut:\n"
            "  alt → älter, groß → größer, jung → jünger, gesund → gesünder\n"
            "IRREGULAR (learn them!):\n"
            "  gut → besser → am besten · viel → mehr → am meisten · "
            "gern → lieber → am liebsten\n"
            "• Ich esse lieber Fisch als Fleisch.  ·  Schokolade mag ich am liebsten.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "Pizza is cheaper than sushi.", "de": "Pizza ist billiger als Sushi."},
            {"en": "Tea is healthier than cola.", "de": "Tee ist gesünder als Cola."},
            {"en": "I like fish more than meat.", "de": "Ich mag Fisch lieber als Fleisch."},
            {"en": "Coffee tastes best.", "de": "Kaffee schmeckt am besten."},
            {"en": "This restaurant is more expensive.", "de": "Dieses Restaurant ist teurer."},
            {"en": "Apples are cheaper than mangoes.", "de": "Äpfel sind billiger als Mangos."},
            {"en": "She eats more than me.", "de": "Sie isst mehr als ich."},
            {"en": "Water is the healthiest.", "de": "Wasser ist am gesündesten."},
            {"en": "The soup is hotter than the tea.", "de": "Die Suppe ist heißer als der Tee."},
            {"en": "I prefer to drink tea.", "de": "Ich trinke lieber Tee."},
            {"en": "This cake is the best.", "de": "Dieser Kuchen ist am besten."},
            {"en": "Vegetables are healthier than chips.", "de": "Gemüse ist gesünder als Chips."},
            {"en": "He eats the most.", "de": "Er isst am meisten."},
            {"en": "Bread is cheaper here.", "de": "Brot ist hier billiger."},
            {"en": "I like chocolate the most.", "de": "Ich mag Schokolade am liebsten."},
            {"en": "The fish is fresher than the meat.", "de": "Der Fisch ist frischer als das Fleisch."},
            {"en": "This wine is better.", "de": "Dieser Wein ist besser."},
            {"en": "Lemons are more sour than oranges.", "de": "Zitronen sind saurer als Orangen."},
            {"en": "The pizza is bigger than the salad.", "de": "Die Pizza ist größer als der Salat."},
            {"en": "I eat fruit more often now.", "de": "Ich esse jetzt öfter Obst."},
            {"en": "Cooking at home is cheaper.", "de": "Zu Hause kochen ist billiger."},
            {"en": "This is the most delicious meal.", "de": "Das ist das leckerste Essen."},
            {"en": "Honey is sweeter than sugar.", "de": "Honig ist süßer als Zucker."},
            {"en": "She drinks more coffee than I do.", "de": "Sie trinkt mehr Kaffee als ich."},
            {"en": "The new café is better.", "de": "Das neue Café ist besser."},
            {"en": "I prefer cooking myself.", "de": "Ich koche lieber selbst."},
            {"en": "This dish is spicier.", "de": "Dieses Gericht ist schärfer."},
            {"en": "Milk is healthier than soda.", "de": "Milch ist gesünder als Limonade."},
            {"en": "That was the best dinner.", "de": "Das war das beste Abendessen."},
            {"en": "Rice is cheaper than potatoes.", "de": "Reis ist billiger als Kartoffeln."},
            {"en": "He likes tea less than coffee.", "de": "Er mag Tee weniger als Kaffee."},
            {"en": "The market is cheaper than the supermarket.", "de": "Der Markt ist billiger als der Supermarkt."},
            {"en": "Fresh food tastes better.", "de": "Frisches Essen schmeckt besser."},
            {"en": "This is my favorite dish.", "de": "Das ist mein Lieblingsgericht."},
            {"en": "The portion is bigger here.", "de": "Die Portion ist hier größer."},
            {"en": "I eat less sugar now.", "de": "Ich esse jetzt weniger Zucker."},
            {"en": "Strawberries are sweeter than lemons.", "de": "Erdbeeren sind süßer als Zitronen."},
            {"en": "The breakfast was the best.", "de": "Das Frühstück war am besten."},
            {"en": "I like vegetables more and more.", "de": "Ich mag Gemüse immer mehr."},
            {"en": "Good food makes life better.", "de": "Gutes Essen macht das Leben besser."},
        ],
    },

    ("A2", "education"): {
        "note": (
            "📖 Education — A2\n\n"
            "SUBORDINATE CLAUSES with weil (because)\n"
            "weil gives a reason. In the weil-clause the conjugated verb goes to the VERY END.\n"
            "  Main clause , weil + … + VERB.\n"
            "• Ich lerne Deutsch, weil ich in Berlin wohne.  (wohne → end)\n"
            "• Sie ist müde, weil sie viel gearbeitet hat.  (hat → end, after the participle)\n"
            "A comma always separates the two clauses.\n\n"
            "Compare denn (same meaning, NORMAL order):\n"
            "  Ich lerne Deutsch, denn ich wohne in Berlin.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I learn German because I live in Berlin.", "de": "Ich lerne Deutsch, weil ich in Berlin wohne."},
            {"en": "She is tired because she worked a lot.", "de": "Sie ist müde, weil sie viel gearbeitet hat."},
            {"en": "I study because I want a good job.", "de": "Ich lerne, weil ich einen guten Job will."},
            {"en": "He is happy because he passed the exam.", "de": "Er ist glücklich, weil er die Prüfung bestanden hat."},
            {"en": "We stay home because it is raining.", "de": "Wir bleiben zu Hause, weil es regnet."},
            {"en": "I am learning because I have an exam.", "de": "Ich lerne, weil ich eine Prüfung habe."},
            {"en": "She cannot come because she is sick.", "de": "Sie kann nicht kommen, weil sie krank ist."},
            {"en": "I like the course because the teacher is good.", "de": "Ich mag den Kurs, weil der Lehrer gut ist."},
            {"en": "He reads a lot because he loves books.", "de": "Er liest viel, weil er Bücher liebt."},
            {"en": "We are late because the bus did not come.", "de": "Wir sind spät, weil der Bus nicht gekommen ist."},
            {"en": "I drink coffee because I am tired.", "de": "Ich trinke Kaffee, weil ich müde bin."},
            {"en": "She studies medicine because she wants to help people.", "de": "Sie studiert Medizin, weil sie Menschen helfen will."},
            {"en": "I cannot answer because I do not understand the question.", "de": "Ich kann nicht antworten, weil ich die Frage nicht verstehe."},
            {"en": "He learns English because he needs it for work.", "de": "Er lernt Englisch, weil er es für die Arbeit braucht."},
            {"en": "We are happy because the holidays start.", "de": "Wir sind glücklich, weil die Ferien beginnen."},
            {"en": "I take the bus because my car is broken.", "de": "Ich nehme den Bus, weil mein Auto kaputt ist."},
            {"en": "She is nervous because she has a test.", "de": "Sie ist nervös, weil sie einen Test hat."},
            {"en": "I stay because I want to learn more.", "de": "Ich bleibe, weil ich mehr lernen will."},
            {"en": "He is proud because he did well.", "de": "Er ist stolz, weil er es gut gemacht hat."},
            {"en": "We practice because we want to improve.", "de": "Wir üben, weil wir besser werden wollen."},
            {"en": "I am hungry because I did not eat.", "de": "Ich habe Hunger, weil ich nicht gegessen habe."},
            {"en": "She is at home because she is ill.", "de": "Sie ist zu Hause, weil sie krank ist."},
            {"en": "I read the book because it is interesting.", "de": "Ich lese das Buch, weil es interessant ist."},
            {"en": "He works hard because he needs money.", "de": "Er arbeitet viel, weil er Geld braucht."},
            {"en": "We are quiet because the baby is sleeping.", "de": "Wir sind leise, weil das Baby schläft."},
            {"en": "I ask the teacher because I have a question.", "de": "Ich frage den Lehrer, weil ich eine Frage habe."},
            {"en": "She is happy because she got good grades.", "de": "Sie ist glücklich, weil sie gute Noten bekommen hat."},
            {"en": "I learn the words because I want to remember them.", "de": "Ich lerne die Wörter, weil ich sie behalten will."},
            {"en": "He is tired because he got up early.", "de": "Er ist müde, weil er früh aufgestanden ist."},
            {"en": "We cancel the trip because the weather is bad.", "de": "Wir sagen die Reise ab, weil das Wetter schlecht ist."},
            {"en": "I am glad because you came.", "de": "Ich bin froh, weil du gekommen bist."},
            {"en": "She writes notes because she wants to learn.", "de": "Sie schreibt Notizen, weil sie lernen will."},
            {"en": "I do not go out because I have to study.", "de": "Ich gehe nicht aus, weil ich lernen muss."},
            {"en": "He is late because he missed the train.", "de": "Er ist spät, weil er den Zug verpasst hat."},
            {"en": "We like the school because it is modern.", "de": "Wir mögen die Schule, weil sie modern ist."},
            {"en": "I am tired because I studied all night.", "de": "Ich bin müde, weil ich die ganze Nacht gelernt habe."},
            {"en": "She helps me because I am her friend.", "de": "Sie hilft mir, weil ich ihr Freund bin."},
            {"en": "I close the window because it is cold.", "de": "Ich mache das Fenster zu, weil es kalt ist."},
            {"en": "He smiles because he is happy.", "de": "Er lächelt, weil er glücklich ist."},
            {"en": "Learning is important because it opens doors.", "de": "Lernen ist wichtig, weil es Türen öffnet."},
        ],
    },

    ("A2", "work"): {
        "note": (
            "📖 Work — A2\n\n"
            "SUBORDINATE CLAUSES with dass (that)\n"
            "dass introduces a reported fact or opinion. Like weil, the conjugated verb "
            "goes to the END, after a comma.\n"
            "• Ich glaube, dass der Job interessant ist.\n"
            "• Er sagt, dass er morgen arbeiten muss.  (muss → last)\n"
            "• Ich weiß, dass du viel gearbeitet hast.  (hast → last)\n\n"
            "Common starters: Ich glaube/denke/weiß/hoffe, dass … · "
            "Es ist gut/wichtig, dass …\n"
            "• Es ist wichtig, dass du pünktlich bist.\n\n"
            "Tap Start: 40 sentences, easy → harder. 💪"
        ),
        "questions": [
            {"en": "I think that the job is interesting.", "de": "Ich glaube, dass der Job interessant ist."},
            {"en": "He says that he has to work tomorrow.", "de": "Er sagt, dass er morgen arbeiten muss."},
            {"en": "I know that you worked a lot.", "de": "Ich weiß, dass du viel gearbeitet hast."},
            {"en": "It is important that you are on time.", "de": "Es ist wichtig, dass du pünktlich bist."},
            {"en": "I hope that the meeting is short.", "de": "Ich hoffe, dass das Meeting kurz ist."},
            {"en": "She thinks that the boss is nice.", "de": "Sie denkt, dass der Chef nett ist."},
            {"en": "I believe that he is right.", "de": "Ich glaube, dass er recht hat."},
            {"en": "We know that the work is hard.", "de": "Wir wissen, dass die Arbeit schwer ist."},
            {"en": "He hopes that he gets the job.", "de": "Er hofft, dass er den Job bekommt."},
            {"en": "It is good that you are here.", "de": "Es ist gut, dass du hier bist."},
            {"en": "I think that she is a good colleague.", "de": "Ich glaube, dass sie eine gute Kollegin ist."},
            {"en": "She says that the office is closed.", "de": "Sie sagt, dass das Büro geschlossen ist."},
            {"en": "I know that you can do it.", "de": "Ich weiß, dass du es kannst."},
            {"en": "He believes that the project is important.", "de": "Er glaubt, dass das Projekt wichtig ist."},
            {"en": "It is true that the salary is good.", "de": "Es ist wahr, dass das Gehalt gut ist."},
            {"en": "I hope that we finish early.", "de": "Ich hoffe, dass wir früh fertig sind."},
            {"en": "She thinks that the work is interesting.", "de": "Sie denkt, dass die Arbeit interessant ist."},
            {"en": "I am sure that he comes.", "de": "Ich bin sicher, dass er kommt."},
            {"en": "We hope that the customer is happy.", "de": "Wir hoffen, dass der Kunde zufrieden ist."},
            {"en": "He says that he likes his job.", "de": "Er sagt, dass er seinen Job mag."},
            {"en": "I think that we need more time.", "de": "Ich glaube, dass wir mehr Zeit brauchen."},
            {"en": "It is clear that she works hard.", "de": "Es ist klar, dass sie viel arbeitet."},
            {"en": "I know that the meeting starts at ten.", "de": "Ich weiß, dass das Meeting um zehn beginnt."},
            {"en": "She hopes that she can stay.", "de": "Sie hofft, dass sie bleiben kann."},
            {"en": "I believe that the plan works.", "de": "Ich glaube, dass der Plan funktioniert."},
            {"en": "He says that he is tired.", "de": "Er sagt, dass er müde ist."},
            {"en": "It is good that you asked.", "de": "Es ist gut, dass du gefragt hast."},
            {"en": "I think that the idea is great.", "de": "Ich glaube, dass die Idee toll ist."},
            {"en": "We know that the deadline is tomorrow.", "de": "Wir wissen, dass die Frist morgen ist."},
            {"en": "She says that she helps.", "de": "Sie sagt, dass sie hilft."},
            {"en": "I hope that everything is okay.", "de": "Ich hoffe, dass alles in Ordnung ist."},
            {"en": "He thinks that the price is too high.", "de": "Er denkt, dass der Preis zu hoch ist."},
            {"en": "I am glad that you came.", "de": "Ich bin froh, dass du gekommen bist."},
            {"en": "It is possible that he is late.", "de": "Es ist möglich, dass er zu spät kommt."},
            {"en": "She knows that I am busy.", "de": "Sie weiß, dass ich beschäftigt bin."},
            {"en": "I think that we start now.", "de": "Ich glaube, dass wir jetzt anfangen."},
            {"en": "He hopes that the team wins.", "de": "Er hofft, dass das Team gewinnt."},
            {"en": "I know that you are honest.", "de": "Ich weiß, dass du ehrlich bist."},
            {"en": "It is important that we work together.", "de": "Es ist wichtig, dass wir zusammenarbeiten."},
            {"en": "I believe that hard work pays off.", "de": "Ich glaube, dass sich harte Arbeit lohnt."},
        ],
    },

    # === append new lessons above this line ===
}
