import pandas as pd
import matplotlib.pyplot as plt

# Replace 'path_to_your_file.csv' with the actual path to your CSV file
csv_path = './data/contracts.csv'

# Load the CSV data, handling potential BOM
data = pd.read_csv(csv_path, encoding='utf-8-sig')

# Convert the DAY column to datetime, with error handling
data['DAY'] = pd.to_datetime(data['DAY'], errors='coerce')

# Drop rows where DAY could not be converted to datetime
data = data.dropna(subset=['DAY'])

# Plotting the top interacted contracts
def plot_top_interacted(data, output_file='top_interacted_contracts.png'):
    plt.figure(figsize=(14, 7))
    top_interacted = data.sort_values(by='INTERACTIONS', ascending=False).head(10)

    plt.barh(top_interacted['CONTRACT_ADDRESS'], top_interacted['INTERACTIONS'], color='skyblue')
    plt.xlabel('Interactions')
    plt.ylabel('Contract Address')
    plt.title('Top Interacted Contracts')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest value at the top
    plt.tight_layout()
    plt.savefig(output_file)  # Save the figure as PNG
    plt.close()

# Plotting overall interactions by environment
def plot_interactions_by_environment(data, output_file='interactions_by_environment.png'):
    plt.figure(figsize=(10, 5))
    interactions_by_env = data.groupby('ENVIRONMENT')['INTERACTIONS'].sum().sort_values()

    interactions_by_env.plot(kind='bar', color=['#1b96ff', '#04e1cb'])
    plt.xlabel('Environment')
    plt.ylabel('Total Interactions')
    plt.title('Total Interactions by Environment')
    plt.tight_layout()
    plt.savefig(output_file)  # Save the figure as PNG
    plt.close()

# Plotting and saving the figures
plot_top_interacted(data)
plot_interactions_by_environment(data)

print('Top interacted contracts plot saved as "top_interacted_contracts.png" and total interactions by environment plot saved as "interactions_by_environment.png".')

