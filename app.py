import datetime

import pytz
import sqlite3
from uuid import uuid4

from openai import OpenAI
import streamlit as st
from modal import Modal

# Create a user_id for the session
user_id = uuid4()

# Custom image for the app icon and the assistant's avatar
csp_logo = 'https://apcentral.collegeboard.org/media/images/desktop/ap-computer-science-principles-192.png'
college_board_logo = "https://wthsscratchpaper.net/wp-content/uploads/2023/03/College-Board-Logo-Icon.jpg"

# Configure streamlit page
st.set_page_config(
    page_icon=college_board_logo
)

# Adding user_id to title
st.subheader(f"{user_id}")

with st.expander("ℹ️ Disclaimer"):
    st.caption(
        f"""We appreciate your engagement! Please note, this is research purposes only. Thank you for your understanding.
        Your user-id is {user_id}. Be sure to add this to the survey.
        """
    )
    
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")

client = OpenAI(api_key=openai_api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

# Initialize chat history
if "messages" not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant", 
                                  "content": f"Hi student! I'm an intelligent AI for Computer Science Principles. How can I help you today?"}]

# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=csp_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if prompt := st.chat_input("Let's chat"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=csp_logo):
        message_placeholder = st.empty()
        result = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        response = result.choices[0].message.content
        full_response = ""
        
        # Simulate stream of response with milliseconds delay
        for chunk in response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
        # Create modal
        modal = Modal(title="", key="modal")
        
        with modal.container():

            user_input = st.session_state.messages[-1]["content"]
            model_output = full_response
            st.write(f"**{user_input}**")
            st.write(model_output)
    
            with st.form("feedback"):

                # Initialize disabled for form_submit_button to False
                if "disabled" not in st.session_state:
                    st.session_state.disabled = False
        
                q1 = st.radio(
                    label="Rate how accurately the chatbot answered your question.",
                    options=["Very Poor", "Poor", "Acceptable", "Good", "Very Good"],
                    index=2,
                    horizontal=True
                )
                q2 = st.radio(
                    label="Rate the level that the agent’s response enabled you to learn based on your personal experience.",
                    options=["Very Poor", "Poor", "Acceptable", "Good", "Very Good"],
                    index=2,
                    horizontal=True
                )
                q3 = st.radio(
                    label="Rate your level of understanding of the agent’s response.",
                    options=["Very Poor", "Poor", "Acceptable", "Good", "Very Good"],
                    index=2,
                    horizontal=True
                )
                q4 = st.radio(
                    label="If there are examples present, rate your level of understanding of the examples.",
                    options=["Very Poor", "Poor", "Acceptable", "Good", "Very Good", "N/A - Not Applicable"],
                    index=2,
                    horizontal=True
                )

                submitted = st.form_submit_button("Submit")
                
                user_input = user_input.replace("'", "").replace('"', "").replace(",", "\,").replace("\n", " ")
                model_output = model_output.replace("'", "").replace('"', "").replace(",", "\,").replace("\n", " ")
                
                timestamp = datetime.datetime.now(tz=pytz.timezone('America/New_York')).strftime("%Y-%m-%d %H:%M:%S")

                con = sqlite3.connect("results.db")
                with con:
                    cur = con.cursor()
                    cur.execute(f"""
                            INSERT INTO results
                            VALUES
                            ('{user_id}', 
                            '{user_input}', 
                            '{model_output}', 
                            '{q1}', 
                            '{q2}', 
                            '{q3}', 
                            '{q4}',
                            '{timestamp}')
                        """)
    
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )