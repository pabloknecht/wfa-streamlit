import streamlit as st
import requests
import numpy as np

st.title(' Website Watching from above ')

st.header('With Sentinel-2 satellite (EuroSAT) and Google Maps')

'''
1. Variables asked:
- adress
- year_1
- year_2

2. Define the url API
3. Build a dictionary containing the parameters for our API...
4. Call our API using the `requests` package...
5. Retrieve the prediction from the **JSON** returned by the API...
6. Display the prediction to the user
'''

with st.form(key='params_for_api'):

    adress = st.text_input('Adress or GPS coordinates','160 Av. des Martyrs, 38000 Grenoble')
    year_1 = st.selectbox('Year 1', ('2017', '2018', '2019', '2020', 'Google'))
    year_2 = st.selectbox('Year 2', ('2017', '2018', '2019', '2020', 'Google'))

    st.form_submit_button('Landscape evolution')

params = dict(
    adress = adress,
    year_1 = year_1,
    year_2 = year_2)

wfa_api_url = '' # url link to be provided
response = requests.get(wfa_api_url, params=params)

results = response.json()
#get.image
#get.image
classification_summary = results['summary'] # summary to be confirmed
classification_1 = np.array(results['year_1']) # year_1 to be confirmed
classification_2 = np.array(results['year_2']) # year_2 to be confirmed
classification_delta = classification_1 - classification_2

col1, col2, col3 = st.columns(3)

st.header(f'Landscape evolution: {year_1} vs. {year_2}')

with col1:
   st.header("Year 1")
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
   st.header("Year 2")
   st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
   st.header("Landscape evolution")
   st.image("https://static.streamlit.io/examples/owl.jpg")

col4, col5, col6 = st.columns(3)

with col4:
   st.image("https://static.streamlit.io/examples/cat.jpg")

with col5:
   st.image("https://static.streamlit.io/examples/dog.jpg")

with col6:
   st.image("https://static.streamlit.io/examples/owl.jpg")
