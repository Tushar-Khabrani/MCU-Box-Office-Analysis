import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.float_format', lambda x: '{:,.0f}'.format(x))
pd.set_option('display.max_columns', None)

df = pd.read_csv('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/data/mcu_clean.csv')

print(" DATA LOADED ")
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print(" DATASET INFO ")
print(df.info())
print("\n BASIC STATISTICS ")
print(df.describe())
print("\n PHASE WISE FILM COUNT ")
print(df['Phase'].value_counts())
print("\n YEAR WISE FILM COUNT ")
print(df['Release_Year'].value_counts().sort_index())

best_film = df.loc[df['Worldwide_BO'].idxmax(), 'Film']
best_earning = df['Worldwide_BO'].max()
print(f" HIGHEST GROSSING FILM ")
print(f"{best_film}: ${best_earning:,.0f}")

worst_film = df.loc[df['Worldwide_BO'].idxmin(), 'Film']
worst_earning = df['Worldwide_BO'].min()
print(f"\n LOWEST GROSSING FILM ")
print(f"{worst_film}: ${worst_earning:,.0f}")

best_roi_film = df.loc[df['ROI'].idxmax(), 'Film']
best_roi = df['ROI'].max()
print(f"\n HIGHEST ROI FILM ")
print(f"{best_roi_film}: {best_roi:.2f}x")

print(f"\n PHASE WISE TOTAL EARNINGS ")
phase_earnings = df.groupby('Phase')['Worldwide_BO'].sum().reset_index()
phase_earnings.columns = ['Phase', 'Total_Earning']
print(phase_earnings)

print(f"\n PHASE WISE AVERAGE EARNINGS ")
phase_avg = df.groupby('Phase')['Worldwide_BO'].mean().reset_index()
phase_avg.columns = ['Phase', 'Avg_Earning']
print(phase_avg)

print(f"\n FILMS THAT LOST MONEY ")
loss_films = df[df['Profit'] < 0][['Film', 'Budget_avg', 'Worldwide_BO', 'Profit', 'ROI']]
print(loss_films)

print(f"\n TOP 10 FILMS ")
top10 = df.nlargest(10, 'Worldwide_BO')[['Film', 'Phase', 'Worldwide_BO', 'ROI', 'Profit']]
print(top10)

print(f"\n YEARLY EARNINGS ")
yearly = df.groupby('Release_Year')['Worldwide_BO'].sum().reset_index()
print(yearly)

#graphs

plt.style.use('dark_background')
sns.set_palette("husl") 

#Chart 1 — Top 10 Films
top10 = df.nlargest(10, 'Worldwide_BO').sort_values('Worldwide_BO')
plt.figure(figsize=(12, 7))
bars = plt.barh(top10['Film'], top10['Worldwide_BO'] / 1e9, color=sns.color_palette("husl", 10))
plt.xlabel('Worldwide Box Office (Billions $)', fontsize=12)
plt.title('Top 10 MCU Films by Worldwide Box Office', fontsize=15, fontweight='bold')
for bar, val in zip(bars, top10['Worldwide_BO'] / 1e9):
    plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, f'${val:.2f}B', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/top10_films.png', dpi=150)
plt.show()

#Chart 2 — Yearly Trend#
yearly = df.groupby('Release_Year')['Worldwide_BO'].sum() / 1e9
plt.figure(figsize=(12, 6))
plt.plot(yearly.index, yearly.values, marker='o', linewidth=2.5, markersize=8, color='cyan')
plt.fill_between(yearly.index, yearly.values, alpha=0.3, color='cyan')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Earnings (Billions $)', fontsize=12)
plt.title('MCU Yearly Earnings Trend', fontsize=15, fontweight='bold')
plt.xticks(yearly.index, rotation=45)
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/yearly_trend.png', dpi=150)
plt.show()

