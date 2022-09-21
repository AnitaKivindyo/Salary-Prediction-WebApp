import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# the data cleaning functions
def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than Bachelors'

#the pd script from begining to end
@st.cache
def load_data():
    df=pd.read_csv('data/survey_results_public.csv')
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 300000]
    df = df[df["Salary"] >= 100000]
    df = df[df["Country"] != 'Other']


    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)

    return df

df = load_data()

def show_explore_page():
    st.title("Explore Softaware Developers Salaries")

    st.write(
        """
        ### Stack Overflow Developer survay 2020
        """
    )
#pie chart
    data = df["Country"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal") #equal aspect ratio ensures that the pie is drawn as a circle

    st.write(""" #### Number of data from different countries """)

    st.pyplot(fig1)
#bar-chart
    st.write(
        """
        #### Mean Salary based on country
        """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)
#line_graph
    st.write(
        """
        #### Mean Salary based on Experience
        """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)





