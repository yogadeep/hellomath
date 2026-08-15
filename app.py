import streamlit as st
import json
import os
import hashlib


# ============================================================
# SETTINGS
# ============================================================

USER_FILE = "data/user.json"

SETS_QUIZ_FILE = "data/sets_quiz.json"
RELATIONS_QUIZ_FILE = "data/relations_quiz.json"
TRIGONOMETRY_QUIZ_FILE = "data/trigonometry_quiz.json"

LEADERBOARD_FILE = "data/leaderboard.json"

MATHS_ICON = "assets/maths_icon.png"

CHAPTER_META = {
    "sets": {
        "label": "Sets",
        "number": "01",
        "glyph": "{ }",
        "blurb": "Unions, intersections and subsets.",
    },
    "relations": {
        "label": "Relations & Functions",
        "number": "02",
        "glyph": "\u0192(x)",
        "blurb": "Mappings, domains and inverses.",
    },
    "trigonometry": {
        "label": "Trigonometry",
        "number": "03",
        "glyph": "\u03b8",
        "blurb": "Identities, angles and equations.",
    },
}


# ============================================================
# PAGE CONFIGURATION
# ============================================================

if os.path.exists(MATHS_ICON):
    st.set_page_config(
        page_title="Hello Math",
        page_icon=MATHS_ICON,
        layout="wide"
    )
else:
    st.set_page_config(
        page_title="Hello Math",
        page_icon="\u222b",
        layout="wide"
    )


# ============================================================
# CUSTOM COLOUR THEME
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    --ink: #10233F;
    --indigo: #1D4577;
    --indigo-dark: #142F52;
    --accent: #E3A234;
    --accent-soft: #FBEBCB;
    --paper: #F5F7FB;
    --card: #FFFFFF;
    --border: #DCE3EE;
    --muted: #5B6B82;
    --success: #2E9E6D;
    --success-soft: #E4F5EE;
    --warning: #E3A234;
    --warning-soft: #FCF1DC;
    --danger: #D8553D;
    --danger-soft: #FBEAE5;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: var(--paper);
    background-image:
        linear-gradient(rgba(29, 69, 119, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(29, 69, 119, 0.05) 1px, transparent 1px);
    background-size: 34px 34px;
}

h1, h2, h3 {
    font-family: 'Fraunces', serif;
    letter-spacing: -0.01em;
}

h1 {
    color: var(--ink);
    font-weight: 700;
}

h2 {
    color: var(--indigo);
    font-weight: 650;
}

h3 {
    color: var(--indigo);
    font-weight: 600;
}

p, span, label, li {
    color: var(--muted);
}

/* -------------------- BUTTONS -------------------- */

.stButton > button,
.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #FFFFFF !important;
}

.stButton > button {
    background-color: var(--indigo);
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
    font-weight: 600;
    font-family: 'Inter', sans-serif;
    transition: all 0.15s ease;
    box-shadow: 0 1px 2px rgba(16, 35, 63, 0.08);
}

.stButton > button:hover,
.stButton > button:hover p,
.stButton > button:hover span {
    color: #FFFFFF !important;
}

.stButton > button:hover {
    background-color: var(--indigo-dark);
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(16, 35, 63, 0.18);
}

.stButton > button:focus:not(:active),
.stButton > button:focus {
    color: #FFFFFF !important;
}

.stButton > button:active {
    transform: translateY(0);
}

/* Primary CTA buttons (submit / login / create account) get the accent treatment */
div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: var(--indigo);
}

/* -------------------- INPUTS -------------------- */

[data-testid="stTextInput"] input {
    background-color: white;
    color: var(--ink);
    border-radius: 9px;
    border: 1px solid var(--border);
    padding: 10px 12px;
}

[data-testid="stTextInput"] input:focus {
    border-color: var(--indigo);
    box-shadow: 0 0 0 3px rgba(29, 69, 119, 0.15);
}

[data-testid="stTextInput"] label {
    color: var(--ink);
    font-weight: 500;
    font-size: 0.88rem;
}

/* -------------------- TABS -------------------- */

