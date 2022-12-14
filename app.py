import streamlit as st
import requests
import numpy as np
from PIL import Image
from get_new_images import get_new_image
from image_viz import summary, landscape_changes, image_colormap

#set images
logo = Image.open('wfa_logo.png')
icon = Image.open('wfa_icon.png')

#set streamlit page config
st.set_page_config(page_title="Watching From Above", page_icon=icon)

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

#Remove Menu Button and Streamlit Icon
hide_default_format = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_default_format, unsafe_allow_html=True)

# hide fullsize button
hide_img_fs = '''
    <style>
        button[title="View fullscreen"] {
            visibility: hidden;
        }
        .css-1j77i4l {
            display: flex;
            justify-content: center;
        }
        .css-keje6w {
            display: flex;
            align-items: center;
        }
    </style>
    '''
st.markdown(hide_img_fs, unsafe_allow_html=True)

# Remove whitespace from the top of the page
remove_w_s = '''
        <style>
                div.block-container {
                    padding-top:1rem;
                    padding-bottom:0rem;
                }
        </style>
        '''
st.markdown(remove_w_s, unsafe_allow_html=True)

st.image(logo, width=400)

st.subheader('Discover landscape evolution with Sentinel-2 satellite (EuroSAT)')

##################################################
#                  test FORM                     #
##################################################
colf1, colf2, colf3 = st.columns([1, 2, 1])

with colf2:
    with st.form(key='params_for_api'):

        address = st.text_input('Adress or GPS coordinates','-20.859100, -61.143501')
        year_1 = st.selectbox('Year 1', ('2017 (Europe only)', '2018', '2019', '2020'),index=1)
        year_2 = st.selectbox('Year 2', ('2017 (Europe only)', '2018', '2019', '2020'),index=3)

        submitted = st.form_submit_button('Landscape evolution')

        if year_1 == '2017 (Europe only)':
            year_1 = '2017'

        if year_2 == '2017 (Europe only)':
            year_2 = '2017'


params = dict(
    address = address,
    year_1 = year_1,
    year_2 = year_2)

wfa_api_url = 'https://wfa04-tqv5zy4gla-ew.a.run.app/watchingfromabove/prediction'

if submitted:
    ##################################################
    #          API Call                              #
    ##################################################
    response = requests.get(wfa_api_url, params=params)
    results = response.json()

    # Extract predictions for each image
    cat_year_1_np = np.array(results['year_1']) # year_1 to be confirmed
    cat_year_2_np = np.array(results['year_2']) # year_2 to be confirmed

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
    col11, col12, col13, col14 = st.columns([1, 1, 1, 1])

    with col12:
        st.header(f"{year_1}")
        st.image(image_year_1)

    with col13:
        st.header(f"{year_2}")
        st.image(image_year_2)


    ##################################################
    #                  TABLE Colormap                #
    ##################################################
    col31, col32, col33, col34 = st.columns([1, 1, 1, 1])

    with col32:
        st.header(f"{year_1}")
        img_colormap_1 = image_colormap(cat_year_1_np)
        st.image(img_colormap_1)

    with col33:
        st.header(f"{year_2}")
        img_colormap_2 = image_colormap(cat_year_2_np)
        st.image(img_colormap_2)


    st.image('Labels.png', width=700)
    ##################################################
    #          SECOND TABLE - Plot comparision       #
    ##################################################
    col21, col22, col23, col24 = st.columns([1, 1, 1, 1])

    with col22:
        st.header(f"{year_1}")
        img_changes_1 = landscape_changes(image_year_1, changes)
        st.image(img_changes_1)

    with col23:
        st.header(f"{year_2}")
        img_changes_2 = landscape_changes(image_year_2, changes)
        st.image(img_changes_2)


    ##################################################
    #          Table                                 #
    ##################################################
    col41, col42, col43 = st.columns([1, 1, 1])

    with col42:
        columns_names = ["Categories", f"{year_1}", f"{year_2}", "Difference"]
        sry.columns = columns_names
        sry.set_index("Categories")
        st.dataframe(data=sry[columns_names], width=700)

    st.balloons()
