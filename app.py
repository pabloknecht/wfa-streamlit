import streamlit as st
import requests
import numpy as np
from PIL import Image
from get_new_images import get_new_image
from image_viz import summary, landscape_changes, image_colormap
import streamlit as st
import pandas as pd
import numpy as np

#set images
logo = Image.open('wfa_logo.png')
icon = Image.open('wfa_icon.png')

# Labels size
lbls = Image.open('Labels2.png')
factor = 0.9
h = int(lbls.size[0]*factor)
w = int(lbls.size[1]*factor)
size = (h, w)
lbls = lbls.resize(size)

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


    ########################################################
    #          FIRST TABLE - Plot original images          #
    ########################################################
    st.markdown("***")
    colesp, col10, col11, col12, col13, col14, col15 = st.columns([0.4, 0.2, 0.85, 0.85, 0.85, 0.4, 0.2])
    with col10:
        st.subheader(f"{year_1}")

    with col11:
        st.image(image_year_1)

    with col12:
        img_changes_1 = landscape_changes(image_year_1, changes)
        st.image(img_changes_1)


    with col13:
        img_colormap_1 = image_colormap(cat_year_1_np)
        st.image(img_colormap_1)


    with col14:
        st.image(lbls)

    #######################################################
    #          SECOND TABLE - Plot comparision            #
    #######################################################
    colesp, col20, col21, col22, col23, col24, col25 = st.columns([0.4, 0.2, 0.85, 0.85, 0.85, 0.4, 0.2])
    with col20:
        st.subheader(f"{year_2}")

    with col21:
        st.image(image_year_2)

    with col22:
        img_changes_2 = landscape_changes(image_year_2, changes)
        st.image(img_changes_2)


    with col23:
        img_colormap_2 = image_colormap(cat_year_2_np)
        st.image(img_colormap_2)

    with col24:
       pass


    #######################################################
    #                       SUMMARY                       #
    #######################################################
    st.markdown("***")
    colt1, colt2, colt3 = st.columns([1, 1, 1])
    with colt2:
        columns_names = ["Categories", f"{year_1}", f"{year_2}", "Difference"]
        sry.columns = columns_names
        sry.set_index("Categories", inplace=True)

        ########## dataframe style
        th_props = [
        ('font-size', '20px'),
        ('text-align', 'center'),
        ('font-weight', 'bold'),
        ('color', '#FFFFFF'),
#        ('background-color', '#060537'),
        ('border','1px solid #0f0d8a')
        ]

        td_props = [
        ('font-size', '18px'),
        ('text-align', 'centersssss'),
        ('color', '#FFFFFF'),
        ('border','1px solid #0f0d8a')
        ]

        styles = [
        dict(selector="th", props=th_props),
        dict(selector="td", props=td_props)
        ]

        # table
        df2=sry.style.set_properties(**{}).set_table_styles(styles)
        st.table(df2)
        #st.dataframe(data=sry, width=700)

    st.balloons()