button[data-baseweb="tab"] {
    color: var(--muted);
    font-weight: 600;
    font-size: 1rem;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: var(--indigo);
}

[data-baseweb="tab-highlight"] {
    background-color: var(--accent) !important;
    height: 3px !important;
}

/* -------------------- RADIO / QUIZ OPTIONS -------------------- */

[data-testid="stRadio"] {
    background-color: transparent;
    padding: 0;
    border: none;
}

[data-testid="stRadio"] > div {
    gap: 8px;
}

[data-testid="stRadio"] label {
    background-color: white;
    border: 1.5px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    width: 100%;
    margin: 0 !important;
    transition: all 0.12s ease;
    cursor: pointer;
}

[data-testid="stRadio"] label:hover {
    border-color: var(--indigo);
    background-color: #F7FAFF;
}

[data-testid="stRadio"] label[data-checked="true"] {
    border-color: var(--indigo);
    background-color: var(--accent-soft);
}

hr {
    border-color: var(--border);
}

/* -------------------- BRAND / HERO -------------------- */

.hero {
    background: linear-gradient(135deg, var(--indigo) 0%, var(--ink) 100%);
    border-radius: 18px;
    padding: 40px 44px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}

.hero::after {
    content: "\u03a3   \u222b   \u03c0   \u03b8   \u2211";
    position: absolute;
    right: 28px;
    bottom: 10px;
    font-family: 'Fraunces', serif;
    font-size: 1.4rem;
    letter-spacing: 10px;
    color: rgba(255,255,255,0.14);
}

.brand {
    font-family: 'Fraunces', serif;
    font-size: 40px;
    font-weight: 700;
    color: white;
    margin: 0;
    line-height: 1.1;
}

.brand-subtitle {
    font-size: 16px;
    color: rgba(255,255,255,0.72);
    margin-top: 6px;
    font-weight: 400;
}

.hero-tag {
    display: inline-block;
    background: rgba(255,255,255,0.14);
    color: white;
    font-size: 12.5px;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 999px;
    margin-bottom: 14px;
}

/* -------------------- WELCOME / AVATAR -------------------- */

.welcome-row {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 4px;
}

.avatar-circle {
    width: 52px;
    height: 52px;
    min-width: 52px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), #C97F17);
    color: white;
    font-family: 'Fraunces', serif;
    font-size: 22px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 8px rgba(227, 162, 52, 0.35);
}

/* -------------------- CHAPTER CARDS -------------------- */

.chapter-card {
    background-color: white;
    padding: 26px 24px 22px 24px;
    border-radius: 16px;
    border: 1px solid var(--border);
    min-height: 190px;
    box-shadow: 0 2px 8px rgba(16, 35, 63, 0.05);
    position: relative;
    overflow: hidden;
    transition: all 0.15s ease;
}

.chapter-card:hover {
    box-shadow: 0 10px 22px rgba(16, 35, 63, 0.12);
    transform: translateY(-3px);
    border-color: var(--indigo);
}

.chapter-ghost-num {
    position: absolute;
    top: -6px;
    right: 14px;
    font-family: 'Fraunces', serif;
    font-size: 58px;
    font-weight: 700;
    color: var(--paper);
    -webkit-text-stroke: 1.4px var(--border);
    z-index: 0;
}

.chapter-glyph {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: var(--accent-soft);
    color: var(--indigo);
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 17px;
    margin-bottom: 12px;
    position: relative;
    z-index: 1;
}

.chapter-card h3 {
    margin-top: 0;
    margin-bottom: 6px;
    color: var(--ink);
    position: relative;
    z-index: 1;
    font-size: 1.15rem;
}

.chapter-card p {
    color: var(--muted);
    font-size: 0.92rem;
    position: relative;
    z-index: 1;
    margin-bottom: 10px;
}

.chapter-best {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 600;
    background: var(--success-soft);
    color: var(--success);
    padding: 3px 10px;
    border-radius: 999px;
    position: relative;
    z-index: 1;
}

.chapter-best.empty {
    background: var(--paper);
    color: var(--muted);
    border: 1px dashed var(--border);
}

