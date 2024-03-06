import streamlit as st #all streamlit commands will be available through the "st" alias
import chatbot_lib as glib #reference to local lib script
import os
from pypdf import PdfReader


st.set_page_config(page_title="Chatbot with your email here") #HTML title
st.title("Chatbot with your email here") #page title



if 'memory' not in st.session_state: #see if the memory hasn't been created yet
    st.session_state.memory = glib.get_memory() #initialize the memory


if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] #initialize the chat history


#Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: #loop through the chat history
    with st.chat_message(message["role"]): #renders a chat line for the given role, containing everything in the with block
        st.markdown(message["text"]) #display the chat content

#def save_file(file):
#    with open(os.path.join("uploads", file.name), "wb") as f:
#        f.write(file.getbuffer())
#    return st.sidebar.success(f"File saved successfully: {file.name}")


#if not os.path.exists("uploads"):
 #       os.makedirs("uploads")


        
input_text = st.chat_input("Chat with your email here") #display a chat input box

if input_text: #run the code in this if block after the user submits a chat message
    
    with st.chat_message("user"): #display a user chat message
        st.markdown(input_text) #renders the user's latest message
    
    st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history
    
    chat_response = glib.get_chat_response(input_text=input_text, memory=st.session_state.memory) #call the model through the supporting library
    
    with st.chat_message("assistant"): #display a bot chat message
        st.markdown(chat_response) #display bot's latest response
    
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history



uploaded_file = st.sidebar.file_uploader("Upload your emails here as a single PDF file.", type="pdf")

if uploaded_file is not None:
        # Save the uploaded file
        #save_file(uploaded_file)
        text = ""
        reader = PdfReader(uploaded_file)
        page = reader.pages[0]
        for page in reader.pages:
            text = text + page.extract_text()
        st.session_state.memory.save_context({"input":"The following is a list of emails:"+text},{"output":"okay, I understand"})