import nbformat as nbf

nb = nbf.v4.new_notebook()
text = """\
# Disease Spread Dataset Analysis
This notebook performs exploratory data analysis (EDA) on our generated disease spread dataset."""
code1 = """\
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('../data/disease_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
df.head()"""

code2 = """\
# Plot SIR curves
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['Susceptible'], label='Susceptible', color='blue')
plt.plot(df['Date'], df['Infected'], label='Infected', color='red')
plt.plot(df['Date'], df['Recovered'], label='Recovered', color='green')
plt.title('Disease Spread Over Time')
plt.xlabel('Date')
plt.ylabel('Population')
plt.legend()
plt.show()"""

code3 = """\
# Correlation heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()"""

nb['cells'] = [
    nbf.v4.new_markdown_cell(text),
    nbf.v4.new_code_cell(code1),
    nbf.v4.new_code_cell(code2),
    nbf.v4.new_code_cell(code3)
]

with open('dataset_analysis.ipynb', 'w') as f:
    nbf.write(nb, f)
print("Notebook dataset_analysis.ipynb created.")
