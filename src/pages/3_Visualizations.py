import bson
import pandas as pd
import altair as alt
from PIL import Image
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t



# format page (browser, logo, title, )
st.set_page_config(layout="wide", page_title="LifeSnaps Web Interface", page_icon=Image.open('./content/datalab_logo.png'))
st.image(Image.open('./content/datalab_logo_full.png'), width=200)
st.title("The LifeSnaps through Visualizations")
st.sidebar.title("LifeSnaps Web Interface")
# change css for h1
st.markdown(""" <style> h1{ text-align:center; font-family: 'Cooper Black'; color: #0e3f6e;} </style> """, unsafe_allow_html=True)
# change css for h2
st.markdown(""" <style> h2{ font-family: 'Cooper Black'; color: #0e3f6e;} </style> """, unsafe_allow_html=True)
# change css for h3
st.markdown(""" <style> h3{  font-family: 'Cooper Black'; color: #2e8c7f;} p{  font-size: 20px;} </style> """, unsafe_allow_html=True)

# create horizontal menu
selected = option_menu(None, ["Health", "Exercise", 'Sleep', 'Self-reports'], menu_icon="cast",
                       default_index=0, orientation="horizontal")

df = pd.read_csv('./data/data_unprocessed.csv', index_col=0)

if selected == "Health":
    st.markdown(""" ## Health """)

    # heart rate plot
    st.markdown("""
               ### Heart Rate Daily Trend for all participants
               """)

    heartRate = df[['id', 'date', 'bpm']]
    heartRate_max = heartRate.groupby('date').agg({'bpm': 'max'})
    heartRate_max.reset_index(inplace=True)
    heartRate_max = heartRate_max.rename(columns={'bpm': 'Max', 'date': 'Date'})
    heartRate_min = heartRate.groupby('date').agg({'bpm': 'min'})
    heartRate_min = heartRate_min.rename(columns={'bpm': 'Min'})
    heartRate_min.reset_index(inplace=True, drop=True)
    heartRate_mean = round(heartRate.groupby('date').agg({'bpm': 'mean'}), 1)
    heartRate_mean = heartRate_mean.rename(columns={'bpm': 'Mean'})
    heartRate_mean.reset_index(inplace=True, drop=True)
    heartRate_trend = pd.concat([heartRate_max, heartRate_min, heartRate_mean], axis=1)
    st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)
    # info section
    info_hr = '''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
        <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below compares the min, max and mean heart rate versus the experiment dates for all participants.                                                                                                                          
        '''
    st.markdown(info_hr, unsafe_allow_html=True)
    st.markdown('\n')
    st.line_chart(heartRate_trend, x='Date', height=300)

    # calories plot

    st.markdown("""
                   ### Mean calories burned per experiment day
                   """)
    st.markdown('\n')

    # info section
    info_hr = '''
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
                <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below visualizes the mean calories burned throughout the experiment dates.                                                                                                                          
                '''
    st.markdown(info_hr, unsafe_allow_html=True)
    st.markdown('\n')


    calories = df[['id', 'date', 'gender', 'calories']]
    calories.gender = calories.gender.fillna('Not answered')

    col1, col2 = st.columns([1, 2], gap='large')
    col1.markdown('**Select data to preview**')
    category = col1.radio("Select gender:", ["All", "MALE", "FEMALE", "Not answered"])

    # Filter the data based on the selected gender
    if category == "All":
        filtered_data = calories
    else:
        filtered_data = calories[calories["gender"] == category]

    mean_calories_per_day = filtered_data.groupby("date")["calories"].mean()
    col2.line_chart(mean_calories_per_day, y='calories')


