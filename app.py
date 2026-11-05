"""RecallBuddy Streamlit web UI."""

import os
from dotenv import load_dotenv

import streamlit as st

from ingestion.loader import load_text
from ingestion.chunker import split_into_chunks
from config import build_vectorstore
from quiz.generator import generate_question
from quiz.grader import grade_answer
from progress.tracker import ProgressTracker
from style import apply_custom_css

load_dotenv()

st.set_page_config(page_title="RecallBuddy", page_icon="🧠", layout="wide")
apply_custom_css()

if "initialized" not in st.session_state:
    st.session_state.vectorstore = None
    st.session_state.tracker = ProgressTracker()
    st.session_state.current_q = None
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.q_count = 0
    st.session_state.initialized = True

# ============================================================
# HERO SECTION
# ============================================================
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown(
        """
        <span class="badge">Instant Start</span>
        <span class="badge" style="margin-left:6px;">AI Generated</span>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<h1 style="color: black; font-weight: 900; text-transform: uppercase;">STOP THE SCROLL.<br>TEST YOUR KNOWLEDGE.</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="hero-sub">Your personal AI tutor. Enter a topic, generate a quiz, and see how much you really know.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div style="display:flex; gap:20px; margin-top:20px; font-weight:bold; color:#000000;">
            <div>4.9/5.0<br><span style="font-size:12px; font-weight:normal; color:#000000;">Rating</span></div>
            <div>50,000+<br><span style="font-size:12px; font-weight:normal; color:#000000;">Quizzes Taken</span></div>
            <div>10M+<br><span style="font-size:12px; font-weight:normal; color:#000000;">Questions Asked</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div style="border: 5px solid #000000; border-radius: 16px; padding: 6px;
                    background: #000000;">
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.image("assets/character.png", use_column_width=True)
    st.markdown(
        """
        <div style="border: 5px solid #000000; border-radius: 16px; padding: 6px;
                    background: #000000; margin-top: -8px;">
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================================
# BOTTOM SECTION (Readable Cards)
# ============================================================
col_left, col_mid, col_right = st.columns([1.2, 2, 1.2])

with col_left:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown("### How it works")
    st.markdown(
        """
        <ul>
            <li><strong>1. Load Material</strong> — Build your knowledge base from your notes.</li>
            <li><strong>2. Enter Topic</strong> — Tell us what you want to be quizzed on.</li>
            <li><strong>3. Take Quiz</strong> — Answer, get an explanation, and level up.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_mid:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown("### 📝 The Quiz")

    if "OPENAI_API_KEY" not in os.environ and "GROQ_API_KEY" not in os.environ:
        st.error("API Key not found in .env. Please set OPENAI_API_KEY or GROQ_API_KEY.")

    if st.button("1. Load Study Material", use_container_width=True):
        with st.spinner("Building knowledge base..."):
            text = load_text("data/sample_article.txt")
            chunks = split_into_chunks(text)
            st.session_state.vectorstore = build_vectorstore(chunks)
        st.rerun()

    topic = st.text_input(
        "2. Enter Topic to be quizzed on:",
        value="Artificial Intelligence",
    )

    if st.button("3. Start Quiz", use_container_width=True):
        st.session_state.current_q = None
        st.session_state.answered = False
        st.session_state.feedback = ""
        if st.session_state.vectorstore is None:
            st.error("Load study material first.")
        else:
            try:
                st.session_state.current_q = generate_question(
                    st.session_state.vectorstore, topic
                )
            except Exception as e:
                st.error("API Error: " + str(e))

    # --- Game logic (inside the middle card) ---
    if st.session_state.current_q is not None:
        q = st.session_state.current_q
        st.markdown(f"**{q.question}**")

        user_choice = st.radio("Select Answer:", options=q.options, index=None)

        if (
            st.button("Submit", use_container_width=True)
            and user_choice is not None
            and not st.session_state.answered
        ):
            user_idx = q.options.index(user_choice)
            try:
                st.session_state.feedback = grade_answer(q, user_idx)
            except Exception as e:
                st.session_state.feedback = "API Error: " + str(e)
            is_correct = user_idx == q.correct_index
            st.session_state.tracker.record_attempt(topic, q.question, is_correct)
            st.session_state.answered = True
            st.rerun()

        if st.session_state.answered:
            st.info(st.session_state.feedback)
            if st.button("Next Question", use_container_width=True):
                try:
                    st.session_state.current_q = generate_question(
                        st.session_state.vectorstore, topic
                    )
                except Exception as e:
                    st.error("API Error: " + str(e))
                st.session_state.answered = False
                st.session_state.feedback = ""
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="white-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Your Progress")
    stats = st.session_state.tracker.get_stats()
    st.markdown(
        f"<h1 style='font-size: 3rem; margin: 0; color: #000000;'>{stats['accuracy']}%</h1>",
        unsafe_allow_html=True,
    )
    st.markdown("Accuracy")
    st.markdown(
        f"<span style='background: #B4FF39; padding: 4px 8px; border-radius: 4px; font-weight: bold; color: #000000;'>"
        f"{stats['correct']} Correct out of {stats['total']}</span>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)