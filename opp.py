import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv('./data/pro_am_games.csv')

# Convert Result to binary
df['Win'] = (df['Result'] == 'W').astype(int)

# Aggregate all opponent stats per game
stats = ['Points', 'Rebounds', 'Assists', 'FGM']

for stat in stats:
    # Sum up all 5 opponents' stats
    df[f'Opp_Total_{stat}'] = (df[f'opp1_{stat}'] + df[f'opp2_{stat}'] + 
                                 df[f'opp3_{stat}'] + df[f'opp4_{stat}'] + 
                                 df[f'opp5_{stat}'])

# Calculate correlations (negative = bad for us, they win when this is high)
opp_correlations = []
for stat in stats:
    col_name = f'Opp_Total_{stat}'
    corr = df[col_name].corr(df['Win'])
    
    opp_correlations.append({
        'Stat': f'Opponent {stat}',
        'Correlation': corr,
        'Avg_In_Wins': df[df['Win'] == 1][col_name].mean(),
        'Avg_In_Losses': df[df['Win'] == 0][col_name].mean(),
        'Difference': df[df['Win'] == 1][col_name].mean() - df[df['Win'] == 0][col_name].mean()
    })

opp_df = pd.DataFrame(opp_correlations)
opp_df['Abs_Correlation'] = opp_df['Correlation'].abs()
opp_df = opp_df.sort_values('Correlation', ascending=True)  # Most negative first

# Display results
print("=" * 80)
print("WHAT OPPONENT STATS KILL US THE MOST?")
print("=" * 80)
print("(Negative correlation = when opponents do this, we LOSE)")
print()
print(opp_df[['Stat', 'Correlation', 'Avg_In_Wins', 'Avg_In_Losses', 'Difference']].to_string(index=False))
print()

# Find biggest weakness
biggest_weakness = opp_df.iloc[0]
print("=" * 80)
print("🚨 BIGGEST DEFENSIVE WEAKNESS:")
print("=" * 80)
print(f"{biggest_weakness['Stat']} (Correlation: {biggest_weakness['Correlation']:.3f})")
print(f"When we WIN: Opponents average {biggest_weakness['Avg_In_Wins']:.1f}")
print(f"When we LOSE: Opponents average {biggest_weakness['Avg_In_Losses']:.1f}")
print(f"Difference: {biggest_weakness['Difference']:.1f} (they get {abs(biggest_weakness['Difference']):.1f} more in losses)")
print("=" * 80)
print()

# Visualization 1: Bar chart of opponent stat impact
plt.figure(figsize=(12, 6))
colors = ['red' if x < 0 else 'green' for x in opp_df['Correlation']]
plt.barh(range(len(opp_df)), opp_df['Correlation'], color=colors, alpha=0.7, edgecolor='black')
plt.yticks(range(len(opp_df)), opp_df['Stat'])
plt.xlabel('Correlation with Our Wins', fontsize=12, fontweight='bold')
plt.title('What Opponent Stats Hurt Us Most?\n(More negative = bigger problem)', 
          fontsize=14, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='-', linewidth=1)
plt.grid(axis='x', alpha=0.3)

# Add values on bars
for i, (stat, corr) in enumerate(zip(opp_df['Stat'], opp_df['Correlation'])):
    plt.text(corr - 0.02 if corr < 0 else corr + 0.02, i, f'{corr:.3f}', 
             ha='right' if corr < 0 else 'left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('opponent_impact.png', dpi=300, bbox_inches='tight')
plt.show()

# Visualization 2: Wins vs Losses comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for i, stat in enumerate(stats):
    col_name = f'Opp_Total_{stat}'
    
    win_data = df[df['Win'] == 1][col_name]
    loss_data = df[df['Win'] == 0][col_name]
    
    # Create box plots
    bp = axes[i].boxplot([win_data, loss_data], labels=['Our WINS', 'Our LOSSES'],
                          patch_artist=True)
    
    # Color boxes
    bp['boxes'][0].set_facecolor('lightgreen')
    bp['boxes'][1].set_facecolor('lightcoral')
    
    axes[i].set_title(f'Opponent {stat}', fontsize=13, fontweight='bold')
    axes[i].set_ylabel(stat, fontsize=11)
    axes[i].grid(axis='y', alpha=0.3)
    
    # Add average lines
    axes[i].axhline(win_data.mean(), color='green', linestyle='--', 
                    linewidth=2, alpha=0.7, label=f'Win Avg: {win_data.mean():.1f}')
    axes[i].axhline(loss_data.mean(), color='red', linestyle='--', 
                    linewidth=2, alpha=0.7, label=f'Loss Avg: {loss_data.mean():.1f}')
    axes[i].legend(loc='upper right', fontsize=9)

plt.suptitle('What Do Opponents Do Differently When They Beat Us?', 
             fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('opponent_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# Detailed breakdown
print()
print("=" * 80)
print("DETAILED BREAKDOWN - WHAT WE GIVE UP:")
print("=" * 80)
for _, row in opp_df.iterrows():
    print(f"\n{row['Stat']}:")
    print(f"  Correlation with OUR wins: {row['Correlation']:.3f}")
    print(f"  When we WIN: Opponents get {row['Avg_In_Wins']:.1f}")
    print(f"  When we LOSE: Opponents get {row['Avg_In_Losses']:.1f}")
    print(f"  We give up {abs(row['Difference']):.1f} MORE in losses")
    
    if row['Correlation'] < -0.3:
        print(f"  ⚠️  CRITICAL WEAKNESS - This is killing us!")
    elif row['Correlation'] < -0.1:
        print(f"  ⚠️  Moderate weakness - Needs attention")
    else:
        print(f"  ✓ Not a major issue")

print("\n" + "=" * 80)
print("DEFENSIVE GAME PLAN:")
print("=" * 80)

# Create action items based on biggest weaknesses
weaknesses = opp_df[opp_df['Correlation'] < -0.2]
if len(weaknesses) > 0:
    print("\n🎯 PRIORITY DEFENSIVE FOCUSES:\n")
    for i, (_, row) in enumerate(weaknesses.iterrows(), 1):
        stat_type = row['Stat'].replace('Opponent ', '')
        diff = abs(row['Difference'])
        print(f"{i}. LIMIT OPPONENT {stat_type.upper()}")
        print(f"   - Currently giving up {diff:.1f} more in losses")
        print(f"   - Target: Keep them under {row['Avg_In_Wins']:.1f} {stat_type.lower()}")
        print()

print("=" * 80)