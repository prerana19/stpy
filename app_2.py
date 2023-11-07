import streamlit as st
import base64
st.set_page_config(page_title="SmartKYC", page_icon="📖", layout="wide")
st.header("SmartKYC")


st.session_state.default_input = False
global_selected_file = None
# def clear_submit():
#     st.session_state["submit"] = False
# @st.cache_data
# def getDataResponse(selected_bytes_data):
#     return "got the json response"

# @st.cache_data
def displayPDF(selected_file):
    print("selected pdf:"+ selected_file.name)
    # Read file as bytes:
    bytes_data = selected_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')

    # Embed PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="650" height="500" type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)

# @st.cache_data    
def displayChat(selected_file):
    start_sequence = "\nYou: "
    restart_sequence = "\nBot: "
#     st.session_state.default_input = "Say something"
    
#     if user_input:
#         st.write("User said:" + user_input)
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

# @st.cache_data
def handle_fileclick(file):
    global global_selected_file
    global_selected_file = file
    print("g_s_f after click:" + global_selected_file.name)
#     getDataResponse(selected_file.getvalue())
    with col1:
        displayPDF(file)
        
    with col2:
        displayChat(file)
            
def main():
    with st.sidebar: 
        uploaded_files = st.file_uploader(
            "Choose a PDF file", type=["pdf"],accept_multiple_files=True, 
            help="Only PDF files are supported")
        print(type(uploaded_files))
        if uploaded_files:
            btn_key = 0
            for file in uploaded_files:
                filename = file.name
        #         st.write("filename:", uploaded_file.name)
                st.button(file.name,on_click=handle_fileclick, args=[file],use_container_width = True, key = btn_key)
                btn_key += 1

    user_input = st.chat_input(disabled= st.session_state.default_input)

    if user_input:
        print("selected file in user input:"+global_selected_file.name)
        displayPDF(global_selected_file)
        
if __name__ == '__main__':
    main()
