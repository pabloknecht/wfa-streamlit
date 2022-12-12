import streamlit as st
import requests
import numpy as np
from get_new_images import get_new_image
from image_viz import summary, landscape_changes, image_colormap_changes


st.title(' Website Watching from above ')

st.header('With Sentinel-2 satellite (EuroSAT) and Google Maps')

# '''
# 1. Variables asked:
# - adress
# - year_1
# - year_2

# 2. Define the url API
# 3. Build a dictionary containing the parameters for our API...
# 4. Call our API using the `requests` package...
# 5. Retrieve the prediction from the **JSON** returned by the API...
# 6. Display the prediction to the user
# '''

with st.form(key='params_for_api'):

    adress = st.text_input('Adress or GPS coordinates','160 Av. des Martyrs, 38000 Grenoble')
    year_1 = st.selectbox('Year 1', ('2017', '2018', '2019', '2020', 'Google'))
    year_2 = st.selectbox('Year 2', ('2017', '2018', '2019', '2020', 'Google'))

    submitted = st.form_submit_button('Landscape evolution')

params = dict(
    adress = adress,
    year_1 = year_1,
    year_2 = year_2)

wfa_api_url = 'https://wfa01-tqv5zy4gla-ew.a.run.app/watchingfromabove/prediction'

if submitted:
    response = requests.get(wfa_api_url, params=params)
    results = response.json()
    # st.write(results)

    # Extract predictions for each image
    cat_year_1_np = np.array(results['current_year']) # year_1 to be confirmed
    cat_year_2_np = np.array(results['historical_year']) # year_2 to be confirmed

    # Get the correspondent images
    image_year_1 = get_new_image(adress, year_1)
    image_year_2 = get_new_image(adress, year_2)

    # using summary function to compare results
    changes, sry = summary(cat_year_1_np, cat_year_2_np)


    ##################################################
    #          FIRST TABLE - Plot original images    #
    ##################################################
    col11, col12 = st.columns(2)

    st.header(f'Landscape evolution: {year_1} vs. {year_2}')

    with col11:
        st.header("Year 1")
        st.image(image_year_1)

    with col12:
        st.header("Year 2")
        st.image(image_year_2)


    ##################################################
    #          SECOND TABLE - Plot comparision       #
    ##################################################
    col21, col22 = st.columns(2)

    with col21:
        st.header("Year 1")
        img_changes_1 = landscape_changes(image_year_1, changes)
        st.image(img_changes_1)

    with col22:
        st.header("Year 2")
        img_changes_2 = landscape_changes(image_year_2, changes)
        st.image(img_changes_2)


    ##################################################
    #          THIRD TABLE - Plot comparision        #
    ##################################################




    ##################################################
    #          FORTH TABLE - Plot comparision        #
    ##################################################
    col41, col42 = st.columns(2)

    with col41:
        st.header("Landscape evolution")
        st.dataframe(sry)

    with col42:
        BW_img = image_colormap_changes(changes)
        st.image(BW_img)
