import pandas as pd
from PIL import Image
import streamlit as st
from statistics import mean
import plotly.express as px


# format page (browser, logo, title, )
st.set_page_config(layout="wide", page_title="LifeSnaps Web Interface", page_icon=Image.open('./content/datalab_logo.png'))
st.image(Image.open('./content/datalab_logo_full.png'), width=200)
st.title("Demographics & Engagement of the LifeSnaps Participants")
st.sidebar.title("LifeSnaps Web Interface")
# change css for h1
st.markdown(""" <style> h1{ text-align:center; font-family: 'Cooper Black'; color: #0e3f6e;} </style> """, unsafe_allow_html=True)

# change css for h3, p, info text, h4 and h5
st.markdown(""" <style> h3, h4 {font-family: 'Cooper Black'; color: #2e8c7f;} p{font-size: 20px;} h4{text-align: center;}
.css-5rimss{font-size: 20px;} h5{font-family: 'Cooper Black'; color: #0e3f6e;} </style> """, unsafe_allow_html=True)


# add the section for Demographics
st.markdown(""" ### Participants' Demographics """)

# info section
info_demographics = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
<i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> The plots below describe the demographics of the LifeSnaps sample.                                                                                                                                                                      
'''
st.markdown(info_demographics, unsafe_allow_html=True)
st.markdown('\n')

# plots
df = pd.read_csv('./data/data_unprocessed.csv', index_col=0)
df_demographics = df.groupby('id').first()
df_demographics = df_demographics[['gender', 'age', 'bmi']]

col1_dem, col2_dem, col3_dem = st.columns(3)
with col1_dem:
    # GENDER header
    st.markdown(""" #### GENDER """)

    # create the donut chart
    gender = pd.DataFrame(df_demographics['gender'].value_counts()).reset_index()
    gender.loc["Not answered"] = ['Not answered', 71-gender['gender'].sum()]
    gender.reset_index(drop=True, inplace=True)
    gender.rename(columns={'index': 'Gender', 'gender': 'Value'}, inplace=True)
    fig = px.pie(gender, values='Value', names='Gender', color='Gender', color_discrete_map={'MALE': '#b0d0e8', 'FEMALE': '#95d0c7', 'Not answered': '#bfbfbf'})
    st.plotly_chart(fig, use_container_width=True)

with col2_dem:
    # AGE header
    st.markdown(""" #### AGE """)

    # create the bar chart
    age = pd.DataFrame(df_demographics['age'].value_counts()).reset_index()
    age.loc["Not answered"] = ['Not answered', 71-age['age'].sum()]
    age.reset_index(drop=True, inplace=True)
    age.rename(columns={'index': 'Age', 'age': 'Value'}, inplace=True)
    fig = px.bar(age, x='Age', y='Value', color='Age', text='Value', color_discrete_map={'<30': '#b0d0e8', '>=30': '#95d0c7', 'Not answered': '#bfbfbf'})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col3_dem:
    # BMI header
    st.markdown(""" #### BMI """)

    # create the donut chart
    bmi = pd.read_csv('./data/df_bmi.csv', index_col=0)
    bmi = pd.DataFrame(bmi.value_counts()).reset_index()
    bmi.loc["Not answered"] = ['Not answered', 71-bmi[0].sum()]
    bmi.reset_index(drop=True, inplace=True)
    bmi.rename(columns={'bmi': 'BMI', 0: 'Value'}, inplace=True)
    fig = px.bar(bmi, x='Value', y='BMI', color='BMI', text='Value', orientation='h',
                 color_discrete_map={'Normal': '#b0d0e8', 'Overweight': '#95d0c7', 'Underweight': '#ffccb3', 'Obese': '#ffff99', 'Not answered': '#bfbfbf'})
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
st.markdown('\n')


# add the section for Engagement
st.markdown(""" ### Participants' Engagement """)

# info section
info_engagement = '''
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
<i class="fa-solid fa-circle-info" style="color: #0e3f6e;"></i> Below are presented the statistics of the 
average engagement of all the participants, as well as based on their demographic characteristics (gender, age, bmi). 
It describes how many days on average the participants have tracked features of each category, 
out of the maximum days that a participant has tracked the corresponding category.                                                                                                                                                                        
'''
st.markdown(info_engagement, unsafe_allow_html=True)
st.markdown('\n')

# create the selectbox
session = st.selectbox('session',options=['All', 'Gender', 'Age', 'BMI'], label_visibility = 'collapsed')

# create the function that aggregates the data
def data_aggregation(selection, df, value):
    # find max tracking days per user
    users = df['id'].unique()
    max_days_health = []
    max_days_exercise = []
    max_days_sleep = []
    for user in users:
        if selection =='All':
                df_user = df.loc[df['id'] == user]
                max_days_health.append(df_user['resting_hr'].count())
                max_days_exercise.append(df_user['steps'].count())
                max_days_sleep.append(df_user['sleep_duration'].count())
        elif selection == 'Gender':
                if df.loc[df['id'] == user, 'gender'].iloc[0] == value:
                    df_user = df.loc[df['id'] == user]
                    max_days_health.append(df_user['resting_hr'].count())
                    max_days_exercise.append(df_user['steps'].count())
                    max_days_sleep.append(df_user['sleep_duration'].count())
        elif selection == 'Age':
                if df.loc[df['id'] == user, 'age'].iloc[0] == value:
                    df_user = df.loc[df['id'] == user]
                    max_days_health.append(df_user['resting_hr'].count())
                    max_days_exercise.append(df_user['steps'].count())
                    max_days_sleep.append(df_user['sleep_duration'].count())
        elif selection == 'BMI':
            if df.loc[df['id'] == user, 'bmi'].iloc[0] == value:
                df_user = df.loc[df['id'] == user]
                max_days_health.append(df_user['resting_hr'].count())
                max_days_exercise.append(df_user['steps'].count())
                max_days_sleep.append(df_user['sleep_duration'].count())

    return max_days_health, max_days_exercise, max_days_sleep


# change label's css
st.markdown(
    """ <style> .css-1wivap2 > div > p {font-family: 'Cooper Black'; font-weight: 600; font-size: 1.5rem; text-align: center; color: #2e8c7f;} </style> """,
    unsafe_allow_html=True)
st.markdown(""" <style> .css-1wivap2 {font-size: 28px;} </style>""", unsafe_allow_html=True)

if session == 'All':
    # call function
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('All', df, 'None')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str((mean(max_days_health).round(2)/max(max_days_health)*100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str((mean(max_days_exercise).round(2)/max(max_days_exercise)*100).round(2)) + '%)')
    col3stats.metric(label='SLEEP', value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str((mean(max_days_sleep).round(2)/max(max_days_sleep)*100).round(2)) + '%)')
    # finding
    st.markdown('\n')
    finding_all = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> Participants' engagement fluctuates around 50% in the health and exercise
    tracking, while is lower, ~43%, in the sleep tracking.'''
    st.markdown(finding_all, unsafe_allow_html=True)

