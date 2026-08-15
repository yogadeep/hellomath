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


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Class 11 Mathematics",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# GENERAL JSON FUNCTIONS
# ============================================================

def load_json(file_path, default):

    if not os.path.exists(file_path):
        return default

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return default


def save_json(file_path, data):

    os.makedirs("data", exist_ok=True)

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


# ============================================================
# USER FUNCTIONS
# ============================================================

def load_users():

    data = load_json(
        USER_FILE,
        {}
    )

    if isinstance(data, dict):
        return data

    return {}


def save_users(users):

    save_json(
        USER_FILE,
        users
    )


def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# QUIZ FUNCTIONS
# ============================================================

def load_quiz(file_path, key):

    data = load_json(
        file_path,
        {}
    )

    if not isinstance(data, dict):
        return []

    questions = data.get(
        key,
        []
    )

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

        if not isinstance(
            question["options"],
            list
        ):
            continue

        if not isinstance(
            question["answer"],
            int
        ):
            continue

        if (
            question["answer"] < 0
            or question["answer"] >= len(
                question["options"]
            )
        ):
            continue

        valid_questions.append(
            question
        )

    return valid_questions


def load_sets_quiz():

    return load_quiz(
        SETS_QUIZ_FILE,
        "sets"
    )


def load_relations_quiz():

    return load_quiz(
        RELATIONS_QUIZ_FILE,
        "relations"
    )


def load_trigonometry_quiz():

    return load_quiz(
        TRIGONOMETRY_QUIZ_FILE,
        "trigonometry"
    )


# ============================================================
# LEADERBOARD FUNCTIONS
# ============================================================

def load_leaderboard():

    data = load_json(
        LEADERBOARD_FILE,
        {}
    )

    if isinstance(data, dict):
        return data

    return {}


def save_leaderboard(leaderboard):

    save_json(
        LEADERBOARD_FILE,
        leaderboard
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
            "sets": {
                "score": 0,
                "total": 0
            },
            "relations": {
                "score": 0,
                "total": 0
            },
            "trigonometry": {
                "score": 0,
                "total": 0
            }
        }

    current_score = leaderboard[username][quiz_name]["score"]
    current_total = leaderboard[username][quiz_name]["total"]

    # Save the best result
    if score > current_score:

        leaderboard[username][quiz_name] = {
            "score": score,
            "total": total
        }

    elif score == current_score and total > current_total:

        leaderboard[username][quiz_name] = {
            "score": score,
            "total": total
        }

    save_leaderboard(
        leaderboard
    )


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

    st.session_state.current_quiz = "sets"


# ============================================================
# AUTHENTICATION PAGE
# ============================================================

