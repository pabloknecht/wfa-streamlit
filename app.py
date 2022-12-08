import streamlit as st
import requests
st.markdown(' Website Watching from above ')

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

    adress = st.text_input('adress','160 Av. des Martyrs, 38000 Grenoble')
    # longitude = st.number_input('longitude', value=40.7614327)
    # latitude = st.number_input('latitude', value=-73.9798156)
    historical_year = st.number_input('historical year',min_value=2017, max_value=2020, step=1)
    comparison_year = st.number_input('comparison year',min_value=2018, max_value=2020, step=1)

    st.form_submit_button('Landscape evolution calculation')

params = dict(
    #longitude=longitude,
    #latitude=latitude,
    adress = adress,
    historical_year=historical_year,
    comparison_year=comparison_year)

wfa_api_url = '' # url link to be provided
response = requests.get(wfa_api_url, params=params)

prediction = response.json()

st.header(f'evolution landscape percentage: {(prediction)}')
