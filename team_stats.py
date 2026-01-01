import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

team_df = pd.read_csv('./data/pro_am_games.csv')

print(team_df)

df = pd.read_csv('./data/pro_am_games.csv')
print(df.head())

# Convert Result to binary (1 for Win, 0 for Loss)
df['Win'] = (df['Result'] == 'W').astype(int)

# Get all your team's player stats (exclude opponent stats)
team_players = ['tymelxss', 'AbuTalibaan', 'Glo4Prezz', 'Yurselln', 'MajinKemboi']
stats = ['Points', 'Rebounds', 'Assists', 'FGM']

# Create a list to store correlations
correlations = []

for player in team_players:
    for stat in stats:
        col_name = f"{player}_{stat}"
        corr = df[col_name].corr(df['Win'])
        correlations.append({
            'Player': player,
            'Stat': stat,
            'Correlation': corr,
            'Player_Stat': f"{player}_{stat}"
        })

# Convert to DataFrame and sort by absolute correlation
corr_df = pd.DataFrame(correlations)
corr_df['Abs_Correlation'] = corr_df['Correlation'].abs()
corr_df = corr_df.sort_values('Abs_Correlation', ascending=False)

# Display top 10 stats that correlate with wins
print("=" * 60)
print("TOP 10 STATS THAT CORRELATE WITH WINNING")
print("=" * 60)
print(corr_df[['Player', 'Stat', 'Correlation']].head(10).to_string(index=False))
print("\n")

# Show summary by player
print("=" * 60)
print("AVERAGE CORRELATION BY PLAYER (All Stats)")
print("=" * 60)
player_avg = corr_df.groupby('Player')['Correlation'].mean().sort_values(ascending=False)
print(player_avg)
print("\n")

# Visualization 1: Heatmap of correlations
plt.figure(figsize=(12, 8))
pivot_corr = corr_df.pivot(index='Player', columns='Stat', values='Correlation')
sns.heatmap(pivot_corr, annot=True, cmap='RdYlGn', center=0, 
            vmin=-1, vmax=1, linewidths=1, cbar_kws={'label': 'Correlation with Wins'})
plt.title('Correlation Between Player Stats and Team Wins', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.show()

# Visualization 2: Bar chart of top correlations
plt.figure(figsize=(14, 8))
top_15 = corr_df.head(15)
colors = ['green' if x > 0 else 'red' for x in top_15['Correlation']]
plt.barh(range(len(top_15)), top_15['Correlation'], color=colors, alpha=0.7)
plt.yticks(range(len(top_15)), top_15['Player_Stat'])
plt.xlabel('Correlation with Wins', fontsize=12)
plt.title('Top 15 Stats Most Correlated with Winning', fontsize=16, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='-', linewidth=0.5)
plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('top_correlations.png', dpi=300, bbox_inches='tight')
plt.show()

# Additional analysis: Win vs Loss comparison
print("=" * 60)
print("AVERAGE STATS: WINS vs LOSSES")
print("=" * 60)
for player in team_players:
    print(f"\n{player}:")
    for stat in stats:
        col_name = f"{player}_{stat}"
        win_avg = df[df['Win'] == 1][col_name].mean()
        loss_avg = df[df['Win'] == 0][col_name].mean()
        diff = win_avg - loss_avg
        print(f"  {stat}: Wins={win_avg:.1f}, Losses={loss_avg:.1f}, Diff={diff:+.1f}")

# Show overall record
wins = df['Win'].sum()
losses = len(df) - wins
print(f"\n{'=' * 60}")
print(f"OVERALL RECORD: {wins} Wins - {losses} Losses")
print(f"{'=' * 60}")