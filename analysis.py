# Import libraries
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime as dt

# Load data
data = pd.read_csv('data/coffee_cleaned.csv')

# Add a column for day (of month)
data['day'] = pd.to_datetime(data['transaction_date']).dt.day

# Predefine figsize
figsize1_1 = (8,4)
figsize1_2 = (16, 5)

# Univariate Analysis
# Total transactions in different stores
store_transactions = data.groupby('store_location')['transaction_qty'].count().sort_values(ascending=False)

fig9, ax0 = plt.subplots(figsize=figsize1_1)
color_palette_stores = sns.color_palette("husl", len(store_transactions))
ax0.bar(store_transactions.index, store_transactions.values, color=color_palette_stores)

ax0.set_xlabel('Store Location')
ax0.set_ylabel('Records count')
ax0.set_title('Transaction records per store')

# Quantity per transaction
transaction_qty_count = data.groupby('transaction_qty').size()

fig8, ax0 = plt.subplots(figsize=figsize1_1)

# Convert the colormap to a list of colors
colors = sns.color_palette("viridis", n_colors=len(transaction_qty_count))

ax0.bar(transaction_qty_count.index, transaction_qty_count.values, color=colors)

ax0.set_xlabel('Purchase volume')
ax0.set_ylabel('Frequency')
ax0.set_title('Distribution of purchase volumes per transaction')

# Distribution of product categories
product_cat_distribution = data.groupby('product_category')['transaction_qty'].count().sort_values(ascending=False)
colorblind_palette = sns.color_palette("colorblind")

fig5, (ax0, ax1) = plt.subplots(1, 2, figsize=figsize1_2)
ax0.bar(product_cat_distribution.index.values, product_cat_distribution, color=colorblind_palette)
ax0.set_xlabel('Category')
ax0.set_ylabel('Records')
ax0.set_title('Product category records')
ax0.xaxis.set_tick_params(rotation=45)

threshold_pie = 2 * product_cat_distribution.sum() / 100
small_portions = product_cat_distribution[product_cat_distribution < threshold_pie]
others_value = small_portions.sum()

print(others_value / product_cat_distribution.sum())
print((product_cat_distribution['Coffee']+product_cat_distribution['Tea']) / product_cat_distribution.sum())

new_distrib = product_cat_distribution.drop(small_portions.index)
new_distrib['Others'] = others_value

def autopct_format(values: pd.Series) -> str:
    def my_format(pct):
        total = sum(values)
        ini_val = int(round(pct*total/100.0)) // 100
        val = ini_val /10
        return '{:.1f}% ({v:.1f}k)'.format(pct, v=val)
    return my_format

ax1.pie(new_distrib.values, 
        labels=new_distrib.index, 
        colors=colorblind_palette, 
        pctdistance=0.6,
        autopct=autopct_format(new_distrib))
ax1.set_title('Records pie chart')

plt.subplots_adjust(wspace=-.15)
plt.xticks(rotation=45)

# Unit price for different categories
unique_prices = data.drop_duplicates(subset=['product_category', 'unit_price'])

fig, ax = plt.subplots(figsize=figsize1_1)

sns.boxplot(x='product_category', y='unit_price', data=unique_prices, palette="pastel")

ax.set_xlabel('Product category')
ax.set_ylabel('Unit price ($)')
ax.set_title('Unit price distribution of product categories')

# Popular Menu
categories_list = list(product_cat_distribution.index)

fig, axes = plt.subplots(3, 3, figsize=(20, 14))

