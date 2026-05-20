import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

df_raw = pd.read_csv('C:/Users/Tushar/OneDrive/Desktop/Marvel/mscu_py/data/mcu.csv')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

print(df_raw.shape)
print(df_raw)

print("Shape:", df_raw.shape)
print("\nColumns:", df_raw.columns.tolist())
print("\nData Types:\n", df_raw.dtypes)
print("\nMissing Values:\n", df_raw.isnull().sum())
print("\nBasic Stats:\n", df_raw.describe())

df = df_raw.copy()
df = df.drop(columns=['Ref'])
df = df[df['Film'] != 'Total']
df = df.reset_index(drop=True)

print("Shape after cleaning:", df.shape)
print("\n")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
print(df)

bo_columns = ['US_Canada_BO', 'Other_Territories_BO', 'Worldwide_BO']
for col in bo_columns:
    df[col] = df[col].str.replace('$', '', regex=False)
    df[col] = df[col].str.replace(',', '', regex=False)
    df[col] = df[col].str.replace('[e]', '', regex=False)
    df[col] = df[col].str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')
print(" BOX OFFICE COLUMNS CLEANED ")
print(df[['Film', 'US_Canada_BO', 'Other_Territories_BO', 'Worldwide_BO']])

df['Budget'] = df['Budget'].str.replace('$', '', regex=False)
df['Budget'] = df['Budget'].str.replace('\xa0', '', regex=False)  
df['Budget'] = df['Budget'].str.replace('million', '', regex=False)
df['Budget'] = df['Budget'].str.replace('–', '-', regex=False)
df['Budget'] = df['Budget'].str.replace('\u2013', '-', regex=False)
df['Budget'] = df['Budget'].str.strip()
df['Budget_min'] = df['Budget'].str.split('-').str[0].str.strip()
df['Budget_max'] = df['Budget'].str.split('-').str[-1].str.strip()
df['Budget_min'] = pd.to_numeric(df['Budget_min'], errors='coerce') * 1000000
df['Budget_max'] = pd.to_numeric(df['Budget_max'], errors='coerce') * 1000000
df['Budget_avg'] = (df['Budget_min'] + df['Budget_max']) / 2

df['ROI'] = round((df['Worldwide_BO'] - df['Budget_avg']) / df['Budget_avg'], 2)
df['Profit'] = round(df['Worldwide_BO'] - df['Budget_avg'], 2)
pd.set_option('display.float_format', lambda x: '{:,.0f}'.format(x))

print(" BUDGET COLUMNS CLEANED ")
print(df[['Film', 'Budget', 'Budget_min', 'Budget_max', 'Budget_avg', 'ROI', 'Profit']])

df['Release_Date'] = pd.to_datetime(df['Release_Date'])
df['Release_Year'] = df['Release_Date'].dt.year
df['Release_Month'] = df['Release_Date'].dt.month

df.to_csv('C:/Users/Tushar/OneDrive/Desktop/Marvel/mscu_py/data/mcu_clean.csv', index=False)

print(" FINAL CLEAN DATA ")
print(df.head())
print("\nShape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nMissing Values:\n", df.isnull().sum())
