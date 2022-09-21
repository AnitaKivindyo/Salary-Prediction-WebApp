import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl','rb') as file:
        data=pickle.load(file)
    return data

data = load_model()

regressor= data["model"]
le_country= data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some Information to predict the salary!""")


    countries = (
        "United States",         
        "India",                 
        "United Kingdom",        
        "Germany",               
        "Canada",                
        "Brazil",                
        "France",               
        "Spain",                  
        "Australia",              
        "Netherlands",            
        "Poland",                 
        "Italy",                 
        "Russian Federation",     
        "Sweden",
    )

    education = (
        "Less than Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox( "Country", countries)
    education = st.selectbox( "Level of Education", education)

    experience= st.slider("Years of Experience", 0,50,2 )

    ok =st.button("Calculate the Salary") 
    if ok: #if ok is true
        X= np.array([[country,education,experience] ])

        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
