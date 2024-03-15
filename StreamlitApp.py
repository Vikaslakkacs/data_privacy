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
    if load_button is not None:
        ##Read the data
        anonymize=anonymization(upload_file, synthetic_data=True)
        #anonymize.initate_deanonymize_model()
        st.text("Case:\n\n")
        st.text(upload_file.read().decode("utf-8"))


### Now we will create changed