if session == 'Gender':
    # male
    st.markdown(""" ##### MALE """)
    # call function
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('Gender', df, 'MALE')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',
                     value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str(
                         (mean(max_days_health).round(2) / max(max_days_health) * 100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',
                     value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str(
                         (mean(max_days_exercise).round(2) / max(max_days_exercise) * 100).round(2)) + '%)')
    col3stats.metric(label='SLEEP',
                     value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str(
                         (mean(max_days_sleep).round(2) / max(max_days_sleep) * 100).round(2)) + '%)')
    # female
    st.markdown(""" ##### FEMALE """)
    # call function
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('Gender', df, 'FEMALE')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',
                     value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str(
                         (mean(max_days_health).round(2) / max(max_days_health) * 100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',
                     value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str(
                         (mean(max_days_exercise).round(2) / max(max_days_exercise) * 100).round(2)) + '%)')
    col3stats.metric(label='SLEEP',
                     value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str(
                         (mean(max_days_sleep).round(2) / max(max_days_sleep) * 100).round(2)) + '%)')
    # finding
    st.markdown('\n')
    finding_all = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> Participants' engagement level is not significantly affected by their 
    gender and it fluctuates again around 50% in the health and exercise tracking, while is lower, ~42%, in the sleep tracking.'''
    st.markdown(finding_all, unsafe_allow_html=True)

if session == 'Age':
    # <30
    st.markdown(""" ##### <30 """)
    # call function
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('Age', df, '<30')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',
                     value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str(
                         (mean(max_days_health).round(2) / max(max_days_health) * 100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',
                     value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str(
                         (mean(max_days_exercise).round(2) / max(max_days_exercise) * 100).round(2)) + '%)')
    col3stats.metric(label='SLEEP',
                     value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str(
                         (mean(max_days_sleep).round(2) / max(max_days_sleep) * 100).round(2)) + '%)')
    # >=30
    st.markdown(""" ##### >=30 """)
    # call function
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('Age', df, '>=30')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',
                     value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str(
                         (mean(max_days_health).round(2) / max(max_days_health) * 100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',
                     value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str(
                         (mean(max_days_exercise).round(2) / max(max_days_exercise) * 100).round(2)) + '%)')
    col3stats.metric(label='SLEEP',
                     value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str(
                         (mean(max_days_sleep).round(2) / max(max_days_sleep) * 100).round(2)) + '%)')
    # finding
    st.markdown('\n')
    finding_all = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> Participants' engagement level is significantly affected by their 
    age! In more detail, participants aged less than 30, appear lower engagement in all the features' tracking, ranging from ~ 38% to 44%. In contrast, 
    participants aged 30 or more, appear higher engagement in all the features' tracking, ranging from ~ 50% to 59%. The higher difference is
    observed in the tracking of health. '''
    st.markdown(finding_all, unsafe_allow_html=True)

if session == 'BMI':
    # Normal
    st.markdown(""" ##### Normal """)
    # call function
    df = pd.read_csv('./data/df_bmi_eng.csv', index_col=0)
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('BMI', df, 'Normal')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',
                     value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str(
                         (mean(max_days_health).round(2) / max(max_days_health) * 100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',
                     value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str(
                         (mean(max_days_exercise).round(2) / max(max_days_exercise) * 100).round(2)) + '%)')
    col3stats.metric(label='SLEEP',
                     value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str(
                         (mean(max_days_sleep).round(2) / max(max_days_sleep) * 100).round(2)) + '%)')
    # Overweight
    st.markdown(""" ##### Overweight """)
    # call function
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('BMI', df, 'Overweight')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',
                     value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str(
                         (mean(max_days_health).round(2) / max(max_days_health) * 100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',
                     value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str(
                         (mean(max_days_exercise).round(2) / max(max_days_exercise) * 100).round(2)) + '%)')
    col3stats.metric(label='SLEEP',
                     value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str(
                         (mean(max_days_sleep).round(2) / max(max_days_sleep) * 100).round(2)) + '%)')
    # Underweight
    st.markdown(""" ##### Underweight """)
    # call function
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('BMI', df, 'Underweight')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',
                     value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str(
                         (mean(max_days_health).round(2) / max(max_days_health) * 100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',
                     value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str(
                         (mean(max_days_exercise).round(2) / max(max_days_exercise) * 100).round(2)) + '%)')
    col3stats.metric(label='SLEEP',
                     value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str(
                         (mean(max_days_sleep).round(2) / max(max_days_sleep) * 100).round(2)) + '%)')
    # Obese
    st.markdown(""" ##### Obese """)
    # call function
    max_days_health, max_days_exercise, max_days_sleep = data_aggregation('BMI', df, 'Obese')
    # display the statistics
    col1stats, col2stats, col3stats = st.columns(3)
    col1stats.metric(label='HEALTH',
                     value=str(mean(max_days_health).round(2)) + '/' + str(max(max_days_health)) + ' days (' + str(
                         (mean(max_days_health).round(2) / max(max_days_health) * 100).round(2)) + '%)')
    col2stats.metric(label='EXERCISE',
                     value=str(mean(max_days_exercise).round(2)) + '/' + str(max(max_days_exercise)) + ' days (' + str(
                         (mean(max_days_exercise).round(2) / max(max_days_exercise) * 100).round(2)) + '%)')
    col3stats.metric(label='SLEEP',
                     value=str(mean(max_days_sleep).round(2)) + '/' + str(max(max_days_sleep)) + ' days (' + str(
                         (mean(max_days_sleep).round(2) / max(max_days_sleep) * 100).round(2)) + '%)')
    # finding
    st.markdown('\n')
    finding_all = '''
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">                                                                                                    
    <i class="fa-solid fa-magnifying-glass" style="color: #2d5986;"></i> Participants' engagement level is also significantly affected by their 
    BMI! Firstly, underweight and obese participants tracked their data fewer days than the normal and overweight participants. However, 
    the underweight participants show the higher consistency in their tracking behavior, as their engagement level is greater than 55% in all
    the features, while all the other participants have engagement level lower than 55%.'''
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
