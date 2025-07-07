from dotenv import *
load_dotenv()  # loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    response_text = ""
    source_info = "Source: AI-based responses generated using educational resources."
    
    for chunk in response:
        response_text += chunk.text
    return response_text, source_info

# Initialize our Streamlit app
st.set_page_config(page_title="Education Chatbot", layout="wide")

# Sidebar for user instructions
with st.sidebar:
    st.header("Instructions")
    st.write("👋 Welcome to the Education Chatbot!")
    st.write("You can ask me questions related to:")
    st.write("- Admissions")
    st.write("- Minimum Rank")
    st.write("- Fee Structure")
    st.write("- Faculty")
    st.write("- Location")
    st.write("- Transport")
    st.write("- Hostel Facilities")
    st.write("- Internships")
    st.write("- Placements")
    st.write("- Courses")
    st.write("- Safety")
    st.write("- Anti-bullying Measures")
    st.write("- Curriculum")
    st.write("- Academic Calendar")
    st.write("- Scholarships")
    st.write("- Extracurricular Activities")
    st.write("\nType your question in the input box and hit 'Ask the question'.")

# Main application header
st.header("🎓 COLLEGE FAQ 'CHATBOT'")
st.write("")
st.write("")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Define allowed education topics
allowed_education_topics = [
    "admissions", "minimum rank", "fee structure", "faculty", 
    "location", "transport", "hostel facilities", "internships", 
    "placements", "courses", "safety", "anti-bullying measures",
    "curriculum", "academic calendar", "scholarships", "extracurricular activities"
]

# User input
input = st.text_input("Input your question here:", key="input", placeholder="ie.placements in IIT bombay this year.")

# Submit button
submit = st.button("Submit your question")
st.write("")
st.write("")

if submit and input:
    # Check if the input contains any allowed education topic
    if any(topic in input.lower() for topic in allowed_education_topics):
        response, source_info = get_gemini_response(input)
        
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is:")
        st.write(response)
        
        # Display source information
        st.markdown(f"<div style='color: gray;'>{source_info}</div>", unsafe_allow_html=True)
        
        # Append the response and source to chat history
        st.session_state['chat_history'].append(("Bot", response))
        st.session_state['chat_history'].append(("Bot Source", source_info))
        
    else:
        # Return a message indicating the restriction
        st.session_state['chat_history'].append(("You", input))
        st.subheader("The Response is:")
        st.write("I'm sorry, but I can only provide information related to education topics such as admissions, fee structure, faculty, courses, and more.")
        st.session_state['chat_history'].append(("Bot", "I'm sorry, but I can only provide information related to education topics such as admissions, fee structure, faculty, courses, and more."))

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    if role == "You":
        st.markdown(f"<div style='text-align: left; color:\t#0fa4d4;'>{role}:{text}</div>", unsafe_allow_html=True)
    elif role == "Bot Source":
        st.markdown(f"<div style='text-align: left; color:\t#da4c0e; font-size: smaller;'>{text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; color:\t#f9ff45;'>{role}:{text}</div>", unsafe_allow_html=True)