import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv('./data/pro_am_games.csv')

# Convert Result to binary (1 for Win, 0 for Loss)
df['Win'] = (df['Result'] == 'W').astype(int)

# Convert letter grades to numerical values
grade_map = {
    'A+': 4.3, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'D-': 0.7,
    'F': 0.0
}

# Get all your team's players
team_players = ['tymelxss', 'AbuTalibaan', 'Glo4Prezz', 'Yurselln', 'MajinKemboi']

# Convert grades to numerical for all players
for player in team_players:
    grade_col = f"{player}_Grade"
    df[f"{player}_Grade_Numeric"] = df[grade_col].map(grade_map)

# Calculate correlations for teammate grades
grade_correlations = []
for player in team_players:
    numeric_col = f"{player}_Grade_Numeric"
    corr = df[numeric_col].corr(df['Win'])
    grade_correlations.append({
        'Player': player,
        'Correlation': corr
    })

# Convert to DataFrame and sort
grade_corr_df = pd.DataFrame(grade_correlations)
grade_corr_df = grade_corr_df.sort_values('Correlation', ascending=False)

# Display results
print("=" * 70)
print("TEAMMATE GRADE CORRELATION WITH WINS")
print("=" * 70)
print(grade_corr_df.to_string(index=False))
print("\n")

# Show average grades in wins vs losses
print("=" * 70)
print("AVERAGE TEAMMATE GRADES: WINS vs LOSSES")
print("=" * 70)
for player in team_players:
    grade_col = f"{player}_Grade"
    numeric_col = f"{player}_Grade_Numeric"
    
    win_avg = df[df['Win'] == 1][numeric_col].mean()
    loss_avg = df[df['Win'] == 0][numeric_col].mean()
    diff = win_avg - loss_avg
    
    # Get most common grade in wins and losses
    win_grades = df[df['Win'] == 1][grade_col].mode()
    loss_grades = df[df['Win'] == 0][grade_col].mode()
    win_grade = win_grades.iloc[0] if len(win_grades) > 0 else 'N/A'
    loss_grade = loss_grades.iloc[0] if len(loss_grades) > 0 else 'N/A'
    
    print(f"\n{player}:")
    print(f"  Wins: {win_avg:.2f} (most common: {win_grade})")
    print(f"  Losses: {loss_avg:.2f} (most common: {loss_grade})")
    print(f"  Difference: {diff:+.2f}")

# Visualization: Bar chart of grade correlations
plt.figure(figsize=(12, 6))
colors = ['green' if x > 0 else 'red' for x in grade_corr_df['Correlation']]
plt.bar(grade_corr_df['Player'], grade_corr_df['Correlation'], color=colors, alpha=0.7, edgecolor='black')
plt.xlabel('Player', fontsize=12, fontweight='bold')
plt.ylabel('Correlation with Wins', fontsize=12, fontweight='bold')
plt.title('Which Player\'s Teammate Grade Matters Most for Winning?', fontsize=14, fontweight='bold')
plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.grid(axis='y', alpha=0.3)
plt.xticks(rotation=45, ha='right')

# Add correlation values on top of bars
for i, (player, corr) in enumerate(zip(grade_corr_df['Player'], grade_corr_df['Correlation'])):
    plt.text(i, corr + 0.02 if corr > 0 else corr - 0.02, f'{corr:.3f}', 
             ha='center', va='bottom' if corr > 0 else 'top', fontweight='bold')

plt.tight_layout()
plt.savefig('teammate_grade_correlations.png', dpi=300, bbox_inches='tight')
plt.show()

# Box plot showing grade distribution in wins vs losses
fig, axes = plt.subplots(1, 5, figsize=(18, 5))
for i, player in enumerate(team_players):
    numeric_col = f"{player}_Grade_Numeric"
    
    win_data = df[df['Win'] == 1][numeric_col]
    loss_data = df[df['Win'] == 0][numeric_col]
    
    axes[i].boxplot([win_data, loss_data], labels=['Wins', 'Losses'])
    axes[i].set_title(player, fontweight='bold')
    axes[i].set_ylabel('Grade (Numeric)' if i == 0 else '')
    axes[i].grid(axis='y', alpha=0.3)

plt.suptitle('Teammate Grade Distribution: Wins vs Losses', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('grade_distributions.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "=" * 70)
print("KEY TAKEAWAY:")
print("=" * 70)
max_corr_player = grade_corr_df.iloc[0]['Player']
max_corr_value = grade_corr_df.iloc[0]['Correlation']
print(f"🏆 {max_corr_player}'s teammate grade has the strongest correlation")
print(f"   with wins ({max_corr_value:.3f})")
print(f"\nWhen {max_corr_player} plays well (high grade), the team wins more!")
print("=" * 70)