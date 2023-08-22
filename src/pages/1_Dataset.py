import bson
import pandas as pd
from PIL import Image
import streamlit as st
import plotly.express as px
from streamlit_extras.dataframe_explorer import dataframe_explorer


# format page (browser, logo, title, )
st.set_page_config(layout="wide", page_title="LifeSnaps Web Interface", page_icon=Image.open('./content/datalab_logo.png'))
st.image(Image.open('./content/datalab_logo_full.png'), width=200)
st.title("The LifeSnaps Dataset")
st.sidebar.title("LifeSnaps Web Interface")
# change css for h1
st.markdown(""" <style> h1{ text-align:center; font-family: 'Cooper Black'; color: #0e3f6e;} </style> """, unsafe_allow_html=True)


# change css for h3 and p
st.markdown(""" <style> h3{  font-family: 'Cooper Black'; color: #2e8c7f;} p{  font-size: 20px;} </style> """, unsafe_allow_html=True)


# add LifeSnaps' table
st.markdown("""
    ### The dataset's table
    """)
df = pd.read_csv('./data/data_unprocessed.csv', index_col=0)
filtered_df = dataframe_explorer(df, case=False)
st.dataframe(filtered_df, use_container_width=True)

st.markdown(""" 
    ##### Note
    The above dataset is not exactly the one that is uploaded in Zenodo [here](https://zenodo.org/record/7229547). 
    It includes some basic preprocessing actions that facilitate its use and dissemination. 
    In more detail, this dataframe contains only the days of the experiment's period. Moreover, it does not contain duplicate rows and all the variables have their appropriate data type. 
    Finally, the raw Fitbit features are merged with all the self-reported data. """)
st.markdown(""" \n """)
# change h5 css
st.markdown(""" <style> h5{ font-style: italic; font-family: 'Cooper Black'; color: #2e8c7f;} </style> """, unsafe_allow_html=True)


# download the dataset
st.markdown("""
    ### Download the dataset
    You can download the LifeSnaps dataset in a csv file. 
    The dataset that will be downloaded by clicking the button below contains only the dates of experiment, 
    does not contain duplicates, all the variables are in their appropriate data type and the fitbit data are merged
    with the self-reports.
    """)
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


data_csv = convert_df(df)
st.download_button(label="Download data", data=data_csv, file_name="LifeSnaps_dataset.csv", mime='text/csv')
# change button css
st.markdown(""" <style> .css-1x8cf1d{ background-color: #a7d7d0; border: 0px solid;} .css-1vbkxwb p{ font-size: 24px; padding: 8px; } </style> """, unsafe_allow_html=True)
st.markdown(""" \n """)


# correlation matrix
st.markdown(""" ### The correlations of the dataset """)

# change info and findings text css
st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)

# info section
info_demographics = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
<i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The matrix below describes how strong and in what direction the variables of the 
LifeSnaps dataset are correlated. The darker blue or lighter yellow, the stronger correlation between the variables.                                                                                                                                                                
'''
st.markdown(info_demographics, unsafe_allow_html=True)
st.markdown('\n')
# plot
corr_matrix = df.corr()
fig = px.imshow(corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                height=800,
                color_continuous_scale='YlGnBu')
st.plotly_chart(fig, use_container_width=True)
st.markdown('\n')

# finding
finding_all = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
<i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> Beyond the expected high correlations (greater than 0.98) between specific variables 
(e.g., steps and distance, sleep duration and minutes asleep, etc.) there are observed some very meaningful insights. For instance, stress score is
  highly correlated (~ 0.95) with sleep points, exertion points and responsiveness points. Furthermore, calories are higher correlated with very active minutes
  than the moderately active minutes (0.68 and 0.60 respectively). Finally, the activation of EDA (scl_avg) is significantly correlated with
  the sleep efficiency (~ 0.74).'''
st.markdown(finding_all, unsafe_allow_html=True)


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
