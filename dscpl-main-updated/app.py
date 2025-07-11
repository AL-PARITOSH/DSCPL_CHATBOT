import streamlit as st
from gemini_chain import get_chat_chain
from rag.rag_chain import get_rag_context
from utils import get_sos_message, get_reflection_prompt, generate_ics
from video_links import video_map
import random
import datetime

# --- Page Config ---
st.set_page_config(page_title="DSCPL - Your Spiritual Companion", layout="wide")

# --- Constants ---
CATEGORY_TOPICS = {
    "Devotion": ["Dealing with Stress", "Overcoming Fear", "Conquering Depression", "Relationships", "Healing", "Purpose & Calling", "Anxiety", "Something else..."],
    "Prayer": ["Personal Growth", "Healing", "Family/Friends", "Forgiveness", "Finances", "Work/Career", "Something else..."],
    "Meditation": ["Peace", "God's Presence", "Strength", "Wisdom", "Faith", "Something else..."],
    "Accountability": ["Pornography", "Alcohol", "Drugs", "Sex", "Addiction", "Laziness", "Something else..."]
}

PROMPT_TEMPLATES = {
    "Devotion": """You are a wise Christian spiritual mentor speaking to your beloved disciple. Provide a 5-minute devotion on the topic '{topic}' that includes:
1. A Bible Verse
2. A short reflective prayer
3. A faith-based declaration
Speak with a pastoral, scripture-rooted, and encouraging voice.""",
    "Prayer": """You are a compassionate spiritual companion. Based on the topic '{topic}', lead a prayer using the ACTS model:
- Adoration
- Confession
- Thanksgiving
- Supplication
Let the tone be humble, heartfelt, and grounded in faith.""",
    "Meditation": """You are a peaceful Christian meditation guide. On the topic '{topic}', provide:
1. A scripture focus
2. Two reflective prompts
3. A breathing rhythm (Inhale 4s, Hold 4s, Exhale 4s)
Use a voice filled with grace and calm.""",
    "Accountability": """You are a spiritual accountability mentor. For the topic '{topic}', provide:
1. A strength-based Bible verse
2. A truth declaration rooted in faith
3. A healthy alternative action
4. A short SOS encouragement
Be gentle, understanding, and scripture-infused."""
}

EMERGENCY_MESSAGES = [
    "🚘 I'm here for you. Let's pause and breathe together... 🌬️<br><br><b>'The Lord is my strength and my shield.'</b> (Psalm 28:7)<br><br>You are not alone. You are loved. 💖",
    "🌟 Even now, God's love surrounds you.<br><br><b>'When I am afraid, I put my trust in You.'</b> (Psalm 56:3)<br><br>You are stronger than this. 💪",
    "💖 Pause. Breathe. You're doing your best.<br><br><b>'Come to me, all who are weary, and I will give you rest.'</b> (Matthew 11:28)<br><br>You're not alone.",
    "🙏 Let your heart rest in God's presence.<br><br><b>'Be still and know that I am God.'</b> (Psalm 46:10)<br><br>You are seen. You are valued.",
    "🕊️ It's okay to need help.<br><br><b>'Cast your cares on the Lord and He will sustain you.'</b> (Psalm 55:22)<br><br>I'm here for you.",
]

