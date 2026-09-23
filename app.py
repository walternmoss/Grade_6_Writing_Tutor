from google import genai
import streamlit as st

st.title("✍️ 6th Grade Writing & Grammar Tutor")
st.write(
    "Hi George! Paste some text you're working on or ask a grammar question"
    " below."
)

# Initialize the Gemini client and store it in session state to prevent client-closed errors
if "client" not in st.session_state:
  if "GEMINI_API_KEY" in st.secrets:
    st.session_state.client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
  else:
    st.error("API key not found in Streamlit secrets.")
    st.stop()

# Initialize chat session with tuned, concise Socratic instructions
if "chat" not in st.session_state:
  st.session_state.chat = st.session_state.client.chats.create(
      model="gemini-2.5-flash",
      config={
          "system_instruction": (
              "You are a friendly, concise, and encouraging writing and"
              " grammar tutor for an 11-year-old 6th-grade student. Do not"
              " rewrite his sentences directly, but keep your guidance"
              " brief. Point out only one error at a time, give a clear"
              " and simple hint, and ask a single guiding question to help"
              " him fix it. Keep your responses short and punchy so he"
              " stays engaged."
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
