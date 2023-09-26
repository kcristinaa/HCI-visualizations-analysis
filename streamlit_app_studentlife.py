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
    st.markdown("""The StudentLife continuous sensing app assesses the day-to-day and week-by-week impact of workload on 
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
    selected = option_menu(None, ["Behavior Patterns", "Exercise", 'Self-reports'], menu_icon="cast",
                           default_index=0, orientation="horizontal")

    if selected == "Behavior Patterns":

        st.markdown(""" ## Behavior Patterns """)
        st.markdown("""
                                   ### Sound Surroundings 
                                   """)
        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
        # info section
        info_hr = '''
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
                        <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The audio classifier runs 24/7 with duty cycling. It makes audio inferences for 1 
                minutes, then pause for 3 minutes before restart. If the conversation classifier detects that there is 
                a conversation going on, it will keep running until the conversation is finished. It generates one 
                audio inference every 2~3 seconds. The plot below visualizes the total hours per day the participants
                spent in silence, voice and noise environment.                                                                                                                       
                        '''
        st.markdown(info_hr, unsafe_allow_html=True)
        st.markdown('\n')

        df['silence (in hours)'] = df['silence (in hours)'].apply(pd.to_numeric, errors='coerce')
        df['voice (in hours)'] = df['voice (in hours)'].apply(pd.to_numeric, errors='coerce')
        df['noise (in hours)'] = df['noise (in hours)'].apply(pd.to_numeric, errors='coerce')


        col1, col2 = st.columns([1, 2])
        col1.markdown('**Select data to preview**')
        category = col1.radio("Select variable:", ["silence (in hours)", "voice (in hours)", "noise (in hours)"])

        # Filter the data based on the selected variable
        if category == "silence (in hours)":
            filtered_data = df[["date", "silence (in hours)"]]
        if category == "voice (in hours)":
            filtered_data = df[["date", "voice (in hours)"]]
        if category == "noise (in hours)":
            filtered_data = df[["date", "noise (in hours)"]]

        #st.write(filtered_data)

        mean_per_day = filtered_data.groupby("date")[category].mean()
        col2.line_chart(mean_per_day)

        st.markdown("""
                        ### Conversation Daily Trends
                    """)
        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
        # info section
        info_hr = '''
                                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
                                <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below visualizes the time the participants
                spent participating in conversations and in phone calls.                                                                                                  
                                '''
        st.markdown(info_hr, unsafe_allow_html=True)
        st.markdown('\n')

        df['conversation_duration_in_hours'] = df['conversation_duration_in_hours'].apply(pd.to_numeric, errors='coerce')
        df['CALLS_duration_in_minutes'] = df['CALLS_duration_in_minutes'].apply(pd.to_numeric, errors='coerce')

        col1, col2 = st.columns([1, 2])
        col1.markdown('**Select data to preview**')
        category = col1.radio("Select variable:", ["conversation_duration_in_hours", "CALLS_duration_in_minutes"])

        # Filter the data based on the selected variable
        if category == "conversation_duration_in_hours":
            filtered_data = df[["date", "conversation_duration_in_hours"]]
        if category == "CALLS_duration_in_minutes":
            filtered_data = df[["date", "CALLS_duration_in_minutes"]]

        # st.write(filtered_data)

        mean_per_day = filtered_data.groupby("date")[category].mean()
        col2.line_chart(mean_per_day)


    if selected == "Exercise":
        st.markdown(""" ## Exercise """)
        st.markdown("""
                           ### Exercise Daily Pattern 
                           """)

        EXAMPLE_PLOT_VAR = {"walking (in hours)": "walking (in hours)",
                            "running (in hours)": "running (in hours)"}

        plot_var_name = st.selectbox("Select variable to calculate its daily average value:", list(EXAMPLE_PLOT_VAR.keys()), 0)
        plot_var = EXAMPLE_PLOT_VAR[plot_var_name]

        df['walking (in hours)'] = df['walking (in hours)'].astype(float)
        df['running (in hours)'] = df['running (in hours)'].astype(float)

        heartRate = df[['id', 'date', plot_var_name]]
        heartRate_max = heartRate.groupby('date').agg({plot_var_name: 'max'})
        heartRate_max.reset_index(inplace=True)
        heartRate_max = heartRate_max.rename(columns={plot_var_name: 'Max', 'date': 'Date'})
        heartRate_min = heartRate.groupby('date').agg({plot_var_name: 'min'})
        heartRate_min = heartRate_min.rename(columns={plot_var_name: 'Min'})
        heartRate_min.reset_index(inplace=True, drop=True)
        heartRate_mean = round(heartRate.groupby('date').agg({plot_var_name: 'mean'}), 1)
        heartRate_mean = heartRate_mean.rename(columns={plot_var_name: 'Mean'})
        heartRate_mean.reset_index(inplace=True, drop=True)
        heartRate_trend = pd.concat([heartRate_max, heartRate_min, heartRate_mean], axis=1)

        all_mean = round(df[plot_var_name].mean(),2)

        col1, col2, col3 = st.columns(3)
        col1.metric(label='Average hours per day',value=str(all_mean))


        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)


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

        df['date'] = pd.to_datetime(df['date'])
        df['DayName'] = df['date'].dt.day_name()

        summer_data = df[['id', 'DayName', 'label_panas_PA']].rename(columns={'label_panas_PA': 'panas_PA'})
        winter_data = df[['id', 'DayName', 'label_panas_NA']].rename(columns={'label_panas_NA': 'panas_NA'})

        sorted_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        summer_data['DayName'] = pd.Categorical(summer_data['DayName'], categories=sorted_days, ordered=True)
        winter_data['DayName'] = pd.Categorical(winter_data['DayName'], categories=sorted_days, ordered=True)

        # Define a function to calculate mean, min, and max values for each day
        def calculate_aggregates(data, col):
            grouped_data = data.groupby('DayName')[col]
            mean_stress = grouped_data.mean().reset_index()
            min_stress = grouped_data.min().reset_index()
            max_stress = grouped_data.max().reset_index()
            return mean_stress, min_stress, max_stress


        # Calculate and merge aggregate values for both seasons
        df1_mean, df1_min, df1_max = calculate_aggregates(summer_data, 'panas_PA')
        summer_data = summer_data.merge(df1_mean, on='DayName', suffixes=('', '_mean'))
        summer_data = summer_data.merge(df1_min, on='DayName', suffixes=('', '_min'))
        summer_data = summer_data.merge(df1_max, on='DayName', suffixes=('', '_max'))
        summer_data['PANAS'] = 'Positive Affect'

        df2_mean, df2_min, df2_max = calculate_aggregates(winter_data, 'panas_NA')
        winter_data = winter_data.merge(df2_mean, on='DayName', suffixes=('', '_mean'))
        winter_data = winter_data.merge(df2_min, on='DayName', suffixes=('', '_min'))
        winter_data = winter_data.merge(df2_max, on='DayName', suffixes=('', '_max'))
        winter_data['PANAS'] = 'Negative Affect'

        # Combine the two datasets and sort by day of the week
        combined_df = pd.concat([summer_data, winter_data])
        combined_df['DayName'] = pd.Categorical(combined_df['DayName'], categories=sorted_days, ordered=True)

        sorted_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        combined_df['DayName'] = pd.Categorical(combined_df['DayName'], categories=sorted_days, ordered=True)
        sorted_df = combined_df.sort_values(by='DayName')

        summer_data['PANAS'] = 'Positive Affect'
        winter_data['PANAS'] = 'Negative Affect'

        #st.write(summer_data)
        #st.write(winter_data)

        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
        # info section
        info_stai = """
                ### PANAS Questionnaire
                The [PANAS](https://psycnet.apa.org/doiLanding?doi=10.1037%2F0022-3514.54.6.1063) questionnaire stands for Positive and Negative Affect Schedule . It's a widely used 
                self-report measure for assessing the two primary dimensions of mood. The higher the score on 
                the PANAS questionnaire, the greater the level of positive/negative emotions the participant reported feeling.
                """
        st.markdown(info_stai, unsafe_allow_html=True)
        st.markdown('\n')

        scale = alt.Scale(domain=['Positive Affect', 'Negative Affect'], range=['#ffccb3', '#95d0c7'])

        line_chart1 = alt.Chart(summer_data).mark_line(color='#ffccb3').encode(
            x=alt.X('DayName:N', sort=sorted_days,
                    axis=alt.Axis(labelFontSize=15, titleFontSize=20, title='Day of the Week')),
            y=alt.Y('panas_PA_mean:Q',
                    axis=alt.Axis(labelFontSize=15, title='PANAS Scores', titleFontSize=20)),
            # color='Season of the year:N',
            color=alt.Color('PANAS:N', scale=scale),
            tooltip=['DayName', 'panas_PA_mean', 'panas_PA_min', 'panas_PA_max']
        )

        confidence_interval1 = alt.Chart(summer_data).mark_area(opacity=0.3, color='#ffccb3').encode(
            x=alt.X('DayName', axis=alt.Axis(labelFontSize=15), sort=sorted_days),
            y='panas_PA_min',
            y2='panas_PA_max'
        )

        line_chart2 = alt.Chart(winter_data).mark_line(color='#95d0c7').encode(
            x=alt.X('DayName', axis=alt.Axis(labelFontSize=15), sort=sorted_days),
            y='panas_NA_mean',
            # color='Season of the year:N',
            color=alt.Color('PANAS:N', scale=scale),
            tooltip=['DayName', 'panas_NA_mean', 'panas_NA_min', 'panas_NA_max']
        )

        confidence_interval2 = alt.Chart(winter_data).mark_area(opacity=0.3, color='#95d0c7').encode(
            x=alt.X('DayName', axis=alt.Axis(labelFontSize=15), sort=sorted_days),
            y='panas_NA_min',
            y2='panas_NA_max'
        )

        # Combine the line charts and shaded confidence intervals into one interactive chart
        combined_chart = (line_chart1 + line_chart2).properties(
            width=800, height=400
        ).interactive().configure_legend(
            labelFontSize=20
        )
        # Show the interactive chart in Streamlit
        st.altair_chart(combined_chart, use_container_width=True)

        st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
        # info section
        info_stai = """
                        ### Big Five Personality Test
                        blablabla
                        """
        st.markdown(info_stai, unsafe_allow_html=True)
        st.markdown('\n')

        df.columns = [col.replace('label_', '') for col in df.columns]

        def plot_stacked_bar(df):
            columns_to_stack = [
                'extraversion',
                'agreeableness',
                'conscientiousness',
                'neuroticism',
                'openness',
                'loneliness'
            ]

            # Melt the dataframe to have 'id' as identifier and stacked columns as values
            df_melted = df.melt(id_vars=['id'], value_vars=columns_to_stack)

            chart = alt.Chart(df_melted).mark_bar().encode(
                x='id:N',
                y='sum(value):Q',
                color='variable:N',
                tooltip=['variable', 'value']
            ).interactive().properties(width=800, height=400).configure_range(
                category=alt.RangeScheme(
                    ['#b0d0e8', '#95d0c7', '#ffccb3', '#ffffb3', '#e6b3cc', '#d0e8d5']
                )
            )

            return chart

        st.write(plot_stacked_bar(df))

        def plot_stacked_bar(df):
            columns_to_stack = [
                'extraversion',
                'agreeableness',
                'conscientiousness',
                'neuroticism',
                'openness',
                'loneliness'
            ]

            # Melt the dataframe to have 'id' as identifier and stacked columns as values
            df_melted = df.melt(id_vars=['id'], value_vars=columns_to_stack)

            chart = alt.Chart(df_melted).mark_bar().encode(
                x=alt.X('variable:N', axis=alt.Axis(title='Personality Type')),
                y=alt.Y('value:Q', axis=alt.Axis(title='Score')),
                color='variable:N',
                order=alt.Order('variable:N', sort='ascending')
            ).properties(width=800, height=400).configure_range(
                category=alt.RangeScheme(
                    ['#b0d0e8', '#95d0c7', '#ffccb3', '#ffffb3', '#e6b3cc', '#d0e8d5']
                )
            )

            return chart

        st.write(plot_stacked_bar(df))



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
