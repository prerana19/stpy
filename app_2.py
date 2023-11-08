import streamlit as st
from streamlit_chat import message
import base64
import pandas as pd
import numpy as np
import io
import json

st.set_page_config(page_title="SmartKYC", page_icon="📖", layout="wide")
st.header("SmartKYC")

# Storing the chat
if 'bot_current' not in st.session_state:
    st.session_state['bot_current'] = []

if 'user_current' not in st.session_state:
    st.session_state['user_current'] = []

st.session_state.default_input = False
col1, col2 = st.columns(spec=[2, 1], gap="small")

def displayPDF(selected_file):
    with col1:
        print("selected pdf:"+ selected_file.name)
        # Read file as bytes:
        bytes_data = selected_file.getvalue()

        # Convert to utf-8
        base64_pdf = base64.b64encode(bytes_data).decode('utf-8')

        # Embed PDF in HTML
        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width=100% height="200" type="application/pdf"></iframe>'

        # Display file
        st.markdown(pdf_display, unsafe_allow_html=True)
    
def displayChat():
    with col2:
        start_sequence = "\nYou: "
        restart_sequence = "\nBot: "
        st.session_state.default_input = "Say something"

        if st.session_state['bot_current']:
            print("length of session state gen:" + str(len(st.session_state['bot_current'])))

            for i in range(0,len(st.session_state['bot_current']),1):
                message(st.session_state['user_current'][i], is_user=True,avatar_style="fun-emoji", seed="Peanut", key=str(i) + '_user')
                message(st.session_state["bot_current"][i],avatar_style="thumbs", seed="Bandit", key=str(i)+'_bot')

                
def displayGrid():
    
    if "selected_file" in st.session_state:
        with col1:
            buffer = io.BytesIO()
            with open('code/res.json') as f:
                data = json.load(f)['data']
            jsonStr = json.dumps(data)

            # Use pd.json_normalize to convert the JSON to a DataFrame
            df = pd.read_json(jsonStr, orient ='index')
            df.columns = ['Value']
            st.table(df)
#     st.download_button(label="Click to Download Template File",data=df,
#                             file_name="template.xlsx",
#                             mime='application/octet-stream')
            

def displayWidgets(file):
    displayPDF(file)
    displayGrid()
    displayChat()
    
# @st.cache_data
def handle_fileclick(file):
    st.session_state.selected_file = file
    print("g_s_f after click:" + st.session_state.selected_file.name)
#     getDataResponse(selected_file.getvalue())
# call method here to get data
#     displayWidgets(file)
    displayChat()
       
def getResponse(prompt):
#     global i
#     i = i + 1
#     j = i
    return "response for " + str(prompt)

def chat(user_input):
    if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
    # Save init prompt in the bot_prompt.
    if len(user_input):
        st.session_state.chat_history.append(f'User: {user_input}')
        st.session_state.user_current.append(user_input)
        bot_output = getResponse(user_input)
        st.session_state.chat_history.append(f'\n Bot: {bot_output}')
        st.session_state.bot_current.append(bot_output)

    displayChat()    
            
def main():
    with st.sidebar: 
        doc_type = st.radio("Document Type",["10K","ADV","Fund Prospectus"])
        if doc_type:
            st.session_state.doc_type = doc_type
        uploaded_files = st.file_uploader(
            "Choose a PDF file", type=["pdf"],accept_multiple_files=True, 
            help="Only PDF files are supported")
        print(type(uploaded_files))
        if uploaded_files:
            btn_key = 0
            for file in uploaded_files:
                filename = file.name
                st.button(file.name,on_click=handle_fileclick, args=[file],use_container_width = True, key = btn_key)
                btn_key += 1

    user_input = st.chat_input()
    if "selected_file" in st.session_state:
        displayPDF(st.session_state.selected_file)
        displayGrid()
        if user_input:
            print("selected file in user input:"+st.session_state.selected_file.name)
            chat(user_input)
        
if __name__ == '__main__':
    main()
