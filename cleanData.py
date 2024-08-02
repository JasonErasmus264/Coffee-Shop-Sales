import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset from a CSV file
data = pd.read_csv('data/coffee.csv')

# Display the first few rows of the dataset
data.head()

# Display information about the dataset including data types and non-null counts
print("Dataset information:")
data.info()

# Generate summary statistics for quantitative columns
data_summary = data.describe()
num_cols = ['transaction_qty', 'unit_price', 'Total_Bill']
data_summary = data_summary[num_cols]
data_summary

# Create boxplots for quantitative columns to visualize outliers
fig, axes = plt.subplots(ncols=3, figsize=(9, 4))
for i, num_col in enumerate(num_cols):
    sns.boxplot(y=data[num_col], ax=axes[i])
fig.subplots_adjust(wspace=0.4)

# Identify and display any duplicate rows in the dataset
duplicate = data[data.duplicated()]
duplicate

# Drop unnecessary columns from the dataset
data.drop(['transaction_id', 'transaction_time', 'store_id', 'product_id', 'Month', 'Day of Week'], axis=1, inplace=True)

# Check for missing values in the dataset
data.isna().sum()

# Convert 'transaction_date' column to datetime format and save cleaned data to a new CSV file
data['transaction_date'] = pd.to_datetime(data['transaction_date'], format="mixed", dayfirst=True)
data.to_csv('../data/coffee_cleaned.csv', index=False)
