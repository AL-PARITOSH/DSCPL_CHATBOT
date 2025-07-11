# pages/just_chat.py
import streamlit as st
import time
from gemini_chain import get_chat_chain
from rag.rag_chain import get_rag_context

st.set_page_config(page_title="Just Chat – DSCPL", layout="wide")

# Header
st.markdown("""
    <h1 style='text-align: center; font-size: 3rem; color: #7F5AF0;'>🧘 DSCPL</h1>
    <h4 style='text-align: center; color: #94A3B8;'>Your Spiritual Companion</h4>
    <hr>
    <h3 style='text-align: center;'>💬 Welcome to Just Chat</h3>
    <p style='text-align: center;'>This is your space to talk freely — about faith, life, or whatever's on your heart.</p>
""", unsafe_allow_html=True)

chat_chain = get_chat_chain()

# Initialize session states
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_user_input" not in st.session_state:
    st.session_state.pending_user_input = None
if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False

# Show chat messages
for i, message in enumerate(st.session_state.chat_history):
    if message["role"] == "user":
        col1, col2 = st.columns([0.6, 5.4])
        with col1:
            st.markdown("🧑‍💻", unsafe_allow_html=True)
        with col2:
            st.markdown(
                f"<div style='background-color: #E0E7FF; padding: 12px; border-radius: 10px;'>{message['content']}</div>",
                unsafe_allow_html=True,
            )
    else:
        col1, col2 = st.columns([5.4, 0.6])
        with col1:
            st.markdown(
                f"<div style='background-color: #DCFCE7; padding: 12px; border-radius: 10px; text-align: right;'>{message['content']}</div>",
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown("✝️", unsafe_allow_html=True)

    # Add space between messages
    st.markdown("<br>", unsafe_allow_html=True)

# Show typing animation if awaiting response
if st.session_state.awaiting_response:
    col1, col2 = st.columns([5.4, 0.6])
    with col1:
        with st.empty():
            for dot in ["", ".", "..", "..."]:
                st.markdown(
                    f"<div style='background-color: #F0FDF4; padding: 12px; border-radius: 10px; text-align: right;'>✝️ <i>DSCPL is typing{dot}</i></div>",
                    unsafe_allow_html=True,
                )
                time.sleep(0.4)
    with col2:
        st.markdown("✝️", unsafe_allow_html=True)

    # Get response from model
    user_input = st.session_state.pending_user_input
    context = get_rag_context(user_input)
    prompt = f"You are a Christian spiritual mentor responding with scripture, grace, and love. Here's some spiritual context:\n\n{context}\n\nUser said: {user_input}"
    response = chat_chain.invoke({"input": prompt}, config={"configurable": {"session_id": "default"}})

    # Append response and reset
    st.session_state.chat_history.append({"role": "assistant", "content": response.content})
    st.session_state.awaiting_response = False
    st.session_state.pending_user_input = None
    st.rerun()

# 🔽 Dummy div to scroll to
st.markdown("<div id='bottom-of-chat'></div>", unsafe_allow_html=True)
# 🧠 JS to scroll to that div
st.markdown("""
    <script>
        var bottom = document.getElementById("bottom-of-chat");
        if (bottom) {
            bottom.scrollIntoView({behavior: "smooth"});
        }
    </script>
""", unsafe_allow_html=True)

# User input box
if user_input := st.chat_input("Type your thoughts here..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.pending_user_input = user_input
    st.session_state.awaiting_response = True
    st.rerun()
