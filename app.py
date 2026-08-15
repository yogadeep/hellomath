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

if os.path.exists(MATHS_ICON):
    st.set_page_config(
        page_title="Hello Math",
        page_icon=MATHS_ICON,
        layout="wide"
    )
else:
    st.set_page_config(
        page_title="Hello Math",
        layout="wide"
    )


# ============================================================
# CUSTOM COLOUR THEME
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

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

p {
    color: #26384A;
}

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

button[data-baseweb="tab"] {
    color: #24558C;
    font-weight: 600;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #173B6C;
}

[data-testid="stRadio"] {
    background-color: white;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #D8E1EC;
}

hr {
    border-color: #D8E1EC;
}

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


    col1, col2, col3 = st.columns(3)


    # ========================================================
    # SETS
    # ========================================================

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

            start_quiz(
                "sets",
                "sets_quiz"
            )


    # ========================================================
    # RELATIONS & FUNCTIONS
    # ========================================================

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

            start_quiz(
                "relations",
                "relations_quiz"
            )


    # ========================================================
    # TRIGONOMETRY
    # ========================================================

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

            start_quiz(
                "trigonometry",
                "trigonometry_quiz"
            )


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
                key=get_quiz_widget_key(
                    quiz_key,
                    i
                )
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
                key=get_quiz_widget_key(
                    quiz_key,
                    i
                )
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
                key=get_quiz_widget_key(
                    quiz_key,
                    i
                )
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

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# QUIZ RESULT PAGE
# ============================================================

elif st.session_state.page == "quiz_result":

    quiz_name = st.session_state.get(
        "current_quiz_name",
        "Quiz"
    )

    st.title(
        f"{quiz_name} Quiz Results"
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

        quiz_key = st.session_state.current_quiz

        st.session_state.quiz_attempt += 1


        if quiz_key == "sets":

            st.session_state.page = "sets_quiz"

        elif quiz_key == "relations":

            st.session_state.page = "relations_quiz"

        elif quiz_key == "trigonometry":

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