if st.session_state.page == "authentication":

    st.title("Class 11 Mathematics")

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

                entered_hash = hash_password(
                    password
                )

                stored_hash = (
                    st.session_state.users[
                        username
                    ]["password"]
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

                st.session_state.users[
                    new_username
                ] = {
                    "password": hash_password(
                        new_password
                    )
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

    st.title("Class 11 Mathematics")

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
            "Practice difficult questions based on Sets."
        )

        if st.button(
            "Start Quiz",
            key="sets_quiz"
        ):

            st.session_state.current_quiz = "sets"

            st.session_state.page = "sets_quiz"

            st.rerun()


    # ========================================================
    # RELATIONS & FUNCTIONS
    # ========================================================

    with col2:

        st.subheader("Relations & Functions")

        st.write(
            "Practice difficult questions on Relations and Functions."
        )

        if st.button(
            "Start Quiz",
            key="relations_quiz"
        ):

            st.session_state.current_quiz = "relations"

            st.session_state.page = "relations"

            st.rerun()


    # ========================================================
    # TRIGONOMETRY
    # ========================================================

    with col3:

        st.subheader("Trigonometry")

        st.write(
            "Practice difficult Trigonometry questions."
        )

        if st.button(
            "Start Quiz",
            key="trigonometry_quiz"
        ):

            st.session_state.current_quiz = "trigonometry"

            st.session_state.page = "trigonometry"

            st.rerun()


    st.divider()

    st.header("Leaderboard")

    st.write(
        "View the best quiz scores of all students."
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
# SETS QUIZ
# ============================================================

elif st.session_state.page == "sets_quiz":

    st.title("Sets Quiz")

    questions = load_sets_quiz()

    quiz_name = "sets"


    if not questions:

        st.error(
            "No Sets quiz questions were found."
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
                key=f"sets_question_{i}"
            )

            st.divider()


        if st.button(
            "Submit Quiz",
            key="submit_sets"
        ):

            unanswered = []

            for i in range(len(questions)):

                if st.session_state.get(
                    f"sets_question_{i}"
                ) is None:

                    unanswered.append(
                        i + 1
                    )

            if unanswered:

                st.warning(
                    "Please answer all questions."
                )

            else:

                score = 0

                for i, question in enumerate(
                    questions
                ):

                    selected = st.session_state[
                        f"sets_question_{i}"
                    ]

                    correct = question[
                        "options"
                    ][
                        question["answer"]
                    ]

                    if selected == correct:

                        score += 1

                st.session_state.quiz_score = score

                st.session_state.quiz_total = len(
                    questions
                )

                save_quiz_score(
                    st.session_state.logged_in_user,
                    quiz_name,
                    score,
                    len(questions)
                )

                st.session_state.page = "quiz_result"

                st.rerun()


    if st.button(
        "Back to Home",
        key="sets_home"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# RELATIONS & FUNCTIONS QUIZ
# ============================================================

elif st.session_state.page == "relations":

    st.title("Relations & Functions Quiz")

    questions = load_relations_quiz()

    quiz_name = "relations"


    if not questions:

        st.error(
            "No Relations & Functions quiz questions were found."
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
                key=f"relations_question_{i}"
            )

            st.divider()


        if st.button(
            "Submit Quiz",
            key="submit_relations"
        ):

            unanswered = []

            for i in range(len(questions)):

                if st.session_state.get(
                    f"relations_question_{i}"
                ) is None:

                    unanswered.append(
                        i + 1
                    )

            if unanswered:

                st.warning(
                    "Please answer all questions."
                )

            else:

                score = 0

                for i, question in enumerate(
                    questions
                ):

                    selected = st.session_state[
                        f"relations_question_{i}"
                    ]

                    correct = question[
                        "options"
                    ][
                        question["answer"]
                    ]

                    if selected == correct:

                        score += 1

                st.session_state.quiz_score = score

                st.session_state.quiz_total = len(
                    questions
                )

                save_quiz_score(
                    st.session_state.logged_in_user,
                    quiz_name,
                    score,
                    len(questions)
                )

                st.session_state.page = "quiz_result"

                st.rerun()


    if st.button(
        "Back to Home",
        key="relations_home"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# TRIGONOMETRY QUIZ
# ============================================================

elif st.session_state.page == "trigonometry":

    st.title("Trigonometry Quiz")

    questions = load_trigonometry_quiz()

    quiz_name = "trigonometry"


    if not questions:

        st.error(
            "No Trigonometry quiz questions were found."
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
                key=f"trigonometry_question_{i}"
            )

            st.divider()


        if st.button(
            "Submit Quiz",
            key="submit_trigonometry"
        ):

            unanswered = []

            for i in range(len(questions)):

                if st.session_state.get(
                    f"trigonometry_question_{i}"
                ) is None:

                    unanswered.append(
                        i + 1
                    )

            if unanswered:

                st.warning(
                    "Please answer all questions."
                )

            else:

                score = 0

                for i, question in enumerate(
                    questions
                ):

                    selected = st.session_state[
                        f"trigonometry_question_{i}"
                    ]

                    correct = question[
                        "options"
                    ][
                        question["answer"]
                    ]

                    if selected == correct:

                        score += 1

                st.session_state.quiz_score = score

                st.session_state.quiz_total = len(
                    questions
                )

                save_quiz_score(
                    st.session_state.logged_in_user,
                    quiz_name,
                    score,
                    len(questions)
                )

                st.session_state.page = "quiz_result"

                st.rerun()


    if st.button(
        "Back to Home",
        key="trigonometry_home"
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

    if score == total:

        st.success(
            "Excellent! You answered every question correctly."
        )

    elif score >= total / 2:

        st.info(
            "Good attempt. Keep practising to improve your score."
        )

    else:

        st.warning(
            "Keep practising. You can improve your score with more practice."
        )

    st.divider()

    current_quiz = st.session_state.current_quiz

    if current_quiz == "sets":
        quiz_page = "sets_quiz"

    elif current_quiz == "relations":
        quiz_page = "relations"

    else:
        quiz_page = "trigonometry"


    if st.button(
        "Try Again",
        key="try_again"
    ):

        # Remove previous answers
        for key in list(
            st.session_state.keys()
        ):

            if (
                key.startswith("sets_question_")
                or key.startswith("relations_question_")
                or key.startswith("trigonometry_question_")
            ):

                del st.session_state[key]

        st.session_state.page = quiz_page

        st.rerun()


    if st.button(
        "Back to Home",
        key="result_home"
    ):

        st.session_state.page = "home"

        st.rerun()


# ============================================================
# LEADERBOARD PAGE
# ============================================================

elif st.session_state.page == "leaderboard":

    st.title("Leaderboard")

    st.write(
        "Students are ranked according to their best quiz performance."
    )

    st.divider()

    leaderboard = load_leaderboard()

    if not leaderboard:

        st.info(
            "No quiz scores have been recorded yet."
        )

    else:

        leaderboard_rows = []

        for username, data in leaderboard.items():

            sets_score = data.get(
                "sets",
                {}
            )

            relations_score = data.get(
                "relations",
                {}
            )

            trigonometry_score = data.get(
                "trigonometry",
                {}
            )

            sets_points = sets_score.get(
                "score",
                0
            )

            relations_points = relations_score.get(
                "score",
                0
            )

            trigonometry_points = trigonometry_score.get(
                "score",
                0
            )

            total_score = (
                sets_points
                + relations_points
                + trigonometry_points
            )

            leaderboard_rows.append(
                {
                    "username": username,
                    "sets": sets_points,
                    "relations": relations_points,
                    "trigonometry": trigonometry_points,
                    "total": total_score
                }
            )


        # Sort by total score
        leaderboard_rows.sort(
            key=lambda x: x["total"],
            reverse=True
        )


        st.subheader(
            "Overall Leaderboard"
        )

        for position, student in enumerate(
            leaderboard_rows,
            start=1
        ):

            col1, col2, col3, col4, col5, col6 = st.columns(
                [0.7, 2, 1.2, 1.5, 1.5, 1.2]
            )

            with col1:

                st.write(
                    f"**{position}**"
                )

            with col2:

                st.write(
                    f"**{student['username']}**"
                )

            with col3:

                st.write(
                    f"Sets: {student['sets']}/10"
                )

            with col4:

                st.write(
                    f"Relations: {student['relations']}/10"
                )

            with col5:

                st.write(
                    f"Trigonometry: {student['trigonometry']}/10"
                )

            with col6:

                st.write(
                    f"**{student['total']}/30**"
                )

            st.divider()


    if st.button(
        "Back to Home",
        key="leaderboard_home"
    ):

        st.session_state.page = "home"

        st.rerun()