#Chart 3 — Phase wise Earnings
phase_data = df.groupby('Phase')['Worldwide_BO'].sum() / 1e9
plt.figure(figsize=(10, 6))
bars = plt.bar(phase_data.index, phase_data.values, color=sns.color_palette("husl", len(phase_data)))
plt.xlabel('Phase', fontsize=12)
plt.ylabel('Total Earnings (Billions $)', fontsize=12)
plt.title('MCU Phase Wise Total Earnings', fontsize=15, fontweight='bold')
for bar, val in zip(bars, phase_data.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'${val:.2f}B', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/phase_earnings.png', dpi=150)
plt.show()

#Chart 4 — Budget vs Worldwide BO
plt.figure(figsize=(12, 7))
scatter = plt.scatter(df['Budget_avg']/1e6, df['Worldwide_BO']/1e9, c=df['ROI'], cmap='RdYlGn', s=100, alpha=0.8)
plt.colorbar(scatter, label='ROI')
plt.xlabel('Budget (Millions $)', fontsize=12)
plt.ylabel('Worldwide BO (Billions $)', fontsize=12)
plt.title('Budget vs Worldwide Box Office', fontsize=15, fontweight='bold')
for _, row in df.iterrows():
    plt.annotate(row['Film'].split(':')[0], (row['Budget_avg']/1e6, row['Worldwide_BO']/1e9), fontsize=7, alpha=0.8)
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/budget_vs_bo.png', dpi=150)
plt.show()

#Chart 5 — ROI per Film
df_sorted = df.sort_values('ROI', ascending=True)
colors = ['red' if x < 0 else 'green' for x in df_sorted['ROI']]
plt.figure(figsize=(12, 10))
plt.barh(df_sorted['Film'], df_sorted['ROI'], color=colors)
plt.xlabel('ROI', fontsize=12)
plt.title('MCU Films ROI Comparison', fontsize=15, fontweight='bold')
plt.axvline(x=0, color='white', linewidth=0.8)
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/roi_comparison.png', dpi=150)
plt.show()

#Chart 6 — US vs International Split
us_total = df['US_Canada_BO'].sum() / 1e9
intl_total = df['Other_Territories_BO'].sum() / 1e9
plt.figure(figsize=(8, 8))
plt.pie([us_total, intl_total], labels=['US & Canada', 'International'], autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4'], startangle=90, explode=(0.05, 0.05))
plt.title('MCU US vs International Earnings Split', fontsize=15, fontweight='bold')
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/us_vs_intl.png', dpi=150)
plt.show()

#Chart 7 — Phase wise Avg Budget vs Avg Earning
phase_budget = df.groupby('Phase')['Budget_avg'].mean() / 1e6
phase_earning = df.groupby('Phase')['Worldwide_BO'].mean() / 1e6
x = np.arange(len(phase_budget))
width = 0.35
plt.figure(figsize=(12, 6))
plt.bar(x - width/2, phase_budget, width, label='Avg Budget', color='#FF6B6B')
plt.bar(x + width/2, phase_earning, width, label='Avg Earning', color='#4ECDC4')
plt.xlabel('Phase', fontsize=12)
plt.ylabel('Amount (Millions $)', fontsize=12)
plt.title('Phase Wise Avg Budget vs Avg Earning', fontsize=15, fontweight='bold')
plt.xticks(x, phase_budget.index)
plt.legend()
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/budget_vs_earning.png', dpi=150)
plt.show()

#Chart 8 — Heatmap — Month wise Earnings
month_phase = df.pivot_table(values='Worldwide_BO', index='Phase', columns='Release_Month', aggfunc='sum') / 1e6
plt.figure(figsize=(14, 6))
sns.heatmap(month_phase, annot=True, fmt='.0f', cmap='YlOrRd', linewidths=0.5, cbar_kws={'label': 'Earnings (Millions $)'})
plt.title('Phase vs Month Earnings Heatmap', fontsize=15, fontweight='bold')
plt.xlabel('Release Month', fontsize=12)
plt.ylabel('Phase', fontsize=12)
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/heatmap.png', dpi=150)
plt.show()

#Chart 9 — Box Plot — Phase wise Earnings Distribution
plt.figure(figsize=(12, 6))
df.boxplot(column='Worldwide_BO', by='Phase', figsize=(12, 6))
plt.suptitle('')
plt.title('Phase Wise Earnings Distribution', fontsize=15, fontweight='bold')
plt.xlabel('Phase', fontsize=12)
plt.ylabel('Worldwide BO ($)', fontsize=12)
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/boxplot.png', dpi=150)
plt.show()

# CHART 10 — Top 5 ROI Films
top5_roi = df.nlargest(5, 'ROI')[['Film', 'ROI', 'Budget_avg', 'Worldwide_BO']]
plt.figure(figsize=(10, 6))
bars = plt.bar(top5_roi['Film'], top5_roi['ROI'], color=sns.color_palette("husl", 5))
plt.xlabel('Film', fontsize=12)
plt.ylabel('ROI', fontsize=12)
plt.title('Top 5 MCU Films by ROI', fontsize=15, fontweight='bold')
plt.xticks(rotation=20, ha='right')
for bar, val in zip(bars, top5_roi['ROI']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{val:.2f}x', ha='center', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('C:/Users/Tushar/OneDrive/Desktop/Marvel/mcu_py/graphs/top5_roi.png', dpi=150)
plt.show()
