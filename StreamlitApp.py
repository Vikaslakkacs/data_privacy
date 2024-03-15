import os
import traceback
from dotenv import load_dotenv
from src.data_privacy.anonymization import anonymization
import streamlit as st
from langchain.callbacks import get_openai_callback

##Creating Applications
st.header('Data Security')
st.subheader('A playground to implement methodologies and concepts on managing data privacy and security')

##Stream lit creating
with st.form("user_inputs"):
    upload_file= st.file_uploader("Upload the scene", type=['txt'], accept_multiple_files=False)
    load_button=st.form_submit_button("anonymize data")

###Create Chat option for the case uploaded.
    #st.text(load_button)
    if load_button ==True:
        ##Read the data

        scene_text_data= upload_file.read().decode("utf-8")
        st.text("Case:\n\n")
        #st.text(upload_file.read())
        st.text(scene_text_data)
        #anonymize=anonymization("/Users/vikaslakka/Desktop/FSDS/GenAI/poc/data_privacy/data_privacy/cases/theft_case.txt", synthetic_data=True)
        anonymize=anonymization(doc_path=scene_text_data, synthetic_data=True)
        chain= anonymize.initate_deanonymize_model()
        response= chain.invoke("who lost the wallet?")
        st.text(response)



### Now we will create changed
with st.sidebar:
    st.title("Ask anything about the scene...")
    messages= st.container(height=400)
    
    if question := st.chat_input("Ask anything about the scene..."):
        messages.chat_message("user").write(question)
        with st.spinner("Fethcing details..."):
            try:
                
                response= chain.invoke("who lost the wallet?")
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
        