/* -------------------- QUIZ PROGRESS -------------------- */

.quiz-meta-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 6px;
    flex-wrap: wrap;
    gap: 8px;
}

.quiz-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
    font-weight: 600;
    color: var(--indigo);
    background: var(--accent-soft);
    padding: 5px 12px;
    border-radius: 999px;
}

.stProgress > div > div > div {
    background-color: var(--indigo);
}

.stProgress > div > div {
    background-color: var(--border);
}

/* -------------------- QUESTION NUMBER BADGE -------------------- */

.q-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 30px;
    height: 30px;
    border-radius: 9px;
    background: var(--indigo);
    color: white;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 13px;
    margin-right: 10px;
}

.q-header {
    display: flex;
    align-items: center;
    margin-bottom: 4px;
}

.q-header span.q-text {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: 1.05rem;
    color: var(--ink);
}

/* -------------------- RESULT CARD -------------------- */

.result-card {
    background-color: white;
    padding: 38px 30px;
    border-radius: 18px;
    border: 1px solid var(--border);
    text-align: center;
    box-shadow: 0 4px 16px rgba(16, 35, 63, 0.07);
}

.result-ring {
    width: 128px;
    height: 128px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 18px auto;
    font-family: 'Fraunces', serif;
    font-size: 28px;
    font-weight: 700;
    color: white;
    box-shadow: 0 6px 18px rgba(16, 35, 63, 0.18);
}

