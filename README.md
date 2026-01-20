# NBA 2K Pro-Am Team Analytics

A data-driven analytics project for optimizing team performance in NBA 2K Pro-Am. This project analyzes game-by-game statistics to identify winning patterns, player strengths, and build recommendations.

## Overview

This project tracks and analyzes performance data from 5v5 Pro-Am games to answer key questions:
- What stats correlate most with winning?
- Which players need build changes?
- What defensive strategies work best?
- How can we optimize our team composition?

## Team Roster

| Player | Role |
|--------|------|
| tymelxss | Facilitator/Playmaker |
| AbuTalibaan | Rebounder/Interior Presence |
| Glo4Prezz | Scorer/All-Around |
| Yurselln | Defensive Support |
| MajinKemboi | All-Around Contributor |

## Project Structure

```
nba_2k_pro_am/
├── data/
│   └── pro_am_games.csv       # Game-by-game performance data
├── final_data.py              # Comprehensive winning formula analysis
├── nba_player_update.py       # Build change recommendations
├── team_data.py               # Team stat correlation analysis
├── team_stats.py              # Basic team statistics
├── four_quad_char.py          # Four-quadrant player impact matrix
├── opp.py                     # Opponent/defensive analysis
├── snsplot.py                 # Pairplot visualization
└── *.png                      # Generated visualizations
```

## Data Tracked

For each game, the following is recorded:
- **Game metadata**: Date, Game #, Result (W/L)
- **Team stats** (per player): Grade, Points, Rebounds, Assists, FGM
- **Opponent stats** (per opponent): Grade, Points, Rebounds, Assists, FGM

## Analysis Scripts

| Script | Purpose |
|--------|---------|
| `final_data.py` | Generates the complete winning formula dashboard with top offensive/defensive factors |
| `nba_player_update.py` | Calculates inefficiency scores and recommends build changes per player |
| `team_data.py` | Creates correlation heatmap and identifies top 15 stats correlated with wins |
| `team_stats.py` | Compares player performance in wins vs losses |
| `four_quad_char.py` | Maps players on a 4-quadrant chart (stat correlation vs grade correlation) |
| `opp.py` | Analyzes what opponent stats hurt the team most |
| `snsplot.py` | Exploratory pairplot of all team stats |

## Key Findings

**Defense > Offense**: Opponent scoring correlation with losses is nearly 2x stronger than any offensive stat's correlation with wins.

**Winning Formula**:
- Hold opponents under 62 points
- Dominate the boards (especially Abu & Glo)
- Facilitate ball movement (assists matter)

## Generated Visualizations

- `correlation_heatmap.png` - All player stats vs wins
- `top_correlations.png` - Top 15 most impactful stats
- `four_quadrant_analysis.png` - Player impact classification
- `teammate_grade_correlations.png` - Grade importance by player
- `grade_distributions.png` - Performance in wins vs losses
- `opponent_impact.png` - Defensive weaknesses
- `opponent_comparison.png` - Opponent stats in wins vs losses
- `complete_winning_formula.png` - Summary dashboard
- `build_recommendations.png` - Build change priorities

## Tech Stack

- Python 3.13
- pandas
- numpy
- matplotlib
- seaborn

## Setup

```bash
# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install pandas numpy matplotlib seaborn
```

## Usage

```bash
# Run the main winning formula analysis
python final_data.py

# Get build recommendations
python nba_player_update.py

# Generate correlation heatmap
python team_data.py
```

## Adding New Game Data

Add new rows to `data/pro_am_games.csv` with the following format:
- Date, Game #, Result (W/L)
- Each teammate's Grade, Points, Rebounds, Assists, FGM
- Each opponent's Grade, Points, Rebounds, Assists, FGM

Then re-run the analysis scripts to update insights.
