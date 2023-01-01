import pandas as pd
import plotly_express as px
import streamlit as st
from PIL import Image


@st.cache
def get_data_from_excel():
    df=pd.read_excel('EmpResults.xlsx')
    return df

img=Image.open('tf.png')
st.set_page_config(layout='wide',page_icon=img,page_title='EMP Dashboard',initial_sidebar_state='expanded')
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

df=get_data_from_excel()

st.sidebar.header('Dashboard `version 1`')
st.sidebar.header("Filter The Data Here:")
country = st.sidebar.multiselect(
    "Select the Country:",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

bu = st.sidebar.multiselect(
    "Select the Business Unit:",
    options=df["Business Unit"].unique(),
    default=df["Business Unit"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)
age = st.sidebar.slider('Specify the age range',18,65, value=[18,65])


st.sidebar.markdown('''
---
Made with ❤️ by [Bensaid Mohamed](mohamed2018bensaid@gmail.com/).
''')

df_selection = df.query("Country == @country & `Business Unit` == @bu & Gender == @gender & @age[1]>= Age >= @age[0]")

labels = {1:'yes', 0:'no'}
df_selection['Still Working']=df_selection['Still Working'].map(labels)

st.title("EMP Dashboard")

avg_sal = int(df_selection["Total Salary"].mean())
avg_age = int(df_selection["Age"].mean())
persdata = int((df_selection.shape[0]/df.shape[0])*100)

st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Average Salary:", f"{avg_sal} $","")
col2.metric("Average Age:", f"{avg_age}","")
col3.metric("Data Selected:", f"{persdata}%",f"{df_selection.shape[0]}")

st.markdown('### Plots')
df2 = pd.DataFrame(df_selection['Hire Year'].value_counts().reset_index().values, columns=["Year", "Hires Number"])
df2=df2.sort_values(by=['Year'])

df3 = pd.DataFrame(df_selection['Department'].value_counts().reset_index().values, columns=["Department", "Employees Number"])

fig_1 = px.line(
    df2,
    x="Year",
    y="Hires Number",
    title="<b>Number of Hires per years</b>",
    template="plotly_white",
    width=550, height=350
)


avg_sal2=df_selection.groupby(by=["Department"]).mean()[["Total Salary"]].sort_values(by="Total Salary")
avg_sal2=avg_sal2.rename(columns={'Total Salary':'Average Salary'})
fig_2 = px.bar(
    avg_sal2,
    x="Average Salary",
    y=avg_sal2.index,
    orientation="h",
    title="<b>Average Salary by Department</b>",
    color_discrete_sequence=["#0083B8"] * len(avg_sal2),
    template="plotly_white",
)

fig_4 = px.line(
    df_selection.sort_values(by=['Working Duration']),
    x="Working Duration",
    y="Total Salary",
    title="<b>Total Salary by Working Duration</b>",
    template="plotly_white",
)
fig_5 = px.pie(df_selection, names='Gender', title='Gender',hole=0.7,width=300, height=350)
fig_6 = px.pie(df_selection, names='Still Working', title='Active Employes',hole=0.7,width=300, height=350)
fig_7 = px.histogram(df_selection, x="Department",color='Gender', title='Department by Gender',barmode='group',width=550, height=350)
c1, c2 = st.columns((7,3))
c3, c4 = st.columns((4,6))
with c1:
    fig_1
with c2:
    fig_6
with c3:
    fig_5
with c4:
    fig_7

st.plotly_chart(fig_2)
st.plotly_chart(fig_4)

st.markdown('### Data Table')
st.dataframe(df_selection)