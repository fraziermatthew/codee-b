import datetime
import time

import pytz
import sqlite3

from openai import OpenAI
import streamlit as st
from modal import Modal

# Custom image for the app icon and the assistant's avatar
csp_logo = 'https://apcentral.collegeboard.org/media/images/desktop/ap-computer-science-principles-192.png'
college_board_logo = "https://wthsscratchpaper.net/wp-content/uploads/2023/03/College-Board-Logo-Icon.jpg"
codee_avatar = 'https://miro.medium.com/v2/resize:fit:525/1*lyyXmbeoK5JiIBNCnzzjjg.png'
codee_avatar2 = 'https://images-platform.99static.com/EQHRK-j49KSCLj-fiK-trxxBR8Q=/1043x113:2040x1110/500x500/top/smart/99designs-contests-attachments/96/96241/attachment_96241792'

# Configure streamlit page
st.set_page_config(
    page_icon=college_board_logo
)

# Adding user_id to title
# st.subheader(f"{user_id}")

with st.expander("ℹ️ Disclaimer"):
    st.caption(
        f"""We appreciate your engagement! Please note, this is research purposes only. 
        Thank you for your understanding. Be sure to add this to the survey.
        """
    )
    
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    # Create a user_id for the session
    user_id = st.text_input("Participant #", key="user_id", type="password")
    admin = st.text_input("Admin Only", key="db_key", type="password")
    
    if admin == "matthew":
        # Button to download db file
        with open("results.db", "rb") as fp:
            btn = st.download_button(
                label="Download db file",
                data=fp,
                file_name="results.db",
                mime="application/octet-stream"
            )

client = OpenAI(api_key=openai_api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

# Initialize chat history
if "messages" not in st.session_state:
    # Start with first message from assistant
    st.session_state['messages'] = [{"role": "assistant", 
                                  "content": f"Hi student! I'm Codee, an intelligent AI for Computer Science Principles. How can I help you today?"}]

# Display chat messages from history on app rerun
# Custom avatar for the assistant, default avatar for user
for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar=codee_avatar):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


if prompt := st.chat_input("Let's chat"):
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
        
    if not user_id:
        st.info("Please add your Participant # to continue.")
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
                    label="How well do you believe that the chatbot answered your question?",
                    options=["Very Poor", "Poor", "Acceptable", "Good", "Very Good"],
                    index=2,
                    horizontal=True
                )
                q2 = st.radio(
                    label="How well did the agent’s response take into account your personal background and experience?",
                    options=["Very Poor", "Poor", "Acceptable", "Good", "Very Good"],
                    index=2,
                    horizontal=True
                )
                q3 = st.radio(
                    label="How understandable do you believe the agent's response was to you?",
                    options=["Very Poor", "Poor", "Acceptable", "Good", "Very Good"],
                    index=2,
                    horizontal=True
                )
                q4 = st.radio(
                    label="If there are examples shown to you, how  understandable do you believe the examples were to you?",
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