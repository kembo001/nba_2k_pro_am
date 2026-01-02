import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
df = pd.read_csv('./data/pro_am_games.csv')
df['Win'] = (df['Result'] == 'W').astype(int)

team_players = ['tymelxss', 'AbuTalibaan', 'Glo4Prezz', 'Yurselln', 'MajinKemboi']
stats = ['Points', 'Rebounds', 'Assists', 'FGM']

# Analyze each player's stat correlations and performance

player_analysis = []

for player in team_players:
    points_corr = df[f"{player}_Points"].corr(df['Win'])
    rebounds_corr = df[f"{player}_Rebounds"].corr(df['Win'])
    assists_corr = df[f"{player}_Assists"].corr(df['Win'])
    fgm_corr = df[f"{player}_FGM"].corr(df['Win'])
    
    # Calculate offensive vs supporting roles
    offensive_impact = (points_corr + fgm_corr) / 2
    supporting_impact = (rebounds_corr + assists_corr) / 2
    total_impact = np.mean([points_corr, rebounds_corr, assists_corr, fgm_corr])
    
    # Get averages in wins vs losses
    pts_win = df[df['Win'] == 1][f"{player}_Points"].mean()
    pts_loss = df[df['Win'] == 0][f"{player}_Points"].mean()
    reb_win = df[df['Win'] == 1][f"{player}_Rebounds"].mean()
    reb_loss = df[df['Win'] == 0][f"{player}_Rebounds"].mean()
    ast_win = df[df['Win'] == 1][f"{player}_Assists"].mean()
    ast_loss = df[df['Win'] == 0][f"{player}_Assists"].mean()
    
    # Calculate "inefficiency score" - how much they do things that don't help win
    inefficiency = 0
    if points_corr < 0:
        inefficiency += abs(points_corr)
    if rebounds_corr < 0:
        inefficiency += abs(rebounds_corr)
    if assists_corr < 0:
        inefficiency += abs(assists_corr)
    
    player_analysis.append({
        'Player': player,
        'Points_Corr': points_corr,
        'Rebounds_Corr': rebounds_corr,
        'Assists_Corr': assists_corr,
        'FGM_Corr': fgm_corr,
        'Offensive_Impact': offensive_impact,
        'Supporting_Impact': supporting_impact,
        'Total_Impact': total_impact,
        'Inefficiency_Score': inefficiency,
        'Pts_Win_Avg': pts_win,
        'Pts_Loss_Avg': pts_loss,
        'Reb_Win_Avg': reb_win,
        'Reb_Loss_Avg': reb_loss,
        'Ast_Win_Avg': ast_win,
        'Ast_Loss_Avg': ast_loss
    })

analysis_df = pd.DataFrame(player_analysis)

# Sort by inefficiency score to find who needs build change most
analysis_df = analysis_df.sort_values('Inefficiency_Score', ascending=False)

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Chart 1: Player stat correlations heatmap
ax1 = axes[0, 0]
corr_data = analysis_df[['Player', 'Points_Corr', 'Rebounds_Corr', 'Assists_Corr', 'FGM_Corr']].set_index('Player')
sns.heatmap(corr_data.T, annot=True, fmt='.3f', cmap='RdYlGn', center=0, 
            vmin=-0.5, vmax=0.5, ax=ax1, cbar_kws={'label': 'Correlation'})
ax1.set_title('Player Stat Correlations with Wins\n(Red = Hurting, Green = Helping)', 
              fontsize=13, fontweight='bold')
ax1.set_xlabel('')
ax1.set_ylabel('Stat Type', fontsize=11, fontweight='bold')

# Chart 2: Inefficiency scores (who's doing things that don't help)
ax2 = axes[0, 1]
colors_ineff = ['#d32f2f' if x > 0.3 else '#ff9800' if x > 0.15 else '#4caf50' 
                for x in analysis_df['Inefficiency_Score']]
bars = ax2.barh(analysis_df['Player'], analysis_df['Inefficiency_Score'], 
                color=colors_ineff, alpha=0.8, edgecolor='black', linewidth=1.5)
