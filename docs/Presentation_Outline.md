# Presentation Outline: Disease Spread Simulator

## Slide 1: Title Slide
- Project Title: Disease Spread Simulator
- Course Name: IT3016 Simulation and Modelling
- Presenter Name

## Slide 2: Introduction & Problem Statement
- Understanding the rapid spread of infectious diseases.
- The need for computational models to predict and mitigate outbreaks.
- How simulation helps policymakers in decision making.

## Slide 3: Project Objectives
- Fulfill requirements for CLO.3 and CLO.4.
- Build a mathematical simulation of disease dynamics.
- Integrate Machine Learning to predict future trends based on historical data.

## Slide 4: Theoretical Background: The SIR Model
- **Susceptible (S):** Population at risk.
- **Infectious (I):** Population currently infected and contagious.
- **Recovered (R):** Population that has recovered and gained immunity.
- System of ordinary differential equations.

## Slide 5: Dataset Generation & EDA
- Generating synthetic data using an SIR model with Gaussian noise.
- Features included: Stringency Index and Testing Rates.
- Exploratory Data Analysis: Correlation matrices and time-series plotting.

## Slide 6: Machine Learning Architecture
- Time-series forecasting using 7-day lag features.
- Model 1: Linear Regression (Baseline model).
- Model 2: Random Forest Regressor (Handles non-linear relationships).
- Model 3: Gradient Boosting Regressor (Ensemble learning for high accuracy).

## Slide 7: Model Evaluation & Comparison
- Evaluation metrics: Mean Squared Error (MSE) and R-squared.
- Random Forest performed best on non-linear epidemic curves.
- Discussion on overfitting vs. generalization.

## Slide 8: Streamlit Dashboard Architecture
- Component 1: EDA Viewer (Dataframes, Matplotlib plots).
- Component 2: Interactive Simulator (Adjustable $\beta$ and $\gamma$).
- Component 3: ML Predictor Interface.

## Slide 9: Interactive Simulation & Results
- Demonstration of the simulation.
- How changing the transmission rate ("flattening the curve") impacts the healthcare system.
- Real-time updates without recompiling code.

## Slide 10: Challenges & Limitations
- Assumptions of the standard SIR model (e.g., constant population, no vital dynamics).
- Limitations of synthetic datasets vs. real-world noisy data.
- Computational limits of lag-based time-series forecasting.

## Slide 11: Conclusion & Future Enhancements
- Successfully created a full-stack data science & simulation application.
- Future work: Expanding to SEIR models (adding "Exposed" compartment).
- Adding deep learning (LSTMs) for more robust predictions.

## Slide 12: Q&A
- Thank you for your time!
- Any questions?
