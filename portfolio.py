import pandas as pd

# df = pd.read_csv('customer_shopping_behaviour.csv')
# Replace line 3 with the absolute path
df = pd.read_csv(r'D:\Projects\Data Analyst Projects\Data Analytics Portfolio\customer_shopping_behaviour.csv')

print(df.head())
print(df.info())
print(df.describe(include='all'))
print(df.isnull().sum())
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x:x.fillna(x.median()))
print(df.isnull().sum())
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ', '_')
df = df.rename(columns = {'purchase_amount__(usd)' : 'purchase_amount'})
df.columns

#create a column age_group
labels =   ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)
df[['age', 'age_group']].head(10)
#create column purchase_frequency_days
frequency_mapping = {
    'Fortnightly': 14,
    'weekly': 7,
    'monthly': 30,
    'quarterly': 90,
    'biweekly': 14,
    'annually': 365,
    'Every 3 months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
df[['purchase_frequency_days', 'frequency_of_purchases']].head(10)
df[['discount_applied', 'promo_code_used']].head(10)
(df['discount_applied']== df['promo_code_used']).all()
df = df.drop('promo_code_used', axis=1)
df.columns
# Install required packages from your terminal/command prompt (do not run pip install inside the script)
# Example:
#pip install psycopg2-binary sqlalchemy 
# run this in your terminal/command prompt, not inside the script
from sqlalchemy import create_engine
username = "root"
password = "RDS2421"
host = "localhost"
port = "3306"
database = "customer_behaviour"

engine = create_engine(f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}")

table_name = "customer"

df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'")