if selected == "Exercise":
    st.markdown(""" ## Exercise """)

    # show plot
    EXAMPLE_PLOT_VAR = {"Steps": "steps",
                        "Exercise Minutes": ["lightly_active_minutes", "moderately_active_minutes",
                                             "very_active_minutes"]}

    plot_var_name = st.selectbox("Select column to visualize", list(EXAMPLE_PLOT_VAR.keys()), 0)
    plot_var = EXAMPLE_PLOT_VAR[plot_var_name]

    st.markdown("""
           ### Example plot

           Variable: **{}**
           """.format(plot_var_name))

    if isinstance(plot_var, str):
        df_male = df[df['gender'] == 'MALE']
        df_female = df[df['gender'] == 'FEMALE']

        all_mean = df[plot_var].mean().round(2)
        male_mean = df_male[plot_var].mean().round(2)
        female_mean = df_female[plot_var].mean().round(2)

        col1, col2, col3 = st.columns(3)
        col2.metric(label='Avg. value', value=all_mean)
        col1.metric(label='Avg. value (Male)', value=male_mean, delta=round(male_mean - all_mean, 2))
        col3.metric(label='Avg. value (Female)', value=female_mean, delta=round(female_mean - all_mean, 2))

    st.markdown("""#### All users""")
    st.line_chart(df.groupby(by='date', as_index=False).mean(), x='date', y=plot_var)


