# AI Learning Buddy — How Bitcoin Mining Works

An AI Learning Buddy built with Streamlit. It explains a topic, gives a
real-life example, quizzes the learner, and gives feedback on their answers —
using five reusable prompt templates that work for any topic, not just this
one. Supports **OpenAI**, **Groq**, or **Gemini** as the model provider
(switchable from the sidebar), so you're not stuck if one provider's quota
runs out.

## Deliverables (assignment checklist)

| # | Deliverable | Location |
|---|---|---|
| 1 | Topic selected | **How Bitcoin Mining Works** |
| 2 | AI Buddy persona description | [`deliverables/01_persona.md`](deliverables/01_persona.md) |
| 3 | 5 reusable prompt templates | [`deliverables/02_prompt_templates.md`](deliverables/02_prompt_templates.md) (implemented in [`prompts.py`](prompts.py)) |
| 4 | Sample learning conversation | [`deliverables/03_sample_conversation.md`](deliverables/03_sample_conversation.md) |
| 5 | 5-question quiz + answers | [`deliverables/04_quiz_and_answers.md`](deliverables/04_quiz_and_answers.md) |
| 6 | Reflection on AI limitations | [`deliverables/05_reflection.md`](deliverables/05_reflection.md) |
| 7 | Streamlit app | [`app.py`](app.py) (run/deploy instructions below) |

## Running locally

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (default `http://localhost:8501`),
pick a **Provider** (OpenAI, Groq, or Gemini) in the sidebar, paste the
matching API key, and pick an activity: **Explain**, **Real-life example**,
**Quiz me**, **Full session**, or **Get feedback on an answer**.

The API key is only held in memory for your session — it is never written to
disk or logged.

### Where to get a free API key per provider

- **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys) (paid quota).
- **Groq**: [console.groq.com/keys](https://console.groq.com/keys) — free tier, fast open-source models.
- **Gemini**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — free tier, listed in the assignment brief's suggested tools.

## Deploying to Streamlit Community Cloud (for the mandatory app link)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in, and click
   "New app."
3. Point it at this repo, branch, and `app.py`.
4. Deploy, then open the app, pick a provider in the sidebar, and paste the
   matching API key.
5. Confirm the deployed link opens correctly in a fresh, logged-out browser
   tab before submitting.

## Project structure

```
app.py            Streamlit UI
llm.py            Provider-agnostic call wrapper (OpenAI / Groq / Gemini)
prompts.py        The 5 reusable prompt templates + persona system prompt
requirements.txt  Python dependencies
deliverables/     Written submission materials (persona, templates doc,
                  sample conversation, quiz+answers, reflection)
```
