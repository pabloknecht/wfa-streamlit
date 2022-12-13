import streamlit as st
import requests
import numpy as np
from get_new_images import get_new_image
from image_viz import summary, landscape_changes, image_colormap

#have full-page configuration in streamlit
st.set_page_config(layout="wide")

#set path
img_path='wfa_logo.png'

#set image
#logo = Im

st.title('Watching from above ')

st.header('With Sentinel-2 satellite (EuroSAT) and Google Maps')

with st.form(key='params_for_api'):

    address = st.text_input('Adress or GPS coordinates','160 Av. des Martyrs, 38000 Grenoble')
    year_1 = st.selectbox('Year 1', ('2017', '2018', '2019', '2020', 'Google'))
    year_2 = st.selectbox('Year 2', ('2017', '2018', '2019', '2020', 'Google'))

    submitted = st.form_submit_button('Landscape evolution')

params = dict(
    address = address,
    year_1 = year_1,
    year_2 = year_2)

wfa_api_url = 'https://wfa01-tqv5zy4gla-ew.a.run.app/watchingfromabove/prediction'

if submitted:

    ##################################################
    #          API Call                              #
    ##################################################
    response = requests.get(wfa_api_url, params=params)
    results = response.json()

    # Extract predictions for each image
    cat_year_1_np = np.array(results['current_year']) # year_1 to be confirmed
    cat_year_2_np = np.array(results['historical_year']) # year_2 to be confirmed

    # using summary function to compare results
    changes, sry = summary(cat_year_1_np, cat_year_2_np)


    ##################################################
    #          Getting images for display            #
    ##################################################
    # Get the correspondent images
    image_year_1 = get_new_image(address, year_1)
    image_year_2 = get_new_image(address, year_2)


    ##################################################
    #          FIRST TABLE - Plot original images    #
    ##################################################
    col11, col12 = st.columns(2)

    st.header(f'Landscape evolution: {year_1} vs. {year_2}')

    with col11:
        st.header(f"{year_1}")
        st.image(image_year_1)

    with col12:
        st.header(f"{year_2}")
        st.image(image_year_2)


    ##################################################
    #                  TABLE Colormap                #
    ##################################################
    col31, col32, col33 = st.columns([2, 2, 1])

    with col31:
        st.header(f"{year_1}")
        img_colormap_1 = image_colormap(cat_year_1_np)
        st.image(img_colormap_1)

    with col32:
        st.header(f"{year_2}")
        img_colormap_2 = image_colormap(cat_year_2_np)
        st.image(img_colormap_2)

    with col33:
        st.header("Labels")
        st.image('LABEL_ONLY.png')

    ##################################################
    #          SECOND TABLE - Plot comparision       #
    ##################################################
    col21, col22, col23 = st.columns([2, 2, 1])

    with col21:
        st.header(f"{year_1}")
        img_changes_1 = landscape_changes(image_year_1, changes)
        st.image(img_changes_1)

    with col22:
        st.header(f"{year_2}")
        img_changes_2 = landscape_changes(image_year_2, changes)
        st.image(img_changes_2)

    with col23:
        pass


    ##################################################
    #          Table                                 #
    ##################################################
    col41, col42, col43 = st.columns([1, 3, 1])

    with col42:
        st.header("Landscape evolution")
        st.dataframe(sry)

    st.balloons()