ax2.set_xlabel('Inefficiency Score (Higher = Need Build Change)', fontsize=11, fontweight='bold')
ax2.set_title('Who Needs a New Build Most?\n(Based on Negative Stat Correlations)', 
              fontsize=13, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)

# Add value labels
for i, (player, score) in enumerate(zip(analysis_df['Player'], analysis_df['Inefficiency_Score'])):
    ax2.text(score + 0.01, i, f'{score:.3f}', ha='left', va='center', fontweight='bold')

# Chart 3: Role mismatch - Offensive vs Supporting impact
ax3 = axes[1, 0]
scatter = ax3.scatter(analysis_df['Offensive_Impact'], analysis_df['Supporting_Impact'],
                     s=500, alpha=0.6, c=analysis_df['Inefficiency_Score'], 
                     cmap='RdYlGn_r', edgecolors='black', linewidth=2)
ax3.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax3.axvline(x=0, color='black', linestyle='--', linewidth=1)
ax3.set_xlabel('Offensive Impact (Scoring) →', fontsize=11, fontweight='bold')
ax3.set_ylabel('Supporting Impact (Rebounds/Assists) →', fontsize=11, fontweight='bold')
ax3.set_title('Current Role vs Ideal Role\n(Color shows need for change)', 
              fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3)

# Add player labels
for _, row in analysis_df.iterrows():
    ax3.annotate(row['Player'], (row['Offensive_Impact'], row['Supporting_Impact']),
                fontsize=9, fontweight='bold', ha='center', va='center')

plt.colorbar(scatter, ax=ax3, label='Need for Build Change')

# Chart 4: What they should focus on
ax4 = axes[1, 1]
ax4.axis('off')

# Generate recommendations
recommendations = []
for _, row in analysis_df.iterrows():
    player = row['Player']
    
    # Determine what they should focus on
    strengths = []
    weaknesses = []
    
    if row['Points_Corr'] > 0.2:
        strengths.append('Scoring')
    elif row['Points_Corr'] < -0.1:
        weaknesses.append('Scoring hurts team')
    
    if row['Rebounds_Corr'] > 0.2:
        strengths.append('Rebounding')
    elif row['Rebounds_Corr'] < -0.1:
        weaknesses.append('Rebounding not needed')
    
    if row['Assists_Corr'] > 0.2:
        strengths.append('Playmaking')
    elif row['Assists_Corr'] < -0.1:
        weaknesses.append('Over-passing')
    
    recommendations.append({
        'Player': player,
        'Strengths': strengths,
        'Weaknesses': weaknesses,
        'Score': row['Inefficiency_Score']
    })

# Display recommendations
rec_text = "🔧 BUILD CHANGE PRIORITY:\n\n"
for i, rec in enumerate(recommendations[:3], 1):  # Top 3
    rec_text += f"{i}. {rec['Player']}\n"
    if rec['Weaknesses']:
        rec_text += f"   ❌ Fix: {', '.join(rec['Weaknesses'])}\n"
    if rec['Strengths']:
        rec_text += f"   ✅ Keep: {', '.join(rec['Strengths'])}\n"
    rec_text += "\n"