.ring-good { background: linear-gradient(135deg, #2E9E6D, #1F7A55); }
.ring-mid  { background: linear-gradient(135deg, #E3A234, #C97F17); }
.ring-low  { background: linear-gradient(135deg, #D8553D, #B23F2B); }

.result-score {
    font-size: 42px;
    font-weight: 700;
    color: var(--ink);
    font-family: 'Fraunces', serif;
}

.result-message {
    font-size: 15px;
    color: var(--muted);
    margin-top: 4px;
}

.result-tag {
    display: inline-block;
    font-size: 12.5px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 999px;
    margin-bottom: 14px;
}

.tag-good { background: var(--success-soft); color: var(--success); }
.tag-mid  { background: var(--warning-soft); color: #A9741E; }
.tag-low  { background: var(--danger-soft); color: var(--danger); }

/* -------------------- LEADERBOARD -------------------- */

.podium-row {
    display: flex;
    gap: 14px;
    align-items: flex-end;
    margin: 10px 0 26px 0;
}

.podium-card {
    flex: 1;
    background: white;
    border-radius: 14px;
    border: 1px solid var(--border);
    text-align: center;
    padding: 18px 10px 16px 10px;
    box-shadow: 0 2px 8px rgba(16, 35, 63, 0.05);
}

.podium-card.first {
    border-color: var(--accent);
    box-shadow: 0 8px 20px rgba(227, 162, 52, 0.25);
    transform: translateY(-10px);
}

.podium-medal {
    font-size: 26px;
    margin-bottom: 4px;
}

.podium-name {
    font-family: 'Fraunces', serif;
    font-weight: 700;
    color: var(--ink);
    font-size: 1rem;
    margin-bottom: 2px;
    word-break: break-word;
}

.podium-score {
    font-family: 'JetBrains Mono', monospace;
    color: var(--indigo);
    font-weight: 600;
    font-size: 0.9rem;
}

.rank-row {
    display: flex;
    align-items: center;
    background: white;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 16px;
    margin-bottom: 8px;
}

.rank-row.me {
    border-color: var(--indigo);
    background: #F7FAFF;
}

.rank-num {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    color: var(--muted);
    width: 32px;
}

.rank-name {
    flex-grow: 1;
    font-weight: 600;
    color: var(--ink);
}

.rank-score {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    color: var(--indigo);
}

/* -------------------- BREADCRUMB -------------------- */

.breadcrumb {
    font-size: 13.5px;
    color: var(--muted);
    font-weight: 500;
    margin-bottom: 2px;
}

.breadcrumb b {
    color: var(--indigo);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# USER DATA FUNCTIONS
# ============================================================

def load_users():

    if not os.path.exists(USER_FILE):
        return {}

    try:

        with open(
            USER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            return data

        return {}

    except (json.JSONDecodeError, OSError):

        return {}


def save_users(users):

    os.makedirs("data", exist_ok=True)

    with open(
        USER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=4
        )


def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# QUIZ DATA FUNCTIONS
# ============================================================

def is_valid_question(question):

    if not isinstance(question, dict):
        return False

    if "question" not in question:
        return False

    if "options" not in question:
        return False

    if "answer" not in question:
        return False

    if not isinstance(question["question"], str):
        return False

    if not isinstance(question["options"], list):
        return False

    if len(question["options"]) == 0:
        return False

    answer = question["answer"]

    if isinstance(answer, bool):
        return False

    if not isinstance(answer, int):
        return False

    if answer < 0:
        return False

    if answer >= len(question["options"]):
        return False

    return True


def find_questions(data):

    # --------------------------------------------------------
    # Direct list of questions
    # --------------------------------------------------------

    if isinstance(data, list):

        questions = []

        for item in data:

            if is_valid_question(item):
                questions.append(item)

        if questions:
            return questions

        # Check nested lists as well
        for item in data:

            result = find_questions(item)

            if result:
                return result

        return []


    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    if isinstance(data, dict):

        # First check common quiz names
        preferred_keys = [
            "questions",
            "quiz",
            "sets",
            "relations",
            "relation",
            "trigonometry",
            "relations_and_functions",
            "relation_and_functions",
            "relations_functions"
        ]

        for key in preferred_keys:

            if key in data:

                result = find_questions(
                    data[key]
                )

                if result:
                    return result

        # Then check every value
        for value in data.values():

            result = find_questions(value)

            if result:
                return result

    return []


def load_quiz(file_path):

    if not os.path.exists(file_path):
        return []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

    except (json.JSONDecodeError, OSError):

        return []

    return find_questions(data)


# ============================================================
# LEADERBOARD FUNCTIONS
# ============================================================

def load_leaderboard():

    if not os.path.exists(LEADERBOARD_FILE):
        return {}

    try:

        with open(
            LEADERBOARD_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, dict):
            return data

        return {}

    except (json.JSONDecodeError, OSError):

        return {}


def save_leaderboard(data):

    os.makedirs("data", exist_ok=True)

    with open(
        LEADERBOARD_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


def save_quiz_score(
    username,
    quiz_name,
    score,
    total
):

    leaderboard = load_leaderboard()

    if username not in leaderboard:

        leaderboard[username] = {
            "Sets": {
                "score": 0,
                "total": 0
            },
            "Relations & Functions": {
                "score": 0,
                "total": 0
            },
            "Trigonometry": {
                "score": 0,
                "total": 0
            }
        }

    if quiz_name not in leaderboard[username]:

        leaderboard[username][quiz_name] = {
            "score": 0,
            "total": 0
        }

    leaderboard[username][quiz_name] = {
        "score": score,
        "total": total
    }

    save_leaderboard(leaderboard)


def get_best_score(username, quiz_key):
    """Look up a user's stored score for a chapter, tolerant of either
    the display name or the lowercase key being used in the file."""

    leaderboard = load_leaderboard()

    user_scores = leaderboard.get(username, {})

    if not isinstance(user_scores, dict):
        return None

    lookup_names = [
        CHAPTER_META.get(quiz_key, {}).get("label", quiz_key),
        quiz_key
    ]

    for name in lookup_names:

        entry = user_scores.get(name)

        if isinstance(entry, dict) and entry.get("total", 0) > 0:
            return entry

    return None


# ============================================================
# SESSION STATE
# ============================================================

if "users" not in st.session_state:

    st.session_state.users = load_users()


if "page" not in st.session_state:

    st.session_state.page = "authentication"


if "logged_in_user" not in st.session_state:

    st.session_state.logged_in_user = None


if "quiz_score" not in st.session_state:

    st.session_state.quiz_score = 0


if "quiz_total" not in st.session_state:

    st.session_state.quiz_total = 0


if "current_quiz" not in st.session_state:

    st.session_state.current_quiz = ""


if "current_quiz_name" not in st.session_state:

    st.session_state.current_quiz_name = ""


if "quiz_attempt" not in st.session_state:

    st.session_state.quiz_attempt = 0


# ============================================================
# QUIZ HELPER FUNCTIONS
# ============================================================

def get_quiz_widget_key(
    quiz_key,
    question_number
):

    return (
        f"{quiz_key}_"
        f"attempt_{st.session_state.quiz_attempt}_"
        f"question_{question_number}"
    )


def start_quiz(
    quiz_key,
    page_name
):

    st.session_state.quiz_attempt += 1

    st.session_state.current_quiz = quiz_key

    st.session_state.page = page_name

    st.rerun()


def calculate_and_submit_quiz(
    questions,
    quiz_name,
    quiz_key
):

    unanswered = []

    for i in range(len(questions)):

        widget_key = get_quiz_widget_key(
            quiz_key,
            i
        )

        selected = st.session_state.get(
            widget_key
        )

        if selected is None:

            unanswered.append(i + 1)


    if unanswered:

        numbers = ", ".join(
            str(number)
            for number in unanswered
        )

        st.warning(
            f"Please answer question(s): {numbers}"
        )

        return


    score = 0

    for i, question in enumerate(questions):

        widget_key = get_quiz_widget_key(
            quiz_key,
            i
        )

        selected = st.session_state.get(
            widget_key
        )

        correct_answer = question["options"][
            question["answer"]
        ]

        if selected == correct_answer:

            score += 1


    st.session_state.quiz_score = score

    st.session_state.quiz_total = len(
        questions
    )

    st.session_state.current_quiz = quiz_key

    st.session_state.current_quiz_name = quiz_name


    if st.session_state.logged_in_user:

        save_quiz_score(
            st.session_state.logged_in_user,
            quiz_name,
            score,
            len(questions)
        )


    st.session_state.page = "quiz_result"

    st.rerun()


def render_quiz_page(quiz_file, quiz_name, quiz_key, title):
    """Shared, polished renderer used by every chapter quiz page."""

    meta = CHAPTER_META.get(quiz_key, {})

    st.markdown(
        f'<div class="breadcrumb">Home &nbsp;&rsaquo;&nbsp; '
        f'<b>{meta.get("label", title)}</b></div>',
        unsafe_allow_html=True
    )

    st.title(title)

    questions = load_quiz(quiz_file)

    if not questions:

        st.error(
            f"No valid {title} questions were found."
        )

        st.info(
            f"Check {quiz_file}."
        )

    else:

        answered = 0

        for i in range(len(questions)):

            widget_key = get_quiz_widget_key(quiz_key, i)

            if st.session_state.get(widget_key) is not None:
                answered += 1

        st.markdown(
            f"""
            <div class="quiz-meta-row">
                <span class="quiz-pill">{answered} / {len(questions)} answered</span>
                <span class="quiz-pill">{len(questions)} questions total</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(answered / len(questions))

        st.write("")


        for i, question in enumerate(questions):

            with st.container(border=True):

                st.markdown(
                    f"""
                    <div class="q-header">
                        <span class="q-badge">{i + 1}</span>
                        <span class="q-text">{question["question"]}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")

                st.radio(
                    "Choose your answer:",
                    question["options"],
                    index=None,
                    key=get_quiz_widget_key(quiz_key, i),
                    label_visibility="collapsed"
                )

            st.write("")


        st.write("")

        submit_col, _ = st.columns([1, 3])

        with submit_col:

            if st.button(
                "Submit Quiz",
                key=f"submit_{quiz_key}",
                use_container_width=True
            ):

                calculate_and_submit_quiz(
                    questions,
                    quiz_name,
                    quiz_key
                )


    st.divider()

    if st.button(
        "\u2190 Back to Home",
        key=f"back_{quiz_key}"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# AUTHENTICATION PAGE
# ============================================================

if st.session_state.page == "authentication":

    left, mid, right = st.columns([1, 2, 1])

    with mid:

        st.markdown(
            """
            <div class="hero" style="text-align:center; padding: 44px 30px;">
                <div class="hero-tag">Class 11 &middot; Mathematics</div>
                <div class="brand">Hello Math</div>
                <div class="brand-subtitle">
                    Sharpen your Sets, Relations &amp; Functions and
                    Trigonometry with focused practice quizzes.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        login_tab, signup_tab = st.tabs(
            ["Login", "Sign Up"]
        )


        # ========================================================
        # LOGIN
        # ========================================================

        with login_tab:

            with st.container(border=True):

                st.markdown("#### Welcome back")

                username = st.text_input(
                    "Username",
                    key="login_username",
                    placeholder="Enter your username"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password",
                    placeholder="Enter your password"
                )

                if st.button(
                    "Login",
                    key="login_button",
                    use_container_width=True
                ):

                    if not username or not password:

                        st.error(
                            "Please enter your username and password."
                        )

                    elif username not in st.session_state.users:

                        st.error(
                            "Username not found. Please sign up first."
                        )

                    else:

                        user_data = (
                            st.session_state.users[username]
                        )

                        stored_hash = ""

                        if isinstance(user_data, dict):

                            stored_hash = user_data.get(
                                "password",
                                ""
                            )

                        elif isinstance(user_data, str):

                            stored_hash = user_data

                        entered_hash = hash_password(
                            password
                        )

                        if entered_hash == stored_hash:

                            st.session_state.logged_in_user = username

                            st.session_state.page = "home"

                            st.rerun()

                        else:

                            st.error(
                                "Incorrect password."
                            )


        # ========================================================
        # SIGN UP
        # ========================================================

        with signup_tab:

            with st.container(border=True):

                st.markdown("#### Create your account")

                new_username = st.text_input(
                    "Choose a username",
                    key="signup_username",
                    placeholder="At least 3 characters"
                )

                new_password = st.text_input(
                    "Create a password",
                    type="password",
                    key="signup_password",
                    placeholder="At least 8 characters"
                )

                confirm_password = st.text_input(
                    "Confirm password",
                    type="password",
                    key="signup_confirm_password",
                    placeholder="Re-enter your password"
                )

                if st.button(
                    "Create Account",
                    key="signup_button",
                    use_container_width=True
                ):

                    if (
                        not new_username
                        or not new_password
                        or not confirm_password
                    ):

                        st.error(
                            "Please fill in all fields."
                        )

                    elif len(new_username) < 3:

                        st.error(
                            "Username must be at least 3 characters long."
                        )

                    elif new_username in st.session_state.users:

                        st.error(
                            "Username already exists."
                        )

                    elif len(new_password) < 8:

                        st.error(
                            "Password must be at least 8 characters long."
                        )

                    elif new_password != confirm_password:

                        st.error(
                            "Passwords do not match."
                        )

                    else:

                        password_hash = hash_password(
                            new_password
                        )

                        st.session_state.users[new_username] = {
                            "password": password_hash
                        }

                        save_users(
                            st.session_state.users
                        )

                        st.success(
                            "Account created successfully. You can now log in."
                        )


# ============================================================
# HOME PAGE
# ============================================================

elif st.session_state.page == "home":

    username = st.session_state.logged_in_user or "?"

    initial = username[0].upper() if username else "?"

    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-tag">Class 11 &middot; Mathematics</div>
            <div class="welcome-row">
                <div class="avatar-circle">{initial}</div>
                <div>
                    <div class="brand" style="font-size:30px;">Welcome, {username}</div>
                    <div class="brand-subtitle">Pick a chapter below and keep your streak going.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.header("Choose a Chapter")


    col1, col2, col3 = st.columns(3)

    columns = {
        "sets": col1,
        "relations": col2,
        "trigonometry": col3
    }


    # ========================================================
    # CHAPTER CARDS (Sets, Relations & Functions, Trigonometry)
    # ========================================================

    for quiz_key, column in columns.items():

        meta = CHAPTER_META[quiz_key]

        best = get_best_score(username, quiz_key)

        if best:

            best_html = (
                f'<span class="chapter-best">'
                f'Best: {best.get("score", 0)} / {best.get("total", 0)}'
                f'</span>'
            )

        else:

            best_html = (
                '<span class="chapter-best empty">Not attempted yet</span>'
            )

        with column:

            st.markdown(
                f"""
                <div class="chapter-card">
                    <div class="chapter-ghost-num">{meta['number']}</div>
                    <div class="chapter-glyph">{meta['glyph']}</div>
                    <h3>{meta['label']}</h3>
                    <p>{meta['blurb']}</p>
                    {best_html}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            if st.button(
                "Start Quiz",
                key=f"{quiz_key}_quiz",
                use_container_width=True
            ):

                start_quiz(
                    quiz_key,
                    f"{quiz_key}_quiz"
                )


    st.divider()


    # ========================================================
    # LEADERBOARD
    # ========================================================

    lb_col, logout_col = st.columns([3, 1])

    with lb_col:

        st.subheader("Leaderboard")

        st.caption(
            "See how your quiz performance compares with everyone else."
        )

        if st.button(
            "View Leaderboard",
            key="leaderboard_button"
        ):

            st.session_state.page = "leaderboard"

            st.rerun()

    with logout_col:

        st.write("")
        st.write("")

        if st.button(
            "Logout",
            key="logout_button",
            use_container_width=True
        ):

            st.session_state.logged_in_user = None

            st.session_state.page = "authentication"

            st.rerun()


# ============================================================
# SETS QUIZ PAGE
# ============================================================

elif st.session_state.page == "sets_quiz":

    render_quiz_page(
        SETS_QUIZ_FILE,
        "Sets",
        "sets",
        "Sets Quiz"
    )


# ============================================================
# RELATIONS & FUNCTIONS QUIZ PAGE
# ============================================================

elif st.session_state.page == "relations_quiz":

    render_quiz_page(
        RELATIONS_QUIZ_FILE,
        "Relations & Functions",
        "relations",
        "Relations & Functions Quiz"
    )


# ============================================================
# TRIGONOMETRY QUIZ PAGE
# ============================================================

elif st.session_state.page == "trigonometry_quiz":

    render_quiz_page(
        TRIGONOMETRY_QUIZ_FILE,
        "Trigonometry",
        "trigonometry",
        "Trigonometry Quiz"
    )


# ============================================================
# QUIZ RESULT PAGE
# ============================================================

elif st.session_state.page == "quiz_result":

    quiz_name = st.session_state.get(
        "current_quiz_name",
        "Quiz"
    )

    score = st.session_state.get(
        "quiz_score",
        0
    )

    total = st.session_state.get(
        "quiz_total",
        0
    )

    percentage = 0

    if total > 0:

        percentage = (
            score / total
        ) * 100

    if percentage >= 80:
        ring_class, tag_class, tag_text, message = (
            "ring-good", "tag-good", "Excellent",
            "Strong grasp of this chapter \u2014 keep it up!"
        )
    elif percentage >= 50:
        ring_class, tag_class, tag_text, message = (
            "ring-mid", "tag-mid", "Good effort",
            "You're on the right track. A little more practice will help."
        )
    else:
        ring_class, tag_class, tag_text, message = (
            "ring-low", "tag-low", "Keep practicing",
            "Revisit the concepts and give this chapter another attempt."
        )

    left, mid, right = st.columns([1, 2, 1])

    with mid:

        st.markdown(
            f"""
            <div class="breadcrumb">Home &nbsp;&rsaquo;&nbsp;
            <b>{quiz_name}</b> &nbsp;&rsaquo;&nbsp; Results</div>
            """,
            unsafe_allow_html=True
        )

        st.title(f"{quiz_name} Results")

        st.markdown(f"""
        <div class="result-card">
            <div class="result-tag {tag_class}">{tag_text}</div>
            <div class="result-ring {ring_class}">{percentage:.0f}%</div>
            <div class="result-score">{score} / {total}</div>
            <p class="result-message">{message}</p>
        </div>
        """, unsafe_allow_html=True)


        st.write("")


        # ========================================================
        # TRY AGAIN / BACK TO HOME
        # ========================================================

        again_col, home_col = st.columns(2)

        with again_col:

            if st.button(
                "Try Again",
                key="try_again",
                use_container_width=True
            ):

                quiz_key = st.session_state.current_quiz

                st.session_state.quiz_attempt += 1


                if quiz_key == "sets":

                    st.session_state.page = "sets_quiz"

                elif quiz_key == "relations":

                    st.session_state.page = "relations_quiz"

                elif quiz_key == "trigonometry":

                    st.session_state.page = "trigonometry_quiz"

                st.rerun()

        with home_col:

            if st.button(
                "Back to Home",
                key="back_result",
                use_container_width=True
            ):

                st.session_state.page = "home"

                st.rerun()


# ============================================================
# LEADERBOARD PAGE
# ============================================================

elif st.session_state.page == "leaderboard":

    st.markdown(
        '<div class="breadcrumb">Home &nbsp;&rsaquo;&nbsp; <b>Leaderboard</b></div>',
        unsafe_allow_html=True
    )

    st.title("Leaderboard")

    st.caption("Combined score across Sets, Relations & Functions and Trigonometry.")

    leaderboard = load_leaderboard()


    if not leaderboard:

        st.info(
            "No quiz scores have been recorded yet. Be the first to take a quiz!"
        )

    else:

        rows = []

        current_user = st.session_state.logged_in_user

        for username, scores in leaderboard.items():

            if not isinstance(scores, dict):
                continue


            sets_score = scores.get(
                "Sets",
                {}
            )

            relations_score = scores.get(
                "Relations & Functions",
                {}
            )

            trig_score = scores.get(
                "Trigonometry",
                {}
            )


            if not isinstance(
                sets_score,
                dict
            ):
                sets_score = {}


            if not isinstance(
                relations_score,
                dict
            ):
                relations_score = {}


            if not isinstance(
                trig_score,
                dict
            ):
                trig_score = {}


            total_score = (
                sets_score.get("score", 0)
                + relations_score.get("score", 0)
                + trig_score.get("score", 0)
            )


            total_questions = (
                sets_score.get("total", 0)
                + relations_score.get("total", 0)
                + trig_score.get("total", 0)
            )


            rows.append({
                "Username": username,
                "Total Score": total_score,
                "Total Questions": total_questions
            })


        rows.sort(
            key=lambda x: x["Total Score"],
            reverse=True
        )

        if not rows:

            st.info(
                "No quiz scores have been recorded yet. Be the first to take a quiz!"
            )

        else:

            # ----------------------------------------------------
            # PODIUM for the top 3
            # ----------------------------------------------------

            top_three = rows[:3]

            medals = ["\U0001F947", "\U0001F948", "\U0001F949"]

            podium_cards = []

            for idx, row in enumerate(top_three):

                card_class = "podium-card first" if idx == 0 else "podium-card"

                podium_cards.append(
                    f'<div class="{card_class}">'
                    f'<div class="podium-medal">{medals[idx]}</div>'
                    f'<div class="podium-name">{row["Username"]}</div>'
                    f'<div class="podium-score">{row["Total Score"]} / {row["Total Questions"]}</div>'
                    f'</div>'
                )

            podium_html = (
                '<div class="podium-row">'
                + "".join(podium_cards)
                + "</div>"
            )

            if top_three:

                st.markdown(podium_html, unsafe_allow_html=True)


            # ----------------------------------------------------
            # Full ranked list
            # ----------------------------------------------------

            for position, row in enumerate(rows):

                is_me = row["Username"] == current_user

                row_class = "rank-row me" if is_me else "rank-row"

                you_tag = " &nbsp;<span style='color:#E3A234; font-weight:700;'>(You)</span>" if is_me else ""

                st.markdown(
                    f"""
                    <div class="{row_class}">
                        <div class="rank-num">#{position + 1}</div>
                        <div class="rank-name">{row['Username']}{you_tag}</div>
                        <div class="rank-score">{row['Total Score']} / {row['Total Questions']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    st.divider()

    if st.button(
        "\u2190 Back to Home",
        key="back_leaderboard"
    ):

        st.session_state.page = "home"

        st.rerun()
