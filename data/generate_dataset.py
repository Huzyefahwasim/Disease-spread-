import pandas as pd
import numpy as np
import os

def generate_sir_data(days=365, population=1000000, initial_infected=50, beta=0.25, gamma=0.1):
    """
    Generates synthetic disease spread data using an SIR model with noise.
    """
    S = [population - initial_infected]
    I = [initial_infected]
    R = [0]
    
    for _ in range(1, days):
        # Calculate new changes
        new_infections = (beta * S[-1] * I[-1]) / population
        new_recoveries = gamma * I[-1]
        
        # Add random noise to simulate real-world reporting fluctuations
        inf_noise = np.random.normal(0, max(1, new_infections * 0.1))
        new_infections = max(0, new_infections + inf_noise)
        
        S.append(max(0, S[-1] - new_infections))
        I.append(max(0, I[-1] + new_infections - new_recoveries))
        R.append(min(population, R[-1] + new_recoveries))
        
    dates = pd.date_range(start='2020-03-01', periods=days)
    
    df = pd.DataFrame({
        'Date': dates,
        'Susceptible': [int(x) for x in S],
        'Infected': [int(x) for x in I],
        'Recovered': [int(x) for x in R]
    })
    
    # Calculate daily new cases
    df['New_Cases'] = df['Infected'].diff().fillna(initial_infected)
    df['New_Cases'] = df['New_Cases'].apply(lambda x: max(0, int(x)))
    
    # Add external factors (features for ML)
    # E.g., a "Stringency Index" representing government lockdown measures
    # Starts low, increases as cases go up
    stringency = []
    current_stringency = 10
    for cases in df['New_Cases']:
        if cases > 1000:
            current_stringency = min(100, current_stringency + 2)
        elif cases < 500:
            current_stringency = max(0, current_stringency - 1)
        stringency.append(current_stringency + np.random.normal(0, 2))
        
    df['Stringency_Index'] = np.clip(stringency, 0, 100)
    
    # Add testing rate
    df['Tests_Performed'] = df['New_Cases'] * np.random.uniform(5, 15, days)
    df['Tests_Performed'] = df['Tests_Performed'].astype(int)
    
    return df

if __name__ == "__main__":
    np.random.seed(42)
    df = generate_sir_data(days=500)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'disease_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Synthetic dataset generated and saved to {output_path}")