for i, cat in enumerate(categories_list):
    cat_df = data[data['product_category'] == cat]
    cat_df = cat_df[['transaction_qty', 'product_category', 'product_type']]
    cat_type_aggsum = cat_df.groupby('product_type')['transaction_qty'].sum().sort_values()

    # Convert colormap to a list of colors
    colors = sns.color_palette("cubehelix", n_colors=len(cat_type_aggsum))

    axes[i // 3, i % 3].barh(width=cat_type_aggsum.values, y=cat_type_aggsum.index, color=colors)
    axes[i // 3, i % 3].set_title(cat)

fig.subplots_adjust(wspace=0.5)

# Popular Menu Detail
categories_list = list(product_cat_distribution.index)

fig, axes = plt.subplots(3, 3, figsize=(20, 14))

for i, cat in enumerate(categories_list):
    cat_df = data[data['product_category'] == cat]
    cat_df = cat_df[['transaction_qty', 'product_category', 'product_detail']]
    cat_detail_aggsum = cat_df.groupby('product_detail')['transaction_qty'].sum().sort_values()

    # Convert colormap to a list of colors
    colors = sns.color_palette("coolwarm", n_colors=len(cat_detail_aggsum))

    axes[i // 3, i % 3].barh(width=cat_detail_aggsum.values, y=cat_detail_aggsum.index, color=colors)
    axes[i // 3, i % 3].set_title(cat)

fig.subplots_adjust(wspace=0.7)

# Drink size distribution
drink_list = ['Coffee', 'Tea', 'Drinking Chocolate']
drink_df = data[data['product_category'].isin(drink_list)]

drink_size = drink_df.groupby('Size')['transaction_qty'].sum().sort_values(ascending=False)

fig7, ax0 = plt.subplots(figsize=figsize1_1)

ax0.bar(drink_size.index, drink_size.values, color=sns.color_palette("Set1"))

ax0.set_xlabel('Drink Size')
ax0.set_ylabel('Total transaction volume')
ax0.set_title('Distribution of drink sizes purchased')

print(drink_size.loc['Not Defined']/ drink_size.sum())

# Fixing sizes
filtered_drink_df = drink_df.loc[~drink_df['product_detail'].isin(['Ouro Brasileiro shot', 'Espresso shot'])]

latte_fix_df = filtered_drink_df.copy()
latte_fix_df.loc[(latte_fix_df['product_detail'] == 'Latte') & (latte_fix_df['Size'] == 'Not Defined'), 'Size'] = 'Small'

final_drink_df = latte_fix_df.copy()
final_drink_df.loc[(final_drink_df['product_detail'] == 'Cappuccino') & (final_drink_df['Size'] == 'Not Defined'), 'Size'] = 'Regular'

group_drink_df = final_drink_df.groupby('Size')['transaction_qty'].count().sort_values(ascending=False)

fig7, ax0 = plt.subplots(figsize=figsize1_1)

ax0.bar(group_drink_df.index, group_drink_df.values, color=sns.color_palette("Set1"))

ax0.set_xlabel('Drink Size')
ax0.set_ylabel('Records')
ax0.set_title('Distribution of drink sizes purchased')

# Time-series analysis of sales and purchases
daily_sales = data.groupby('transaction_date')['Total_Bill'].sum()
daily_purchase = data.groupby('transaction_date')['transaction_qty'].sum()

monthly_sales = data.groupby('Month Name')['Total_Bill'].sum()
monthly_sales = monthly_sales.reindex(index=['January', 'February', 'March', 'April', 'May', 'June'])
monthly_purchase = data.groupby('Month Name')['transaction_qty'].sum()
monthly_purchase = monthly_purchase.reindex(index=['January', 'February', 'March', 'April', 'May', 'June'])

fig0, (ax0, ax2) = plt.subplots(1, 2, figsize=figsize1_2)

# Plotting the trends
ax1 = ax0.twinx()
ax0.plot(daily_sales.index, daily_sales, color='forestgreen')
ax1.plot(daily_purchase.index, daily_purchase, color='royalblue')

# Customize figure
ax0.set_xticks(ax0.get_xticks()[::30])  # Show only every 30th label (monthly)
ax0.set_xlabel('Date')
ax0.set_ylabel('Sales', color='forestgreen')
ax0.tick_params('x', rotation=45)
ax0.tick_params('y', colors='forestgreen')
ax1.set_ylabel('Purchases', color='royalblue')
ax1.tick_params('y', colors='royalblue')
ax0.set_title('Daily sales and purchases trend over 6 months')

# Plotting the trends
ax3 = ax2.twinx()
ax2.bar(monthly_sales.index, monthly_sales, color='lightgreen', edgecolor='lightgreen')
ax3.bar(monthly_purchase.index, monthly_purchase, color='lightblue', edgecolor='lightblue')

# Customize figure
ax2.set_xlabel('Month')
ax2.set_ylabel('Sales', color='forestgreen')
ax2.tick_params('y', colors='forestgreen')
ax3.set_ylabel('Purchases', color='royalblue')
ax3.tick_params('y', colors='royalblue')
ax2.set_title('Monthly sales and purchases total in 2023')

plt.subplots_adjust(wspace=0.3)

# Daily sales per transaction by month
monthly_trend = data.copy()

daily_sales_per_transac_6months = monthly_trend.groupby('transaction_date')['Total_Bill'].mean()
daily_sales_per_transac_by_month = monthly_trend.groupby('day')['Total_Bill'].mean()

fig2, (ax0, ax1) = plt.subplots(1, 2, figsize=figsize1_2)

ax0.plot(daily_sales_per_transac_6months.index, daily_sales_per_transac_6months.values, color='crimson')

ax0.set_xticks(ax0.get_xticks()[::30])  # Show only every 30th label (monthly)
ax0.set_xlabel('Date')
ax0.set_ylabel('Average Sales per Transaction')
ax0.tick_params('x', rotation=45)
ax0.set_title('Daily average sales per transaction')

ax1.plot(daily_sales_per_transac_by_month.index, daily_sales_per_transac_by_month.values, color='darkorange')

ax1.set_xlabel('Day of the Month')
ax1.set_ylabel('Average Sales per Transaction')
ax1.set_title('Average sales per transaction by day of the month')

plt.subplots_adjust(wspace=0.3)

plt.show()


# Daily sales per week
total_sales_per_day_of_week = data.groupby('Day Name')['Total_Bill'].sum()
total_sales_per_day_of_week = total_sales_per_day_of_week.reindex(['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'])

unique_dates = data.drop_duplicates('transaction_date')

# Counting how many days' names are recorded
days_of_week_count = unique_dates['Day Name'].value_counts(sort=True)
avg_daily_sales_per_week = total_sales_per_day_of_week / days_of_week_count

print(avg_daily_sales_per_week.mean())

fig3, ax0 = plt.subplots(figsize=(8, 4))

ax0.bar(avg_daily_sales_per_week.index, avg_daily_sales_per_week.values)
ax0.set_xlabel('Day Name')
ax0.set_ylabel('Average daily sales')
ax0.set_title('Average daily sales over different days of the week')

plt.show()


# Hourly sales per day
total_sales_per_hour_of_day = data.groupby('Hour')['Total_Bill'].sum()

unique_dates = data.drop_duplicates(['transaction_date', 'Hour'])

hours_of_day_count = unique_dates['Hour'].value_counts(sort=True).sort_index(ascending=True)

avg_hourly_sales_per_day = total_sales_per_hour_of_day / hours_of_day_count

fig4, ax0 = plt.subplots(figsize=figsize1_1)

ax0.plot(avg_hourly_sales_per_day.index, avg_hourly_sales_per_day.values)
ax0.set_xlabel('Hour')
ax0.set_ylabel('Average hourly sales')
ax0.set_title('Average hourly sales in a day')

plt.show()


# Multivariate Analysis

# Product category performance across each store
pivot_df = data.pivot_table(index='product_category', columns='store_location', values='transaction_qty', aggfunc='sum')

# Reset index to convert product_category from index to a regular column
pivot_df.reset_index(inplace=True)

# Extract the 'product_category' column as a separate Series
product_category_column = pivot_df['product_category']

# Drop the 'product_category' column from the DataFrame
pivot_df.drop(columns=['product_category'], inplace=True)

# Concatenate the 'product_category' column back to the DataFrame as the first column
# Removes store_location column
pivot_df = pd.concat([product_category_column, pivot_df], axis=1)

index_list = product_cat_distribution.index.tolist()
store_prod_cat = pivot_df.set_index('product_category').reindex(index_list)

store_prod_cat.plot(figsize=figsize1_1, kind='bar')

plt.xlabel('Product category')
plt.ylabel('Total transaction quantity')
plt.title('Distribution of each product category purchased per store')

plt.show()