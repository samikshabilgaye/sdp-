import os
import streamlit as st

# Import Mistral Client from official library
from mistralai import Mistral

# ----------------------------------------
# Page Title
# ----------------------------------------
st.title("📌 Free Mistral API Chatbot")

# ----------------------------------------
# Load API Key from secrets
# ----------------------------------------
MISTRAL_API_KEY = st.secrets["MISTRAL"]["api_key"]

if not MISTRAL_API_KEY:
    st.error("❌ Add your Mistral API key in .streamlit/secrets.toml")
    st.stop()

# ----------------------------------------
# Initialize Mistral Client
# ----------------------------------------
client = Mistral(api_key=MISTRAL_API_KEY)

# ----------------------------------------
# Chat History in Session
# ----------------------------------------
if "history" not in st.session_state:
    st.session_state["history"] = []

# ----------------------------------------
# User Input
# ----------------------------------------
user_input = st.text_input("Enter your message:")

# ----------------------------------------
# Send to Mistral API
# ----------------------------------------
def get_mistral_response(user_message):
    # build the chat messages list
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_message}
    ]

    # Call the Mistral LLM chat complete endpoint
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=messages,
        response_format={"type": "text"}
    )

    # Extract and return reply
    return response.choices[0].message.content


# ----------------------------------------
# When user hits Enter
# ----------------------------------------
if user_input:
    st.session_state.history.append(
        {"role": "user", "content": user_input}
    )

    with st.spinner("🤖 Thinking..."):
        reply = get_mistral_response(user_input)

        st.session_state.history.append(
            {"role": "assistant", "content": reply}
        )

# ----------------------------------------
# Display Chat History
# ----------------------------------------
for chat in st.session_state.history:
    if chat["role"] == "user":
        st.markdown(f"**You:** {chat['content']}")
    else:
        st.markdown(f"**AI:** {chat['content']}")