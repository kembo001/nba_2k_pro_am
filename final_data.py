import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv('./data/pro_am_games.csv')
df['Win'] = (df['Result'] == 'W').astype(int)

# Get top offensive stats
team_players = ['tymelxss', 'AbuTalibaan', 'Glo4Prezz', 'Yurselln', 'MajinKemboi']
stats = ['Points', 'Rebounds', 'Assists', 'FGM']

offensive_factors = []
for player in team_players:
    for stat in stats:
        col_name = f"{player}_{stat}"
        corr = df[col_name].corr(df['Win'])
        offensive_factors.append({
            'Factor': f"{player}\n{stat}",
            'Correlation': corr,
            'Type': 'Offense'
        })

# Get defensive vulnerabilities (opponent stats)
for stat in stats:
    df[f'Opp_Total_{stat}'] = (df[f'opp1_{stat}'] + df[f'opp2_{stat}'] + 
                                 df[f'opp3_{stat}'] + df[f'opp4_{stat}'] + 
                                 df[f'opp5_{stat}'])
    corr = df[f'Opp_Total_{stat}'].corr(df['Win'])
    offensive_factors.append({
        'Factor': f"Opponent\n{stat}",
        'Correlation': corr,
        'Type': 'Defense'
    })

# Create DataFrame and get top factors
all_factors = pd.DataFrame(offensive_factors)
all_factors['Abs_Correlation'] = all_factors['Correlation'].abs()

# Get top 5 offensive and top 4 defensive
top_offense = all_factors[all_factors['Type'] == 'Offense'].nlargest(5, 'Correlation')
top_defense = all_factors[all_factors['Type'] == 'Defense'].nsmallest(4, 'Correlation')

# Combine
key_factors = pd.concat([top_defense, top_offense]).reset_index(drop=True)

# Create the comprehensive visualization
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 2, height_ratios=[2, 1, 1], hspace=0.4, wspace=0.3)

# Main chart: What drives wins and losses
ax1 = fig.add_subplot(gs[0, :])

colors = ['#d32f2f' if x < 0 else '#388e3c' for x in key_factors['Correlation']]
bars = ax1.barh(range(len(key_factors)), key_factors['Correlation'], 
                color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

ax1.set_yticks(range(len(key_factors)))
ax1.set_yticklabels(key_factors['Factor'], fontsize=11, fontweight='bold')
ax1.set_xlabel('Impact on Winning', fontsize=14, fontweight='bold')
ax1.set_title('COMPLETE WINNING FORMULA: Top Offensive Strengths vs Defensive Weaknesses', 
              fontsize=16, fontweight='bold', pad=20)
ax1.axvline(x=0, color='black', linewidth=2)
ax1.grid(axis='x', alpha=0.3)

# Add value labels
for i, (factor, corr, type_) in enumerate(zip(key_factors['Factor'], 
                                                key_factors['Correlation'],
                                                key_factors['Type'])):
    label = f'{corr:.3f}'
    ax1.text(corr + 0.03 if corr > 0 else corr - 0.03, i, label,
             ha='left' if corr > 0 else 'right', va='center', 
             fontweight='bold', fontsize=10)

# Add section labels
defense_end = len(top_defense) - 0.5
ax1.axhline(y=defense_end, color='black', linestyle='--', linewidth=2, alpha=0.5)
ax1.text(ax1.get_xlim()[0] * 0.95, len(key_factors) - 1, 'OFFENSIVE\nSTRENGTHS', 
         fontsize=12, fontweight='bold', ha='left', va='top', 
         bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
ax1.text(ax1.get_xlim()[0] * 0.95, 0, 'DEFENSIVE\nWEAKNESSES', 
         fontsize=12, fontweight='bold', ha='left', va='bottom',
         bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

# Bottom left: Key takeaways
ax2 = fig.add_subplot(gs[1, 0])
ax2.axis('off')

takeaways = """
🎯 KEY TAKEAWAYS:

1️⃣ DEFENSE > OFFENSE
   • Opponent scoring (-0.75) impacts
     wins MORE than any offensive stat
   
2️⃣ OFFENSIVE PRIORITIES:
   • Abu & Glo: Crash the boards
   • tymelxss: Facilitate, don't force shots
   
3️⃣ DEFENSIVE PRIORITY:
   • Hold teams under 62 points to win
   • Contest shots (limit FGM)
   • Disrupt ball movement (limit assists)
"""

ax2.text(0.05, 0.95, takeaways, transform=ax2.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Bottom right: Win formula
ax3 = fig.add_subplot(gs[1, 1])
ax3.axis('off')

formula = """
🏆 WINNING FORMULA:

✅ DEFENSE FIRST:
   Hold opponents < 62 pts

✅ REBOUND:
   Abu + Glo dominate glass

✅ FACILITATE:
   tymelxss run the offense

✅ ENERGY:
   Every possession matters
   
📊 Current: 9-9
🎯 Goal: Use data to go on a run!
"""

ax3.text(0.05, 0.95, formula, transform=ax3.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

# Stats comparison box
ax4 = fig.add_subplot(gs[2, :])
ax4.axis('off')

# Calculate key numbers
wins = df['Win'].sum()
losses = len(df) - wins
avg_opp_pts_win = df[df['Win']==1][[f'opp{i}_Points' for i in range(1,6)]].sum(axis=1).mean()
avg_opp_pts_loss = df[df['Win']==0][[f'opp{i}_Points' for i in range(1,6)]].sum(axis=1).mean()

stats_summary = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECORD: {wins}-{losses}  |  BIGGEST CORRELATION: Opponent Points (-0.748)  |  TARGET: Hold opponents < 62 points per game
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

ax4.text(0.5, 0.5, stats_summary, transform=ax4.transAxes,
         fontsize=11, ha='center', va='center', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.3))

plt.savefig('complete_winning_formula.png', dpi=300, bbox_inches='tight')
plt.show()

# Print summary
print("\n" + "=" * 90)
print(" " * 25 + "🏀 COMPLETE ANALYSIS SUMMARY 🏀")
print("=" * 90)
print(f"\nCURRENT RECORD: {wins} Wins - {losses} Losses (9-9)\n")

print("TOP 5 OFFENSIVE FACTORS (What WE do to win):")
print("-" * 90)
for i, row in top_offense.iterrows():
    print(f"  {row['Factor'].replace(chr(10), ' ')}: {row['Correlation']:+.3f}")

print("\nTOP 4 DEFENSIVE VULNERABILITIES (What OPPONENTS do to beat us):")
print("-" * 90)
for i, row in top_defense.iterrows():
    print(f"  {row['Factor'].replace(chr(10), ' ')}: {row['Correlation']:+.3f}")

print("\n" + "=" * 90)
print("💡 THE BOTTOM LINE:")
print("=" * 90)
print("""
Defense matters MORE than offense. The opponent scoring correlation (-0.748) is nearly 
TWICE as strong as your best offensive stat (Abu Rebounds: +0.471).

GAME PLAN:
1. DEFENSE FIRST - Hold teams under 62 points
2. Abu & Glo - Dominate the boards  
3. tymelxss - Facilitate over scoring
4. Everyone - Energy, communication, contest shots

Apply these insights and watch your record improve! 📈
""")
print("=" * 90)