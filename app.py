import os
import traceback
from dotenv import load_dotenv
from data_privacy.anonymization.anonymization import anonymization
import streamlit as st
from langchain.callbacks import get_openai_callback
import asyncio

##Creating Applications
st.header('Data Security')
st.subheader('A playground to implement methodologies and concepts on managing data privacy and security')
#st.write(st.session_state)
###Create session state for chat message
session_item_list= ["messages", "scene", "load_button", "anonymized_data"]
if "messages" not in st.session_state:
    st.session_state["messages"]=[]
if "scene" not in st.session_state:    
    st.session_state["scene"]=""
if "load_button" not in st.session_state:
    st.session_state.load_button= False
if "anonymized_data" not in st.session_state:
    st.session_state.anonymized_data=None
##Stream lit creating
with st.form("user_inputs"):
    upload_file= st.file_uploader("Upload the scene", type=['txt'], accept_multiple_files=False)
    load_button=st.form_submit_button("anonymize data")
    

###Create Chat option for the case uploaded.
    #st.text(load_button)
    if load_button ==True:
        st.session_state.load_button= True
        ##Read the data
        scene_text_data= upload_file.read().decode("utf-8")
        
        st.session_state['scene']= scene_text_data
        
        ##Create class and method of anonymization
        #anonymize=anonymization("/Users/vikaslakka/Desktop/FSDS/GenAI/poc/data_privacy/data_privacy/cases/theft_case.txt", synthetic_data=True)
        anonymize=anonymization(doc_path=scene_text_data, synthetic_data=True)
        chain= asyncio.run(anonymize.initate_deanonymize_model())
        

        ##bringing existing object form the class
        st.session_state['anonymized_data']= anonymize.anonymizer.deanonymizer_mapping
        ##Storing the chain method
        st.session_state['chain']= chain
        
        #response= chain.invoke("who lost the wallet?")
        #st.text(response)
        # question= st.text_input("Who lost the wallet?")
        #print(question)
        #question= st.text_input(chain.invoke(question))



### Now we will create changed
with st.sidebar:
    st.title("Ask anything about the scene...")
    messages= st.container(height=200)
    if question := st.chat_input("Ask anything about the scene..."):
        messages.chat_message("user").write(question)
        ###Save chat history with session state
        st.session_state.messages.append({"role":"user", "content": question})
        with st.spinner("Fethcing details..."):
            try:
                
                response= st.session_state.chain.generate_async(question)
                #st.write(response)
                if isinstance(response, str):
                    messages.chat_message("bot").write(f"{response}")
                    ## Save the result to chat history session
                    st.session_state.messages.append({"role":"bot", "content": response})
                    
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
    #st.empty()
    for message in st.session_state.messages:
                        #st.markdown(f"{message['role']} : {message['content']}")
                        messages.chat_message(message['role']).write(f"{message['content']}")

#print(st.session_state)
if st.session_state.load_button==True:
    ### Display the case and scene
    st.write("Case: ")
    st.write(st.session_state.scene)
    st.divider()
    ###Display anonymized personal identifiable information
    st.write("Anonymised PII data:")

    for code, value in st.session_state.anonymized_data.items():
                st.divider()
                st.text(f"{code}:")
                for synthetic, actual in value.items():
                    st.text(f"{actual} : {synthetic}")
                        
