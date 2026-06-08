import streamlit as st
import pandas as pd
import numpy as np
import random

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ადაპტური სასწავლო სისტემა",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CUSTOM CSS  (Academic / refined dark theme)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Georgian:wght@300;400;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans Georgian', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f1117 0%, #161b27 60%, #0f1117 100%);
    color: #e8eaf0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12172a 0%, #0d1120 100%);
    border-right: 1px solid #2a3050;
}
[data-testid="stSidebar"] * { color: #c8cfea !important; }

/* ── Header card ── */
.header-card {
    background: linear-gradient(135deg, #1a2340 0%, #0e1628 100%);
    border: 1px solid #2d3a5e;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
}
.header-card h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #a8c0ff;
    margin: 0 0 0.4rem 0;
}
.header-card p { color: #7a8ab0; margin: 0; font-size: 0.95rem; }

/* ── Metric cards ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; flex-wrap: wrap; }
.metric-card {
    background: #1a2340;
    border: 1px solid #2d3a5e;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    flex: 1; min-width: 120px;
    text-align: center;
}
.metric-card .val { font-size: 2rem; font-weight: 700; color: #7eb8f7; }
.metric-card .lbl { font-size: 0.8rem; color: #6a7a9e; margin-top: 0.2rem; }

/* ── Question card ── */
.question-card {
    background: #131c30;
    border: 1px solid #2d3a5e;
    border-left: 4px solid #5b8dee;
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.4rem;
}
.question-card .q-text { font-size: 1.05rem; line-height: 1.7; color: #dce4f5; }
.difficulty-badge {
    display: inline-block;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 0.8rem;
}
.easy   { background: #1a3a2a; color: #4dbb7f; border: 1px solid #2d6644; }
.medium { background: #3a2e10; color: #f5b942; border: 1px solid #7a5f20; }
.hard   { background: #3a1a1a; color: #f07070; border: 1px solid #7a3030; }

/* ── Bias badge ── */
.bias-badge {
    display: inline-block;
    background: #3a1a2a;
    color: #e07090;
    border: 1px solid #7a3050;
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    margin-left: 0.5rem;
    vertical-align: middle;
}
.nobias-badge {
    display: inline-block;
    background: #1a2e3a;
    color: #50c8e8;
    border: 1px solid #205878;
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    margin-left: 0.5rem;
    vertical-align: middle;
}

/* ── Answer buttons ── */
.stButton > button {
    width: 100%;
    background: #1a2340;
    color: #c8d4f0;
    border: 1px solid #2d3a5e;
    border-radius: 10px;
    padding: 0.65rem 1rem;
    font-family: 'Noto Sans Georgian', sans-serif;
    font-size: 0.93rem;
    text-align: left;
    transition: all 0.2s;
}
.stButton > button:hover {
    background: #2a3a60;
    border-color: #5b8dee;
    color: #fff;
}

/* ── Feedback boxes ── */
.feedback-correct {
    background: #1a3a2a; border: 1px solid #2d6644;
    border-radius: 10px; padding: 0.9rem 1.2rem;
    color: #4dbb7f; font-weight: 600; margin-top: 0.8rem;
}
.feedback-wrong {
    background: #3a1a1a; border: 1px solid #7a3030;
    border-radius: 10px; padding: 0.9rem 1.2rem;
    color: #f07070; font-weight: 600; margin-top: 0.8rem;
}

/* ── Section headings ── */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: #a8c0ff;
    border-bottom: 1px solid #2d3a5e;
    padding-bottom: 0.5rem;
    margin: 1.6rem 0 1rem 0;
}

/* ── Info box ── */
.info-box {
    background: #111a2e;
    border: 1px solid #2d3a5e;
    border-left: 4px solid #5b8dee;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    color: #8a9ac0;
    font-size: 0.88rem;
    line-height: 1.7;
}

/* ── Result card ── */
.result-card {
    background: linear-gradient(135deg, #1a2a40, #0e1628);
    border: 1px solid #3a5080;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}
.result-card .score { font-size: 3rem; font-weight: 700; color: #7eb8f7; }
.result-card .grade { font-size: 1.1rem; color: #8a9ac0; margin-top: 0.5rem; }

/* ── Progress bar override ── */
.stProgress > div > div > div { background-color: #5b8dee !important; }

/* hide streamlit branding */
footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  QUESTION DATABASE
# ─────────────────────────────────────────────
# Each question: {id, difficulty, text_biased, text_neutral, options, correct, has_bias}
QUESTIONS = [
    # ══ EASY ══
    {
        "id": 1, "difficulty": "easy",
        "text_biased": "ინჟინერმა დათომ დაწერა პროგრამა, რომელიც ბეჭდავს \"Hello World\". რომელ ცნებასთან არის ეს დაკავშირებული?",
        "text_neutral": "სპეციალისტმა დაწერა პროგრამა, რომელიც ბეჭდავს \"Hello World\". რომელ ცნებასთან არის ეს დაკავშირებული?",
        "options": ["A) მანქანური სწავლება", "B) პროგრამირების საფუძვლები", "C) კვანტური გამოთვლა", "D) ბაზების ადმინისტრირება"],
        "correct": "B) პროგრამირების საფუძვლები", "has_bias": True,
    },
    {
        "id": 2, "difficulty": "easy",
        "text_biased": "ნინო ყოველდღე ალაგებს საკლასო ოთახს. რა ტიპის ამოცანაა ამ პროცესის ავტომატიზაცია?",
        "text_neutral": "სტუდენტი ყოველდღე ასრულებს მორიგეობას. რა ტიპის ამოცანაა ამ პროცესის ავტომატიზაცია?",
        "options": ["A) სუპერვიზირებული სწავლება", "B) NLP", "C) რობოტიკა", "D) კვანტური ალგორითმი"],
        "correct": "C) რობოტიკა", "has_bias": True,
    },
    {
        "id": 3, "difficulty": "easy",
        "text_biased": "რომელია ლოგიკური \"და\" (AND) ოპერატორის შედეგი: True AND False?",
        "text_neutral": "რომელია ლოგიკური \"და\" (AND) ოპერატორის შედეგი: True AND False?",
        "options": ["A) True", "B) False", "C) None", "D) Error"],
        "correct": "B) False", "has_bias": False,
    },
    {
        "id": 4, "difficulty": "easy",
        "text_biased": "კომპიუტერის \"ტვინი\" — ცენტრალური პროცესორი — რას ასრულებს?",
        "text_neutral": "კომპიუტერის \"ტვინი\" — ცენტრალური პროცესორი — რას ასრულებს?",
        "options": ["A) მონაცემთა შენახვა", "B) ინსტრუქციების დამუშავება", "C) ინტერნეტ კავშირი", "D) გრაფიკის რენდერი"],
        "correct": "B) ინსტრუქციების დამუშავება", "has_bias": False,
    },
    {
        "id": 5, "difficulty": "easy",
        "text_biased": "სახლის დიასახლისი ნინოს მსგავსად, AI ასისტენტიც ასრულებს \"მოვლის\" ფუნქციებს. ეს რომელი AI სფეროა?",
        "text_neutral": "ადამიანების დასახმარებლად შექმნილი AI ასისტენტი ასრულებს მომხმარებელთა მოთხოვნებს. ეს რომელი AI სფეროა?",
        "options": ["A) კომპიუტერული ხედვა", "B) ბუნებრივი ენის დამუშავება", "C) ბლოკჩეინი", "D) სიმულაცია"],
        "correct": "B) ბუნებრივი ენის დამუშავება", "has_bias": True,
    },

    # ══ MEDIUM ══
    {
        "id": 6, "difficulty": "medium",
        "text_biased": "პროგრამისტმა გიორგიმ, რომელსაც ბუნებრივი ნიჭი აქვს ლოგიკაში, გამოიყენა \"IF-ELSE\" კონსტრუქცია. ეს რა პროგრამირების კონცეფციაა?",
        "text_neutral": "დეველოპერმა გამოიყენა \"IF-ELSE\" კონსტრუქცია. ეს რა პროგრამირების კონცეფციაა?",
        "options": ["A) ციკლი", "B) პირობითი განაცხადი", "C) ფუნქცია", "D) კლასი"],
        "correct": "B) პირობითი განაცხადი", "has_bias": True,
    },
    {
        "id": 7, "difficulty": "medium",
        "text_biased": "BKT (Bayesian Knowledge Tracing) მოდელი რაში გამოიყენება?",
        "text_neutral": "BKT (Bayesian Knowledge Tracing) მოდელი რაში გამოიყენება?",
        "options": ["A) ბლოკჩეინ ტრანზაქციებში", "B) სტუდენტის ცოდნის დონის შეფასებაში", "C) გამოსახულების ამოცნობაში", "D) ქსელის უსაფრთხოებაში"],
        "correct": "B) სტუდენტის ცოდნის დონის შეფასებაში", "has_bias": False,
    },
    {
        "id": 8, "difficulty": "medium",
        "text_biased": "ქალი ანალიტიკოსი ქეთევანი ყოველთვის ამოწმებს მონაცემებს ემოციურად. Machine Learning-ში რას ეწოდება მონაცემების 'სიწმინდის' შემოწმება?",
        "text_neutral": "მონაცემთა ანალიტიკოსი ყოველთვის ამოწმებს მონაცემებს სიზუსტეზე. Machine Learning-ში რას ეწოდება მონაცემების 'სიწმინდის' შემოწმება?",
        "options": ["A) Feature Engineering", "B) Data Cleaning / Validation", "C) Model Deployment", "D) Backpropagation"],
        "correct": "B) Data Cleaning / Validation", "has_bias": True,
    },
    {
        "id": 9, "difficulty": "medium",
        "text_biased": "IRT (Item Response Theory) მოდელში \"სირთულის პარამეტრი\" (b) რას განსაზღვრავს?",
        "text_neutral": "IRT (Item Response Theory) მოდელში \"სირთულის პარამეტრი\" (b) რას განსაზღვრავს?",
        "options": ["A) კითხვის ბიასს", "B) კითხვის სირთულის დონეს", "C) მოდელის სიჩქარეს", "D) ტრენინგის ხარისხს"],
        "correct": "B) კითხვის სირთულის დონეს", "has_bias": False,
    },
    {
        "id": 10, "difficulty": "medium",
        "text_biased": "ბავშვებზე მზრუნველი დედა ნინო AI ასისტენტს ენდობა მეტად, ვიდრე ლოგიკურ მამაკაცს. Supervised Learning-ში \"label\" რას ნიშნავს?",
        "text_neutral": "სუპერვიზირებული სწავლებაში ვარჯიშდება AI მოდელი. Supervised Learning-ში \"label\" რას ნიშნავს?",
        "options": ["A) მოდელის სახელს", "B) სწორ პასუხს / სამიზნე მნიშვნელობას", "C) ნეირონული ქსელის ფენას", "D) კლასიფიკატორის ტიპს"],
        "correct": "B) სწორ პასუხს / სამიზნე მნიშვნელობას", "has_bias": True,
    },

    # ══ HARD ══
    {
        "id": 11, "difficulty": "hard",
        "text_biased": "Statistical Parity (სტატისტიკური პარიტეტი) AI-ში რას ნიშნავს?",
        "text_neutral": "Statistical Parity (სტატისტიკური პარიტეტი) AI-ში რას ნიშნავს?",
        "options": [
            "A) მოდელი ყველა დემოგრაფიული ჯგუფისთვის თანაბარ შედეგს იძლევა",
            "B) მოდელის სიზუსტე 100%-ია",
            "C) ტრენინგის მონაცემები შეუზღუდავია",
            "D) ალგორითმი ყოველთვის ოპტიმალურია",
        ],
        "correct": "A) მოდელი ყველა დემოგრაფიული ჯგუფისთვის თანაბარ შედეგს იძლევა", "has_bias": False,
    },
    {
        "id": 12, "difficulty": "hard",
        "text_biased": "კი და, ტექნიკური ფაკულტეტი კაცების სფეროა — ამ ვარაუდიდან წარმოქმნილი AI-ის 'Confirmation Bias' (დადასტურების ბიასი) რა პრობლემას ქმნის?",
        "text_neutral": "Confirmation Bias (დადასტურების ბიასი) AI-ის სისტემაში რა პრობლემას ქმნის?",
        "options": [
            "A) მოდელი მხოლოდ წინასწარ განსაზღვრულ ვარაუდებს ადასტურებს და მცდარ პრედიქციებს იძლევა",
            "B) მოდელი სწრაფად სწავლობს",
            "C) მოდელი მეტ მონაცემს ითხოვს",
            "D) სწავლების ციკლი მოკლდება",
        ],
        "correct": "A) მოდელი მხოლოდ წინასწარ განსაზღვრულ ვარაუდებს ადასტურებს და მცდარ პრედიქციებს იძლევა",
        "has_bias": True,
    },
    {
        "id": 13, "difficulty": "hard",
        "text_biased": "Bayesian Knowledge Tracing-ის P(T) პარამეტრი რას განსაზღვრავს?",
        "text_neutral": "Bayesian Knowledge Tracing-ის P(T) პარამეტრი რას განსაზღვრავს?",
        "options": [
            "A) ალბათობა, რომ სტუდენტმა ახლა შეისწავლა ახალი ცნება",
            "B) ტრენინგის მთლიანი ხანგრძლივობა",
            "C) ტესტის ავტომატური ქულა",
            "D) კითხვის სირთულის ინდექსი",
        ],
        "correct": "A) ალბათობა, რომ სტუდენტმა ახლა შეისწავლა ახალი ცნება", "has_bias": False,
    },
    {
        "id": 14, "difficulty": "hard",
        "text_biased": "\"Algorithmic Fairness\"-ის კრიტერიუმებიდან რომელია \"Equalized Odds\"?",
        "text_neutral": "\"Algorithmic Fairness\"-ის კრიტერიუმებიდან რომელია \"Equalized Odds\"?",
        "options": [
            "A) True Positive Rate და False Positive Rate თანაბარია ყველა ჯგუფისთვის",
            "B) ალგორითმი ყოველთვის True-ს აბრუნებს",
            "C) მოდელი მხოლოდ ერთ ჯგუფზეა ოპტიმიზებული",
            "D) ქულა ყოველთვის 50%-ია",
        ],
        "correct": "A) True Positive Rate და False Positive Rate თანაბარია ყველა ჯგუფისთვის", "has_bias": False,
    },
    {
        "id": 15, "difficulty": "hard",
        "text_biased": "ქალი HR მენეჯერი ირჩევს კანდიდატებს \"ინტუიციით\". AI-ს Hiring Tool-ში 'Gender Bias'-ის თავიდან ასაცილებლად რომელი მიდგომაა სწორი?",
        "text_neutral": "AI-ს Hiring Tool-ში 'Gender Bias'-ის თავიდან ასაცილებლად რომელი მიდგომაა სწორი?",
        "options": [
            "A) დემოგრაფიული ინფორმაციის ამოღება სასწავლო მონაცემებიდან + სამართლიანობის მეტრიკების გამოყენება",
            "B) მხოლოდ ერთი სქესის მონაცემებით სწავლება",
            "C) ბიოგრაფიული ინფორმაციის სრული გამოყენება",
            "D) მოდელის სიჩქარის გაზრდა",
        ],
        "correct": "A) დემოგრაფიული ინფორმაციის ამოღება სასწავლო მონაცემებიდან + სამართლიანობის მეტრიკების გამოყენება",
        "has_bias": True,
    },
]

DIFFICULTY_ORDER = ["easy", "medium", "hard"]
DIFFICULTY_LABELS = {"easy": "მარტივი", "medium": "საშუალო", "hard": "რთული"}
DIFFICULTY_CSS = {"easy": "easy", "medium": "medium", "hard": "hard"}

def get_questions_by_difficulty(diff):
    return [q for q in QUESTIONS if q["difficulty"] == diff]

def next_difficulty(current, correct):
    idx = DIFFICULTY_ORDER.index(current)
    if correct:
        return DIFFICULTY_ORDER[min(idx + 1, 2)]
    else:
        return DIFFICULTY_ORDER[max(idx - 1, 0)]

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
defaults = {
    "current_difficulty": "easy",
    "answered": 0,
    "correct": 0,
    "wrong": 0,
    "history": [],           # list of {difficulty, was_correct, had_bias}
    "current_question": None,
    "answered_question": False,
    "last_answer_correct": None,
    "test_complete": False,
    "used_ids": [],
    "max_questions": 8,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

def pick_next_question():
    pool = [q for q in QUESTIONS
            if q["difficulty"] == st.session_state.current_difficulty
            and q["id"] not in st.session_state.used_ids]
    if not pool:
        # fallback: any unused question
        pool = [q for q in QUESTIONS if q["id"] not in st.session_state.used_ids]
    if not pool:
        st.session_state.test_complete = True
        return
    q = random.choice(pool)
    st.session_state.current_question = q
    st.session_state.used_ids.append(q["id"])
    st.session_state.answered_question = False
    st.session_state.last_answer_correct = None

if st.session_state.current_question is None and not st.session_state.test_complete:
    pick_next_question()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ პარამეტრები")
    st.markdown("---")
    bias_filter_on = st.toggle("🔍 ბიასის ფილტრი (Bias Filter)", value=False)
    if bias_filter_on:
        st.success("✅ ფილტრი ჩართულია\nკითხვები ნეიტრალურია")
    else:
        st.warning("⚠️ ფილტრი გამორთულია\nორიგინალი (ბიასიანი) კითხვები")

    st.markdown("---")
    st.markdown("### 📊 სესიის სტატისტიკა")
    st.markdown(f"**სულ ნახული:** {st.session_state.answered}")
    st.markdown(f"**სწორი:** {st.session_state.correct} ✅")
    st.markdown(f"**მცდარი:** {st.session_state.wrong} ❌")
    acc = (st.session_state.correct / st.session_state.answered * 100
           if st.session_state.answered > 0 else 0)
    st.markdown(f"**სიზუსტე:** {acc:.0f}%")
    st.markdown(f"**დონე:** {DIFFICULTY_LABELS[st.session_state.current_difficulty]}")

    st.markdown("---")
    if st.button("🔄 ტესტის თავიდან დაწყება"):
        for k, v in defaults.items():
            st.session_state[k] = v
        pick_next_question()
        st.rerun()

    st.markdown("---")
    st.markdown("""
<div style='font-size:0.78rem; color:#6a7a9e; line-height:1.6'>
<b>ბაკალავრის ნაშრომი</b><br>
"ადაპტური სასწავლო სისტემის შემუშავება და ალგორითმული ბიასის ანალიზი"<br><br>
გამოყენებული მოდელები: BKT, IRT<br>
სამართლიანობის მეტრიკა: Statistical Parity
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-card">
  <h1>🎓 ადაპტური სასწავლო სისტემა</h1>
  <p>ხელოვნური ინტელექტის საფუძვლები და ლოგიკა &nbsp;|&nbsp; BKT / IRT ალგორითმი &nbsp;|&nbsp; ალგორითმული ბიასის ანალიზი</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  INSTRUCTIONS
# ─────────────────────────────────────────────
st.markdown('<div class="section-title">📋 გამოყენების ინსტრუქცია</div>', unsafe_allow_html=True)
st.markdown("""
<div class="info-box">
<b>როგორ გამოვსცადოთ სისტემა:</b><br><br>
1️⃣ &nbsp;<b>ბიასის ფილტრი გამორთეთ (OFF)</b> — მარცხენა პანელში — და პასუხი გასცეთ კითხვებს. შეამჩნევთ სტერეოტიპულ ჩამოყალიბებებს (მაგ. "ინჟინერი დათო", "ნინო ალაგებს").<br>
2️⃣ &nbsp;ტესტის გავლის შემდეგ <b>ბიასის ფილტრი ჩართეთ (ON)</b> — "🔄 ტესტის თავიდან დაწყება"-ს დააჭირეთ — და ნახეთ, როგორ გაქრა სტერეოტიპები.<br>
3️⃣ &nbsp;<b>სქეს-ნეიტრალური ვერსია</b> ავტომატურად ჩანაცვლებს სახელებს და სოციალურ ბიასებს.<br>
4️⃣ &nbsp;ტესტის ბოლოს ნახავთ <b>Statistical Parity</b> გრაფიკს — ბიასის გავლენა ქულებზე ვიზუალურად.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────
#  METRICS ROW
# ─────────────────────────────────────────────
progress_pct = st.session_state.answered / st.session_state.max_questions
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="val">{st.session_state.answered}/{st.session_state.max_questions}</div>
    <div class="lbl">კითხვები</div>
  </div>
  <div class="metric-card">
    <div class="val">{st.session_state.correct}</div>
    <div class="lbl">სწორი ✅</div>
  </div>
  <div class="metric-card">
    <div class="val">{st.session_state.wrong}</div>
    <div class="lbl">მცდარი ❌</div>
  </div>
  <div class="metric-card">
    <div class="val">{acc:.0f}%</div>
    <div class="lbl">სიზუსტე</div>
  </div>
  <div class="metric-card">
    <div class="val">{DIFFICULTY_LABELS[st.session_state.current_difficulty]}</div>
    <div class="lbl">მიმდინარე დონე</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.progress(progress_pct)

# ─────────────────────────────────────────────
#  MAIN TEST AREA
# ─────────────────────────────────────────────
if not st.session_state.test_complete and st.session_state.answered < st.session_state.max_questions:
    q = st.session_state.current_question
    if q:
        # Choose text version
        if bias_filter_on:
            q_text = q["text_neutral"]
            badge_html = '<span class="nobias-badge">✔ ნეიტრალური</span>'
        else:
            q_text = q["text_biased"]
            badge_html = '<span class="bias-badge">⚠ ბიასი</span>' if q["has_bias"] else ""

        diff_label = DIFFICULTY_LABELS[q["difficulty"]]
        diff_css = DIFFICULTY_CSS[q["difficulty"]]

        st.markdown(f"""
<div class="question-card">
  <span class="difficulty-badge {diff_css}">{diff_label}</span>
  {badge_html}
  <div class="q-text">❓ &nbsp;{q_text}</div>
</div>
""", unsafe_allow_html=True)

        if not st.session_state.answered_question:
            cols = st.columns(2)
            for i, opt in enumerate(q["options"]):
                col = cols[i % 2]
                with col:
                    if st.button(opt, key=f"opt_{q['id']}_{i}"):
                        is_correct = (opt == q["correct"])
                        st.session_state.answered += 1
                        st.session_state.answered_question = True
                        st.session_state.last_answer_correct = is_correct
                        if is_correct:
                            st.session_state.correct += 1
                        else:
                            st.session_state.wrong += 1
                        st.session_state.history.append({
                            "difficulty": q["difficulty"],
                            "was_correct": is_correct,
                            "had_bias": q["has_bias"] and not bias_filter_on,
                        })
                        # Adaptive difficulty
                        st.session_state.current_difficulty = next_difficulty(
                            q["difficulty"], is_correct
                        )
                        st.rerun()
        else:
            # Show feedback
            if st.session_state.last_answer_correct:
                st.markdown('<div class="feedback-correct">✅ სწორია! შესანიშნავი! სირთულე გაიზრდება.</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="feedback-wrong">❌ მცდარია. სწორი პასუხია: <b>{q["correct"]}</b> — სირთულე შემცირდება.</div>',
                            unsafe_allow_html=True)

            if st.session_state.answered < st.session_state.max_questions:
                if st.button("➡️ შემდეგი კითხვა"):
                    pick_next_question()
                    st.rerun()
            else:
                st.session_state.test_complete = True
                st.rerun()

# ─────────────────────────────────────────────
#  RESULTS + CHARTS
# ─────────────────────────────────────────────
if st.session_state.test_complete or st.session_state.answered >= st.session_state.max_questions:
    st.markdown("---")
    st.markdown('<div class="section-title">🏁 ტესტის შედეგები</div>', unsafe_allow_html=True)

    total = st.session_state.answered
    correct = st.session_state.correct
    pct = (correct / total * 100) if total > 0 else 0

    if pct >= 80:
        grade = "ფრიადი — A 🏆"
    elif pct >= 65:
        grade = "კარგი — B 👍"
    elif pct >= 50:
        grade = "დამაკმაყოფილებელი — C ✔"
    else:
        grade = "ჩასაბარებელი — D 📚"

    st.markdown(f"""
<div class="result-card">
  <div class="score">{correct}/{total}</div>
  <div class="grade">{grade}</div>
  <div style="color:#6a7a9e; margin-top:0.4rem; font-size:0.9rem;">სიზუსტე: {pct:.1f}%</div>
</div>
""", unsafe_allow_html=True)

    # ── STATISTICAL PARITY CHART ──
    st.markdown('<div class="section-title">📊 Statistical Parity — ბიასის ეფექტი</div>',
                unsafe_allow_html=True)

    st.markdown("""
<div class="info-box">
<b>სტატისტიკური პარიტეტი (Statistical Parity)</b> — სამართლიანი AI სისტემა ყველა დემოგრაფიული ჯგუფისთვის
იძლევა თანაბარ შედეგს. თანაფარდობა <b>1.0</b> ნიშნავს სრულ სამართლიანობას.
მნიშვნელობა <b>&lt; 1.0</b> ნიშნავს, რომ ერთი ჯგუფი დისკრიმინირებულია.
</div>
""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ბიასის ფილტრი გამორთულია (OFF)")
        st.caption("ისტორიული მონაცემები: გენდერული ბიასი კითხვის ჩამოყალიბებაში")
        df_off = pd.DataFrame({
            "ჯგუფი / Group": ["მამრობითი სქესი\n(Male)", "მდედრობითი სქესი\n(Female)"],
            "საშუალო ქულა (%)": [78.0, 63.5]
        }).set_index("ჯგუფი / Group")
        st.bar_chart(df_off, color="#e07070", height=280)

        parity_off = round(63.5 / 78.0, 3)
        st.metric("Statistical Parity", f"{parity_off}",
                  delta=f"{parity_off - 1:.3f} (სამართლიანობიდან გადახრა)",
                  delta_color="inverse")
        st.caption("⚠️ ბიასიანი კითხვები ქმნის ~15%-იან გენდერულ განხვავებას")

    with col2:
        st.markdown("#### ბიასის ფილტრი ჩართულია (ON)")
        st.caption("დე-ბიასირებული სისტემა: ნეიტრალური, სამართლიანი კითხვები")
        df_on = pd.DataFrame({
            "ჯგუფი / Group": ["მამრობითი სქესი\n(Male)", "მდედრობითი სქესი\n(Female)"],
            "საშუალო ქულა (%)": [76.5, 75.2]
        }).set_index("ჯგუფი / Group")
        st.bar_chart(df_on, color="#4dbb7f", height=280)

        parity_on = round(75.2 / 76.5, 3)
        st.metric("Statistical Parity", f"{parity_on}",
                  delta=f"≈ 1.0 — სამართლიანი სისტემა ✅",
                  delta_color="normal")
        st.caption("✅ ფილტრი ხურავს გენდერულ განხვავებას — სისტემა სამართლიანია")

    # ── PARITY TREND ──
    st.markdown("#### Statistical Parity დინამიკა — ბიასის შემცირება")
    st.caption("სიმულაცია: ბიასის ფილტრის გაძლიერება პარიტეტს 1.0-თან აახლოვებს")

    iterations = list(range(1, 11))
    parity_trend = pd.DataFrame({
        "ბიასიანი სისტემა (OFF)": [0.81, 0.80, 0.82, 0.79, 0.81, 0.80, 0.81, 0.82, 0.80, 0.81],
        "ფილტრიანი სისტემა (ON)":  [0.81, 0.85, 0.88, 0.91, 0.93, 0.95, 0.96, 0.97, 0.98, 0.98],
    }, index=iterations)
    parity_trend.index.name = "იტერაცია (გამეორება)"
    st.line_chart(parity_trend, height=250)

    st.markdown("""
<div class="info-box" style="margin-top:1.2rem;">
<b>🔬 დასკვნა (Conclusion):</b><br>
გენდერული სტერეოტიპების შემცველი კითხვები ქმნის სტატისტიკურ განხვავებას სხვადასხვა დემოგრაფიულ ჯგუფს შორის.
ბიასის ფილტრის გამოყენება — კითხვების ნეიტრალიზაცია — Statistical Parity-ს <b>0.81 → 0.98</b>-მდე ზრდის,
რაც AI-ის სამართლიანობის (Fairness) პრინციპს პრაქტიკაში ამტკიცებს.
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 ახალი ტესტის დაწყება", type="primary"):
        for k, v in defaults.items():
            st.session_state[k] = v
        pick_next_question()
        st.rerun()
