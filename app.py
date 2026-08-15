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


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hello Math",
    page_icon=MATHS_ICON,
    layout="wide"
)


# ============================================================
# CUSTOM COLOUR THEME
# ============================================================

st.markdown("""
<style>

/* =========================================================
   MAIN WEBSITE
   ========================================================= */

.stApp {
    background-color: #F4F7FB;
}


/* =========================================================
   HEADINGS
   ========================================================= */

h1 {
    color: #173B6C;
    font-weight: 700;
}

h2 {
    color: #24558C;
    font-weight: 650;
}

h3 {
    color: #326FA8;
    font-weight: 600;
}


/* =========================================================
   NORMAL TEXT
   ========================================================= */

p {
    color: #26384A;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    background-color: #24558C;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #173B6C;
    color: white;
}


/* =========================================================
   TEXT INPUTS
   ========================================================= */

[data-testid="stTextInput"] input {
    background-color: white;
    color: #26384A;
    border-radius: 8px;
    border: 1px solid #B8C7D9;
}

[data-testid="stTextInput"] input:focus {
    border-color: #24558C;
    box-shadow: 0 0 0 1px #24558C;
}


/* =========================================================
   TABS
   ========================================================= */

button[data-baseweb="tab"] {
    color: #24558C;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #173B6C;
}


/* =========================================================
   QUIZ OPTIONS
   ========================================================= */

[data-testid="stRadio"] {
    background-color: white;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #D8E1EC;
}


/* =========================================================
   DIVIDERS
   ========================================================= */

hr {
    border-color: #D8E1EC;
}


/* =========================================================
   CHAPTER CARDS
   ========================================================= */

.chapter-card {
    background-color: white;
    padding: 25px;
    border-radius: 14px;
    border: 1px solid #D8E1EC;
    min-height: 180px;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.05);
}

.chapter-card h3 {
    margin-top: 0;
    color: #173B6C;
}

.chapter-card p {
    color: #526579;
}


/* =========================================================
   RESULT CARD
   ========================================================= */

.result-card {
    background-color: white;
    padding: 30px;
    border-radius: 14px;
    border: 1px solid #D8E1EC;
    text-align: center;
    box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.05);
}

.result-score {
    font-size: 42px;
    font-weight: 700;
    color: #173B6C;
}


/* =========================================================
   BRAND
   ========================================================= */

.brand {
    font-size: 42px;
    font-weight: 800;
    color: #173B6C;
}

.brand-subtitle {
    font-size: 18px;
    color: #526579;
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
# GENERIC QUIZ LOADER
# ============================================================

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


    # --------------------------------------------------------
    # The quiz files can use different top-level names.
    # We check the common structures.
    # --------------------------------------------------------

    questions = None

    if isinstance(data, dict):

        if isinstance(data.get("questions"), list):

            questions = data["questions"]

        elif isinstance(data.get("sets"), list):

            questions = data["sets"]

        elif isinstance(data.get("quiz"), list):

            questions = data["quiz"]


    elif isinstance(data, list):

        questions = data


    if questions is None:
        return []


    # --------------------------------------------------------
    # Validate every question
    # --------------------------------------------------------

    valid_questions = []

    for question in questions:

        if not isinstance(question, dict):
            continue

        if "question" not in question:
            continue

        if "options" not in question:
            continue

        if "answer" not in question:
            continue

        if not isinstance(question["options"], list):
            continue

        if not isinstance(question["answer"], int):
            continue

        if question["answer"] < 0:
            continue

        if question["answer"] >= len(question["options"]):
            continue

        valid_questions.append(question)

    return valid_questions


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


def save_quiz_score(username, quiz_name, score, total):

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


    leaderboard[username][quiz_name] = {
        "score": score,
        "total": total
    }

    save_leaderboard(leaderboard)


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


# ============================================================
# AUTHENTICATION PAGE
# ============================================================

if st.session_state.page == "authentication":

    st.markdown(
        '<div class="brand">Hello Math</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'Class 11 Mathematics Learning Platform'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()


    login_tab, signup_tab = st.tabs(
        ["Login", "Sign Up"]
    )


    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.header("Login")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            key="login_button"
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

                entered_hash = hash_password(password)

                stored_hash = (
                    st.session_state.users
                    [username]
                    ["password"]
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

        st.header("Create an Account")

        new_username = st.text_input(
            "Choose a username",
            key="signup_username"
        )

        new_password = st.text_input(
            "Create a password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            key="signup_confirm_password"
        )

        if st.button(
            "Create Account",
            key="signup_button"
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

    st.markdown(
        '<div class="brand">Hello Math</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"Welcome, {st.session_state.logged_in_user}!"
    )

    st.write(
        "Choose a chapter to begin your practice."
    )

    st.divider()

    st.header("Choose a Chapter")


    # ========================================================
    # CHAPTER CARDS
    # ========================================================

    col1, col2, col3 = st.columns(3)


    # --------------------------------------------------------
    # SETS
    # --------------------------------------------------------

    with col1:

        st.markdown("""
        <div class="chapter-card">
            <h3>Sets</h3>
            <p>
                Learn and practice questions based on Sets.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button(
            "Start Quiz",
            key="sets_quiz"
        ):

            st.session_state.current_quiz = "sets"

            st.session_state.page = "sets_quiz"

            st.rerun()


    # --------------------------------------------------------
    # RELATIONS & FUNCTIONS
    # --------------------------------------------------------

    with col2:

        st.markdown("""
        <div class="chapter-card">
            <h3>Relations & Functions</h3>
            <p>
                Practice Relations and Functions concepts.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button(
            "Start Quiz",
            key="relations_quiz"
        ):

            st.session_state.current_quiz = "relations"

            st.session_state.page = "relations_quiz"

            st.rerun()


    # --------------------------------------------------------
    # TRIGONOMETRY
    # --------------------------------------------------------

    with col3:

        st.markdown("""
        <div class="chapter-card">
            <h3>Trigonometry</h3>
            <p>
                Practice important Trigonometry concepts.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.button(
            "Start Quiz",
            key="trigonometry_quiz"
        ):

            st.session_state.current_quiz = "trigonometry"

            st.session_state.page = "trigonometry_quiz"

            st.rerun()


    st.divider()


    # ========================================================
    # LEADERBOARD
    # ========================================================

    st.header("Leaderboard")

    st.write(
        "See your quiz performance and compare scores."
    )

    if st.button(
        "View Leaderboard",
        key="leaderboard_button"
    ):

        st.session_state.page = "leaderboard"

        st.rerun()


    st.divider()


    # ========================================================
    # LOGOUT
    # ========================================================

    if st.button(
        "Logout",
        key="logout_button"
    ):

        st.session_state.logged_in_user = None

        st.session_state.page = "authentication"

        st.rerun()


# ============================================================
# SETS QUIZ PAGE
# ============================================================

elif st.session_state.page == "sets_quiz":

    st.title("Sets Quiz")

    questions = load_quiz(
        SETS_QUIZ_FILE
    )

    quiz_name = "Sets"

    quiz_key = "sets"


    if not questions:

        st.error(
            "No valid Sets quiz questions were found."
        )

        st.info(
            "Check data/sets_quiz.json."
        )

    else:

        st.write(
            f"Total Questions: {len(questions)}"
        )

        st.divider()


        for i, question in enumerate(questions):

            st.subheader(
                f"Question {i + 1}"
            )

            st.write(
                question["question"]
            )

            st.radio(
                "Choose your answer:",
                question["options"],
                index=None,
                key=f"{quiz_key}_question_{i}"
            )

            st.divider()


        if st.button(
            "Submit Quiz",
            key="submit_sets"
        ):

            calculate_and_submit_quiz(
                questions,
                quiz_name,
                quiz_key
            )


    if st.button(
        "Back to Home",
        key="back_sets"
    ):

        clear_quiz_answers(quiz_key)

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# RELATIONS & FUNCTIONS QUIZ PAGE
# ============================================================

elif st.session_state.page == "relations_quiz":

    st.title("Relations & Functions Quiz")

    questions = load_quiz(
        RELATIONS_QUIZ_FILE
    )

    quiz_name = "Relations & Functions"

    quiz_key = "relations"


    if not questions:

        st.error(
            "No valid Relations & Functions quiz questions were found."
        )

        st.info(
            "Check data/relations_quiz.json."
        )

    else:

        st.write(
            f"Total Questions: {len(questions)}"
        )

        st.divider()


        for i, question in enumerate(questions):

            st.subheader(
                f"Question {i + 1}"
            )

            st.write(
                question["question"]
            )

            st.radio(
                "Choose your answer:",
                question["options"],
                index=None,
                key=f"{quiz_key}_question_{i}"
            )

            st.divider()


        if st.button(
            "Submit Quiz",
            key="submit_relations"
        ):

            calculate_and_submit_quiz(
                questions,
                quiz_name,
                quiz_key
            )


    if st.button(
        "Back to Home",
        key="back_relations"
    ):

        clear_quiz_answers(quiz_key)

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# TRIGONOMETRY QUIZ PAGE
# ============================================================

elif st.session_state.page == "trigonometry_quiz":

    st.title("Trigonometry Quiz")

    questions = load_quiz(
        TRIGONOMETRY_QUIZ_FILE
    )

    quiz_name = "Trigonometry"

    quiz_key = "trigonometry"


    if not questions:

        st.error(
            "No valid Trigonometry quiz questions were found."
        )

        st.info(
            "Check data/trigonometry_quiz.json."
        )

    else:

        st.write(
            f"Total Questions: {len(questions)}"
        )

        st.divider()


        for i, question in enumerate(questions):

            st.subheader(
                f"Question {i + 1}"
            )

            st.write(
                question["question"]
            )

            st.radio(
                "Choose your answer:",
                question["options"],
                index=None,
                key=f"{quiz_key}_question_{i}"
            )

            st.divider()


        if st.button(
            "Submit Quiz",
            key="submit_trigonometry"
        ):

            calculate_and_submit_quiz(
                questions,
                quiz_name,
                quiz_key
            )


    if st.button(
        "Back to Home",
        key="back_trigonometry"
    ):

        clear_quiz_answers(quiz_key)

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# QUIZ RESULT PAGE
# ============================================================

elif st.session_state.page == "quiz_result":

    st.title(
        f"{st.session_state.current_quiz} Quiz Results"
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


    st.markdown(f"""
    <div class="result-card">

        <div class="result-score">
            {score} / {total}
        </div>

        <p>
            You scored {percentage:.1f}%
        </p>

    </div>
    """, unsafe_allow_html=True)


    st.divider()


    # ========================================================
    # TRY AGAIN
    # ========================================================

    if st.button(
        "Try Again",
        key="try_again"
    ):

        clear_quiz_answers(
            st.session_state.current_quiz
        )

        if st.session_state.current_quiz == "sets":

            st.session_state.page = "sets_quiz"

        elif st.session_state.current_quiz == "relations":

            st.session_state.page = "relations_quiz"

        elif st.session_state.current_quiz == "trigonometry":

            st.session_state.page = "trigonometry_quiz"

        st.rerun()


    # ========================================================
    # BACK TO HOME
    # ========================================================

    if st.button(
        "Back to Home",
        key="back_result"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# LEADERBOARD PAGE
# ============================================================

elif st.session_state.page == "leaderboard":

    st.title("Leaderboard")

    leaderboard = load_leaderboard()


    if not leaderboard:

        st.info(
            "No quiz scores have been recorded yet."
        )

    else:

        rows = []

        for username, scores in leaderboard.items():

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


        for position, row in enumerate(rows):

            st.write(
                f"**{position + 1}. "
                f"{row['Username']}** — "
                f"{row['Total Score']} / "
                f"{row['Total Questions']}"
            )


    st.divider()


    if st.button(
        "Back to Home",
        key="back_leaderboard"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clear_quiz_answers(quiz_key):

    for key in list(st.session_state.keys()):

        if key.startswith(
            f"{quiz_key}_question_"
        ):

            del st.session_state[key]


def calculate_and_submit_quiz(
    questions,
    quiz_name,
    quiz_key
):

    unanswered = []

    for i in range(len(questions)):

        selected = st.session_state.get(
            f"{quiz_key}_question_{i}"
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

        selected = st.session_state[
            f"{quiz_key}_question_{i}"
        ]

        correct = question["options"][
            question["answer"]
        ]

        if selected == correct:

            score += 1


    st.session_state.quiz_score = score

    st.session_state.quiz_total = len(
        questions
    )

    st.session_state.current_quiz = quiz_key


    # --------------------------------------------------------
    # SAVE SCORE
    # --------------------------------------------------------

    if st.session_state.logged_in_user:

        save_quiz_score(
            st.session_state.logged_in_user,
            quiz_name,
            score,
            len(questions)
        )


    clear_quiz_answers(quiz_key)

    st.session_state.page = "quiz_result"

    st.rerun()
