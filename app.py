import streamlit as st
import json
import os
import hashlib


# ============================================================
# SETTINGS
# ============================================================

USER_FILE = "data/user.json"
SETS_QUIZ_FILE = "data/sets_quiz.json"
MATHS_ICON = "ICON/maths_icon.png"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hello Math",
    page_icon=MATHS_ICON,
    layout="wide"
)


# ============================================================
# CUSTOM WEBSITE STYLE
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #F4F7FB;
}

/* Main headings */

h1 {
    color: #173B6C;
}

h2 {
    color: #24558C;
}

h3 {
    color: #326FA8;
}


/* Buttons */

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


/* Text input */

[data-testid="stTextInput"] input {
    border-radius: 8px;
    border: 1px solid #B8C7D9;
}

[data-testid="stTextInput"] input:focus {
    border-color: #24558C;
    box-shadow: 0 0 0 1px #24558C;
}


/* Quiz radio buttons */

[data-testid="stRadio"] {
    background-color: white;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #D8E1EC;
}


/* Dividers */

hr {
    border-color: #D8E1EC;
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
# SETS QUIZ DATA FUNCTIONS
# ============================================================

def load_sets_quiz():

    if not os.path.exists(SETS_QUIZ_FILE):
        return []

    try:

        with open(
            SETS_QUIZ_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, dict):
            return []

        questions = data.get("sets", [])

        if not isinstance(questions, list):
            return []

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

    except (json.JSONDecodeError, OSError):

        return []


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


# ============================================================
# AUTHENTICATION PAGE
# ============================================================

if st.session_state.page == "authentication":

    st.title("Hello Math")

    st.write(
        "Welcome to the Mathematics learning platform."
    )

    st.divider()

    login_tab, signup_tab = st.tabs(
        [
            "Login",
            "Sign Up"
        ]
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

                entered_password_hash = hash_password(
                    password
                )

                stored_password_hash = (
                    st.session_state.users[username]["password"]
                )

                if entered_password_hash == stored_password_hash:

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
                    "Username already exists. Please choose another username."
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

    st.title("Hello Math")

    st.subheader(
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

        st.subheader("Sets")

        st.write(
            "Learn and practice questions based on Sets."
        )

        if st.button(
            "Start Quiz",
            key="sets_quiz"
        ):

            st.session_state.page = "sets_quiz"

            st.rerun()


    # ========================================================
    # RELATIONS & FUNCTIONS
    # ========================================================

    with col2:

        st.subheader("Relations & Functions")

        st.write(
            "Practice Relations and Functions."
        )

        if st.button(
            "Start Quiz",
            key="relations_quiz"
        ):

            st.session_state.page = "relations"

            st.rerun()


    # ========================================================
    # TRIGONOMETRY
    # ========================================================

    with col3:

        st.subheader("Trigonometry")

        st.write(
            "Practice important Trigonometry concepts."
        )

        if st.button(
            "Start Quiz",
            key="trigonometry_quiz"
        ):

            st.session_state.page = "trigonometry"

            st.rerun()


    st.divider()

    st.header("Leaderboard")

    st.write(
        "See how you compare with other students."
    )

    if st.button(
        "View Leaderboard",
        key="leaderboard"
    ):

        st.session_state.page = "leaderboard"

        st.rerun()


    st.divider()

    if st.button(
        "Logout",
        key="logout"
    ):

        st.session_state.logged_in_user = None

        st.session_state.page = "authentication"

        st.rerun()


# ============================================================
# SETS QUIZ PAGE
# ============================================================

elif st.session_state.page == "sets_quiz":

    st.title("Sets Quiz")

    questions = load_sets_quiz()


    if not questions:

        st.error(
            "No valid Sets quiz questions were found."
        )

        st.info(
            "Check data/sets_quiz.json and make sure "
            "the questions are stored inside the 'sets' list."
        )

        if st.button(
            "Back to Home",
            key="back_no_questions"
        ):

            st.session_state.page = "home"

            st.rerun()

    else:

        st.write(
            f"Total Questions: {len(questions)}"
        )

        st.divider()


        # ====================================================
        # QUESTIONS
        # ====================================================

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
                key=f"sets_question_{i}"
            )

            st.divider()


        # ====================================================
        # SUBMIT QUIZ
        # ====================================================

        if st.button(
            "Submit Quiz",
            key="submit_sets_quiz"
        ):

            unanswered = []

            for i in range(len(questions)):

                selected_answer = st.session_state.get(
                    f"sets_question_{i}"
                )

                if selected_answer is None:

                    unanswered.append(i + 1)


            if unanswered:

                question_numbers = ", ".join(
                    str(number)
                    for number in unanswered
                )

                st.warning(
                    f"Please answer question(s): "
                    f"{question_numbers}"
                )

            else:

                score = 0

                for i, question in enumerate(questions):

                    selected_answer = st.session_state[
                        f"sets_question_{i}"
                    ]

                    correct_answer = question["options"][
                        question["answer"]
                    ]

                    if selected_answer == correct_answer:

                        score += 1


                st.session_state.quiz_score = score

                st.session_state.quiz_total = len(
                    questions
                )

                st.session_state.page = "quiz_result"

                st.rerun()


        if st.button(
            "Back to Home",
            key="back_from_sets_quiz"
        ):

            st.session_state.page = "home"

            st.rerun()


# ============================================================
# QUIZ RESULT PAGE
# ============================================================

elif st.session_state.page == "quiz_result":

    st.title("Quiz Results")

    score = st.session_state.get(
        "quiz_score",
        0
    )

    total = st.session_state.get(
        "quiz_total",
        0
    )

    st.header(
        f"Score: {score} / {total}"
    )

    if total > 0:

        percentage = (
            score / total
        ) * 100

        st.write(
            f"Percentage: {percentage:.1f}%"
        )

    st.divider()


    # ========================================================
    # TRY AGAIN
    # ========================================================

    if st.button(
        "Try Again",
        key="try_sets_again"
    ):

        for key in list(st.session_state.keys()):

            if key.startswith("sets_question_"):

                del st.session_state[key]

        st.session_state.page = "sets_quiz"

        st.rerun()


    # ========================================================
    # BACK TO HOME
    # ========================================================

    if st.button(
        "Back to Home",
        key="back_from_result"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# RELATIONS & FUNCTIONS
# ============================================================

elif st.session_state.page == "relations":

    st.title("Relations & Functions Quiz")

    st.write(
        "The Relations & Functions quiz will be created here."
    )

    if st.button(
        "Back to Home",
        key="back_relations"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# TRIGONOMETRY
# ============================================================

elif st.session_state.page == "trigonometry":

    st.title("Trigonometry Quiz")

    st.write(
        "The Trigonometry quiz will be created here."
    )

    if st.button(
        "Back to Home",
        key="back_trigonometry"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# LEADERBOARD
# ============================================================

elif st.session_state.page == "leaderboard":

    st.title("Leaderboard")

    st.write(
        "The leaderboard will be created here."
    )

    if st.button(
        "Back to Home",
        key="back_leaderboard"
    ):

        st.session_state.page = "home"

        st.rerun()