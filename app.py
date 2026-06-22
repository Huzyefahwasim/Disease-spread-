import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import os
from simulation.disease_sim import DiseaseSimulation

st.set_page_config(page_title="Disease Spread Simulator", layout="wide")

st.title("IT3016- SIMULATION AND MODELLING")
st.header("Disease Spread Simulator Dashboard")

data_path = os.path.join('data', 'disease_data.csv')

@st.cache_data
def load_data():
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return None

df = load_data()

tab1, tab2, tab3 = st.tabs(["Dataset Analysis (EDA)", "Interactive Simulation", "ML Predictions"])

with tab1:
    st.subheader("Exploratory Data Analysis")
    if df is not None:
        st.write("### Dataset Preview")
        st.dataframe(df.head(10))
        
        st.write("### Historical Disease Spread")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df['Date'], df['Susceptible'], label='Susceptible', color='blue')
        ax.plot(df['Date'], df['Infected'], label='Infected', color='red')
        ax.plot(df['Date'], df['Recovered'], label='Recovered', color='green')
        ax.set_title("SIR Model History")
        ax.legend()
        st.pyplot(fig)
        
        st.write("### Daily New Cases")
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.bar(df['Date'], df['New_Cases'], color='orange')
        ax2.set_title("Daily New Cases")
        st.pyplot(fig2)
        
    else:
        st.warning("Dataset not found. Please run the dataset generation script.")

with tab2:
    st.subheader("Interactive SIR Simulation")
    st.write("Adjust the parameters below to see how the disease might spread.")
    
    col1, col2 = st.columns(2)
    with col1:
        population = st.number_input("Population", min_value=1000, value=1000000)
        initial_infected = st.number_input("Initial Infected", min_value=1, value=50)
        days = st.slider("Simulation Days", 10, 365, 100)
        
    with col2:
        beta = st.slider("Transmission Rate (beta)", 0.0, 1.0, 0.25)
        gamma = st.slider("Recovery Rate (gamma)", 0.0, 1.0, 0.1)
        
    if st.button("Run Simulation"):
        sim = DiseaseSimulation(population=population, initial_infected=initial_infected, beta=beta, gamma=gamma, days=days)
        results = sim.run()
        
        sim_df = pd.DataFrame(results)
        
        st.write("### Simulation Results")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(sim_df.index, sim_df['Susceptible'], label='Susceptible', color='blue')
        ax.plot(sim_df.index, sim_df['Infected'], label='Infected', color='red')
        ax.plot(sim_df.index, sim_df['Recovered'], label='Recovered', color='green')
        ax.set_title("Simulated Disease Spread")
        ax.set_xlabel("Days")
        ax.set_ylabel("Population")
        ax.legend()
        st.pyplot(fig)

with tab3:
    st.subheader("Machine Learning Predictions")
    st.write("Comparing ML models on predicting 'New_Cases'")
    
    # Check if models exist
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')] if os.path.exists(models_dir) else []
    
    if len(model_files) > 0 and df is not None:
        selected_model = st.selectbox("Select Model to Evaluate", model_files)
        
        with open(os.path.join(models_dir, selected_model), 'rb') as f:
            model = pickle.load(f)
            
        st.write(f"Loaded model: {selected_model}")
        
        # Prepare latest data point to make a prediction
        st.write("### Make a Prediction for Tomorrow")
        last_7_days = df['New_Cases'].tail(7).values[::-1] # get lag 1 to 7
        latest_stringency = df['Stringency_Index'].iloc[-1]
        latest_tests = df['Tests_Performed'].iloc[-1]
        
        features = list(last_7_days) + [latest_stringency, latest_tests]
        feature_df = pd.DataFrame([features], columns=[f'New_Cases_Lag_{i}' for i in range(1, 8)] + ['Stringency_Index', 'Tests_Performed'])
        
        prediction = model.predict(feature_df)[0]
        
        st.metric(label="Predicted New Cases (Tomorrow)", value=int(prediction))
        
        st.info("The models were trained to predict the number of new cases based on 7-day lag features and other external factors.")
    else:
        st.warning("No ML models found. Please run the model training script.")
