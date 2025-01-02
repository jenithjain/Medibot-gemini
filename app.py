import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv  # Import the load_dotenv function

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction="You are a highly knowledgeable and empathetic medical assistant. Your role is to analyze medical reports, provide insights, suggest possible recommendations, and guide users based on their health conditions. Ensure your responses are accurate, concise, and in line with medical best practices.\nYou are trained in all aspects of medicine, including general health, diagnostics, treatments, chronic disease management, and medical terminology. Use your expertise to explain medical conditions, lab results, and provide suggestions for follow-ups or preventive care.\nWhen analyzing a medical report, identify the key parameters such as blood test results, imaging data, or patient history. Provide insights into abnormal values, possible conditions, and actionable recommendations. Always prioritize patient safety and suggest consulting a healthcare professional if required.\nYou have deep expertise in areas like cardiology, endocrinology, pediatrics, and preventive care. When faced with domain-specific queries, provide detailed and accurate responses that reflect best practices in that medical field.\nA user uploads a blood test report showing elevated cholesterol levels. Analyze the report, explain the implications of high cholesterol, and suggest lifestyle changes or follow-up actions.",
)

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Streamlit UI
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #00BFFF;  /* Aqua green */
        color: white;  /* White font color */
    }
    .user-message {
        color: white;
        font-weight: bold;
        text-align: right;  /* Align user messages to the right */
    }
    .assistant-message {
        color: white;
        font-weight: bold;
        text-align: left;  /* Align assistant messages to the left */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Welcome to CARERICH Medical Bot")
st.write("Ask your medical questions below:")

user_input = st.text_input("Your question:")

if st.button("Send"):
    if user_input:
        # Append user input to chat history
        st.session_state.chat_history.append({"role": "user", "parts": [user_input]})

        # Start chat session and get response
        chat_session = model.start_chat(history=st.session_state.chat_history)
        response = chat_session.send_message(user_input)

        # Append model response to chat history
        st.session_state.chat_history.append({"role": "model", "parts": [response.text]})

        # Display chat history
        for chat in st.session_state.chat_history:
            if chat["role"] == "user":
                st.write(f"<div class='user-message'>**You:** {chat['parts'][0]}</div>", unsafe_allow_html=True)
            else:
                st.write(f"<div class='assistant-message'>**Assistant:** {chat['parts'][0]}</div>", unsafe_allow_html=True)
    else:
        st.write("Please enter a question.") 