if selected == "Sleep":
    st.markdown(""" ## Sleep """)
    # change info and findings text css
    st.markdown(""" <style> .css-5rimss{font-size: 20px;} </style> """, unsafe_allow_html=True)

    # --------- First plot ----------------
    st.markdown(""" ### Sleep minutes for all participants """)
    # info section
    info_demographics = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below compares the minutes spent in bed versus the minutes asleep,
    as well as depicts the total sleep duration, on average for all the participants per day of the week.                                                                                                                          
    '''
    st.markdown(info_demographics, unsafe_allow_html=True)
    st.markdown('\n')
    # plot
    # df for bars
    df_v1 = pd.DataFrame()
    df_v1["date"] = pd.to_datetime(df['date'])
    df_v1['Day of the week'] = df_v1['date'].dt.day_name()
    df_v1["Asleep"] = df["minutesAsleep"]
    df_v1["To fall asleep"] = df["minutesToFallAsleep"]
    df_v1["Awake"] = df["minutesAwake"]
    df_v1["After wake up"] = df["minutesAfterWakeup"]
    df_v1["In bed"] = df_v1.iloc[:, -3:-1].sum(axis=1)
    df_v1 = df_v1.drop(columns=["date", "To fall asleep", "Awake", "After wake up"])
    melted_df = pd.melt(df_v1, id_vars=['Day of the week'],value_vars=['Asleep', 'In bed'], var_name='Sleep State')
    grouped_df = melted_df.groupby(['Day of the week', 'Sleep State']).mean().reset_index()
    grouped_df = grouped_df.rename(columns={'value': 'Sleep Minutes'})
    # df for line
    line_df = pd.DataFrame()
    line_df = df[['date', 'sleep_duration']]
    line_df["date"] = pd.to_datetime(line_df['date'])
    line_df['Day of the week'] = line_df['date'].dt.day_name()
    line_df['Sleep Duration'] = df['sleep_duration'] / 60000
    line_df = line_df.drop(columns=["date", "sleep_duration"])
    line_df = line_df.groupby(['Day of the week']).mean().reset_index()
    line_df = line_df.rename(columns={'value': 'Sleep Duration'})
    # combine information
    grouped_df = grouped_df.merge(line_df, how='left', on='Day of the week')
    # create
    fig = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('Day of the week', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], axis=alt.Axis(labelAngle=0)))
    bar = fig.mark_bar().encode(y='Sleep Minutes', color='Sleep State', tooltip=['Day of the week', 'Sleep State', 'Sleep Minutes'])
    line = fig.mark_line(point=True).encode(y='Sleep Duration', tooltip=['Day of the week', 'Sleep Duration'])
    fig = (bar+line).configure_range(category=alt.RangeScheme(['#b0d0e8', '#95d0c7']))
    st.altair_chart(fig, use_container_width=True)
    # finding
    finding_all = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> Firstly, it is observed that there are no significant variations
    of the sleep distribution between the days of the week. However, it is noticeable that on average the users sleep more and spent more 
    time in bed on Tuesdays, thus the total sleep duration is higher than the other days. On the other hand the users total sleep duration 
    is lower on Wednesdays, but they actually are asleep less on Mondays and they spent less time in bed on Saturdays. '''
    st.markdown(finding_all, unsafe_allow_html=True)
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')


    # --------- Second plot ----------------
    st.markdown(""" ### Sleep quality for all participants """)
    # info section
    info_demographics = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below examines if the changes in the values of sleep efficiency, 
    sleep points and sleep duration, on average for all the users during the entire period of the experiment, follow similar patterns.                                                                                                              
    '''
    st.markdown(info_demographics, unsafe_allow_html=True)
    st.markdown('\n')
    # plot
    options = st.multiselect('Select Variables', ['Sleep Efficiency', 'Sleep Duration', 'Sleep Points'], ['Sleep Efficiency', 'Sleep Duration', 'Sleep Points'])
    df_v2 = df[['date', 'sleep_efficiency', 'sleep_duration', 'sleep_points_percentage']]
    df_normalized = df_v2.set_index('date')
    scaler = MinMaxScaler()
    df_normalized = pd.DataFrame(scaler.fit_transform(df_normalized), columns=df_normalized.columns)
    df_normalized['date'] = df_v2['date']
    df_normalized = df_normalized.set_index('date')
    df_normalized = df_normalized.rename(columns={'sleep_efficiency': 'Sleep Efficiency', 'sleep_duration': 'Sleep Duration', 'sleep_points_percentage': 'Sleep Points'})
    grouped_df = df_normalized.groupby(['date']).mean()
    # create
    fig = go.Figure()
    colors = {'Sleep Efficiency': '#b0d0e8', 'Sleep Duration': '#95d0c7', 'Sleep Points': '#ffccb3'}
    for col in options:
        trace = go.Scatter(x=grouped_df.index, y=grouped_df[col], name=col,
                          marker={'color': colors.get(col)})
        fig.add_trace(trace)
        fig.update_traces(hovertemplate='Date: %{x}<br> Value: %{y}')
        fig.update_layout(xaxis_title='Date', yaxis_title='Value')
    st.plotly_chart(fig, use_container_width=True)
    # finding
    finding_all = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> Firstly, it is observed that the values of Sleep Points range over 
    a larger set of values (~ 0.5-0.9), in contrast to the values of Sleep Duration and Efficiency that range over a smaller one (~ 0.26-0.4 
    and ~ 0.86-0.95 respectively). Surprisingly, the changes in variables' values do not behave similarly (e.g., there are not only peaks or curves
    or lines in a specific date). '''
    st.markdown(finding_all, unsafe_allow_html=True)
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')


    # --------- Third plot ----------------
    st.markdown(""" ### Sleep stages for all participants """)
    # info section
    info_demographics = '''
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
        <i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plot below depicts the distribution of the ratio of sleep stages, 
        on average for all the users per day of the week.                                                                                                                                                                
        '''
    st.markdown(info_demographics, unsafe_allow_html=True)
    st.markdown('\n')
    # plot
    df_v3 = pd.DataFrame()
    df_v3["date"] = pd.to_datetime(df['date'])
    df_v3['Day of the week'] = df_v3['date'].dt.day_name()
    df_v3["Deep"] = df["sleep_deep_ratio"]
    df_v3["Wake"] = df["sleep_wake_ratio"]
    df_v3["Light"] = df["sleep_light_ratio"]
    df_v3["Rem"] = df["sleep_rem_ratio"]
    melted_df = pd.melt(df_v3, id_vars=['Day of the week'], value_vars=['Deep', 'Wake', 'Light', 'Rem'],
                        var_name='Sleep Stage')
    grouped_df = melted_df.groupby(['Day of the week', 'Sleep Stage']).mean().reset_index()
    grouped_df = grouped_df.rename(columns={'value': 'Stage Ratio'})
    # create
    fig = alt.Chart(grouped_df).mark_bar().encode(
        x=alt.X('Day of the week', sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                axis=alt.Axis(labelAngle=0)), y='Stage Ratio', color='Sleep Stage',
        tooltip=['Day of the week', 'Sleep Stage', 'Stage Ratio']) \
        .configure_range(category=alt.RangeScheme(['#b0d0e8', '#95d0c7', '#ffccb3', '#ffffb3']))
    st.altair_chart(fig, use_container_width=True)
    # finding
    finding_all = '''
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
            <i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> Firstly, it is observed that there are no significant changes in 
             the distribution of sleep stages between the days of the week. However, in a stage level analysis, it is noticeable that in terms of the
             Wake sleep stage, the highest ration is observed on Sundays, while the lowest is observed on Wednesdays. Moreover, in terms of the Rem sleep 
             stage, the highest is on Fridays and the lowest on Mondays, while in terms of the Light sleep stage, the highest is observed on Sundays and
             the lowest on Wednesdays. Finally, regarding the Deep sleep stage, the highest sleep ratio is observed on Sundays, while the lowest on Mondays.'''
    st.markdown(finding_all, unsafe_allow_html=True)
    st.markdown('\n')
    st.markdown('\n')
    st.markdown('\n')


