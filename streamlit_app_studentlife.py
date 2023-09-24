from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
from streamlit_extras.dataframe_explorer import dataframe_explorer

# format page (browser, logo, title, )
st.set_page_config(layout="wide", page_title="StudentLife Web Interface",
                   page_icon=Image.open('./content/iot.png'))
st.image(Image.open('./content/iot.png'), width=200)
st.title("Welcome to your mHealth data")
st.sidebar.title("StudentLife Web Interface")
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
        ### The StudentLife continuous sensing app assesses the day-to-day and week-by-week impact of workload on 
        stress, sleep, activity, mood, sociability, mental well-being and academic performance of a single class 
        of 48 students across a 10 week term at Dartmouth College using Android phones. Results from the 
        StudentLife study show a number of significant correlations between the automatic objective sensor data 
        from smartphones and mental health and educational outcomes of 
        the student body [[1]](https://studentlife.cs.dartmouth.edu/studentlife.pdf).        
        """)

    st.markdown(""" \n """)

    st.markdown("""
        ### The dataset's table
        """)
    df = pd.read_pickle('data/dataframe')
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

    st.download_button(label="StudentLife", data=data_csv, file_name="StudentLife_dataframe.csv", mime='text/csv')

    # change button css
    st.markdown(
        """ <style> .css-1x8cf1d{ background-color: #a7d7d0; border: 0px solid;} .css-1vbkxwb p{ font-size: 22px; padding: 8px; } </style> """,
        unsafe_allow_html=True)
    st.markdown(""" \n """)



if choose == "Demographics":
    st.markdown(""" ### Participants' Demographics """)
    col1_dem, col2_dem = st.columns(2)
    with col1_dem:
        # GENDER header
        st.markdown(""" #### GENDER """)
        labels = ["Female", "Male"]
        sizes = [10, 38]
        color_map = {"Female": "#95d0c7", "Male": "#b0d0e8"}
        fig = px.pie(names=labels, values=sizes, color=labels, color_discrete_map=color_map)
        fig.update_layout(
            showlegend=True,
            width=400,
            height=400,
            legend=dict(
                x=1.1,
                y=0.5,
                traceorder="normal",
                font=dict(
                    family="sans-serif",
                    size=12,
                    color="black"
                ),
                bgcolor="White"
            )
        )
        st.plotly_chart(fig)
    with col2_dem:
        # Student header
        st.markdown(""" #### EDUCATION LEVEL """)
        bar_labels = ["Undergraduates", "Graduates"]
        bar_sizes = [30, 18]
        bar_fig = px.bar(x=bar_labels, y=bar_sizes, color=bar_labels,
                         color_discrete_map={label: "#ffccb3" for label in bar_labels},
                         labels={'color': 'Education Level'})
        bar_fig.update_layout(showlegend=False, xaxis_title="Education level", yaxis_title="No. Participants")
        st.plotly_chart(bar_fig)
    st.markdown('\n')

if choose == "Interactive visualizations":
    df = pd.read_pickle('data/dataframe')
    df['date'] = pd.to_datetime(df['date'].astype("str"), format='%Y-%m-%d')
    selected = option_menu(None, ["Behavior Patterns", "Exercise", 'Sleep', 'Self-reports'], menu_icon="cast",
                           default_index=0, orientation="horizontal")
    if selected == "Behavior Patterns":

        st.markdown(""" ## Behavior Patterns """)

        col1, col2 = st.columns([1, 2], gap='large')
        col1.markdown('**Select data to preview**')
        category = col1.radio("Select variable:", ["silence", "voice", "noise"])

        # Filter the data based on the selected gender
        if category == "silence":
            filtered_data = calories
        else:
            filtered_data = calories[calories["gender"] == category]

        mean_calories_per_day = filtered_data.groupby("date")["calories"].mean()
        col2.line_chart(mean_calories_per_day, y='calories')


    if selected == "Exercise":
        st.markdown(""" ## Exercise """)
        st.markdown("""
                           ### Exercise Daily Pattern 
                           """)

        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by="date")
        df['walking (in hours)'] = df['walking (in hours)'].astype(float)
        df['running (in hours)'] = df['running (in hours)'].astype(float)

        # Calculate the mean data for each date
        df_mean = df.groupby('date').agg({
            'walking (in hours)': 'mean',
            'running (in hours)': 'mean'
        }).reset_index()

        df_long = df_mean.melt(id_vars=['date'],
                               value_vars=['walking (in hours)', 'running (in hours)'],
                               var_name='activity', value_name='hours')

        color_scale = alt.Scale(domain=['walking (in hours)', 'running (in hours)'],
                                range=['#FFB6C1', '#CD5C5C'])

        combined_chart = alt.Chart(df_long).mark_line(color='indianred').encode(
            x=alt.X('date:T', axis=alt.Axis(title='Date', format='%d %b %Y', labelFontSize=25,
                                            titleFontSize=25)),
            y=alt.Y('hours:Q', axis=alt.Axis(title='Hours per day', labelFontSize=25,
                                             titleFontSize=25)),
            color=alt.Color('activity:N', scale=color_scale,legend=alt.Legend(title='Activity', labelFontSize=15,
                                                            titleFontSize=15)),
            tooltip=['date', 'activity', 'hours']).interactive()
        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
        # info section
        info_hr = '''
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
                <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below visualizes the hours the participants walked or runned thoughout the experiment dates.                                                                                                                          
                '''
        st.markdown(info_hr, unsafe_allow_html=True)
        st.markdown('\n')
        st.altair_chart(combined_chart, use_container_width=True)

    if selected == "Self-reports":

        st.markdown(""" ## Self-reported Data """)





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
