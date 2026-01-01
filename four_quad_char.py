import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv('./data/pro_am_games.csv')

# Convert Result to binary
df['Win'] = (df['Result'] == 'W').astype(int)

# Convert grades to numeric
grade_map = {
    'A+': 4.3, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0
}

team_players = ['tymelxss', 'AbuTalibaan', 'Glo4Prezz', 'Yurselln', 'MajinKemboi']
stats = ['Points', 'Rebounds', 'Assists', 'FGM']

# Convert grades to numeric
for player in team_players:
    grade_col = f"{player}_Grade"
    df[f"{player}_Grade_Numeric"] = df[grade_col].map(grade_map)

# Calculate stat correlations for each player
player_data = []
for player in team_players:
    # Get grade correlation
    grade_corr = df[f"{player}_Grade_Numeric"].corr(df['Win'])
    
    # Get average stat correlation
    stat_corrs = []
    for stat in stats:
        col_name = f"{player}_{stat}"
        stat_corrs.append(df[col_name].corr(df['Win']))
    avg_stat_corr = np.mean(stat_corrs)
    
    player_data.append({
        'Player': player,
        'Grade_Correlation': grade_corr,
        'Stat_Correlation': avg_stat_corr
    })

player_df = pd.DataFrame(player_data)

# Create the four-quadrant chart
fig, ax = plt.subplots(figsize=(14, 10))

# Set up the plot with a nice style
sns.set_style("whitegrid")

# Calculate midpoints for quadrant lines
x_mid = player_df['Stat_Correlation'].mean()
y_mid = player_df['Grade_Correlation'].mean()

# Create quadrant backgrounds
ax.axhline(y=y_mid, color='black', linestyle='-', linewidth=2, alpha=0.7)
ax.axvline(x=x_mid, color='black', linestyle='-', linewidth=2, alpha=0.7)
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax.axvline(x=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Color quadrants
ax.fill_between([x_mid, ax.get_xlim()[1]], y_mid, ax.get_ylim()[1], alpha=0.15, color='green', label='Complete Players')
ax.fill_between([ax.get_xlim()[0], x_mid], y_mid, ax.get_ylim()[1], alpha=0.15, color='blue', label='Intangible Impact')
ax.fill_between([x_mid, ax.get_xlim()[1]], ax.get_ylim()[0], y_mid, alpha=0.15, color='orange', label='Stat Stuffers')
ax.fill_between([ax.get_xlim()[0], x_mid], ax.get_ylim()[0], y_mid, alpha=0.15, color='red', label='Need Focus')

# Plot each player
colors = {'tymelxss': '#FF6B6B', 'AbuTalibaan': '#4ECDC4', 
          'Glo4Prezz': '#45B7D1', 'Yurselln': '#FFA07A', 'MajinKemboi': '#98D8C8'}

for _, row in player_df.iterrows():
    ax.scatter(row['Stat_Correlation'], row['Grade_Correlation'], 
               s=500, alpha=0.7, color=colors[row['Player']], 
               edgecolors='black', linewidth=2, zorder=5)
    
    # Add player name
    ax.annotate(row['Player'], 
                (row['Stat_Correlation'], row['Grade_Correlation']),
                fontsize=11, fontweight='bold', ha='center', va='center',
                zorder=6)

# Labels and title
ax.set_xlabel('Average Stat Correlation with Wins →', fontsize=14, fontweight='bold')
ax.set_ylabel('Teammate Grade Correlation with Wins →', fontsize=14, fontweight='bold')
ax.set_title('Four-Quadrant Player Impact Analysis\nWho Impacts Winning and How?', 
             fontsize=16, fontweight='bold', pad=20)

# Add quadrant labels
ax.text(ax.get_xlim()[1]*0.85, ax.get_ylim()[1]*0.95, 'COMPLETE\nPLAYERS', 
        fontsize=12, fontweight='bold', ha='center', va='top', alpha=0.6, color='darkgreen')
ax.text(ax.get_xlim()[0]*0.85, ax.get_ylim()[1]*0.95, 'INTANGIBLE\nIMPACT', 
        fontsize=12, fontweight='bold', ha='center', va='top', alpha=0.6, color='darkblue')
ax.text(ax.get_xlim()[1]*0.85, ax.get_ylim()[0]*0.95, 'STAT\nSTUFFERS', 
        fontsize=12, fontweight='bold', ha='center', va='top', alpha=0.6, color='darkorange')
ax.text(ax.get_xlim()[0]*0.85, ax.get_ylim()[0]*0.95, 'NEED\nFOCUS', 
        fontsize=12, fontweight='bold', ha='center', va='top', alpha=0.6, color='darkred')

plt.tight_layout()
plt.savefig('four_quadrant_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# Print interpretation
print("\n" + "=" * 80)
print("FOUR-QUADRANT ANALYSIS: PLAYER IMPACT ON WINNING")
print("=" * 80)
print("\nQUADRANT BREAKDOWN:\n")

for _, row in player_df.iterrows():
    player = row['Player']
    stat_corr = row['Stat_Correlation']
    grade_corr = row['Grade_Correlation']
    
    # Determine quadrant
    if stat_corr >= x_mid and grade_corr >= y_mid:
        quadrant = "🟢 COMPLETE PLAYER"
        desc = "High stats + high overall performance = maximum impact"
    elif stat_corr < x_mid and grade_corr >= y_mid:
        quadrant = "🔵 INTANGIBLE IMPACT"
        desc = "Wins with hustle, defense, leadership - not just stats"
    elif stat_corr >= x_mid and grade_corr < y_mid:
        quadrant = "🟠 STAT STUFFER"
        desc = "Puts up numbers, but overall performance matters less"
    else:
        quadrant = "🔴 NEEDS FOCUS"
        desc = "Room to grow in both stats and overall play"
    
    print(f"{player}:")
    print(f"  Quadrant: {quadrant}")
    print(f"  Stat Impact: {stat_corr:.3f} | Grade Impact: {grade_corr:.3f}")
    print(f"  Meaning: {desc}")
    print()

print("=" * 80)
print("\nKEY INSIGHTS:")
print("=" * 80)

# Find the complete player
top_player = player_df.loc[player_df[['Stat_Correlation', 'Grade_Correlation']].sum(axis=1).idxmax()]
print(f"🏆 Most Complete Impact: {top_player['Player']}")

# Find the stat stuffer
stat_heavy = player_df.loc[player_df['Stat_Correlation'].idxmax()]
print(f"📊 Biggest Stat Impact: {stat_heavy['Player']} ({stat_heavy['Stat_Correlation']:.3f})")

# Find intangible player
grade_heavy = player_df.loc[player_df['Grade_Correlation'].idxmax()]
print(f"💪 Biggest Intangible Impact: {grade_heavy['Player']} ({grade_heavy['Grade_Correlation']:.3f})")

print("=" * 80)