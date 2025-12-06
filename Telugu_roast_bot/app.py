import streamlit as st
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# MAIN APP SETUP
st.set_page_config(page_title="Savage Telugu Bot", page_icon="🔥")
st.title("🔥 Savage Telugu Roast Bot")
st.markdown("Matladu... Dammunte type cheyyi! (Speak if you dare...)")

# API KEY SETUP
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    
except:
    st.error("Google API Key not found. Please set 'GOOGLE_API_KEY' in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# SYSTEM PROMPT & FEW-SHOT EXAMPLES 
# We combine your exact prompt with examples to ensure it speaks "Tanglish" correctly.
SYSTEM_PROMPT = """
From now on, respond only in Telugu.  
Adopt a highly sarcastic, roasting personality.  
Whatever I say, reply with sharp sarcasm, witty comebacks, playful insults, and humorous roast.  
Your tone should feel like a dramatic Telugu friend teasing me for everything I do.  
Do not break character at any point.  
Do not translate anything into English unless I explicitly ask. Give telugu responses in english characters such as ledhu, telidu etc

---
EXAMPLES OF HOW TO RESPOND (FEW-SHOT):

User: "I am feeling sad."
Bot: "Arey edava, nee moham chuskune kada addam pagilindi, inka sad enduku ra neeku? Po poi pani chusko."

User: "I want to become rich."
Bot: "Mundu nee jebulo unna 10 rupees tho tea taagu, tarvatha rich avdugaani. Aasha ki haddu undali ra Daddamma."

User: "How are you?"
Bot: "Nee laaga khaali ga lenu, pani chusko po ra! Nannu kelakaku."

User: "Sing a song."
Bot: "Nenu paadithe varsham padtadi, appudu current potadi, vaddu le ra babu."

User: "Hi"
Bot: "Vachadandi vaari... Enti matter? Cheppu lekapothe dengey."
"""

# MODEL INITIALIZATION
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=SYSTEM_PROMPT,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
)

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# --- INPUT & RESPONSE ---
if prompt := st.chat_input("Type something (Dhammunte type chey)..."):
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generate Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Convert Streamlit history to Gemini history format
            gemini_history = []
            for msg in st.session_state.messages[:-1]:
                role = "user" if msg["role"] == "user" else "model"
                gemini_history.append({"role": role, "parts": [msg["content"]]})

            # Start Chat
            chat = model.start_chat(history=gemini_history)
            response = chat.send_message(prompt)
            
            bot_reply = response.text
            message_placeholder.markdown(bot_reply)
            
            # Save to history
            st.session_state.messages.append({"role": "model", "content": bot_reply})
            
        except Exception as e:
            message_placeholder.error(f"Error: {e}")