import streamlit as st
import pandas as pd
import google.generativeai as genai
import base64

GOOGLE_API_KEY = 'AIzaSyAc7Ii4wHf_whau2q--rgjfdht8-I5xhSY'
genai.configure(api_key=GOOGLE_API_KEY)

def generate_data(prompt):
    context="""
For no diabetes Range as follows:

Urea: 2.0 - 22.0
Cr: 6.0 - 203.0
HbA1c: 0.9 - 5.6
Chol: 0.0 - 9.5
TG: 0.6 - 5.9
HDL: 0.5 - 4.0
LDL: 0.3 - 4.9
VLDL: 0.2 - 14.5
BMI: 19.0 - 24.5

For pre diabetes Range as follows:

Urea: 2.1 - 17.1
Cr: 37.0 - 344.0
HbA1c: 5.7 - 6.4
Chol: 2.0 - 6.5
TG: 0.8 - 5.3
HDL: 0.6 - 2.5
LDL: 0.8 - 3.9
VLDL: 0.4 - 2.4
BMI: 19.0 - 32.0

For  diabetes Range as follows:

Urea: 0.5 - 38.9
Cr: 20.0 - 800.0
HbA1c: 2.0 - 16.0
Chol: 0.6 - 10.3
TG: 0.3 - 13.8
HDL: 0.2 - 9.9
LDL: 0.5 - 9.9
VLDL: 0.1 - 35.0
BMI: 19.0 - 47.75

 Make sure to generate the data for the given timeline along with the date for each records
 follow the rules for each and every parameter for all 3 classes and follow the ranges instruction
 retuen it in Excel format shown in the Example


   Example:

   {'candidates': [{'content': {'parts': [{'text': '| Date | Age | Health State | Urea | Cr | HbA1c | Chol | TG | HDL | LDL | VLDL | BMI |\n|---|---|---|---|---|---|---|---|---|---|---|\n| 2023-01-01 | 30 | No Diabetes | 15.0 | 100.0 | 5.0 | 5.0 | 3.0 | 1.5 | 2.5 | 1.0 | 22.0 |\n| 2023-06-01 | 30 | No Diabetes | 12.0 | 80.0 | 4.5 | 4.0 | 2.5 | 1.2 | 2.3 | 0.8 | 21.0 |\n| 2023-11-01 | 31 | No Diabetes | 10.0 | 70.0 | 4.0 | 3.0 | 2.0 | 1.0 | 2.0 | 0.6 | 20.0 |\n| 2024-04-01 | 31 | Pre-Diabetes | 14.0 | 120.0 | 5.8 | 4.5 | 3.5 | 1.8 | 2.7 | 1.0 | 23.0 |\n| 2024-09-01 | 32 | Pre-Diabetes | 11.0 | 90.0 | 6.0 | 4.0 | 3.0 | 1.5 | 2.5 | 0.8 | 22.0 |\n| 2025-02-01 | 32 | Diabetes | 25.0 | 200.0 | 8.0 | 6.0 | 5.0 | 2.0 | 4.0 | 1.2 | 25.0 |\n| 2025-07-01 | 33 | Diabetes | 18.0 | 150.0 | 7.5 | 5.0 | 4.0 | 1.7 | 3.3 | 1.0 | 24.0 |\n| 2026-12-01 | 34 | Diabetes | 12.0 | 100.0 | 6.5 | 4.0 | 3.0 | 1.5 | 2.5 | 0.8 | 23.0 |\n| 2027-05-01 | 35 | Diabetes | 10.0 | 80.0 | 6.0 | 3.0 | 2.5 | 1.2 | 2.3 | 0.6 | 22.0 |\n| 2027-10-01 | 36 | Diabetes | 7.0 | 60.0 | 5.5 | 2.0 | 2.0 | 1.0 | 2.0 | 0.4 | 21.0 |'}], 'role': 'model'}, 'finish_reason': 1, 'index': 0, 'safety_ratings': [{'category': 9, 'probability': 1, 'blocked': False}, {'category': 8, 'probability': 1, 'blocked': False}, {'category': 7, 'probability': 1, 'blocked': False}, {'category': 10, 'probability': 1, 'blocked': False}], 'token_count': 0, 'grounding_attributions': []}], 'prompt_feedback': {'safety_ratings': [{'category': 9, 'probability': 1, 'blocked': False}, {'category': 8, 'probability': 1, 'blocked': False}, {'category': 7, 'probability': 1, 'blocked': False}, {'category': 10, 'probability': 1, 'blocked': False}], 'block_reason': 0}}),
)
  

   
 """
    model = genai.GenerativeModel('gemini-1.0-pro-latest')
    response = model.generate_content(f"{context}\n{prompt}")
    texts = response.text.split("\n")
    del texts[1]
    keys = [text.replace(" ", "") for text in texts[0].split('|')[1:-1]]
    data_dict = [{key: val for key, val in zip(keys ,[item.replace(' ', '') for item in text.split("|")[1:-1]])} for text in texts[1:]]
    df = pd.DataFrame(data_dict)
    return df

def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="generated_data.csv">Download CSV File</a>'
    return href

st.title('Generate Data from Prompt')

prompt = st.text_area('Enter your prompt:')
if st.button('Generate Data'):
    df = generate_data(prompt)
    st.write(df)
    st.markdown(get_table_download_link(df), unsafe_allow_html=True)
