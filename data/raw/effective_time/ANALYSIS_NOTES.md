# Effective Playing Time Data: Research Notes

## Date Collected: 2026-03-19

## Overview

This directory contains effective playing time (ball-in-play) data collected from multiple
sources to support Project 907's analysis of the FIFA 2022 stoppage-time directive.

## Key Finding for the Paper

**The extra stoppage time is mostly wasted, not played.**

The ESPN/Opta data (from espn.com/soccer/story/38861516) provides the cleanest evidence:

### Premier League Example

| Period | Ball-in-Play | Stoppage Added |
|--------|-------------|----------------|
| 2020-23 avg | 55:27 | 7:30 |
| 2023-24 | 58:32 | 11:35 |
| **Change** | **+3:05** | **+4:05** |

- Stoppage time increased by 4:05 minutes
- Ball-in-play increased by only 3:05 minutes
- Roughly 1 minute of the extra stoppage was "wasted" (not played)
- However, PL shows the BEST ratio of the big 5 (75% of extra time was played)

### La Liga Example (worst ratio)

| Period | Ball-in-Play | Stoppage Added |
|--------|-------------|----------------|
| 2020-23 avg | 53:21 | 7:15 |
| 2023-24 | 54:47 | 11:25 |
| **Change** | **+1:26** | **+4:10** |

- Stoppage time increased by 4:10 minutes
- Ball-in-play increased by only 1:26 minutes
- Over 2.5 minutes of extra stoppage was "wasted"
- Only 35% of extra time was actually played

### All Big 5 Leagues Summary (2020-23 avg vs 2023-24)

| League | Extra BIP | Extra Stoppage | Ratio (played/added) |
|--------|-----------|----------------|---------------------|
| Premier League | +3:05 | +4:05 | 75% |
| Ligue 1 | +1:48 | +3:27 | 52% |
| Bundesliga | +1:52 | +3:31 | 53% |
| Serie A | +0:48 | +2:35 | 31% |
| La Liga | +1:26 | +4:10 | 35% |

**This is a key table for the paper.** It shows that across Europe, only 31-75% of the
extra stoppage time added post-directive actually produced more football. The rest was
consumed by additional time-wasting behavior that expanded to fill the longer matches.

## How to Use in the Paper

### 1. As a mechanism test (Section 4 or 5)
- If the directive was purely "cosmetic" -> effective time stays constant, only clock expands
- If the directive produced "real" effects -> effective time increases proportionally
- Reality is in between, but closer to cosmetic in most leagues

### 2. As a control variable
- `effective_play_time` at league-season level can control for actual intensity of play
- Matches where the ball was in play longer may have different injury/performance patterns

### 3. For heterogeneity analysis
- Compare the EPL (high uptake, 75% ratio) to La Liga (low uptake, 35%)
- This maps onto the paper's league fixed effects
- Leagues that already had high effective time (Ligue 1, 56:07) gained less than those
  that were lower (PL at 55:27)

### 4. Time-wasting behavioral response
- The fact that effective time increased LESS than stoppage time proves that teams
  adapted their time-wasting behavior: more stoppage -> more waste -> diminishing returns
- This is consistent with a strategic response model where trailing teams waste less
  (they want to play) and leading teams waste more (they want to run down the clock)
- The extra stoppage time mechanically increases the value of time-wasting for
  leading teams, since there's more time to "burn"

### 5. Comparison to World Cup 2022
- World Cup 2018: ~55:41 effective, ~7:18 stoppage
- World Cup 2022: ~59:47 effective, ~11:36 stoppage (10:11 per FIFA)
- Change: +4:06 effective, +4:18 stoppage -> 95% ratio!
- The World Cup achieved MUCH higher efficiency than domestic leagues
- Possible explanation: higher stakes, more intense refereeing, FIFA directive was new

### 6. Reversion in 2024-25 and 2025-26
- After the spike in 2023-24, PL effective time dropped to 56:59 in 2024-25
- Further dropped to 55:00 in 2025-26 (after 70 matches)
- This suggests the directive's effect was TRANSIENT
- Teams and referees adapted: referees backed off on extreme stoppage, teams
  recalibrated time-wasting
- This reversion pattern is crucial for the paper's diff-in-diff design

## Data Sources

### Primary: ESPN/Opta (Best for paper)
- Source: espn.com/soccer/story/_/id/38861516
- Coverage: Pre-VAR, VAR era, 2020-23 avg, 2023-24 for all big 5 leagues
- Includes both ball-in-play AND stoppage time
- **This is the gold standard dataset for the paper**

### Secondary: Premier League Official
- Source: premierleague.com/news/3860720
- Coverage: 2020-21 through 2023-24 (partial)
- Also includes goals/game and avg match time
- Very clean official data

### Tertiary: CIES Football Observatory
- Multiple reports: WP242, WP272, WP368, MR64
- Coverage: 35-37 European leagues
- Reports effective time as PERCENTAGE (not minutes)
- Different methodology (InStat/impect data, not Opta)
- Useful for cross-league comparisons but DIFFERENT NUMBERS than Opta
- Numbers are systematically higher than Opta (e.g., CIES reports ~61% for big 5,
  while Opta/ESPN shows ~55-58 minutes out of ~97-102 = 54-57%)

### Additional Sources
- getgoalsideanalytics.com/stop-the-clock/ - Historical overview
- soccermetrics.net - 2018 World Cup match-level data
- football-italia.net - Since 2018-19 averages
- theanalyst.com - Season-by-season Opta data for PL

## Data Quality Notes

1. **Methodological differences**: CIES (using InStat/impect) and Opta measure "ball in play"
   slightly differently. CIES tends to produce higher numbers. DO NOT mix CIES and Opta
   in the same regression.

2. **Total match time inconsistency**: PL official site reports 96-101 min avg match time;
   ESPN data implies similar. The "90 minute" nominal match is never actually 90 minutes.

3. **Partial season data**: The 2023-24 PL official data was from 203/380 matches. Full
   season Opta figure (58:11) is slightly different from the partial (58:37).

4. **Pre-2020 gap**: We have limited season-by-season data before 2020-21 for most leagues.
   The CIES WP272 (2018-19) and MR64 (since Jul 2019) provide cross-sectional snapshots.

5. **2025-26 is in-season**: Only 70 matches. May change substantially.

## File Inventory

- `effective_playing_time.csv` - Master file with all collected data points
- `stoppage_and_effective_time_espn.csv` - ESPN/Opta paired data (best for regressions)
- `cies_effective_time.csv` - CIES-specific data with report references
- `premier_league_ball_in_play_history.csv` - PL time series
- `sources.md` - Full source URLs with access dates