ax4.text(0.05, 0.95, rec_text, transform=ax4.transAxes, fontsize=11,
         verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

plt.tight_layout()
plt.savefig('build_recommendations.png', dpi=300, bbox_inches='tight')
plt.show()

# Print detailed analysis
print("\n" + "=" * 100)
print(" " * 30 + "🏀 BUILD CHANGE RECOMMENDATIONS 🏀")
print("=" * 100)

print("\nRANKED BY WHO NEEDS A NEW BUILD MOST:\n")
print("-" * 100)

for i, row in analysis_df.iterrows():
    player = row['Player']
    print(f"\n{'🔴 PRIORITY' if row['Inefficiency_Score'] > 0.3 else '🟡 CONSIDER' if row['Inefficiency_Score'] > 0.15 else '🟢 OPTIMAL'}: {player}")
    print(f"Inefficiency Score: {row['Inefficiency_Score']:.3f}")
    print(f"\nStat Correlations:")
    print(f"  Points:   {row['Points_Corr']:+.3f} {'❌ HURTING' if row['Points_Corr'] < -0.1 else '✅ HELPING' if row['Points_Corr'] > 0.2 else '→ NEUTRAL'}")
    print(f"  Rebounds: {row['Rebounds_Corr']:+.3f} {'❌ HURTING' if row['Rebounds_Corr'] < -0.1 else '✅ HELPING' if row['Rebounds_Corr'] > 0.2 else '→ NEUTRAL'}")
    print(f"  Assists:  {row['Assists_Corr']:+.3f} {'❌ HURTING' if row['Assists_Corr'] < -0.1 else '✅ HELPING' if row['Assists_Corr'] > 0.2 else '→ NEUTRAL'}")
    print(f"  FGM:      {row['FGM_Corr']:+.3f} {'❌ HURTING' if row['FGM_Corr'] < -0.1 else '✅ HELPING' if row['FGM_Corr'] > 0.2 else '→ NEUTRAL'}")
    
    print(f"\nWins vs Losses Performance:")
    print(f"  Scoring:    {row['Pts_Win_Avg']:.1f} (wins) vs {row['Pts_Loss_Avg']:.1f} (losses)")
    print(f"  Rebounding: {row['Reb_Win_Avg']:.1f} (wins) vs {row['Reb_Loss_Avg']:.1f} (losses)")
    print(f"  Assists:    {row['Ast_Win_Avg']:.1f} (wins) vs {row['Ast_Loss_Avg']:.1f} (losses)")
    
    # Recommend builds based on the data
    print(f"\n💡 BUILD RECOMMENDATION:")
    
    if row['Assists_Corr'] > 0.3 and row['Points_Corr'] < 0:
        print(f"   → PURE PLAYMAKER (e.g., 'Pace Commander', 'Dot Dispenser')")
        print(f"   → Focus: Max passing, ball handle, speed with ball")
        print(f"   → Why: Your assists win games ({row['Assists_Corr']:+.3f}), but scoring doesn't ({row['Points_Corr']:+.3f})")
    
    elif row['Rebounds_Corr'] > 0.4:
        print(f"   → REBOUNDING SPECIALIST (e.g., 'Pitbull', 'The Guard Dog')")
        print(f"   → Focus: Max rebounding, interior defense, strength")
        print(f"   → Why: Your boards are critical to winning ({row['Rebounds_Corr']:+.3f})")
    
    elif row['Offensive_Impact'] > 0.2 and row['Supporting_Impact'] > 0.2:
        print(f"   → TWO-WAY BUILD (e.g., 'Mr. Two Way', 'Big Glide')")
        print(f"   → Focus: Balanced scoring and supporting stats")
        print(f"   → Why: You impact winning in multiple ways")
    
    elif row['Offensive_Impact'] > 0.2:
        print(f"   → SCORING BUILD (e.g., 'Swish Lord', 'Unguardable')")
        print(f"   → Focus: Max shooting, driving, finishing")
        print(f"   → Why: Your offense drives wins")
    
    elif row['Inefficiency_Score'] > 0.3:
        print(f"   → REBUILD NEEDED - Current build not matching role")
        print(f"   → Pick ONE identity: Either pure playmaker OR pure scorer")
    
    else:
        print(f"   → CURRENT BUILD IS WORKING - Minor adjustments only")
    
    print("-" * 100)

print("\n" + "=" * 100)
print("🎯 BOTTOM LINE:")
print("=" * 100)

worst_player = analysis_df.iloc[0]
print(f"\n{worst_player['Player']} needs a build change MOST.")
print(f"Their inefficiency score ({worst_player['Inefficiency_Score']:.3f}) shows they're doing things that don't help win.")
print(f"\nVisit https://www.nba2klab.com/nba2k-pro-tuned-builds to find the right Pro Tuned Build!")
print("=" * 100)