import streamlit as st
import time
import speech_recognition as sr
from chatbot import get_response, rag_response
from file_loader import load_pdf
from PIL import Image

st.set_page_config(page_title="AI Chatbot Agent", layout="wide")

# ======================
# SIDEBAR
# ======================
with st.sidebar:
    st.header("⚙️ Settings")

    username = st.text_input("Enter your name", "User")

    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []
        st.session_state.pdf_text = None

    # Download chat
    if st.session_state.get("history"):
        chat_text = ""
        for u, b in st.session_state.history:
            chat_text += f"User: {u}\nBot: {b}\n\n"

        st.download_button("⬇️ Download Chat", chat_text, file_name="chat.txt")

# Title
st.title(f"🤖 AI Chatbot Agent - {username}")

# Memory
if "history" not in st.session_state:
    st.session_state.history = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = None

# ======================
# SHOW CHAT
# ======================
for user, bot in st.session_state.history:
    with st.chat_message("user"):
        st.write(user)

    with st.chat_message("assistant"):
        st.write(bot)
        st.code(bot)

# ======================
# INPUT AREA
# ======================
col1, col2, col3 = st.columns([8,1,1])

with col1:
    user_input = st.chat_input("Type a message...")

with col2:
    uploaded_file = st.file_uploader(
        "➕",
        type=["pdf", "png", "jpg", "jpeg"],
        label_visibility="collapsed"
    )

with col3:
    mic = st.button("🎤")

# ======================
# 🎤 VOICE INPUT
# ======================
if mic:
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = recognizer.listen(source)

            user_input = recognizer.recognize_google(audio)
            st.success(f"You said: {user_input}")

    except Exception as e:
        st.error("Mic not working or permission issue")

# ======================
# 📎 FILE HANDLING
# ======================
if uploaded_file:
    file_type = uploaded_file.type

    with st.chat_message("user"):
        st.write(f"📎 {uploaded_file.name}")

    with open("temp_file", "wb") as f:
        f.write(uploaded_file.read())

    # PDF
    if file_type == "application/pdf":
        st.session_state.pdf_text = load_pdf("temp_file")

        with st.chat_message("assistant"):
            st.success("📄 PDF ready! Ask questions.")

    # IMAGE
    else:
        image = Image.open(uploaded_file)

        with st.chat_message("assistant"):
            st.image(image)

        # Simple AI response for image
        with st.chat_message("assistant"):
            st.write("🧠 I can see an image. Ask something about it!")

# ======================
# 🤖 RESPONSE
# ======================
if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        with st.spinner("Thinking... 🤔"):

            if st.session_state.pdf_text:
                response = rag_response(user_input, st.session_state.pdf_text)
            else:
                response = get_response(user_input, st.session_state.history)

        # Typing effect
        full_text = ""
        for word in response.split():
            full_text += word + " "
            placeholder.markdown(full_text + "▌")
            time.sleep(0.02)

        placeholder.markdown(full_text)

        st.code(full_text)

    st.session_state.history.append((user_input, full_text))
