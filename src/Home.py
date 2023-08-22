import bson
import pandas as pd
from PIL import Image
import streamlit as st


# format page (browser, logo, title, )
st.set_page_config(layout="wide", page_title="LifeSnaps Web Interface", page_icon=Image.open('./content/datalab_logo.png'))
st.image(Image.open('./content/datalab_logo_full.png'), width=200)
st.title("Welcome to the LifeSnaps Web Interface")
st.sidebar.title("LifeSnaps Web Interface")
# change css for h1
st.markdown(""" <style> h1{ text-align:center; font-family: 'Cooper Black'; color: #0e3f6e;} </style> """, unsafe_allow_html=True)


# add LifeSnaps' description
st.markdown("""
    ### LifeSnaps: a snapshot of our lives in the wild
    A sneak peek behind the scenes of a Nature Scientific Data user study [[1]](https://www.nature.com/articles/s41597-022-01764-x).
    """)
st.markdown(""" \n """)
st.markdown("""
    ### Our Data
    The newly published data descriptor paper, LifeSnaps, a 4-month multi-modal dataset capturing unobtrusive snapshots of our lives in the wild, introduces a new public dataset empowering future research in different disciplines from diverse perspectives. Pervasive self-tracking devices have penetrated numerous aspects of our lives, from physical and mental health monitoring to fitness and entertainment. Nevertheless, limited data exist on the association between in-the-wild large-scale physical activity patterns, sleep, stress, and overall health, and behavioral and psychological patterns due to challenges in collecting and releasing such datasets, including waning user engagement or privacy considerations. The LifeSnaps dataset is a multi-modal, time, and space-distributed dataset containing a plethora of data collected unobtrusively for more than 4 months by 71 participants. LifeSnaps contains more than 35 different data types totaling more than 71M rows of data. The participants contributed their data through validated self-reported surveys, ecological momentary assessments (EMAs), and a Fitbit Sense smartwatch and consented to make these data available to empower future research. We envision that releasing this large-scale dataset of multi-modal data will open novel research opportunities and potential applications in multiple disciplines.
    """)
# change css for h3
st.markdown(""" <style> h3{  font-family: 'Cooper Black'; color: #2e8c7f;} </style> """, unsafe_allow_html=True)
# change css for p
st.markdown(""" <style> p{  font-size: 20px;} </style> """, unsafe_allow_html=True)


# add LifeSnaps' image
logo = Image.open('./content/1.png')
st.image(logo)
st.markdown("""
    [1] Yfantidou, S., Karagianni, C., Efstathiou, S. et al. LifeSnaps, a 4-month multi-modal dataset capturing unobtrusive snapshots of our lives in the wild. Sci Data 9, 663 (2022). https://doi.org/10.1038/s41597-022-01764-x 
    """)
st.markdown(""" \n """)


# add people of this project
st.markdown("""
    ### Our People
    """)

col1, col2, col3 = st.columns(3)
with col1:
    sofia = Image.open('./content/s_yfantidou.jpg')
    st.image(sofia)
    st.markdown(""" #### Sofia Yfantidou """)
    st.markdown("""few words about me.. """)
with col2:
    christina = Image.open('./content/ckaragianni.jpg')
    st.image(christina)
    st.markdown(""" #### Christina Karagianni """)
    st.markdown("""few words about me.. """)
with col3:
    eva = Image.open('./content/eparaschou.jpg')
    st.image(eva)
    st.markdown(""" #### Eva Paraschou """)
    st.markdown(""" I am a Research Associate and Data Scientist at DataLab. I graduated from the Aristotle University of Thessaloniki (AUTh) with a B.Sc. in Informatics and now I am a Master's student in Data and Web Science, at AUTh. My research interests revolve around mobile and wearable computing for health and well-being, as well as around Responsible AI, specifically explainability and fairness.""")


# add footer section
footer = """
<style>
    footer{
        visibility: visible;
        background-color: #0e3f6e;
    }
    footer:after{
        content: 'This project is a part of the RAIS project. Learn more about the RAIS project at https://rais-itn.eu/ and the Data and Web Science Lab at https://datalab.csd.auth.gr/';
        display: block;
        position: relative;
        color: white;
        font-size: 18px;
    }
    .css-164nlkn{
        padding: 1rem 4rem 7rem 2rem;
    }
</style>
"""
st.markdown(footer, unsafe_allow_html=True)