if selected == "Self-reports":
    st.markdown(""" ## Self-reports """)

    summer_data = pd.read_csv('./data/stai_summer.csv', index_col=0)
    winter_data = pd.read_csv('./data/stai_winter.csv', index_col=0)

    sorted_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    summer_data['DayName'] = pd.Categorical(summer_data['DayName'], categories=sorted_days, ordered=True)
    winter_data['DayName'] = pd.Categorical(winter_data['DayName'], categories=sorted_days, ordered=True)

    df1 = pd.DataFrame(summer_data)
    df2 = pd.DataFrame(winter_data)


    # Function to calculate mean, min, and max values for each day
    def calculate_aggregates(data):
        grouped_data = data.groupby('DayName')['stai_stress']
        mean_stress = grouped_data.mean().reset_index()
        min_stress = grouped_data.min().reset_index()
        max_stress = grouped_data.max().reset_index()
        return mean_stress, min_stress, max_stress

    df1_mean, df1_min, df1_max = calculate_aggregates(df1)
    df2_mean, df2_min, df2_max = calculate_aggregates(df2)

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

    # info section
    st.markdown("""
        ### Stai Stress Scores
        STAI is the “gold standard” for measuring preoperative anxiety [[1]](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6945947/#:~:text=The%20range%20of%20possible%20scores,%E2%80%9D%20(45%2D80).). The higher the  STAI stress score is, the more stressed the participant feels. Blue line is for summer term and green line for the winter term. 
        """)

    st.markdown('\n')


    line_chart1 = alt.Chart(df1).mark_line(color='blue').encode(
        x=alt.X('DayName:N', sort=sorted_days, axis=alt.Axis(title='Day of the Week')),
        y=alt.Y('stai_stress_mean:Q', axis=alt.Axis(title='STAI stress scores')),
        tooltip=['DayName', 'stai_stress_mean', 'stai_stress_min', 'stai_stress_max']
    ).encode(
    color=alt.value('Summer Term')
)

    confidence_interval1 = alt.Chart(df1).mark_area(opacity=0.3, color='blue').encode(
        x=alt.X('DayName', sort=sorted_days),
        y='stai_stress_min',
        y2='stai_stress_max'
    )

    line_chart2 = alt.Chart(df2).mark_line(color='green').encode(
        x=alt.X('DayName', sort=sorted_days),
        y='stai_stress_mean',
        tooltip=['DayName', 'stai_stress_mean', 'stai_stress_min', 'stai_stress_max']
    )

    confidence_interval2 = alt.Chart(df2).mark_area(opacity=0.3, color='green').encode(
        x=alt.X('DayName', sort=sorted_days),
        y='stai_stress_min',
        y2='stai_stress_max'
    )

    # Combine the line charts and shaded confidence intervals into one interactive chart
    combined_chart = (line_chart1 + confidence_interval1 + line_chart2 + confidence_interval2).properties(
        width=600, height=400
    ).interactive()
    # Show the interactive chart in Streamlit
    st.altair_chart(combined_chart)

    # to add stacked bar charts for sema feelings for summer and winter terms

    st.markdown("""
            ### Mood EMA responses
            
            """)

    st.markdown('\n')



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
