# Data

## `raw/` — Immutable Source Data (795 MB)

Collected from 15 external sources. Never modified after collection.

```
raw/
├── football_data_co_uk/    # Match results, odds, referee (Football-Data.co.uk)
├── fbref/                  # Match stats, shots, events (FBref/StatsBomb)
├── understat/              # Expected goals - xG (Understat)
├── statsbomb/              # World Cup + La Liga event data (StatsBomb Open Data)
├── transfermarkt/          # Player appearances, injuries, values, transfers
├── espn/                   # Stoppage time from ESPN match pages
├── wages/                  # Player wages (Capology + predicted)
├── open_meteo/             # Match-day weather conditions
├── champions_league/       # UCL/UEL/Euro event data
├── attendance/             # Stadium attendance
├── goal_minutes/           # Goal timing from Understat
├── effective_time/         # Ball-in-play time (CIES/ESPN)
├── stoppage_alternative/   # Alternative stoppage sources (FotMob, API-Football)
├── mls/                    # MLS data for placebo tests
└── api_football/           # API-Football stoppage times
```

## Processed Data

All processed data from v1 is archived in `../_v1/data/`.
