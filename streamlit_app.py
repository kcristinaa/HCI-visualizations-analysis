from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
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

    col1_dem, col2_dem = st.columns(2)
    with col1_dem:
        # GENDER header
        st.markdown(""" #### GENDER """)

        gender = df[['id', 'Gender']]
        gender = gender.loc[gender.astype(str).drop_duplicates().index]

        # create the donut chart
        gender = pd.DataFrame(df['Gender'].value_counts()).reset_index()
        gender.rename(columns={'index': 'Gender', 'Gender': 'Value'}, inplace=True)
        fig = px.pie(gender, values='Value', names='Gender', color='Gender',
                     color_discrete_map={'male': '#b0d0e8', 'female': '#95d0c7'})
        fig.update_layout(
            legend=dict(
                font=dict(
                    size=25  # Adjust the font size as needed
                )
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2_dem:
        # AGE header
        st.markdown(""" #### AGE """)
        # create the bar chart
        age = df[['id', 'Age']]
        age = age.loc[age.astype(str).drop_duplicates().index]
        age_counts = age['Age'].value_counts().reset_index()
        age_counts.columns = ['Age', 'Count']

        #st.bar_chart(age_counts.set_index('Age'))
        color_discrete_map = {
            24: '#ffccb3',
            25: '#ffccb3',
            26: '#ffccb3',
            27: '#ffccb3',
            28: '#ffccb3',
            29: '#ffccb3',
            34: '#ffccb3',
            35: '#ffccb3'
        }
        age_counts['Color'] = age_counts['Age'].map(color_discrete_map)
        fig = px.bar(age_counts, x='Age', y='Count', color='Age', color_discrete_map=color_discrete_map)
        fig.update_layout(
            showlegend=False,
            xaxis_title='Age',
            yaxis_title='No. Participants',
            xaxis=dict(
                title_font=dict(
                    size=25
                ),
                tickfont=dict(
                    size=20
                )
            ),
            yaxis=dict(
                title_font=dict(
                    size=25
                ),
                tickfont=dict(
                    size=20
                )
            )
        )

        fig.update_traces(marker=dict(color=age_counts['Color']))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('\n')

if choose == "Interactive visualizations":

    # create horizontal menu
    selected = option_menu(None, ["Health", "Exercise", 'Sleep', 'Self-reports'], menu_icon="cast",
                           default_index=0, orientation="horizontal")

    df = pd.read_csv('data\data_total.csv', index_col=0)

    if selected == "Health":
        st.markdown(""" ## Health """)

        # heart rate plot
        st.markdown("""
                   ### Heart Rate Daily Trend 
                   """)

        df['datetime'] = pd.to_datetime(df['datetime'])



        # Split the datetime_column into date and time columns
        df['date'] = df['datetime'].dt.date
        df['HR'] = pd.to_numeric(df['HR'], errors='coerce')

        heartRate = df[['id', 'date', 'HR']]
        heartRate_max = heartRate.groupby('date').agg({'HR': 'max'})
        heartRate_max.reset_index(inplace=True)
        heartRate_max = heartRate_max.rename(columns={'HR': 'Max', 'date': 'Date'})
        heartRate_min = heartRate.groupby('date').agg({'HR': 'min'})
        heartRate_min = heartRate_min.rename(columns={'HR': 'Min'})
        heartRate_min.reset_index(inplace=True, drop=True)
        heartRate_mean = round(heartRate.groupby('date').agg({'HR': 'mean'}), 1)
        heartRate_mean = heartRate_mean.rename(columns={'HR': 'Mean'})
        heartRate_mean.reset_index(inplace=True, drop=True)
        heartRate_trend = pd.concat([heartRate_max, heartRate_min, heartRate_mean], axis=1)

        df_male = df[df['Gender'] == 'male']
        df_female = df[df['Gender'] == 'female']

        all_mean = round(df['HR'].mean(), 2)
        male_mean = round(df_male['HR'].mean(),2)
        female_mean = round(df_female['HR'].mean(),2)

        col1, col2, col3 = st.columns(3)
        col2.metric(label='Avg. value', value=all_mean)
        col1.metric(label='Avg. value (Male)', value=male_mean, delta=round(male_mean - all_mean, 2))
        col3.metric(label='Avg. value (Female)', value=female_mean, delta=round(female_mean - all_mean, 2))

        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
        # info section
        info_hr = '''
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
            <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below compares the min, max and mean heart rate versus the experiment dates for all participants.                                                                                                                          
            '''
        st.markdown(info_hr, unsafe_allow_html=True)
        st.markdown('\n')

        fig = px.line(heartRate_trend, x='Date', y=['Max', 'Min', 'Mean'],
                      labels={'Date': 'Date', 'value': 'Value'}, color_discrete_sequence=['#ffccb3', '#b0d0e8','#95d0c7' ])

        # Customize the layout of the plot
        fig.update_layout(
            height = 500,
            width = 1200,
            showlegend=True,
            xaxis_title='Date',
            yaxis_title='Heart Rate',
            xaxis=dict(
                title_font=dict(
                    size=25
                ),
                tickfont=dict(
                    size=20
                )
            ),
            yaxis=dict(
                title_font=dict(
                    size=25
                ),
                tickfont=dict(
                    size=20
                )
            )        )

        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig)

        #st.line_chart(heartRate_trend, x='Date', height=300)



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
