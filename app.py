import os
from datetime import datetime
import json
from streamlit_lottie import st_lottie
import pandas as pd
import plotly.express as px
import streamlit as st

from analytics import (
    calculate_topic_performance,
    classification_distribution,
    detect_repeated_mistakes,
    get_overall_metrics,
    get_weak_topics,
    performance_over_time,
    subject_performance,
)
from database import (
    authenticate_student,
    create_student,
    get_answers,
    get_student,
    init_indexes,
    insert_question,
    is_connected,
    list_questions,
    list_students,
    list_subjects,
    list_topics,
    register_student,
    save_quiz_attempt,
    show_connection_help,
    update_question,
    update_student,
    update_topic,
    upsert_subject,
    upsert_topic,
)
from models import DIFFICULTIES
from quiz import get_quiz_questions, grade_quiz
from recommendations import generate_recommendation
from seed_data import seed_database

st.set_page_config(
    page_title="Student Performance & Weakness Analyzer",
    page_icon="🎓",
    layout="wide",
)


def safe_run(action, fallback=None):
    """Keep the UI friendly instead of showing raw Python tracebacks."""
    try:
        return action()
    except Exception:
        st.error("Something went wrong while processing this action. Please check your data and try again.")
        return fallback


def setup_app():
    if not is_connected():
        show_connection_help()
        st.info("After adding your MongoDB Atlas URI, run: streamlit run app.py")
        return False
    init_indexes()
    seed_database(force=False)
    return True


