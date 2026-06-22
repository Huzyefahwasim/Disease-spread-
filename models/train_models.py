import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import pickle
import os

def load_data(filepath):
    df = pd.read_csv(filepath)
    # Create lag features to predict future cases based on past cases
    for i in range(1, 8):
        df[f'New_Cases_Lag_{i}'] = df['New_Cases'].shift(i)
    
    df = df.dropna()
    features = [f'New_Cases_Lag_{i}' for i in range(1, 8)] + ['Stringency_Index', 'Tests_Performed']
    X = df[features]
    y = df['New_Cases']
    
    return X, y

def train_and_evaluate():
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'disease_data.csv')
    X, y = load_data(data_path)
    
    # Time-series split (don't shuffle)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)
        
        results[name] = {'MSE': mse, 'R2': r2}
        print(f"{name} - MSE: {mse:.2f}, R2: {r2:.2f}")
        
        # Save model
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{name.replace(" ", "_").lower()}.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
            
    return results

if __name__ == "__main__":
    train_and_evaluate()
