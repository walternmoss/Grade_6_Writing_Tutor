from google import genai
import streamlit as st

st.title("✍️ 6th Grade Writing & Grammar Tutor")
st.write(
    "Hi George! Paste a sentence you're working on or ask a grammar question"
    " below."
)

# Initialize the Gemini client and store it in session state to prevent client-closed errors
if "client" not in st.session_state:
  if "GEMINI_API_KEY" in st.secrets:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
  else:
    st.error("API key not found in Streamlit secrets.")
    st.stop()

# Initialize chat session using the persisted client instance
if "chat" not in st.session_state:
  st.session_state.chat = st.session_state.client.chats.create(
      model="gemini-2.5-flash",
      config={
          "system_instruction": (
              "You are a friendly, encouraging, and patient writing and"
              " grammar tutor for a 6th-grade student. Never just rewrite his"
              " sentences or give direct answers immediately. Instead, use"
              " Socratic questioning, gentle guidance, and simple explanations"
              " suitable for an 11-year-old to help him find and fix his own"
              " mistakes. The goal is to help him improve his writing and learn."
          )
      },
  )

# Render existing chat history
for message in st.session_state.chat.get_history():
  role = "user" if message.role == "user" else "assistant"
  with st.chat_message(role):
    text_content = "".join([part.text for part in message.parts if part.text])
    st.markdown(text_content)

# Handle user input
if prompt := st.chat_input("Type your sentence or question here..."):
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner("Thinking..."):
      response = st.session_state.chat.send_message(prompt)
      st.markdown(response.text)
