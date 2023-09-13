from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import webbrowser
from streamlit_extras.dataframe_explorer import dataframe_explorer

# format page (browser, logo, title, )
st.set_page_config(layout="wide", page_title="WESAD Web Interface",
                   page_icon=Image.open('./content/iot.png'))
st.image(Image.open('./content/iot.png'), width=200)
st.title("Welcome to your mHealth data")
st.sidebar.title("WESAD Web Interface")
# change css for h1
st.markdown(""" <style> h1{ text-align:center; font-family: 'Cooper Black'; color: #0e3f6e;} </style> """,
            unsafe_allow_html=True)


# change css for h3
st.markdown(""" <style> h3{  font-family: 'Cooper Black'; color: #2e8c7f;} </style> """, unsafe_allow_html=True)
# change css for p
st.markdown(""" <style> p{  font-size: 20px;} </style> """, unsafe_allow_html=True)

with st.sidebar:
    choose  = option_menu(None, ["Data Descriptor", "Demographics", "Interactive visualizations", "Personalized data", "Contact"],
    icons=['clipboard', 'grid-3x2', 'graph-down', 'people-fill', 'mailbox'],
    menu_icon="globe2", default_index=0,
styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#2e8c7f"},
    } )

if choose == "Data Descriptor":
    # data description
    st.markdown("""
        ### WESAD, a Multimodal Dataset for Wearable Stress and Affect Detection
        Introducing WESAD, a Multimodal Dataset for Wearable Stress and Affect Detection [[1]](https://dl.acm.org/doi/10.1145/3242969.3242985)

        add text about the dataset and what is visualized
        """)

    st.markdown(""" \n """)

    st.markdown("""
        ### The dataset's table
        """)
    df = pd.read_csv('data\data_total.csv', index_col=0)
    filtered_df = dataframe_explorer(df, case=False)
    st.dataframe(filtered_df)

    st.write("""
        ### Download data
        You can download the above data in a csv file.
        """)

    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    data_csv = convert_df(df)

    st.download_button(label="WESAD", data=data_csv, file_name="WESAD_dataframe.csv", mime='text/csv')

    # change button css
    st.markdown(
        """ <style> .css-1x8cf1d{ background-color: #a7d7d0; border: 0px solid;} .css-1vbkxwb p{ font-size: 22px; padding: 8px; } </style> """,
        unsafe_allow_html=True)
    st.markdown(""" \n """)



if choose == "Demographics":

    st.markdown(""" ### Participants' Demographics """)

    df = pd.read_csv('data\data_total.csv', index_col=0)
    df_demographics = df.groupby('id').first()
    df_demographics = df_demographics[['Gender', 'Age']]

    col1_dem, col2_dem = st.columns(2)
    with col1_dem:
        # GENDER header
        st.markdown(""" #### GENDER """)

        # create the donut chart
        gender = pd.DataFrame(df_demographics['Gender'].value_counts()).reset_index()
        gender.loc["Not answered"] = ['Not answered', 71 - gender['Gender'].sum()]
        gender.reset_index(drop=True, inplace=True)
        gender.rename(columns={'index': 'Gender', 'Gender': 'Value'}, inplace=True)
        fig = px.pie(gender, values='Value', names='Gender', color='Gender',
                     color_discrete_map={'MALE': '#b0d0e8', 'FEMALE': '#95d0c7', 'Not answered': '#bfbfbf'})
        st.plotly_chart(fig, use_container_width=True)

    with col2_dem:
        # AGE header
        st.markdown(""" #### AGE """)

        # create the bar chart
        age = pd.DataFrame(df_demographics['Age'].value_counts()).reset_index()
        age.loc["Not answered"] = ['Not answered', 71 - age['Age'].sum()]
        age.reset_index(drop=True, inplace=True)
        age.rename(columns={'index': 'Age', 'Age': 'Value'}, inplace=True)
        fig = px.bar(age, x='Age', y='Value', color='Age', text='Value',
                     color_discrete_map={'<30': '#b0d0e8', '>=30': '#95d0c7', 'Not answered': '#bfbfbf'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)


    st.markdown('\n')

# add footer section
footer = """
<footer class="custom-footer">
    Christina Karagianni & Labros Vasileiou, September 2023. This project is part of the HCI course at the MSc in Advanced Computer and Communication Systems
    at the School of Electrical Engineering (AUTh).
</footer>
<style>
    footer.custom-footer {
        visibility: visible;
        background-color: #0e3f6e;
        width: calc(100% + 80px + 80px);
        height: auto;
        padding: 40px 60px;
        color: white;
        margin-left: -80px;
        margin-right: 80px;
        font-size: 18px;
    }
    footer.custom-footer a {
        color: #2e8c7f;
    }
    footer.custom-footer a:hover, footer.custom-footer a:active {
        color: #35a192;
    }
    footer:not(.custom-footer) {
        display: none;
    }
    .css-164nlkn{
        padding: 1rem 4rem 7rem 2rem;
    }
    .css-z5fcl4, .egzxvld4 {
        padding-bottom: 0px;
    }

    @media all and (max-width: 578px) {
        footer.custom-footer {
            margin-left: -17px;
            margin-right: 17px;
            width: calc(100% + 17px + 17px);
        }
    }
</style>
"""
st.markdown(footer, unsafe_allow_html=True)
