import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import pickle
import os
from simulation.disease_sim import DiseaseSimulation

# Set page layout to wide
st.set_page_config(page_title="Disease Spread Simulator", layout="wide", page_icon="🦠")

# --- CSS Styling ---
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    h1, h2, h3 {color: #2c3e50;}
    </style>
""", unsafe_allow_html=True)

st.title("🦠 IT3016- SIMULATION AND MODELLING")
st.markdown("**Semester Project: Advanced Disease Spread Simulator (SEIR-D Model)**")
st.markdown("---")

data_path = os.path.join('data', 'disease_data.csv')

@st.cache_data
def load_data():
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return None

df = load_data()

tab1, tab2, tab3 = st.tabs(["Interactive Simulation 🎮", "Dataset Analysis (EDA) 📊", "ML Predictions 🤖"])

with tab1:
    st.sidebar.header("Simulation Parameters ⚙️")
    st.sidebar.markdown("Adjust the dynamics of the disease spread.")
    
    population = st.sidebar.number_input("Population", min_value=1000, value=1000000, step=100000)
    initial_infected = st.sidebar.number_input("Initial Infected", min_value=1, value=50)
    days = st.sidebar.slider("Simulation Duration (Days)", 10, 365, 150)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Disease Characteristics")
    beta = st.sidebar.slider("Transmission Rate (β)", 0.0, 1.0, 0.35, help="Rate at which susceptible individuals get exposed.")
    sigma = st.sidebar.slider("Incubation Rate (σ)", 0.0, 1.0, 0.20, help="Rate at which exposed individuals become infectious.")
    gamma = st.sidebar.slider("Recovery Rate (γ)", 0.0, 1.0, 0.10, help="Rate at which infectious individuals recover.")
    mu = st.sidebar.slider("Mortality Rate (μ)", 0.0, 0.1, 0.02, help="Rate at which infectious individuals die.")
    
    st.subheader("SEIR-D Epidemic Simulation")
    st.write("This simulation uses the advanced SEIR-D mathematical model to predict how an infectious disease spreads through a population over time.")
    
    sim = DiseaseSimulation(population=population, initial_infected=initial_infected, beta=beta, sigma=sigma, gamma=gamma, mu=mu, days=days)
    results = sim.run()
    sim_df = pd.DataFrame(results)
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    peak_infections = int(sim_df['Infectious'].max())
    total_recovered = int(sim_df['Recovered'].iloc[-1])
    total_deaths = int(sim_df['Dead'].iloc[-1])
    day_of_peak = sim_df['Infectious'].idxmax()
    
    with col1:
        st.metric("Peak Infections 🚨", f"{peak_infections:,}", f"Day {day_of_peak}", delta_color="inverse")
    with col2:
        st.metric("Total Recovered 💚", f"{total_recovered:,}", "Recovered")
    with col3:
        st.metric("Total Deaths ⚰️", f"{total_deaths:,}", "Fatalities", delta_color="inverse")
    with col4:
        st.metric("Remaining Susceptible 🛡️", f"{int(sim_df['Susceptible'].iloc[-1]):,}", "Healthy")
        
    st.markdown("<br>", unsafe_allow_html=True)
        
    # Plotly Chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sim_df.index, y=sim_df['Susceptible'], mode='lines', name='Susceptible (S)', line=dict(color='#3498db', width=2)))
    fig.add_trace(go.Scatter(x=sim_df.index, y=sim_df['Exposed'], mode='lines', name='Exposed (E)', line=dict(color='#f1c40f', width=2)))
    fig.add_trace(go.Scatter(x=sim_df.index, y=sim_df['Infectious'], mode='lines', name='Infectious (I)', line=dict(color='#e74c3c', width=3)))
    fig.add_trace(go.Scatter(x=sim_df.index, y=sim_df['Recovered'], mode='lines', name='Recovered (R)', line=dict(color='#2ecc71', width=2)))
    fig.add_trace(go.Scatter(x=sim_df.index, y=sim_df['Dead'], mode='lines', name='Dead (D)', line=dict(color='#34495e', width=2)))
    
    fig.update_layout(
        title="Interactive Disease Progression Curve",
        xaxis_title="Days",
        yaxis_title="Population Count",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.85)
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Historical Dataset Analysis")
    if df is not None:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write("### Dataset Sample")
            st.dataframe(df.head(15), use_container_width=True)
            
        with col2:
            st.write("### Daily New Cases vs Stringency Index")
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=df['Date'], y=df['New_Cases'], name='Daily New Cases', marker_color='rgba(255, 99, 132, 0.6)'))
            fig2.add_trace(go.Scatter(x=df['Date'], y=df['Stringency_Index'], name='Stringency Index', yaxis='y2', line=dict(color='blue', width=2)))
            
            fig2.update_layout(
                yaxis=dict(title="New Cases"),
                yaxis2=dict(title="Stringency Index", overlaying='y', side='right', range=[0, 100]),
                hovermode="x unified",
                template="plotly_white"
            )
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("Dataset not found. Please run the data generation script.")

with tab3:
    st.subheader("Predictive Analytics Engine")
    
    models_dir = 'models'
    model_files = [f for f in os.listdir(models_dir) if f.endswith('.pkl')] if os.path.exists(models_dir) else []
    
    if len(model_files) > 0 and df is not None:
        st.info("Our AI models analyze the last 7 days of historical cases and government stringency levels to predict tomorrow's outbreak severity.")
        
        selected_model = st.selectbox("Select ML Engine", model_files, index=0)
        with open(os.path.join(models_dir, selected_model), 'rb') as f:
            model = pickle.load(f)
            
        last_7_days = df['New_Cases'].tail(7).values[::-1]
        latest_stringency = df['Stringency_Index'].iloc[-1]
        latest_tests = df['Tests_Performed'].iloc[-1]
        
        features = list(last_7_days) + [latest_stringency, latest_tests]
        feature_names = [f'Day -{i} Cases' for i in range(1, 8)] + ['Stringency', 'Tests']
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("### Input Features (Live Context)")
            feat_df = pd.DataFrame([features], columns=feature_names)
            st.dataframe(feat_df, hide_index=True)
            
        with col2:
            st.write("### Forecast Result")
            feature_df = pd.DataFrame([features], columns=[f'New_Cases_Lag_{i}' for i in range(1, 8)] + ['Stringency_Index', 'Tests_Performed'])
            prediction = max(0, model.predict(feature_df)[0])
            
            st.metric(label="Predicted New Cases for Tomorrow", value=f"{int(prediction):,} cases", delta="High Risk" if prediction > 1000 else "Stable", delta_color="inverse" if prediction > 1000 else "normal")
            
    else:
        st.warning("No ML models found. Please train models first.")
