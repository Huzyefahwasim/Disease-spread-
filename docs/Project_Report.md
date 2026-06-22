# IT3016 Simulation and Modelling - Project Report
## Disease Spread Simulator

### 1. Introduction
This project simulates the spread of an infectious disease using an SIR (Susceptible-Infectious-Recovered) model. It aims to fulfill the requirements of CLO.3 and CLO.4 by providing a complete simulation environment coupled with Machine Learning predictions.

### 2. Dataset Analysis
The dataset was synthetically generated using an SIR model with added Gaussian noise to mimic real-world fluctuations in reporting. Exploratory Data Analysis (EDA) was performed to understand the relationships between stringency indices, testing rates, and new case counts.

### 3. Simulation Model
The core simulation uses the SIR compartmental model:
- **Susceptible (S):** Individuals who can contract the disease.
- **Infectious (I):** Individuals who have the disease and can transmit it.
- **Recovered (R):** Individuals who have recovered and are immune.
Parameters such as transmission rate ($\beta$) and recovery rate ($\gamma$) can be interactively modified in the Streamlit dashboard.

### 4. Machine Learning Models
Three models were trained to predict future infection rates based on a 7-day lag history and external factors (Stringency Index and Testing Rate):
1. **Linear Regression:** Serves as a baseline model.
2. **Random Forest Regressor:** Captures non-linear relationships.
3. **Gradient Boosting Regressor:** Provides robust predictions through an ensemble approach.

### 5. Conclusion
The Streamlit dashboard successfully integrates the simulation, dataset analysis, and ML predictions into a single interactive platform, demonstrating a comprehensive understanding of simulation and modelling techniques.