# --- CSS ---
def inject_css():
    st.markdown("""
        <style>
            .sos-box {
                background-color: #F8FAFC;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                border-left: 5px solid #7F5AF0;
            }
            .sos-yes-btn {
                display: inline-block;
                background-color: #7F5AF0;
                color: white;
                padding: 8px 16px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

# --- Emergency SOS Button ---
def render_sos_button():
    top = st.columns([9, 1])
    with top[1]:
        if st.button("🚨 Emergency SOS", key="sos"):
            st.session_state.sos_triggered = True

def render_sos_message():
    if st.session_state.get("sos_triggered", False):
        msg = random.choice(EMERGENCY_MESSAGES)
        st.markdown(f"""
            <div class='sos-box'>
                <b>💬 Immediate Encouragement:</b><br><br>
                {msg}<br><br>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Okay", key="sos_ok"):
            st.session_state.sos_triggered = False
            st.rerun()
            
# --- Header ---
def create_header():
    st.markdown("""
        <div style='text-align: center; margin-top: 2rem; margin-bottom: 1rem;'>
            <span style='font-size: 2.5rem;'>🧘</span>
            <span style='font-size: 2.5rem; font-weight: bold; color: #7F5AF0;'>DSCPL</span>
            <div style='color: #94A3B8; font-size: 1.2rem; margin-top: 0.3rem;'>Your Spiritual Companion</div>
        </div>
        <hr style='border: 1px solid #eee;'>
    """, unsafe_allow_html=True)

# --- Session State Init ---
def initialize_session_state():
    if "stage" not in st.session_state:
        st.session_state.update({
            "stage": "category",
            "selected_category": None,
            "selected_topic": None,
            "duration_days": 1,
            "chat_history": [],
            "program_active": False,
            "program_day": 1,
            "program_total_days": 0,
            "program_category": None,
            "program_topic": None,
            "history": [],
            "sos_triggered": False
        })

# --- Helpers ---
def button_deck(prompt, options, key_prefix):
    st.markdown(f"<div style='margin-bottom:10px; font-weight: bold;'>{prompt}</div>", unsafe_allow_html=True)
    rows = [options[:3], options[3:]]
    for r, row in enumerate(rows):
        cols = st.columns(3)
        for i, option in enumerate(row):
            if i < len(cols) and cols[i].button(option, key=f"{key_prefix}_{r}_{option}"):
                return option
    return None

def show_video_for_topic(category):
    videos = video_map.get(category, [])
    if videos:
        video = random.choice(videos)
        st.markdown(f"<h5 style='margin-top: 1rem;'>🎥 {video['title']}</h5>", unsafe_allow_html=True)
        st.video(video["url"])

# --- Stages ---
def category_selection():
    st.markdown("### ✨ Choose Spiritual Focus Anytime")
    choice = button_deck("What do you need today?", ["Devotion", "Prayer", "Meditation", "Accountability", "Just Chat"], "main_category")
    if choice:
        st.session_state.selected_category = choice
        if choice == "Just Chat":
            st.switch_page("pages/just_chat.py")
        else:
            st.session_state.stage = "duration"
        st.rerun()

def duration_selection():
    if "duration_choice" not in st.session_state:
        choice = button_deck("How many days would you like this program for?", ["Today Only", "3 Days", "7 Days", "14 Days", "30 Days", "Custom Duration"], "duration")
        if choice:
            st.session_state.duration_choice = choice
            st.rerun()
    else:
        choice = st.session_state.duration_choice
        if choice in ["Today Only", "3 Days", "7 Days", "14 Days", "30 Days"]:
            st.session_state.duration_days = int(choice.split()[0]) if choice != "Today Only" else 1
            del st.session_state.duration_choice
            st.session_state.stage = "topic"
            st.rerun()
        elif choice == "Custom Duration":
            days = st.number_input("Enter custom number of days:", min_value=1, max_value=30, step=1)
            if st.button("Confirm Duration"):
                st.session_state.duration_days = days
                del st.session_state.duration_choice
                st.session_state.stage = "topic"
                st.rerun()

def topic_selection():
    category = st.session_state.selected_category
    topics = CATEGORY_TOPICS.get(category, [])
    topic = button_deck(f"What topic would you like help with in {category.lower()}?", topics, "topic")
    if topic:
        st.session_state.selected_topic = topic
        st.session_state.program_active = True
        st.session_state.program_day = 1
        st.session_state.program_total_days = st.session_state.duration_days
        st.session_state.program_category = category
        st.session_state.program_topic = topic
        st.session_state.stage = "program"
        st.rerun()

def program_execution():
    cat = st.session_state.program_category
    topic = st.session_state.program_topic
    day = st.session_state.program_day
    total = st.session_state.program_total_days
    st.markdown(f"## 📅 Day {day} of {total} – {cat}: {topic}")
    prompt = PROMPT_TEMPLATES[cat].format(topic=topic)
    response = chat_chain.invoke({"input": prompt}, config={"configurable": {"session_id": "default"}})
    st.session_state.chat_history.append({"role": "assistant", "content": response.content})
    st.markdown(response.content)
    show_video_for_topic(cat)

    if st.button("✅ Mark Day Complete"):
        st.session_state.history.append({
            "date": str(datetime.date.today()),
            "category": cat,
            "topic": topic,
            "day": day,
            "total_days": total
        })
        if day >= total:
            st.success("🎉 You’ve completed your program! Well done!")
            st.session_state.program_active = False
            st.session_state.stage = "category"
        else:
            st.session_state.program_day += 1
        st.rerun()

def calendar_export():
    if st.session_state.program_active and st.button("📆 Export to Calendar (.ics)"):
        data = generate_ics(st.session_state.program_category, st.session_state.program_topic, st.session_state.program_total_days)
        st.download_button("Download .ics", data=data, file_name="dscpl_program.ics")

def progress_dashboard():
    if st.session_state.history:
        st.markdown("## 📊 Progress Dashboard")
        st.markdown("Track your spiritual journey:")
        all_cats = list({h['category'] for h in st.session_state.history})
        filter_cat = st.selectbox("📂 Filter by Category", ["All"] + sorted(all_cats))
        for i, h in enumerate(st.session_state.history):
            if filter_cat != "All" and h["category"] != filter_cat:
                continue
            st.markdown(f"""
                <div style='background-color:#F1F5F9; padding:15px; border-radius:10px; margin-bottom:15px;'>
                    <b>📅 Date:</b> {h['date']}<br>
                    <b>🧘 Category:</b> {h['category']}<br>
                    <b>📝 Topic:</b> {h['topic']}<br>
                    <b>📈 Day:</b> {h['day']} / {h.get('total_days', '❓')}
                </div>
            """, unsafe_allow_html=True)

# --- MAIN ---
def main():
    inject_css()
    initialize_session_state()
    render_sos_button()
    render_sos_message()
    create_header()

    global chat_chain
    chat_chain = get_chat_chain()

    if st.session_state.stage == "category":
        category_selection()
    elif st.session_state.stage == "duration":
        duration_selection()
    elif st.session_state.stage == "topic":
        topic_selection()
    elif st.session_state.stage == "program":
        program_execution()

    calendar_export()
    progress_dashboard()

if __name__ == "__main__":
    main()
