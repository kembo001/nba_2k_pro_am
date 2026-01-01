import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv('./data/pro_am_games.csv')

# Convert Result to binary (1 for Win, 0 for Loss)
df['Win'] = (df['Result'] == 'W').astype(int)

# Select your team's stat columns (excluding opponent stats for cleaner visualization)
your_team_stats = [
    'tymelxss_Grade', 'tymelxss_Points', 'tymelxss_Rebounds', 'tymelxss_Assists', 'tymelxss_FGM',
    'AbuTalibaan_Grade', 'AbuTalibaan_Points', 'AbuTalibaan_Rebounds', 'AbuTalibaan_Assists', 'AbuTalibaan_FGM',
    'Glo4Prezz_Grade', 'Glo4Prezz_Points', 'Glo4Prezz_Rebounds', 'Glo4Prezz_Assists', 'Glo4Prezz_FGM',
    'Yurselln_Grade', 'Yurselln_Points', 'Yurselln_Rebounds', 'Yurselln_Assists', 'Yurselln_FGM',
    'MajinKemboi_Grade', 'MajinKemboi_Points', 'MajinKemboi_Rebounds', 'MajinKemboi_Assists', 'MajinKemboi_FGM',
    'Win'
]

# Convert grades to numeric (A+ = 4.3, A = 4.0, etc.)
grade_map = {
    'A+': 4.3, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0
}

grade_columns = [col for col in df.columns if 'Grade' in col]
for col in grade_columns:
    df[col] = df[col].map(grade_map)

# Create pairplot
sns.pairplot(df[your_team_stats], hue='Win', palette={0: 'red', 1: 'green'}, 
             diag_kind='kde', plot_kws={'alpha': 0.6})
plt.suptitle('Team Stats vs Wins', y=1.02)
plt.tight_layout()
plt.show()

# Calculate correlations with Win to see which stats matter most
correlations = df[your_team_stats].corr()['Win'].sort_values(ascending=False)
print("\nCorrelation with Wins:")
print(correlations)