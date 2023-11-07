import streamlit as st
import base64
st.set_page_config(page_title="SmartKYC", page_icon="📖", layout="wide")
st.header("SmartKYC")


# def clear_submit():
#     st.session_state["submit"] = False

def displayPDF(uploaded_file):
    
    # Read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')

    # Embed PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="650" height="500" type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)
    
def displayChat(uploaded_file):
    user_input = st.text_input("Say something",disabled=False)
    if user_input:
        st.write("User said:" + user_input)
#     question = st.text_input(
#                 "Ask something about the article",
#                 placeholder="Can you give me a short summary?",
#                 disabled=not uploaded_file,
#                 on_change=clear_submit,
#             )

#     if uploaded_file and question and not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")

#     if uploaded_file and question and openai_api_key:
#         st.info("Answer")
    
col1, col2 = st.columns(spec=[2, 1], gap="small")

def handle_fileclick(uploaded_file):
    with col1:
        displayPDF(uploaded_file)
        
    with col2:
        displayChat(uploaded_file)
            

with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="file_qa_api_key", type="password")
    
    uploaded_files = st.file_uploader(
        "Choose a PDF file", type=["pdf"],accept_multiple_files=True, 
        help="Only PDF files are supported")
    if uploaded_files:
        btn_key = 0
        for uploaded_file in uploaded_files:
            filename = uploaded_file.name
    #         st.write("filename:", uploaded_file.name)
            st.button(uploaded_file.name,on_click=handle_fileclick, args=[uploaded_file],use_container_width = True, key = btn_key)
            btn_key += 1
#         with col1:
#             displayPDF(uploaded_file)
