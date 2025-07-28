import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

load_dotenv()


#loading JSON file
with open('src/mcqgenerator/Response.json','r') as f:
    response_json = json.load(f)
    
# creating title for the APP
st.title("MCQ Generator App with LandChain")

# Creating form for user input
with st.form('user_inputs'):
    
    # File upload
    uploaded_file = st.file_uploader('Upload a PDF or Text File')
    
    #input Fields
    mcq_count = st.number_input('Number of MCQs', min_value=3, max_value=10)
    
    # Subject input field
    subject = st.text_input('Subject', value='Biology')
    
    # Tone input field
    tone = st.text_input('Complexity Level of Ques.', placeholder='Simple',max_chars=20)
    
    # Add button
    button= st.form_submit_button('Generate MCQs')
    
    # check if button is clicked and all fields are filled
    if button and uploaded_file and mcq_count and subject and tone:
        with st.spinner('Generating MCQs...'):
            try:
                text=read_file(uploaded_file)
                
                #count token and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(response_json)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error(f"Error: {e}")
            
            else:
                print(f"Total Tokens Used: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: ${cb.total_cost}")
                if isinstance(response, dict):
                    
                    # Extract quiz data
                    quiz = response.get('quiz')
                    print(type(quiz))
                    print("quiz:", quiz)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data:
                            df=pd.DataFrame(table_data)
                            df.index=df.index + 1
                            st.table(df)
                            
                            # display the review in a text box as well
                            st.text_area(label='Review', value=response.get('review', ''), height=200)
                        else:
                            st.error("Error in table data.")
                else:
                    st.write("Response:", response)
                    
                