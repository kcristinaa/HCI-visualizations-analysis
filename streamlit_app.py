from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import altair as alt
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

    col1_dem, col2_dem, col3_dem = st.columns(3)

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

    with col3_dem:
        st.markdown(""" #### BMI """)

        df['Height (m)'] = (df['Height (cm)'] / 100)
        df['BMI'] = df['Weight (kg)'] / df['Height (m)'] ** 2
        bins = [-np.inf, 18.5, 25, 30, np.inf]
        labels = ["underweight", "healthy", "overweight", "obese"]
        df['bmi_cat'] = pd.cut(df['BMI'], bins=bins, labels=labels)

        # create the bar chart
        bmi = df[['id', 'bmi_cat']]
        bmi = bmi.loc[bmi.astype(str).drop_duplicates().index]
        bmi_counts = bmi['bmi_cat'].value_counts().reset_index()
        bmi_counts.columns = ['bmi_cat', 'Count']

        color_discrete_map = {
            'underweight': '#ffff99',
            'healthy': '#ffff99',
            'overweight': '#ffff99',
            'obese': '#ffff99'}

        bmi_counts['Color'] = bmi_counts['bmi_cat'].map(color_discrete_map)
        fig = px.bar(bmi_counts, x='bmi_cat', y='Count', color='bmi_cat', color_discrete_map=color_discrete_map)
        fig.update_layout(
            showlegend=False,
            xaxis_title='BMI',
            yaxis_title='No. Participants',
            xaxis=dict(
                title_font=dict(
                    size=25, 
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

        fig.update_traces(marker=dict(color=bmi_counts['Color']))
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
        heartRate_trend['Date'] = pd.to_datetime(heartRate_trend['Date'])

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
        fig = st.line_chart(heartRate_trend.set_index('Date'), height=300)
        # Customize the layout of the plot
        #fig.update_layout(height = 500, width = 1200, showlegend=True, xaxis_title='Date',
        ##                  yaxis_title='Heart Rate',xaxis=dict(title_font=dict(size=25),tickfont=dict(size=20)),
        #                  yaxis=dict(title_font=dict(size=25),tickfont=dict(size=20)))
        #st.plotly_chart(fig)

        # body temperature plot

        st.markdown("""
                           ### Body Temperature Daily Trend 
                           """)

        df['datetime'] = pd.to_datetime(df['datetime'])

        # Split the datetime_column into date and time columns
        df['date'] = df['datetime'].dt.date
        df['TEMP'] = pd.to_numeric(df['TEMP'], errors='coerce')

        heartRate = df[['id', 'date', 'TEMP']]
        heartRate_max = heartRate.groupby('date').agg({'TEMP': 'max'})
        heartRate_max.reset_index(inplace=True)
        heartRate_max = heartRate_max.rename(columns={'TEMP': 'Max', 'date': 'Date'})
        heartRate_min = heartRate.groupby('date').agg({'TEMP': 'min'})
        heartRate_min = heartRate_min.rename(columns={'TEMP': 'Min'})
        heartRate_min.reset_index(inplace=True, drop=True)
        heartRate_mean = round(heartRate.groupby('date').agg({'TEMP': 'mean'}), 1)
        heartRate_mean = heartRate_mean.rename(columns={'TEMP': 'Mean'})
        heartRate_mean.reset_index(inplace=True, drop=True)
        heartRate_trend = pd.concat([heartRate_max, heartRate_min, heartRate_mean], axis=1)
        heartRate_trend['Date'] = pd.to_datetime(heartRate_trend['Date'])

        df_male = df[df['Gender'] == 'male']
        df_female = df[df['Gender'] == 'female']

        all_mean = round(df['TEMP'].mean(), 2)
        male_mean = round(df_male['TEMP'].mean(), 2)
        female_mean = round(df_female['TEMP'].mean(), 2)

        col1, col2, col3 = st.columns(3)
        col2.metric(label='Avg. value', value=all_mean)
        col1.metric(label='Avg. value (Male)', value=male_mean, delta=round(male_mean - all_mean, 2))
        col3.metric(label='Avg. value (Female)', value=female_mean, delta=round(female_mean - all_mean, 2))

        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
        # info section
        info_hr = '''
                   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
                   <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below compares the min, max and mean body temperature versus the experiment dates for all participants.                                                                                                                          
                   '''
        st.markdown(info_hr, unsafe_allow_html=True)
        st.markdown('\n')
        fig = st.line_chart(heartRate_trend.set_index('Date'), height=300)


    if selected == "Self-reports":

        st.markdown(""" ## Self-reported Data """)

        df = pd.read_csv('data\data_total.csv', index_col=0)
        df['DayName'] = pd.to_datetime(df['datetime'])
        df['DayName'] = df['DayName'].dt.strftime('%a, %Y-%m-%d')

        summer_data = df[['id', 'DayName', 'PA_Score']]
        winter_data = df[['id', 'DayName', 'NA_Score']]

        sorted_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        summer_data['DayName'] = pd.Categorical(summer_data['DayName'], categories=sorted_days, ordered=True)
        winter_data['DayName'] = pd.Categorical(winter_data['DayName'], categories=sorted_days, ordered=True)

        df1 = pd.DataFrame(summer_data)
        df2 = pd.DataFrame(winter_data)


        # Function to calculate mean, min, and max values for each day
        def calculate_aggregates(data, col='PA_Score'):
            grouped_data = data.groupby('DayName')[col]
            mean_stress = grouped_data.mean().reset_index()
            min_stress = grouped_data.min().reset_index()
            max_stress = grouped_data.max().reset_index()
            return mean_stress, min_stress, max_stress


        df1_mean, df1_min, df1_max = calculate_aggregates(df1, col='PA_Score')
        df2_mean, df2_min, df2_max = calculate_aggregates(df2, col='NA_Score')

        df1 = df1.merge(df1_mean, on='DayName', suffixes=('', '_mean'))
        df1 = df1.merge(df1_min, on='DayName', suffixes=('', '_min'))
        df1 = df1.merge(df1_max, on='DayName', suffixes=('', '_max'))
        df1['Season of the year'] = 'Summer Term'

        df2 = df2.merge(df2_mean, on='DayName', suffixes=('', '_mean'))
        df2 = df2.merge(df2_min, on='DayName', suffixes=('', '_min'))
        df2 = df2.merge(df2_max, on='DayName', suffixes=('', '_max'))
        df2['Season of the year'] = 'Winter Term'

        combined_df = pd.concat([df1, df2])

        sorted_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        combined_df['DayName'] = pd.Categorical(combined_df['DayName'], categories=sorted_days, ordered=True)
        sorted_df = combined_df.sort_values(by='DayName')

        df1['term'] = 'Summer Term'
        df2['term'] = 'Winter Term'

        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
        # info section
        info_stai = """
                ### PANAS
                """
        st.markdown(info_stai, unsafe_allow_html=True)
        st.markdown('\n')

        scale = alt.Scale(domain=['Summer Term', 'Winter Term'], range=['#ffccb3', '#95d0c7'])

        line_chart1 = alt.Chart(df1).mark_line(color='#ffccb3').encode(
            x=alt.X('DayName:N', sort=sorted_days,
                    axis=alt.Axis(labelFontSize=15, titleFontSize=20, title='Day of the Week')),
            y=alt.Y('stai_stress_mean:Q',
                    axis=alt.Axis(labelFontSize=15, title='STAI stress scores', titleFontSize=20)),
            # color='Season of the year:N',
            color=alt.Color('Season of the year:N', scale=scale),
            tooltip=['DayName', 'stai_stress_mean', 'stai_stress_min', 'stai_stress_max']
        )

        confidence_interval1 = alt.Chart(df1).mark_area(opacity=0.3, color='#ffccb3').encode(
            x=alt.X('DayName', axis=alt.Axis(labelFontSize=15), sort=sorted_days),
            y='stai_stress_min',
            y2='stai_stress_max'
        )

        line_chart2 = alt.Chart(df2).mark_line(color='#95d0c7').encode(
            x=alt.X('DayName', axis=alt.Axis(labelFontSize=15), sort=sorted_days),
            y='stai_stress_mean',
            # color='Season of the year:N',
            color=alt.Color('Season of the year:N', scale=scale),
            tooltip=['DayName', 'stai_stress_mean', 'stai_stress_min', 'stai_stress_max']
        )

        confidence_interval2 = alt.Chart(df2).mark_area(opacity=0.3, color='#95d0c7').encode(
            x=alt.X('DayName', axis=alt.Axis(labelFontSize=15), sort=sorted_days),
            y='stai_stress_min',
            y2='stai_stress_max'
        )

        # Combine the line charts and shaded confidence intervals into one interactive chart
        combined_chart = (line_chart1 + confidence_interval1 + line_chart2 + confidence_interval2).properties(
            width=800, height=400
        ).interactive().configure_legend(
            labelFontSize=20
        )
        # Show the interactive chart in Streamlit
        st.altair_chart(combined_chart, use_container_width=True)

        # finding
        finding_all = '''
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
                        <i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> As someone could expect, the highest 
                        stress during the winter months is observed on Sundays before the start of the week. During the summer months, a different pattern is observed probably because the daily routine is altered due to vacations. The highest stress score during the summer months is witnessed on Thursdays.
                        '''
        st.markdown(finding_all, unsafe_allow_html=True)
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