# ============================================================
# LOGIN PAGE — GLASSMORPHISM DESIGN
# ============================================================
def login_page():
    st.markdown("""
    <style>
        /* ---------- Main Background: soft pastel gradient ---------- */
        .stApp {
            background: linear-gradient(135deg,
                #b8c6f0 0%,
                #d4b8e8 35%,
                #f0c8e0 70%,
                #f5d8c8 100%);
        }

        /* ---------- Floating Bokeh Circles ---------- */
        .stApp::before {
            content: '';
            position: fixed;
            top: -200px;
            right: -200px;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, rgba(180, 150, 240, 0.5), transparent 70%);
            border-radius: 50%;
            filter: blur(60px);
            pointer-events: none;
            animation: floatBokeh1 18s ease-in-out infinite;
            z-index: 0;
        }

        .stApp::after {
            content: '';
            position: fixed;
            bottom: -200px;
            left: -200px;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle, rgba(240, 180, 220, 0.5), transparent 70%);
            border-radius: 50%;
            filter: blur(70px);
            pointer-events: none;
            animation: floatBokeh2 22s ease-in-out infinite;
            z-index: 0;
        }

        @keyframes floatBokeh1 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(-40px, 40px) scale(1.1); }
        }

        @keyframes floatBokeh2 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(50px, -30px) scale(1.15); }
        }

        /* ---------- Streamlit columns as glass cards ---------- */
        [data-testid="stHorizontalBlock"] {
            gap: 2rem;
            align-items: center;
        }

        [data-testid="column"] {
            background: rgba(255, 255, 255, 0.22);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 30px;
            padding: 30px 25px;
            box-shadow: 0 25px 50px rgba(80, 60, 120, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.6);
        }

        /* ---------- Speech bubble ---------- */
        .speech-bubble {
            position: relative;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 14px 18px;
            margin: 15px auto 0 auto;
            max-width: 320px;
            text-align: center;
            font-size: 14px;
            color: #5a4a8a;
            font-weight: 600;
            box-shadow: 0 10px 30px rgba(80, 60, 120, 0.15);
            animation: pulseBubble 3s ease-in-out infinite;
        }

        @keyframes pulseBubble {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }

        .speech-bubble:after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 10px 10px 0;
            border-style: solid;
            border-color: rgba(255, 255, 255, 0.85) transparent transparent transparent;
        }

        /* ---------- Titles ---------- */
        .glass-title {
            text-align: center;
            font-size: 30px;
            font-weight: 800;
            color: #4a3a7a;
            margin-bottom: 6px;
            text-shadow: 0 2px 10px rgba(255, 255, 255, 0.5);
            letter-spacing: -0.5px;
        }

        .glass-subtitle {
            text-align: center;
            color: #6a5a9a;
            font-size: 14px;
            margin-bottom: 20px;
            font-weight: 500;
        }

        .login-card-title {
            text-align: center;
            font-size: 24px;
            font-weight: 700;
            color: #4a3a7a;
            margin-bottom: 5px;
            letter-spacing: -0.3px;
        }

        .login-subtitle {
            text-align: center;
            color: #7a6aaa;
            font-size: 13px;
            margin-bottom: 20px;
        }

        /* ---------- Tabs ---------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            justify-content: center;
            background: rgba(255, 255, 255, 0.3);
            padding: 6px;
            border-radius: 14px;
            backdrop-filter: blur(10px);
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 10px;
            padding: 8px 22px;
            font-weight: 600;
            color: #5a4a8a;
            border: none;
            font-size: 14px;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%) !important;
            color: white !important;
            box-shadow: 0 8px 20px rgba(167, 139, 250, 0.4);
        }

        /* ---------- Inputs ---------- */
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            padding: 12px 16px;
            font-size: 14px;
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
            color: #4a3a7a;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input::placeholder {
            color: #9a8aba;
        }

        .stTextInput > div > div > input:focus {
            border-color: #a78bfa;
            background: rgba(255, 255, 255, 0.75);
            box-shadow: 0 0 0 4px rgba(167, 139, 250, 0.2);
        }

        .stTextInput > label {
            color: #5a4a8a !important;
            font-weight: 600 !important;
            font-size: 13px !important;
        }

        /* ---------- Primary button ---------- */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%);
            color: white;
            border: none;
            border-radius: 14px;
            padding: 14px 20px;
            font-size: 15px;
            font-weight: 700;
            width: 100%;
            box-shadow: 0 12px 25px rgba(167, 139, 250, 0.4);
            transition: all 0.3s ease;
            letter-spacing: 0.3px;
        }

        .stButton > button[kind="primary"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 16px 30px rgba(167, 139, 250, 0.5);
        }

        /* ---------- Form container ---------- */
        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.15);
            padding: 22px;
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }

        /* ---------- Stat pills ---------- */
        .stat-pill {
            display: inline-block;
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(10px);
            padding: 8px 14px;
            border-radius: 20px;
            color: #5a4a8a;
            font-size: 12px;
            font-weight: 600;
            margin: 4px 3px;
            border: 1px solid rgba(255, 255, 255, 0.7);
            box-shadow: 0 4px 12px rgba(80, 60, 120, 0.08);
        }

               /* ---------- Hide Streamlit chrome ---------- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* ---------- Floating emojis around character ---------- */
        .float-emoji {
            position: absolute;
            font-size: 22px;
            opacity: 0.75;
            pointer-events: none;
            animation: floatUpDown 3.5s ease-in-out infinite;
        }
        
        .emoji-1 { top: 5%; left: 8%; animation-delay: 0s; }
        .emoji-2 { top: 15%; right: 10%; animation-delay: 0.5s; }
        .emoji-3 { top: 45%; left: 3%; animation-delay: 1s; }
        .emoji-4 { top: 55%; right: 4%; animation-delay: 1.5s; }
        .emoji-5 { bottom: 15%; left: 10%; animation-delay: 2s; }
        .emoji-6 { bottom: 5%; right: 12%; animation-delay: 2.5s; }
        
        @keyframes floatUpDown {
            0%, 100% { transform: translateY(0) rotate(0deg); opacity: 0.6; }
            50% { transform: translateY(-12px) rotate(10deg); opacity: 1; }
        }
        
        /* ---------- Feature list ---------- */
        .feature-list {
            margin-top: 25px;
            padding: 18px 20px;
            background: rgba(255, 255, 255, 0.35);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border-radius: 18px;
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: 0 10px 30px rgba(80, 60, 120, 0.1);
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            padding: 7px 4px;
            color: #4a3a7a;
            font-size: 14px;
            font-weight: 600;
            transition: transform 0.2s ease;
        }
        
        .feature-item:hover {
            transform: translateX(5px);
        }
        
        .feature-icon {
            font-size: 18px;
            margin-right: 12px;
            display: inline-block;
            width: 24px;
            text-align: center;
        }
        
        .feature-text {
            letter-spacing: 0.2px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1], gap="large")

    # ==================== LEFT CARD: Anime Character + Features ====================
    with left_col:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="glass-title">🎓 Student Analyzer</div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-subtitle">Analyze. Learn. Improve. 🌟</div>', unsafe_allow_html=True)

        # ---- Character with floating emojis around it ----
        st.markdown("""
        <div style="position: relative; text-align: center; padding: 10px 0;">
            <span class="float-emoji emoji-1">✨</span>
            <span class="float-emoji emoji-2">📚</span>
            <span class="float-emoji emoji-3">💡</span>
            <span class="float-emoji emoji-4">🎯</span>
            <span class="float-emoji emoji-5">📖</span>
            <span class="float-emoji emoji-6">⭐</span>
        </div>
        """, unsafe_allow_html=True)

        try:
            img_l, img_c, img_r = st.columns([1, 2, 1])
            with img_c:
                st.image("assets/anime_student.png", width=280)
        except Exception:
            st.markdown("""
            <div style='text-align:center; font-size: 110px; padding: 30px 0;'>
                🧑‍🎓
            </div>
            """, unsafe_allow_html=True)

        # Lottie pencil write animation
        try:
            with open("assets/animation.json", "r", encoding="utf-8") as f:
                lottie_data = json.load(f)
            lot_l, lot_c, lot_r = st.columns([1, 2, 1])
            with lot_c:
                st_lottie(lottie_data, height=100, key="pencil_anim_main")
        except Exception:
            pass

        # Speech bubble
        st.markdown("""
        <div class="speech-bubble">
            💭 "Let's find your weak topics<br>and turn them into strengths!"
        </div>
        """, unsafe_allow_html=True)

        # ---- Feature list ----
        st.markdown("""
        <div class="feature-list">
            <div class="feature-item">
                <span class="feature-icon">✨</span>
                <span class="feature-text">Smart Quiz System</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📊</span>
                <span class="feature-text">Real-time Analytics</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🎯</span>
                <span class="feature-text">Weak Topic Detection</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">💡</span>
                <span class="feature-text">Personalized Recommendations</span>
            </div>
            <div class="feature-item">
                <span class="feature-icon">📈</span>
                <span class="feature-text">Progress Tracking</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align: center; margin-top: 22px;'>
            <span class="stat-pill">📊 Real-time Analytics</span><br>
            <span class="stat-pill">🎯 Weak Detection</span>
            <span class="stat-pill">📈 Progress Tracking</span>
        </div>
        """, unsafe_allow_html=True)

    # ==================== RIGHT CARD: Login Form ====================
    with right_col:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔒 Login", "📝 Register"])

        with tab1:
            st.markdown('<div class="login-card-title">Welcome Back! 👋</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">Login to continue your learning journey</div>', unsafe_allow_html=True)

            with st.form("login_form_main"):
                username = st.text_input("👤 Username", placeholder="Enter your username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Login →", type="primary")

                if submitted:
                    if not username.strip() or not password.strip():
                        st.warning("⚠️ Please enter both username and password.")
                    else:
                        user = authenticate_student(username, password)
                        if user:
                            st.session_state["logged_in"] = True
                            st.session_state["student_id"] = user["_id"]
                            st.session_state["student_name"] = user.get("name", "Student")
                            st.success(f"✅ Welcome back, {user.get('name')}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid Username or Password.")

        with tab2:
            st.markdown('<div class="login-card-title">Create Account</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subtitle">Start your journey to mastery today</div>', unsafe_allow_html=True)

            with st.form("register_form_main"):
                new_name = st.text_input("📛 Full Name", placeholder="e.g. Nikita Prajapati")
                new_username = st.text_input("👤 Choose Username", placeholder="Pick a unique username")
                new_password = st.text_input("🔒 Choose Password", type="password", placeholder="Min 4 characters")
                submitted = st.form_submit_button("Create Account →", type="primary")

                if submitted:
                    if not new_name.strip() or not new_username.strip() or not new_password.strip():
                        st.warning("⚠️ Please fill in all fields.")
                    elif len(new_password) < 4:
                        st.warning("⚠️ Password must be at least 4 characters.")
                    else:
                        student_id = register_student(new_username, new_password, new_name)
                        if student_id:
                            st.success("🎉 Account created! Switch to Login tab to sign in.")
                            st.balloons()
                        else:
                            st.error("❌ Username already exists. Try a different one.")


def require_student(student_id):
    if not student_id:
        st.info("Please login to access your profile.")
        return False
    return True


# ============================================================
# DASHBOARD
# ============================================================
def dashboard_page(student_id):
    if not require_student(student_id):
        return

    student = get_student(student_id)
    name = student.get("name", "Student") if student else "Student"
    st.title("🏠 Student Performance & Weakness Analyzer")
    st.caption("MongoDB data storage + Python analytics + weakness detection + rule-based recommendations")
    st.subheader(f"Welcome, {name}")

    metrics = get_overall_metrics(student_id)
    rec = generate_recommendation(student_id)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Accuracy", f"{metrics['overall_accuracy']}%")
    c2.metric("Quizzes Completed", metrics["quizzes_completed"])
    c3.metric("Strongest Subject", metrics["strongest_subject"])
    c4.metric("Weakest Subject", metrics["weakest_subject"])

    st.divider()

    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Top Weak / Practice Topics")
        weak_df = get_weak_topics(student_id, limit=5)
        if weak_df.empty:
            st.info("No weak topic data yet. Take a quiz to generate analysis.")
        else:
            display = weak_df[["subject", "topic", "total_questions", "accuracy", "classification"]]
            st.dataframe(display, hide_index=True, use_container_width=True)

    with right:
        st.subheader("🎯 Recommended Study Topic")
        if not rec:
            st.info("Take at least one quiz to get a recommendation.")
        else:
            st.markdown(f"### {rec['topic']} {rec['classification']}")
            st.write(f"**Subject:** {rec['subject']}")
            st.write(f"**Accuracy:** {rec['accuracy']}%")
            st.write(f"**Incorrect answers:** {rec['incorrect_answers']}")
            st.write(f"**Recent performance:** {rec['recent_performance']}")
            st.write(f"**Why?** {rec['reason']}")
            st.success(f"Recommended action: {rec['recommended_action']}")

    st.subheader("Recent Quiz Results")
    hist = performance_over_time(student_id)
    if hist.empty:
        st.info("No quiz attempts yet. Go to Take Quiz to start.")
    else:
        recent = hist.sort_values("submitted_at", ascending=False).head(8).copy()
        recent["submitted_at"] = recent["submitted_at"].dt.strftime("%Y-%m-%d %H:%M")
        st.dataframe(recent, hide_index=True, use_container_width=True)


# ============================================================
# QUIZ INTERFACE
# ============================================================
def render_quiz_interface(student_id, questions, subject, topic):
    st.subheader(f"{subject} → {topic}")
    selected_answers = {}
    with st.form("quiz_form"):
        for index, q in enumerate(questions, start=1):
            st.markdown(f"**Q{index}. {q['question']}**")
            selected_answers[str(q["_id"])] = st.radio(
                "Choose one answer",
                q["options"],
                key=f"answer_{q['_id']}",
                label_visibility="collapsed",
            )
            st.caption(f"Difficulty: {q.get('difficulty', 'Medium')}")
            st.write("")

        submitted = st.form_submit_button("Submit Quiz", type="primary")

    if submitted:
        answer_rows = grade_quiz(questions, selected_answers)
        attempt_id = save_quiz_attempt(student_id, subject, topic, answer_rows)
        if attempt_id is None:
            st.error("Could not save this attempt. Please check MongoDB connection.")
            return

        correct = sum(1 for row in answer_rows if row["is_correct"])
        total = len(answer_rows)
        percentage = round((correct / total) * 100, 2) if total else 0
        st.session_state["last_result"] = {"answers": answer_rows, "score": f"{correct}/{total}", "percentage": percentage}
        st.success("Quiz submitted and saved to MongoDB.")

    result = st.session_state.get("last_result")
    if result:
        st.subheader("Quiz Result")
        c1, c2 = st.columns(2)
        c1.metric("Score", result["score"])
        c2.metric("Accuracy", f"{result['percentage']}%")

        for i, row in enumerate(result["answers"], start=1):
            if row["is_correct"]:
                st.success(f"Q{i}: Correct — {row['question']}")
            else:
                st.error(f"Q{i}: Incorrect — {row['question']}")
                st.write(f"Your answer: {row['student_answer']}")
                st.write(f"Correct answer: {row['correct_answer']}")


def take_quiz_page(student_id):
    if not require_student(student_id):
        return

    st.title("📝 Take Quiz")

    tab1, tab2 = st.tabs(["📚 Select Topic Quiz", "🎯 Smart Weak Topic Practice"])

    with tab1:
        subjects = list_subjects()
        if not subjects:
            st.warning("No subjects found. Seed sample data from the Management page.")
            return

        col1, col2, col3 = st.columns(3)
        subject = col1.selectbox("Subject", subjects)
        topics = [t["name"] for t in list_topics(subject)]
        if not topics:
            st.warning("No topics found for this subject.")
            return
        topic = col2.selectbox("Topic", topics)
        available_count = len(list_questions(subject, topic))
        max_questions = max(1, available_count)
        num_questions = col3.number_input("Number of questions", min_value=1, max_value=max_questions, value=min(5, max_questions), key="num_q_standard")

        if available_count == 0:
            st.warning("This topic has no questions yet. Add questions in Management.")
            return

        if st.button("Start Standard Quiz", type="primary"):
            st.session_state["quiz_questions"] = get_quiz_questions(subject, topic, int(num_questions))
            st.session_state["quiz_subject"] = subject
            st.session_state["quiz_topic"] = topic
            st.session_state.pop("last_result", None)

    with tab2:
        st.caption("Automatically target your weak areas to improve accuracy.")
        weak_df = get_weak_topics(student_id, limit=5)
        if weak_df.empty:
            st.info("No weak topics detected yet! Complete a few standard quizzes first.")
        else:
            weak_options = [f"{row['subject']} — {row['topic']} ({row['accuracy']}% accuracy)" for _, row in weak_df.iterrows()]
            selected_weak = st.selectbox("Choose a weak topic to practice", weak_options)

            idx = weak_options.index(selected_weak)
            target_row = weak_df.iloc[idx]

            if st.button("Start Targeted Practice Quiz", type="primary"):
                questions = get_quiz_questions(target_row["subject"], target_row["topic"], 5)
                if questions:
                    st.session_state["quiz_questions"] = questions
                    st.session_state["quiz_subject"] = target_row["subject"]
                    st.session_state["quiz_topic"] = target_row["topic"]
                    st.session_state.pop("last_result", None)
                else:
                    st.warning("No questions available for this weak topic.")

    questions = st.session_state.get("quiz_questions", [])
    if questions:
        st.divider()
        render_quiz_interface(student_id, questions, st.session_state.get("quiz_subject"), st.session_state.get("quiz_topic"))


# ============================================================
# WEAK TOPICS
# ============================================================
def weak_topics_page(student_id):
    if not require_student(student_id):
        return

    st.title("⚠️ Weak Topics")
    topic_df = calculate_topic_performance(student_id)
    if topic_df.empty:
        st.info("No performance data yet. Take quizzes to detect weak topics.")
        return

    st.subheader("Topic Performance Classification")
    st.caption("Thresholds: Below 65% = Weak, 65% to 84% = Needs Practice, 85% or above = Strong")
    st.dataframe(
        topic_df[[
            "subject",
            "topic",
            "total_questions",
            "correct_answers",
            "incorrect_answers",
            "accuracy",
            "recent_mistakes",
            "classification",
        ]],
        hide_index=True,
        use_container_width=True,
    )

    weakest = topic_df.iloc[0]
    st.error(f"Weakest topic: {weakest['topic']} — {weakest['accuracy']}% {weakest['classification']}")

    st.subheader("Repeated Mistake Detection")
    repeated_df = detect_repeated_mistakes(student_id)
    if repeated_df.empty:
        st.info("No repeated poor performance detected yet. At least two attempts on a topic are helpful for this analysis.")
    else:
        for _, row in repeated_df.iterrows():
            with st.container(border=True):
                st.markdown(f"### {row['topic']}")
                for i, score in enumerate(row["attempts"], start=1):
                    st.write(f"Attempt {i}: {score}")
                st.write(f"Accuracy: {row['average_accuracy']}%")
                st.warning(row["message"])


# ============================================================
# PROGRESS ANALYTICS
# ============================================================
def progress_page(student_id):
    if not require_student(student_id):
        return

    st.title("📊 Progress Analytics")
    topic_df = calculate_topic_performance(student_id)
    subj_df = subject_performance(student_id)
    time_df = performance_over_time(student_id)
    dist_df = classification_distribution(student_id)

    if topic_df.empty:
        st.info("No chart data yet. Complete a quiz to see progress analytics.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Subject Performance")
        fig = px.bar(subj_df, x="subject", y="accuracy", text="accuracy", range_y=[0, 100], color="accuracy", color_continuous_scale="Blues")
        fig.update_layout(yaxis_title="Average Accuracy (%)", xaxis_title="Subject")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Weak / Practice / Strong Distribution")
        fig = px.pie(dist_df, names="classification_text", values="count", hole=0.35)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Topic Performance")
    fig = px.bar(
        topic_df.sort_values("accuracy"),
        x="accuracy",
        y="topic",
        color="classification_text",
        orientation="h",
        text="accuracy",
        range_x=[0, 100],
        color_discrete_map={"Weak": "#E56458", "Needs Practice": "#D5803B", "Strong": "#46A171"},
    )
    fig.update_layout(xaxis_title="Accuracy (%)", yaxis_title="Topic")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Performance Over Time")
    if time_df.empty:
        st.info("No quiz attempts yet.")
    else:
        fig = px.line(time_df, x="submitted_at", y="percentage", color="topic", markers=True, hover_data=["subject", "score"])
        fig.update_layout(yaxis_title="Quiz Accuracy (%)", xaxis_title="Attempt Date", yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("📥 Export Performance Summary")
    csv_data = topic_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Topic Analytics (CSV)",
        data=csv_data,
        file_name=f"performance_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )


# ============================================================
# QUIZ HISTORY
# ============================================================
def quiz_history_page(student_id):
    if not require_student(student_id):
        return

    st.title("📚 Quiz History")
    hist = performance_over_time(student_id)
    if hist.empty:
        st.info("No quiz history yet. Take your first quiz to create history.")
        return

    display = hist.sort_values("submitted_at", ascending=False).copy()
    display["Date"] = display["submitted_at"].dt.strftime("%Y-%m-%d %H:%M")
    display = display.rename(columns={"subject": "Subject", "topic": "Topic", "score": "Score", "percentage": "Accuracy"})
    st.dataframe(display[["Date", "Subject", "Topic", "Score", "Accuracy"]], hide_index=True, use_container_width=True)

    st.download_button(
        label="📥 Download Quiz History (CSV)",
        data=display[["Date", "Subject", "Topic", "Score", "Accuracy"]].to_csv(index=False).encode('utf-8'),
        file_name=f"quiz_history_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

    st.subheader("Attempt Details")
    attempts = performance_over_time(student_id).sort_values("submitted_at", ascending=False)
    if not attempts.empty:
        label_to_attempt = {
            f"{r.submitted_at.strftime('%Y-%m-%d %H:%M')} | {r.subject} | {r.topic} | {r.score}": r
            for _, r in attempts.iterrows()
        }
        selected = st.selectbox("Select an attempt", list(label_to_attempt.keys()))
        answers = get_answers(student_id)
        if answers:
            details = pd.DataFrame(answers)[["question", "topic", "student_answer", "correct_answer", "is_correct", "difficulty"]]
            st.dataframe(details, hide_index=True, use_container_width=True)


# ============================================================
# MANAGEMENT
# ============================================================
def management_page(student_id):
    st.title("⚙️ Management")
    st.caption("Simple CRUD for subjects, topics, and questions.")

    if st.button("Seed / Refresh Sample Data"):
        if seed_database(force=False):
            st.success("Sample data is available.")
        else:
            st.error("Could not seed data because MongoDB is not connected.")

    tab1, tab2 = st.tabs(["Topics", "Questions"])

    with tab1:
        st.subheader("Add Topic")
        subjects = list_subjects() or ["Mathematics", "Physics", "Chemistry"]
        with st.form("add_topic_form"):
            subject = st.selectbox("Subject", subjects)
            new_topic = st.text_input("Topic name")
            submitted = st.form_submit_button("Add Topic")
            if submitted:
                if new_topic.strip():
                    upsert_subject(subject)
                    upsert_topic(subject, new_topic)
                    st.success("Topic added.")
                    st.rerun()
                else:
                    st.warning("Topic name is required.")

        st.subheader("Edit Topic")
        topics = list_topics()
        if topics:
            selected_topic = st.selectbox("Select topic", topics, format_func=lambda t: f"{t['subject']} — {t['name']}")
            updated_subject = st.selectbox("Updated subject", subjects, index=subjects.index(selected_topic["subject"]) if selected_topic["subject"] in subjects else 0)
            updated_name = st.text_input("Updated topic name", value=selected_topic["name"])
            if st.button("Update Topic"):
                update_topic(selected_topic["_id"], updated_subject, updated_name)
                st.success("Topic updated.")
                st.rerun()
        else:
            st.info("No topics yet.")

    with tab2:
        st.subheader("Add Question")
        subjects = list_subjects()
        if not subjects:
            st.info("Add or seed subjects/topics before adding questions.")
            return
        with st.form("add_question_form"):
            subject = st.selectbox("Question subject", subjects)
            topics = [t["name"] for t in list_topics(subject)]
            topic = st.selectbox("Question topic", topics) if topics else st.text_input("Question topic")
            question_text = st.text_area("Question text")
            options_text = st.text_area("Four options, one per line")
            correct_answer = st.text_input("Correct answer")
            difficulty = st.selectbox("Difficulty", DIFFICULTIES)
            submitted = st.form_submit_button("Add Question")
            if submitted:
                options = [o.strip() for o in options_text.splitlines() if o.strip()]
                if not question_text.strip() or len(options) != 4 or correct_answer not in options:
                    st.warning("Enter question text, exactly four options, and a correct answer matching one option.")
                else:
                    insert_question(
                        {
                            "question": question_text.strip(),
                            "options": options,
                            "correct_answer": correct_answer,
                            "subject": subject,
                            "topic": topic,
                            "difficulty": difficulty,
                        }
                    )
                    st.success("Question added.")
                    st.rerun()

        st.subheader("Edit Question")
        questions = list_questions()
        if questions:
            selected_q = st.selectbox("Select question", questions, format_func=lambda q: f"{q['subject']} / {q['topic']} — {q['question'][:60]}")
            with st.form("edit_question_form"):
                q_text = st.text_area("Question", value=selected_q["question"])
                opts_text = st.text_area("Options", value="\n".join(selected_q["options"]))
                corr = st.text_input("Correct answer", value=selected_q["correct_answer"])
                diff = st.selectbox(
                    "Difficulty",
                    DIFFICULTIES,
                    index=DIFFICULTIES.index(selected_q.get("difficulty", "Medium")) if selected_q.get("difficulty", "Medium") in DIFFICULTIES else 1,
                )
                submitted = st.form_submit_button("Update Question")
                if submitted:
                    opts = [o.strip() for o in opts_text.splitlines() if o.strip()]
                    if len(opts) != 4 or corr not in opts:
                        st.warning("Use exactly four options and make sure the correct answer matches one option.")
                    else:
                        update_question(selected_q["_id"], {"question": q_text, "options": opts, "correct_answer": corr, "difficulty": diff})
                        st.success("Question updated.")
                        st.rerun()
        else:
            st.info("No questions found.")


# ============================================================
# MAIN
# ============================================================
def main():
    st.sidebar.title("🎓 Analyzer")
    if not setup_app():
        return

    if not st.session_state.get("logged_in", False):
        login_page()
        return

    student_id = st.session_state.get("student_id")
    student_name = st.session_state.get("student_name", "Student")

    st.sidebar.markdown(f"👤 **Logged in as:** {student_name}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state.pop("student_id", None)
        st.session_state.pop("student_name", None)
        st.session_state.pop("quiz_questions", None)
        st.rerun()

    st.sidebar.divider()
    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📝 Take Quiz",
            "⚠️ Weak Topics",
            "📊 Progress",
            "📚 Quiz History",
            "⚙️ Management",
        ],
    )

    if page == "🏠 Dashboard":
        safe_run(lambda: dashboard_page(student_id))
    elif page == "📝 Take Quiz":
        safe_run(lambda: take_quiz_page(student_id))
    elif page == "⚠️ Weak Topics":
        safe_run(lambda: weak_topics_page(student_id))
    elif page == "📊 Progress":
        safe_run(lambda: progress_page(student_id))
    elif page == "📚 Quiz History":
        safe_run(lambda: quiz_history_page(student_id))
    elif page == "⚙️ Management":
        safe_run(lambda: management_page(student_id))


if __name__ == "__main__":
    main()