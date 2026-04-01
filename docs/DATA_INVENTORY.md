# Project 907 — Complete Data Inventory

**Date:** 2026-03-30
**Total raw data:** ~810 MB across 19 source directories
**Total processed data:** ~240 MB across 10 analytical panels
**Total build/intermediate:** ~45 MB across 4 files

---

## Table of Contents

1. [Processed Panels (Analysis-Ready)](#1-processed-panels-analysis-ready)
2. [Build / Intermediate Files](#2-build--intermediate-files)
3. [Raw Data Sources](#3-raw-data-sources)
4. [Coverage Matrix](#4-coverage-matrix)
5. [Known Limitations](#5-known-limitations)

---

## 1. Processed Panels (Analysis-Ready)

All files in `data/processed/`. These are the analysis-ready outputs produced by builders in `src/builders/`.

### 1.1 match_panel.csv — Master Match Panel

**The spine of the project.** One row per match across all 16 leagues and 12 seasons.

| Property | Value |
|----------|-------|
| Rows | 55,488 |
| Columns | 65 |
| Size | 16.7 MB |
| Date range | 2014-07-25 to 2026-05-24 |
| Builder | `build_match_panel.py` |

**Columns (65):**

| Group | Columns |
|-------|---------|
| IDs | `v2_match_id`, `date`, `home_team`, `away_team`, `league_code`, `league_name`, `season`, `season_computed`, `matchweek` |
| Source IDs | `fd_key`, `fbref_id`, `espn_id`, `tm_id`, `understat_id`, `att_key` |
| Outcomes | `home_goals`, `away_goals`, `result`, `ht_home_goals`, `ht_away_goals`, `ht_result` |
| Match stats | `home_shots`, `away_shots`, `home_shots_on_target`, `away_shots_on_target`, `home_fouls`, `away_fouls`, `home_corners`, `away_corners`, `home_yellow`, `away_yellow`, `home_red`, `away_red` |
| Stoppage | `stoppage_1h`, `stoppage_2h`, `stoppage_total` |
| Weather | `temperature_c`, `humidity_pct`, `precipitation_mm`, `wind_speed_kmh` |
| Attendance | `attendance`, `stadium_name`, `stadium_capacity`, `attendance_pct` |
| Goal timing | `goals_1h`, `goals_2h`, `goals_90plus`, `goals_stoppage`, `goals_95plus`, `has_late_goal` |
| Derived | `total_goals`, `goal_diff`, `home_win`, `draw`, `away_win`, `total_fouls`, `total_cards`, `total_shots` |
| Treatment | `post_policy_fifa`, `treated_league`, `post_x_treated`, `league_dose`, `is_covid_season` |
| Quality flags | `is_played`, `has_stoppage` |

**Key fill rates:**

| Column | Fill % | Notes |
|--------|--------|-------|
| home_goals / result | 96.4% | 2,002 unplayed (mostly 2025-26 in progress + COVID cancellations) |
| stoppage_2h | 65.6% | 0% for T1; 99%+ for Big 5 |
| attendance | 39.1% | Geographically biased |
| temperature_c | 49.9% | FBref-matched only |
| goals_1h (Understat) | 29.2% | Only 5 leagues + Championship |

**League distribution:**

| League | Code | Country | Matches | Role |
|--------|------|---------|---------|------|
| La Liga 2 | SP2 | Spain | 5,116 | Never-treated |
| Championship | E1 | England | 5,013 | Never-treated |
| Serie B | I2 | Italy | 4,549 | Never-treated |
| Ligue 2 | F2 | France | 4,086 | Never-treated |
| La Liga | SP1 | Spain | 3,445 | **Treated** |
| Serie A | I1 | Italy | 3,432 | **Treated** |
| Premier League | E0 | England | 3,421 | **Treated** |
| 2. Bundesliga | D2 | Germany | 3,375 | Never-treated |
| Ligue 1 | F1 | France | 3,304 | **Treated** |
| Super Lig | T1 | Turkey | 3,104 | Never-treated |
| Belgian Pro League | B1 | Belgium | 3,060 | Never-treated |
| Eredivisie | N1 | Netherlands | 2,848 | Never-treated |
| Bundesliga | D1 | Germany | 2,771 | **Treated** |
| Primeira Liga | P1 | Portugal | 2,769 | Never-treated |
| Greek Super League | G1 | Greece | 2,736 | Never-treated |
| Scottish Premiership | SC0 | Scotland | 2,459 | Never-treated |

**Treatment balance:** 16,373 treated (29.5%) / 39,115 never-treated (70.5%)

---

### 1.2 betting_panel.csv — Betting Odds and Market Efficiency

One row per match with odds from 15+ bookmakers, implied probabilities, Brier scores, and market efficiency measures.

| Property | Value |
|----------|-------|
| Rows | 56,533 |
| Columns | 124 |
| Size | 29.4 MB |
| Builder | `build_betting_panel.py` |

**Column groups (124 total):**

| Group | Columns | Notes |
|-------|---------|-------|
| IDs | `v2_match_id`, `fd_key`, `date`, `league_code`, `league_name`, `season`, `matchweek` | |
| Outcomes | `home_goals`, `away_goals`, `total_goals`, `home_win`, `draw`, `away_win` | |
| Treatment | `post_policy_fifa`, `treated_league`, `post_x_treated` | |
| 1X2 opening odds | `B365H/D/A`, `PSH/D/A`, `BWH/D/A`, `IWH/D/A`, `WHH/D/A`, `VCH/D/A`, `MaxH/D/A`, `AvgH/D/A` | 8 bookmakers × 3 outcomes |
| 1X2 closing odds | `B365CH/CD/CA`, `PSCH/CD/CA`, `BWCH/CD/CA`, `IWCH/CD/CA`, `WHCH/CD/CA`, `VCCH/CD/CA`, `MaxCH/CD/CA`, `AvgCH/CD/CA` | 8 bookmakers × 3 outcomes |
| Over/under | `B365>2.5`, `B365<2.5`, `P>2.5`, `P<2.5`, `Max>2.5`, `Max<2.5`, `Avg>2.5`, `Avg<2.5` + closing variants | |
| Asian handicap | `AHh`, `B365AHH/AHA`, `PSAHH/AHA` + closing variants | |
| Implied probabilities | `implied_prob_home/draw/away`, `pinnacle_implied_home/draw/away` | |
| Overround | `overround_1x2_b365`, `overround_1x2_pin` | B365 mean: 5.7%, Pinnacle mean: 3.2% |
| Market efficiency | `sharp_retail_spread_home`, `bookmaker_disagreement_1x2/ou`, `n_bookmakers_1x2` | |
| Closing drift | `closing_drift_1x2_home`, `closing_drift_ou_over`, `closing_drift_pin_ou` | |
| Brier scores | `brier_score_home/draw/away`, `brier_1x2`, `brier_pin_1x2`, `brier_ou`, `brier_pin_ou`, `brier_excess`, `cumulative_brier_excess` | |
| Policy timing | `matchweek_since_policy`, `ou_line` | |

**Odds validation:** All odds > 1.0 (min B365H = 1.02). Zero inf overround values.

---

### 1.3 event_summary.csv — Goal Timing and Match Events

One row per match with time-binned goal counts, xG splits, late-goal flags, and FBref intensity stats. Includes own goals (1,284 recovered from shots_all.csv).

| Property | Value |
|----------|-------|
| Rows | 14,441 |
| Columns | 33 |
| Size | 2.1 MB |
| Coverage | 5 Big 5 leagues + Championship (Understat) |
| Builder | `build_event_summary.py` |

**Columns (33):**
`v2_match_id`, `goals_1_15`, `goals_16_30`, `goals_31_45`, `goals_45plus`, `goals_46_60`, `goals_61_75`, `goals_76_84`, `goals_85_89`, `goals_90plus`, `total_goals_event`, `goals_regular_time`, `goals_stoppage_time`, `goals_after_90`, `xg_total`, `xg_regular`, `xg_stoppage`, `pct_goals_stoppage`, `result_changed_in_stoppage`, `late_equalizer`, `late_winner`, `fbref_home_shots`, `fbref_away_shots`, `fbref_home_sot`, `fbref_away_sot`, `fbref_home_fouls`, `fbref_away_fouls`, `fbref_home_corners`, `fbref_away_corners`, `fbref_total_shots`, `fbref_total_fouls`, `fbref_total_cards`, `fbref_total_corners`

**Key stats:**

| Metric | Value |
|--------|-------|
| Avg goals per match | 2.99 (includes own goals) |
| Matches with stoppage goals | 4,895 (33.9%) |
| Result changed in stoppage | 1,183 (8.2%) |
| Late equalizers | 815 |
| Late winners | 1,140 |
| FBref intensity coverage | 14,419 (99.8%) |

---

### 1.4 player_match.csv — Player-Match Appearances

One row per player-match appearance with computed workload variables.

| Property | Value |
|----------|-------|
| Rows | 830,569 |
| Columns | 29 |
| Size | 113.5 MB |
| Date range | 2017-08-04 to 2026-02-21 |
| Unique players | 14,012 |
| Coverage | 9 leagues (TM) |
| Builder | `build_player_match_panel.py` |

**Columns (29):**
`v2_match_id`, `tm_match_id`, `player_id`, `player_name`, `team`, `team_side`, `date`, `league_code`, `league_name`, `season`, `started`, `was_subbed_on`, `was_subbed_off`, `sub_on_minute`, `sub_off_minute`, `goals`, `assists`, `yellow_card`, `red_card`, `minutes_played`, `stoppage_exposure`, `match_number_in_season`, `cumulative_minutes_season`, `days_since_last_match`, `congestion_3_matches`, `stoppage_1h`, `stoppage_2h`, `post_policy_fifa`, `treated_league`

**Key ranges:**

| Column | Min | Max | Mean | Notes |
|--------|-----|-----|------|-------|
| minutes_played | 0 | 120 | 72.5 | Capped at 120 |
| stoppage_exposure | 0 | 27 | 5.5 | Minutes played beyond 90' |
| days_since_last_match | 2 | 90 | 13.4 | Winsorized at 90 |
| congestion_3_matches | 0 | 1 | 0.14 | 3+ matches in 10 days |
| match_number_in_season | 1 | 67 | 19.1 | |

**League distribution:** E1: 138K, I1: 99K, SP1: 98K, E0: 95K, F1: 88K, T1: 88K, D1: 79K, N1: 76K, P1: 70K

---

### 1.5 injury_panel.csv — Player-Season Injury Aggregates

One row per player-season with injury counts, severity, and workload from player_match panel.

| Property | Value |
|----------|-------|
| Rows | 46,913 |
| Columns | 22 |
| Size | 5.4 MB |
| Unique players | 13,274 |
| Seasons | 28 (1998-99 to 2024-25, concentrated 2014+) |
| Builder | `build_injury_panel.py` |

**Columns (22):**
`player_id`, `season`, `player_name`, `date_of_birth`, `nationality`, `position_general`, `position_specific`, `height_cm`, `club`, `league`, `league_code_fd`, `n_injuries`, `n_muscular`, `total_days_absent`, `max_severity_days`, `total_games_missed`, `has_recurrence`, `post_policy`, `treated_league`, `total_minutes`, `total_matches`, `avg_days_between_matches`

**Key stats:**

| Metric | Value |
|--------|-------|
| player_name fill | 99.99% |
| treated_league fill | 100% |
| league_code_fd fill | 49.6% (100% for treated leagues) |
| Avg injuries per player-season | 1.65 |
| Avg days absent | 70.9 |
| Recurrence rate | 14.7% |
| Muscular injury share | ~31% |

---

### 1.6 referee_match.csv — Referee-Match Panel

One row per referee-match assignment with cumulative career stats.

| Property | Value |
|----------|-------|
| Rows | 31,093 |
| Columns | 13 |
| Size | 2.6 MB |
| Unique referees | 485 |
| Leagues | 10 |
| Builder | `build_referee_panel.py` |

**Columns:** `v2_match_id`, `referee_name`, `league`, `season`, `date`, `stoppage_1h`, `stoppage_2h`, `total_fouls`, `total_cards`, `post_policy_fifa`, `treated_league`, `cum_matches`, `cum_avg_stoppage`

**Top referees by matches:** Anthony Taylor (261), Michael Oliver (249), Tim Robinson (245)

---

### 1.7 referee_panel.csv — Referee-Season Aggregates

One row per referee × league × season with pre/post policy stoppage comparison.

| Property | Value |
|----------|-------|
| Rows | 2,398 |
| Columns | 17 |
| Size | 267 KB |
| Builder | `build_referee_panel.py` |

**Columns:** `referee_name`, `league`, `season`, `n_matches`, `avg_stoppage_2h`, `avg_fouls`, `avg_cards`, `pre_policy_avg_stoppage`, `post_policy_avg_stoppage`, `stoppage_change`, `stoppage_change_within`, `complied`, `last_pre_avg`, `first_post_avg`, `n_matches_pre`, `n_matches_post`, `treated_league`

**Key stats:** Compliance rate (treated referees who increased stoppage): 78.6%. Mean stoppage change: +0.46 min.

---

### 1.8 substitution_panel.csv — Match-Level Substitution Summary

One row per match with home/away substitution counts and timing.

| Property | Value |
|----------|-------|
| Rows | 28,151 |
| Columns | 18 |
| Size | 2.3 MB |
| Coverage | 9 leagues (TM) |
| Builder | `build_substitution_panel.py` |

**Columns:** `tm_match_id`, `v2_match_id`, `league_code`, `season`, `n_subs_home`, `first_sub_minute_home`, `last_sub_minute_home`, `mean_sub_minute_home`, `n_starters_completing_90_home`, `n_subs_away`, `first_sub_minute_away`, `last_sub_minute_away`, `mean_sub_minute_away`, `n_starters_completing_90_away`, `subs_after_80`, `subs_after_85`, `subs_after_88`, `n_starters_completing_90`

**Key stats:** Avg subs per match: 7.5 (home 3.77, away 3.78). Avg subs after 85': 0.89. Avg subs after 88' (incl. stoppage): 0.42. Note: TM caps sub_on_minute at 89 for all stoppage-time substitutions.

---

### 1.9 player_substitution_detail.csv — Individual Substitution Records

One row per substitution event (player coming on or going off).

| Property | Value |
|----------|-------|
| Rows | 424,408 |
| Columns | 12 |
| Size | 33.8 MB |
| Unique players | 13,448 |
| Builder | `build_substitution_panel.py` |

**Columns:** `tm_match_id`, `v2_match_id`, `player_id`, `player_name`, `team`, `team_side`, `is_starter`, `sub_on_minute`, `sub_off_minute`, `sub_role`, `sub_minute`, `minutes_played`

---

### 1.10 league_standings.csv — Cumulative League Standings

One row per team × matchweek with cumulative points, position, and relegation zone indicators.

| Property | Value |
|----------|-------|
| Rows | 318,020 |
| Columns | 17 |
| Size | 22.7 MB |
| Leagues | 16 |
| Seasons | 12 |
| Teams | 461 |
| Builder | `build_league_standings.py` |

**Columns:** `league_code`, `season`, `team`, `matchweek`, `cumulative_points`, `cumulative_wins`, `cumulative_draws`, `cumulative_losses`, `cumulative_goals_for`, `cumulative_goals_against`, `goal_difference`, `league_position`, `points_from_top`, `points_from_safety`, `is_relegation_zone`, `matches_played`, `matches_remaining`

---

## 2. Build / Intermediate Files

All files in `data/build/`. These are intermediate outputs used by the builders.

### 2.1 match_id_crosswalk.csv — Master Match ID Crosswalk

Maps match IDs across all 6 source systems. This is the spine that all panels join through.

| Property | Value |
|----------|-------|
| Rows | 56,533 |
| Columns | 13 |
| Size | 7.8 MB |

**Columns:** `v2_match_id`, `date`, `home_team`, `away_team`, `league_code`, `league_name`, `season`, `fd_key`, `fbref_id`, `espn_id`, `tm_id`, `understat_id`, `att_key`

**Source ID fill rates:**

| Source ID | Fill % | Matches | Notes |
|-----------|--------|---------|-------|
| fd_key | 94.6% | 53,488 | Football-data.co.uk |
| espn_id | 90.3% | 51,038 | ESPN stoppage times |
| fbref_id | 50.3% | 28,433 | FBref (9 leagues) |
| tm_id | 52.3% | 29,577 | Transfermarkt (9 leagues) |
| understat_id | 28.7% | 16,212 | Understat (6 leagues) |

### 2.2 all_results_expanded.csv — Expanded Football-Data

All football-data.co.uk results with enrichment columns, 16 leagues, 12 seasons.

| Property | Value |
|----------|-------|
| Rows | 53,490 |
| Columns | 212 |
| Size | 34.2 MB |

Includes all raw football-data columns (outcomes, match stats, 40+ bookmaker odds opening + closing), plus derived columns (`league_code`, `country`, `season_label`, `is_treated`, `league_tier`, implied probabilities).

### 2.3 team_name_map.csv — Cross-Source Team Name Mapping

Maps variant team names from 6 sources to 461 canonical names.

| Property | Value |
|----------|-------|
| Rows | 2,148 |
| Columns | 5 |
| Size | 79.5 KB |

**Columns:** `canonical_name`, `source`, `source_name`, `league_code`, `country`
**Sources:** fd (564), espn (552), attendance (294), tm (294), fbref (291), understat (153)

### 2.4 referee_enrichment.csv — Referee Name Assignments

Maps v2_match_id to referee names from FBref and football-data.co.uk.

| Rows | 31,093 | Unique referees | 485 | Sources | fbref: 28,634, football_data: 2,459 |

---

## 3. Raw Data Sources

All files in `data/raw/`. Organized by source system.

### 3.1 Transfermarkt (`transfermarkt/`) — 101 MB

Player-level data: appearances, injuries, registry, market values, contracts, schedules.

| File | Rows | Cols | Size | Description |
|------|------|------|------|-------------|
| `player_appearances.csv` | 830,569 | 14 | 52 MB | Player lineup data per match: starter flag, sub minutes, goals, assists, cards |
| `player_values.csv` | 331,984 | 6 | 15 MB | Historical market value snapshots: player_id, date, value, club, age |
| `player_values_snapshot.csv` | 288,770 | 6 | 14 MB | Alternative value snapshot |
| `player_registry.csv` | 59,197 | 23 | 9.4 MB | Player master data: DOB, nationality, position, height, club, league, contract |
| `player_injuries.csv` | 77,400 | 7 | 4.2 MB | Injury records: type, dates, days_out, games_missed |
| `match_schedule.csv` | 29,577 | 11 | 4.1 MB | Match schedule with scores and URLs |
| `player_contract_history.csv` | 4,326 | 12 | 409 KB | Contract/transfer records (scraper still running) |
| `tm_referees.csv` | 3,134 | 8 | 228 KB | Referee assignments |
| `transfers.csv` | 1,552 | 7 | 91 KB | Transfer records |
| `squad_values.csv` | 1,588 | 9 | 95 KB | Club squad market values |
| `stadiums.csv` | 175 | 4 | 6.9 KB | Stadium metadata |

**Key columns — player_appearances.csv:**
`tm_match_id`, `player_id`, `player_name`, `team`, `team_side`, `is_starter`, `shirt_number`, `sub_on_minute`, `sub_off_minute`, `sub_type`, `goals`, `assists`, `yellow_card`, `red_card`

**Key columns — player_registry.csv:**
`player_id`, `player_name`, `date_of_birth`, `nationality`, `second_nationality`, `position_general`, `position_specific`, `height_cm`, `preferred_foot`, `club`, `club_tm_id`, `league`, `league_code_tm`, `league_code_fd`, `season`, `season_start_year`, `joined_date`, `signed_from`, `contract_expiry`, `market_value_eur`, `squad_number`, `is_loan`, `loan_parent_club`

**Key columns — player_injuries.csv:**
`player_id`, `season`, `injury_type`, `from_date`, `until_date`, `days_out`, `games_missed`

---

### 3.2 Football-Data.co.uk (`football_data_co_uk/`) — 59 MB

Match results and betting odds. Individual season files per league plus combined/extended files.

**Individual season files:** 164 files, format `{LEAGUE}_{SEASON}.csv` (e.g., `E0_1415.csv`)
- 16 leagues × ~11 seasons each
- 52-139 columns depending on season (more bookmakers in recent years)
- Contains: Date, HomeTeam, AwayTeam, FT/HT goals, result, shots, fouls, corners, cards, Referee, and odds from B365/PS/BW/IW/WH/VC/Max/Avg (opening + closing), O/U, Asian handicap

**Combined files:**

| File | Rows | Description |
|------|------|-------------|
| `all_results_combined.csv` | 28,433 | 9 leagues (original set) |
| `extended_1415_1617_combined.csv` | 9,889 | Gap-fill for 2014-17 |
| Per-league `_results.csv` files | 2,500-4,800 each | Individual league histories |
| Per-league `_extended_1415_1617.csv` files | 900-1,700 each | Gap-fill files |

---

### 3.3 ESPN (`espn/`) — 4.6 MB

Stoppage time data — the primary source for added time measurements.

| File | Rows | Cols | Description |
|------|------|------|-------------|
| `stoppage_times.csv` | 28,419 | 12 | Main file: Big 5 + top leagues |
| `stoppage_times_extended.csv` | 23,680 | 13 | Extended: control/placebo leagues |

**Columns:** `espn_event_id`, `date`, `espn_league`, `league_name`, `season`, `home_team`, `away_team`, `home_goals_ft`, `away_goals_ft`, `added_time_1h`, `added_time_2h`, `added_time_total` (+`extraction_method` in extended)

**Coverage note:** ESPN does not cover T1 (Turkey Super Lig) — 0% stoppage data for that league.

---

### 3.4 FBref (`fbref/`) — 24 MB

Match-level intensity stats, referees, xG, and attendance from Football Reference.

| File | Rows | Cols | Size | Description |
|------|------|------|------|-------------|
| `match_level_intensity.csv` | 28,433 | 23 | 3.6 MB | Shots, fouls, corners, cards per match |
| `misc_stats.csv` | 25,075 | 23 | 2.6 MB | Miscellaneous match statistics |
| `referees.csv` | 28,657 | 7 | 2.1 MB | Referee assignments: date, teams, score, referee, league, season |
| `match_level_xg.csv` | 15,464 | 17 | 2.3 MB | Match-level xG from Understat via FBref |
| `shot_intensity_by_match.csv` | 15,464 | 19 | 2.7 MB | Shot-level intensity metrics |
| `attendance.csv` | 29,595 | 7 | 2.3 MB | Venue attendance records |
| `schedules.csv` | 12,104 | 14 | 1.4 MB | Match schedules |
| `shooting_stats.csv` | 12,100 | 21 | 1.4 MB | Shooting statistics |
| `understat_shot_xg_by_match.csv` | 15,464 | 17 | 2.4 MB | Understat xG by match |
| `team_season_intensity.csv` | 877 | 22 | 179 KB | Team-season level stats |

---

### 3.5 Understat (`understat/`) — 103 MB

Shot-level data and match summaries for Big 5 leagues + Championship.

| File | Rows | Cols | Size | Description |
|------|------|------|------|-------------|
| `shots_all.csv` | 388,948 | 33 | 101 MB | Every shot: minute, result, xG, player, coordinates |
| `matches.csv` | 16,213 | 19 | 2.1 MB | Match summaries with xG |

**shots_all.csv columns:** `id`, `minute`, `result`, `X`, `Y`, `xG`, `player`, `h_a`, `player_id`, `situation`, `season`, `shotType`, `match_id`, `h_team`, `a_team`, `h_goals`, `a_goals`, `date`, `player_assisted`, `lastAction`, `league_code`, `league_name`, `league_season`, `is_goal`, `is_stoppage_time`, `stoppage_half`, `added_minutes`, `home_team`, `away_team`, `xg`, `season_label`, `is_on_target`, `is_blocked`

**Result distribution:** Goal, MissedShots, SavedShot, BlockedShot, OwnGoal (1,284 own goals)

---

### 3.6 Goal Minutes (`goal_minutes/`) — 9.3 MB

Derived from Understat shots. Goal-level and match-level summaries.

| File | Rows | Cols | Size | Description |
|------|------|------|------|-------------|
| `understat_goal_minutes.csv` | 41,832 | 24 | 7.7 MB | One row per goal: minute, scoring side, xG, situation, time bin flags |
| `match_goal_summary.csv` | 16,212 | 19 | 1.7 MB | Match-level: goals by half, stoppage goals, late goal flags |

**Note:** `understat_goal_minutes.csv` excludes own goals (is_goal=0 for OwnGoal). Own goals are added at the builder level from `shots_all.csv`.

---

### 3.7 Attendance (`attendance/`) — 6.0 MB

| File | Rows | Cols | Size | Description |
|------|------|------|------|-------------|
| `attendance_master.csv` | 30,826 | 12 | 3.4 MB | Master: league, season, date, teams, attendance, venue, stadium capacity |
| `fbref_attendance_clean.csv` | 30,826 | 9 | 2.6 MB | Cleaned FBref source |
| `stadium_lookup.csv` | 406 | 4 | 16 KB | Stadium name → capacity mapping |

---

### 3.8 Weather — Open-Meteo (`open_meteo/`) — 1.3 MB

| File | Rows | Cols | Description |
|------|------|------|-------------|
| `match_weather.csv` | 27,683 | 5 | Temperature, humidity, precipitation, wind speed keyed on fbref_id |

---

### 3.9 StatsBomb (`statsbomb/`) — 366 MB

Event-level data from StatsBomb open data. La Liga 2017-21, World Cup 2018/2022, Euros, MLS.

| Dataset | Events | Matches | Stoppage Records |
|---------|--------|---------|------------------|
| La Liga 2017-18 | 136,539 | 37 | 37 |
| La Liga 2018-19 | 131,703 | 35 | 35 |
| La Liga 2019-20 | 129,059 | 34 | 34 |
| La Liga 2020-21 | 139,031 | 36 | 36 |
| World Cup 2018 | 227,850 | 65 | 65 |
| World Cup 2022 | 234,653 | 65 | 65 |
| Euro 2020 | 97,627 | 52 | 26 |
| Euro 2024 | 95,052 | 52 | 26 |
| MLS 2023 | 21,787 | 7 | 7 |
| UCL (14 seasons) | ~50K total | ~28 | ~28 each |

**Stoppage time columns:** `match_id`, `stoppage_time_1h`, `stoppage_time_2h`, `stoppage_time_total`, `h1_last_event_minute`, `h2_last_event_minute`, `injury_stoppage_count`, `competition`

**Combined stoppage file:** `stoppage_time_all.csv` — 267 rows across all competitions.

---

### 3.10 Champions League (`champions_league/`) — 109 MB

UCL/UEL/Euro event data and match files from StatsBomb + GitHub sources. Primarily for validation and cross-tournament comparison, not core analysis.

---

### 3.11 Wages (`wages/`) — 19 MB

| File | Rows | Cols | Size | Description |
|------|------|------|------|-------------|
| `wages_expanded.csv` | 95,680 | 12 | 9.1 MB | Multi-source: player, club, league, season, weekly/annual GBP/EUR |
| `wages_fifa_game.csv` | 41,161 | 10 | 3.6 MB | FIFA game-derived wages |
| `wages_predicted.csv` | 43,476 | 10 | 4.4 MB | Model-predicted wages |
| `wages_capology.csv` | 13,899 | 12 | 1.2 MB | Capology source |
| `wages.csv` | 1,351 | 9 | 98 KB | Small direct collection |

**Coverage warning:** Real wage data is ~2% coverage. FIFA game wages and predicted wages are proxies. **Likely unusable for causal analysis.**

---

### 3.12 FotMob (`fotmob/`) — 6.4 MB

| File | Rows | Cols | Description |
|------|------|------|-------------|
| `matches.csv` | 26,461 | 21 | Match data with added time, goals, cards, subs |
| `events.csv` | 1 | 13 | Header only (collection incomplete) |

---

### 3.13 API-Football (`api_football/`) — 1.1 MB

| File | Rows | Description |
|------|------|-------------|
| `stoppage_times.csv` | 9,966 | Alternative stoppage time source |

---

### 3.14 Effective Time (`effective_time/`) — 36 KB

Small reference files on ball-in-play / effective playing time.

| File | Rows | Description |
|------|------|-------------|
| `effective_playing_time.csv` | 37 | League-level effective time stats |
| `cies_effective_time.csv` | 36 | CIES Football Observatory effective time |
| `premier_league_ball_in_play_history.csv` | 12 | PL historical ball-in-play minutes |
| `stoppage_and_effective_time_espn.csv` | 21 | ESPN-derived stoppage vs effective time |

---

### 3.15 Stoppage Alternative (`stoppage_alternative/`) — 1.4 MB

Cross-validation sources for stoppage time measurements.

| File | Rows | Description |
|------|------|-------------|
| `espn_derived_stoppage.csv` | 3,627 | ESPN-derived stoppage times |
| `fotmob_match_ids.csv` | 5,191 | FotMob match ID mapping |
| `api_football_derived_stoppage.csv` | 88 | API-Football derived |

---

### 3.16 MLS (`mls/`) — 678 KB

| File | Rows | Description |
|------|------|-------------|
| `mls_footballdata.csv` | 5,876 | MLS results (out-of-sample comparison) |

---

### 3.17 Placeholder Directories

- `odds_trajectory/` — Empty (Betfair in-play odds, blocked on human download)
- `fifa_game/` — Empty (FIFA game data, blocked on human download)
- `betfair/` — Empty (Betfair exchange data, blocked on human download)

---

## 4. Coverage Matrix

How each source maps to the 16 leagues:

| League | FD Results | ESPN Stoppage | FBref Stats | TM Players | Understat Shots | Referee | Attendance | Weather |
|--------|-----------|---------------|-------------|------------|-----------------|---------|------------|---------|
| E0 | ✓ | ✓ (99.8%) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SP1 | ✓ | ✓ (99.7%) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| D1 | ✓ | ✓ (98.1%) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| I1 | ✓ | ✓ (99.3%) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F1 | ✓ | ✓ (99.5%) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E1 | ✓ | ✓ (99.2%) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| N1 | ✓ | ✓ (67.3%) | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| P1 | ✓ | ✓ (99.4%) | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| T1 | ✓ | **— (0%)** | ✓ | ✓ | — | ✓ | ✓ | ✓ |
| SP2 | ✓ | ✓ (19.3%) | — | — | — | — | — | — |
| I2 | ✓ | ✓ (57.5%) | — | — | — | — | — | — |
| D2 | ✓ | ✓ (66.1%) | — | — | — | — | — | — |
| F2 | ✓ | ✓ (43.0%) | — | — | — | — | — | — |
| B1 | ✓ | ✓ (51.9%) | — | — | — | — | — | — |
| G1 | ✓ | ✓ (52.0%) | — | — | — | — | — | — |
| SC0 | ✓ | ✓ (40.8%) | — | — | — | ✓ | — | — |

**Pattern:** The Big 5 + Championship + Eredivisie/Portugal have rich multi-source coverage. Second divisions and smaller leagues have football-data results + partial ESPN stoppage only.

---

## 5. Known Limitations

### Data gaps
- **T1 (Turkey):** Zero stoppage time data from ESPN. Cannot be used for stoppage-dependent analyses.
- **Second divisions (SP2, I2, D2, F2):** No FBref, TM, Understat, or referee data. Useful for DiD controls on outcomes and betting, not for player-level or event-level analysis.
- **Wage data:** ~2% real coverage. FIFA game wages and predicted wages are proxies, not suitable for causal inference on wages.
- **Betfair/in-play odds:** Not yet collected (blocked on human download).
- **Attendance:** 39% fill in match_panel. Geographically and seasonally biased.

### Source quirks
- **TM sub_on_minute:** Capped at 89 for all stoppage-time substitutions. Cannot distinguish 89th-minute subs from 95th-minute subs.
- **Understat own goals:** Marked as `is_goal=0`, `result="OwnGoal"`. Excluded from `understat_goal_minutes.csv`; added at builder level from `shots_all.csv`.
- **ESPN stoppage outliers:** Raw data contains errors (e.g., 46 min 1H stoppage). Capped at 15 (1H) / 20 (2H) in builder, set to NaN.
- **Football-data odds:** Some early-season entries have odds = 0 (source error). Nulled at builder level.
- **Season boundaries:** Some leagues start in late July (B1, D2, E1, F2, SC0). Source-provided `season` label is canonical; date-based computation fails at July/August boundary.

### Active data collection (as of 2026-03-30)
- **Contract expiry scraper** — Running (PID 1750741). ~4,326 records so far.
- **Manager history scraper** — Running (PID 2069081). ~455 trainers discovered so far.
