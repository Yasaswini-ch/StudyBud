import streamlit as st

from llm import chat, PROVIDERS
from prompts import (
    PERSONA_SYSTEM_PROMPT,
    EXPLAIN_PROMPT,
    EXAMPLE_PROMPT,
    QUIZ_PROMPT,
    FEEDBACK_PROMPT,
    FULL_SESSION_PROMPT,
)

st.set_page_config(page_title="AI Learning Buddy", page_icon="🧠", layout="centered")

DEFAULT_TOPIC = "How Bitcoin Mining Works"

if "history" not in st.session_state:
    st.session_state.history = []  # list of (role, content) for display
if "last_quiz" not in st.session_state:
    st.session_state.last_quiz = None

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("Provider", list(PROVIDERS.keys()))
    api_key = st.text_input(f"{provider} API key", type="password", help="Never stored, used only for this session.")
    model = st.text_input("Model", value=PROVIDERS[provider]["default_model"])
    topic = st.text_input("Topic", value=DEFAULT_TOPIC)
    num_questions = st.slider("Quiz questions", min_value=3, max_value=10, value=5)

    with st.expander("🎭 Buddy's persona (system prompt)"):
        st.code(PERSONA_SYSTEM_PROMPT, language="text")

    if st.button("Clear conversation"):
        st.session_state.history = []
        st.session_state.last_quiz = None
        st.rerun()

st.title("🧠 AI Learning Buddy")
st.caption(f"Currently tutoring: **{topic}** via **{provider}**")


def call_llm(user_prompt: str) -> str:
    return chat(provider, api_key, model, PERSONA_SYSTEM_PROMPT, st.session_state.history, user_prompt)


def ask(prompt_text: str, display_label: str):
    if not api_key:
        st.error(f"Add your {provider} API key in the sidebar to talk to Buddy.")
        return
    st.session_state.history.append(("user", display_label))
    with st.spinner("Buddy is thinking..."):
        try:
            reply = call_llm(prompt_text)
        except Exception as e:
            st.session_state.history.pop()
            st.error(f"{provider} request failed: {e}")
            return
    st.session_state.history.append(("assistant", reply))


# ---------- Activity picker ----------
activity = st.radio(
    "What should Buddy do?",
    ["📖 Explain the topic", "🌍 Give a real-life example", "📝 Quiz me", "🚀 Full session", "✅ Get feedback on an answer"],
    horizontal=False,
)

if activity == "📖 Explain the topic":
    if st.button("Explain it simply"):
        ask(EXPLAIN_PROMPT.format(topic=topic), f"Explain: {topic}")

elif activity == "🌍 Give a real-life example":
    if st.button("Give me an example"):
        ask(EXAMPLE_PROMPT.format(topic=topic), f"Give a real-life example of: {topic}")

elif activity == "📝 Quiz me":
    if st.button("Generate quiz"):
        if not api_key:
            st.error(f"Add your {provider} API key in the sidebar to talk to Buddy.")
        else:
            prompt_text = QUIZ_PROMPT.format(topic=topic, num_questions=num_questions)
            st.session_state.history.append(("user", f"Quiz me on: {topic}"))
            with st.spinner("Buddy is writing your quiz..."):
                try:
                    reply = call_llm(prompt_text)
                except Exception as e:
                    st.session_state.history.pop()
                    st.error(f"{provider} request failed: {e}")
                    reply = None
            if reply is not None:
                st.session_state.history.append(("assistant", reply))
                st.session_state.last_quiz = reply

elif activity == "🚀 Full session":
    if st.button("Start full lesson"):
        prompt_text = FULL_SESSION_PROMPT.format(topic=topic, num_questions=num_questions)
        ask(prompt_text, f"Start a full learning session on: {topic}")

elif activity == "✅ Get feedback on an answer":
    if not st.session_state.last_quiz:
        st.info("Generate a quiz first (under 'Quiz me' or 'Full session'), then come back here to submit an answer.")
    else:
        with st.expander("Show the quiz again"):
            st.write(st.session_state.last_quiz)
        question = st.text_input("Paste the question you're answering")
        learner_answer = st.text_area("Your answer")
        if st.button("Check my answer"):
            if question and learner_answer:
                prompt_text = FEEDBACK_PROMPT.format(topic=topic, question=question, learner_answer=learner_answer)
                ask(prompt_text, f"My answer to '{question}': {learner_answer}")
            else:
                st.warning("Fill in both the question and your answer first.")

# ---------- Conversation display ----------
st.divider()
st.subheader("Conversation")
if not st.session_state.history:
    st.write("No conversation yet — pick an activity above to get started.")
for role, content in st.session_state.history:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.write(content)
