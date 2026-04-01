# V2 Data Plan: Audit, Shopping List, and Organization

**Date:** 2026-03-29
**Purpose:** Map what we have → what we need → how to get it → how to organize it

---

## Part 1: What We Have (Raw Data Audit)

### 1.1 Match-Level Outcomes — STRONG

| Source | File | Matches | Leagues | Seasons | Key Columns |
|--------|------|---------|---------|---------|-------------|
| football-data.co.uk | `all_results_combined.csv` | 28,433 | 9 | 2017/18–2025/26 | Date, teams, FT/HT scores, shots, fouls, cards, corners, referee (28% fill) |
| football-data.co.uk | `extended_1415_1617_combined.csv` | 9,888 | 9 | 2014/15–2016/17 | Same schema, extends pre-treatment window |
| football-data.co.uk | B1/G1/SC0 files | ~5,000 | 3 | 2014/15–2024/25 | Belgium, Greece, Scotland — potential placebos |

**Coverage verdict:** 28,433 matches across all 9 target leagues. Full seasons 2017/18–2024/25 plus partial 2025/26. Pre-treatment extension back to 2014/15 available. Match stats (shots, fouls, cards, corners) at 99.9% fill.

### 1.2 Betting/Odds Data — STRONG (with gaps)

All from football-data.co.uk `all_results_combined.csv`:

| Odds Type | Bookmakers Available | Fill Rate | Seasons with Pinnacle O/U |
|-----------|---------------------|-----------|---------------------------|
| 1X2 match result | B365 (99.8%), Pinnacle (98%), BetWay (95%), WH (90%), BetVictor (81%) | Excellent | All seasons |
| 1X2 closing | B365, Pinnacle, WH, BW, IW, VC + Max/Avg | ~76% | All seasons |
| Over/Under 2.5 | B365, Pinnacle, Max, Avg | ~77% | **2019/20 onward only** |
| O/U 2.5 closing | B365, Pinnacle, Max, Avg | ~77% | **2019/20 onward only** |
| Asian handicap | B365, Pinnacle, Max, Avg (line + odds) | ~77% | **2019/20 onward only** |
| AH closing | B365, Pinnacle, Max, Avg | ~77% | **2019/20 onward only** |
| Betfair Exchange | BFE 1X2, O/U, AH | 2024/25 only | N/A |

**Coverage verdict:** Excellent 1X2 odds across all seasons. O/U and AH data starts 2019/20 — gives 3 pre-treatment and 2+ post-treatment seasons for Pinnacle sharp-vs-retail analysis. **No line movement trajectory** (only opening + closing snapshots). **No 1H-specific lines.** **No in-play odds.**

### 1.3 Stoppage Time (Dependent Variable) — ADEQUATE

| Source | Matches | 1H Fill | 2H Fill | Both Filled | Leagues |
|--------|---------|---------|---------|-------------|---------|
| ESPN | 28,419 | 84.6% | 86.2% | 84.3% (23,964) | All 9 |
| API-Football | 9,965 | **0%** | 28.2% | 0% | All 9 (3 seasons only) |
| StatsBomb | 266 | 100% | 100% | 100% | La Liga + World Cups only |

**Coverage verdict:** ESPN is the primary source with ~24,000 usable observations. The 15.6% missing rate is evenly distributed (not treatment-correlated — confirmed in v1 audit). API-Football adds negligible value.

### 1.4 Event-Level Data — WEAK for control leagues

| Source | Events | Matches Covered | Leagues | Key Fields |
|--------|--------|-----------------|---------|------------|
| StatsBomb | ~850K | 266 | La Liga, World Cups | Full event detail with duration, x/y coordinates |
| FBref | — | 28,433 | All 9 | Match-level aggregates only (total fouls, shots, cards) |

**Coverage verdict:** Rich event data for only 266 matches (1% of sample). FBref gives us match-level behavioral aggregates for all matches but NO within-match timing. **Critical gap: no event timing data for control leagues (Championship, Eredivisie, Primeira Liga, Super Lig).**

### 1.5 Player/Injury Data — GOOD

| Source | Records | Coverage | Key Fields |
|--------|---------|----------|------------|
| TM player_appearances | 830,569 | All 9 leagues | Player-match: starter, sub on/off minute, goals, assists, cards |
| TM player_injuries | 77,399 | 13,274 players | Injury date, return date, days absent, type, body region |
| TM player_registry | 59,196 | All 9 leagues | DOB, nationality, position, height, club, market value |
| TM player_values | 332,000 | ~85% | Market value time series |
| TM match_schedule | 29,577 | All 9 leagues | **Has `league_code_fd` — the Rosetta Stone for cross-source joins** |

**Coverage verdict:** Strong. 830K player-match records with minutes played. 77K injuries with type/severity. The `league_code_fd` column enables joining Transfermarkt to football-data.co.uk.

**Quality issue:** 16% of injuries are "unknown injury" type. Injury-to-match linkage requires date-range overlap logic (~65% linkable based on v1 audit).

### 1.6 Context Variables — MIXED

| Variable | Source | Fill Rate | Limitation |
|----------|--------|-----------|------------|
| Weather | open_meteo | 97.4% (27,682/28,433) | Excellent |
| Attendance | attendance_master | 70.5% overall | **Turkey: 1.8% (essentially zero)** |
| xG | Understat | 57% (16,212/28,433) | **Big 5 only** — no control leagues |
| Wages (real) | Capology | ~15% of player-seasons | Noisy; model-predicted wages have 66% MAPE |
| Wages (game) | FIFA/EA FC | ~35% of player-seasons | In-game estimates, not real wages |

### 1.7 Match ID Ecosystem — NO UNIVERSAL KEY

| System | Format | Sources |
|--------|--------|---------|
| FBref hex | `15a912a4adbc` | FBref, open_meteo |
| ESPN numeric | `483695` | ESPN stoppage |
| Transfermarkt numeric | `3421754` | TM appearances, schedule |
| Understat numeric | `7119` | Understat, goal_minutes |
| StatsBomb numeric | `3857254` | StatsBomb events |
| football-data.co.uk | **None** — join on Date+Home+Away | All odds/match data |

**Critical implication:** Every cross-source join requires fuzzy matching on date + team names. TM's `league_code_fd` helps but team name normalization remains the primary engineering challenge.

---

## Part 2: Gap Analysis (Paper Plan vs. Data)

### Section III: Compliance — DATA READY

| Need | Have? | Gap |
|------|-------|-----|
| Pre/post 2H stoppage time | YES — ESPN, 24K matches | None |
| Referee-level compliance rate | PARTIAL — referee name at 28% in combined file | **Need referee from individual league files or FBref** |
| Referee experience/characteristics | YES — FBref referees.csv, 28,656 rows | None |

**Blocking gap:** Referee name is only 28% filled in the combined odds file. Individual football-data league CSVs AND FBref `referees.csv` have much better coverage. Need to merge referee into the master dataset.

### Section IV.A: Quantity vs. Intensity — DATA READY

| Need | Have? | Gap |
|------|-------|-----|
| Goals by time period (regular, stoppage, ET) | YES — goal_minutes, 41,832 goals | None |
| Per-minute rates pre vs. post | YES — can compute from event timing | None |
| Mechanical decomposition | YES — stoppage time + goals by period | None |

### Section IV.B: Behavioral Margins — GAPS EXIST

| Need | Have? | Gap |
|------|-------|-----|
| Substitution timing distribution | YES — TM appearances (sub_on/off_minute) | None |
| Restart duration / time-wasting | **266 matches only** (StatsBomb) | **CRITICAL GAP — need event-level timing for more matches** |
| Goal displacement (85-89 vs 90+) | YES — goal_minutes has minute-level data | None |
| Tactical foul rates | YES — FBref match_level_intensity | None |

**Critical gap:** Restart duration analysis requires within-match event timing. StatsBomb covers 266 matches. Need to expand to at least 5,000-10,000 matches for meaningful regression analysis.

### Section V: Worker Outcomes — DATA READY

| Need | Have? | Gap |
|------|-------|-----|
| Minutes played per match | YES — TM appearances, 830K rows | None |
| Injury rates post-directive | YES — TM injuries, 77K records | None |
| Muscular injury subtype | PARTIAL — 16% "unknown injury" | Moderate |
| Injury severity distribution | YES — days_absent, games_missed | None |
| Workload/congestion measures | YES — computable from appearances | None |

### Section VI: Market Efficiency — GAPS EXIST

| Need | Have? | Gap |
|------|-------|-----|
| O/U line adjustment speed | YES — Pinnacle + B365 O/U from 2019/20 | None for 3 pre + 2 post seasons |
| Bookmaker disagreement (cross-book variance) | YES — Max/Avg + individual books | None |
| Brier score by matchweek | YES — odds + actual outcomes | None |
| Closing-line drift | YES — opening + closing odds available | None |
| Sharp vs. retail (Pinnacle vs B365) | YES — both available | None |
| **1H lines (placebo)** | **NO** | **CRITICAL GAP — need 1H O/U odds** |
| **Line movement trajectory** | **NO** — only opening + closing | **IMPORTANT GAP — need intermediate snapshots** |
| **In-play odds** | **NO** | **Nice-to-have, not essential** |

### Section VII: Welfare — MIXED

| Need | Have? | Gap |
|------|-------|-----|
| Late-match drama/entropy | YES — goal timing data | None |
| Result-changing events in stoppage | YES — goal_minutes | None |
| Attendance effects | PARTIAL — 70.5% overall, 1.8% Turkey | Moderate |
| Club-level value asymmetry | YES — TM squad values | None |
| TV viewership | **NO** | **Nice-to-have, not gettable for free** |

---

## Part 3: Shopping List (Prioritized)

### PRIORITY 1 — 1H Betting Lines (Section VI Placebo) ★★★

**Why:** The paper plan explicitly calls for 1H O/U lines as the main placebo test in Section VI. Without it, we lose the cleanest falsification: the directive shouldn't affect 1H outcomes, so 1H lines should show no adjustment. This should be "prominently featured in main text."

**Sources (ranked by feasibility):**

| Source | Method | Coverage | Effort |
|--------|--------|----------|--------|
| Betfair Exchange Historical | Free account → download 1H O/U markets | 2016+ all leagues | Medium — register, download, parse JSON |
| OddsPortal | Scrape 1H O/U per match | All leagues, 5+ years | High — JS scraping, ~7,600 matches |

**Recommendation:** Betfair Exchange free tier is the best path. Includes 1H Match Odds and 1H O/U markets with 1-minute-interval traded prices. Register at historicdata.betfair.com, download football markets for 2021-22 through 2024-25.

**Dispatch:** 1 polecat, ~4 hours. Download + parse + normalize to match-level 1H odds panel.

### PRIORITY 2 — Event-Level Data for Control Leagues ★★★

**Why:** Section IV.B needs restart duration / behavioral timing analysis. StatsBomb covers only 266 matches (all La Liga / World Cups). The paper needs event timing for control leagues (Championship, Eredivisie, Primeira Liga, Super Lig) to test behavioral differences in treated vs. untreated settings.

**Sources (ranked by feasibility):**

| Source | Method | Coverage | Effort |
|--------|--------|----------|--------|
| FotMob unofficial API | Python `pyfotmob` | All 9 leagues, extensive history | Medium — API calls, ~28K matches |
| Sofascore API | `sofascore_scraper` or `soccerdata` | All 9 leagues | Medium — scraping |
| WhoScored | `soccerdata` WhoScored module | All 9 leagues | High — heavy JS, anti-bot |
| Flashscore | `FlashscoreScraping` | All 9 leagues | High — scraping |

**What to collect per match:** Goal minutes (with stoppage position), card minutes, substitution minutes, foul count by period. Match-level event summary, not full event stream.

**Recommendation:** FotMob API is the most accessible. Collect match event summaries for all 9 leagues × all seasons. Even match-level aggregates by time period (e.g., fouls in 1-45, 45+, 46-90, 90+) would be valuable.

**Dispatch:** 1 polecat for FotMob collector, 1 polecat for Sofascore backup. ~6 hours each.

### PRIORITY 3 — Odds Line Movement / Trajectory ★★☆

**Why:** Section VI asks "how quickly did markets adjust?" The answer requires seeing the *path* of odds movement, not just opening and closing snapshots. With only opening + closing, we can measure *that* adjustment happened but not *when* during the pre-match window.

**Sources:**

| Source | Method | Coverage | Effort |
|--------|--------|----------|--------|
| OddsPortal | OddsHarvester scraper | All leagues, per-bookmaker trajectory | High — ~7,600 match pages, JS rendering |
| Betfair Exchange free tier | Download → parse 1-min intervals | Pre-match + in-play, 2016+ | Medium |

**Recommendation:** Betfair Exchange free tier gives pre-match price trajectories at 1-minute intervals. Combined with the opening/closing snapshots from football-data.co.uk, this gives a complete picture: football-data for bookmaker-level (Pinnacle vs B365) and Betfair for within-match trajectory.

**Dispatch:** Same polecat as Priority 1 (Betfair download covers both). OddsPortal scraping as a separate polecat if Betfair coverage is insufficient.

### PRIORITY 4 — Referee Data Enrichment ★★☆

**Why:** Section III (compliance) needs referee-level analysis. The combined file has only 28% referee fill. Individual league season files have much better coverage.

**Sources:**

| Source | Method | Coverage | Effort |
|--------|--------|----------|--------|
| football-data.co.uk individual files | Already in raw/ — extract referee column | 9 leagues × 8 seasons | Low — scripting only |
| FBref referees.csv | Already in raw/ — 28,656 rows | All leagues | Low — merge on date+teams |
| WorldReferee.com | Scrape referee profiles | Career stats, experience | Medium |

**Recommendation:** We already have the data — just need to extract referee from individual league CSVs (which have better fill than the combined file) and merge with FBref's referee data. No new collection needed.

**Dispatch:** Part of the data rebuild pipeline, not a separate collection task.

### PRIORITY 5 — Expanded Stoppage Time Sources ★★☆

**Why:** ESPN covers 84% of matches. Filling the remaining 16% would strengthen the dependent variable. Also useful for cross-source validation.

**Sources:**

| Source | Method | Coverage | Effort |
|--------|--------|----------|--------|
| Sofascore | Scrape added-time announcement per match | All 9 leagues | Medium |
| FotMob | API — match detail includes added time | All 9 leagues | Medium |
| Flashscore | Scrape — match timeline shows added time | All 9 leagues | Medium |

**Recommendation:** Bundle with Priority 2 (event-level collection). When collecting match events from FotMob/Sofascore, also extract the official added-time figure.

### PRIORITY 6 — Attendance Gap-Fill ★☆☆

**Why:** Section VII welfare analysis uses attendance. Currently 70.5% overall, 1.8% for Turkey.

**Sources:**

| Source | Method | Coverage | Effort |
|--------|--------|----------|--------|
| Transfermarkt match pages | `transfermarkt-datasets` GitHub (pre-scraped, updated weekly) | All leagues | Low |
| FBref | Already in raw/ — attendance.csv, 29,594 rows | All leagues | Low — merge |

**Recommendation:** `transfermarkt-datasets` (https://github.com/dcaribou/transfermarkt-datasets) provides pre-scraped attendance. Download and merge.

### PRIORITY 7 — Wage Data Improvement ★☆☆

**Why:** Paper plan says wages are "likely unusable" at ~2% real coverage. Worth attempting improvement but not blocking.

**Sources:**

| Source | Method | Coverage | Effort |
|--------|--------|----------|--------|
| Capology via FBref | `worldfootballR::fb_squad_wages()` | Big 5 + Turkey, Portugal | Medium — scraping |
| SoFIFA (FIFA game wages) | Scrape or Kaggle download | Near-complete | Low — Kaggle datasets exist |
| Salary Sport | Scrape | Unknown coverage | Medium |

**Recommendation:** Download FIFA game wage data from Kaggle (FIFA 18 through EA FC 25 = seasons 2017/18–2024/25). These are in-game estimates, not real wages, but correlate well with actual wages and provide near-complete coverage. Use as a proxy, clearly documented.

### PRIORITY 8 — Placebo League Data ★☆☆

**Why:** Belgium (B1), Greece (G1), Scotland (SC0) already exist in football-data.co.uk raw files. Could serve as additional never-treated placebos.

**Sources:** Already collected — in `raw/football_data_co_uk/`. Just need to incorporate into the build pipeline.

### NOT PURSUING

| Data | Why Not |
|------|---------|
| TV viewership | Not available for free at match-level. Aggregate stats insufficient. |
| Fan sentiment | No continuous dataset. Twitter/X data access restricted. |
| VAR review timing | Not publicly available anywhere. |
| In-play odds (live during match) | Free sources inadequate. Betfair free tier has no volume data. |
| Ball-in-play time | CIES publishes league aggregates only, not match-level. Opta commercial. |

---

## Part 4: Data Organization (V2 Structure)

### Principles

1. **Raw stays raw** — `data/raw/` is never modified
2. **One canonical processed directory** — no more processed/interim split
3. **Match-level master as the spine** — everything joins to match_id
4. **Clear provenance** — every derived column traceable to source

### Proposed V2 Directory Structure

```
data/
├── raw/                          # Immutable source data (existing 795MB)
│   ├── football_data_co_uk/      # Match results, odds, referee
│   ├── fbref/                    # Match stats, intensity, referee
│   ├── understat/                # xG, shots
│   ├── statsbomb/                # Event-level (La Liga, World Cups)
│   ├── transfermarkt/            # Players, injuries, values, appearances
│   ├── espn/                     # Stoppage times
│   ├── wages/                    # Capology, FIFA game, predicted
│   ├── open_meteo/               # Weather
│   ├── attendance/               # Attendance
│   ├── betfair/                  # NEW — Exchange historical data
│   ├── fotmob/                   # NEW — Match events, stoppage
│   ├── sofascore/                # NEW — Match events (backup)
│   ├── odds_trajectory/          # NEW — OddsPortal line movement
│   ├── fifa_game/                # NEW — SoFIFA wage/attribute data
│   └── [existing: api_football, champions_league, effective_time,
│         goal_minutes, mls, stoppage_alternative]
│
├── processed/                    # All derived datasets
│   ├── match_panel.csv           # THE master spine (~28K rows, ~100 cols)
│   │                             # One row per match. All match-level variables.
│   │                             # Joins: outcomes + stoppage + odds + referee +
│   │                             #        weather + attendance + goal timing
│   │
│   ├── player_match.csv          # Player-match panel (~830K rows)
│   │                             # Minutes, sub timing, workload, congestion
│   │
│   ├── injury_panel.csv          # Player-season injury panel (~50K rows)
│   │                             # Injury counts, types, severity, workload
│   │
│   ├── referee_panel.csv         # Referee-season panel (~500 rows)
│   │                             # Pre/post compliance, stoppage changes
│   │
│   ├── betting_panel.csv         # Match-level betting panel (~28K rows)
│   │                             # All odds, Brier scores, disagreement,
│   │                             # sharp/retail spread, closing drift
│   │                             # Includes 1H lines if available
│   │
│   └── event_summary.csv         # Match-level event timing summary
│                                 # Goals/fouls/cards by time bin
│                                 # Restart duration aggregates (where available)
│
├── build/                        # Intermediate build artifacts
│   ├── team_name_map.csv         # Canonical team name mapping across sources
│   ├── match_id_crosswalk.csv    # Match ID mapping across all source systems
│   └── [per-source intermediates]
│
├── audit/                        # Data quality documentation
│   ├── coverage_report.md        # Fill rates by source × league × season
│   ├── join_diagnostics.md       # Cross-source merge success rates
│   └── variable_dictionary.md    # Column-level documentation
│
└── README.md                     # This structure explained
```

### Key Design Decisions

**1. Fewer, wider panels instead of many layers.**
V1 had 18 separate layer files that needed complex multi-way joins. V2 has 5 analytical panels, each self-contained for its analysis section. The match panel is the master — everything else links via match_id.

**2. Betting gets its own panel.**
Section VI is the #1 analysis priority and has the richest data. A dedicated `betting_panel.csv` with all odds, Brier scores, disagreement measures, and line movement keeps it clean and fast to iterate on.

**3. Event summary, not event stream.**
Instead of storing 1.35M raw events, aggregate to match-level: goals by 5-minute bin, fouls by period, cards by period, restart duration percentiles. This is what the regressions actually consume.

**4. Team name map is infrastructure.**
The biggest engineering challenge is joining across 6+ source systems with different team names. A canonical `team_name_map.csv` solves this once, used everywhere.

### Match ID Strategy

Create a `match_id_crosswalk.csv` with one row per match:

```
v2_match_id | date | home_team_canonical | away_team_canonical | league | season |
fd_key      | fbref_id | espn_id | tm_id | understat_id | statsbomb_id | fotmob_id
```

Every downstream join goes through canonical names. This eliminates the fuzzy-matching-everywhere problem from v1.

---

## Part 5: Collection Dispatch Plan (Gas Town)

### Wave 1: Data Collection (4 parallel polecats)

| Bead | Task | Source | Output | Est. Time |
|------|------|--------|--------|-----------|
| **DC-1** | Betfair Exchange historical download | historicdata.betfair.com | `raw/betfair/` — 1H + 2H O/U markets, Match Odds, 2019-2025 | 4 hrs |
| **DC-2** | FotMob match events collection | FotMob API via `pyfotmob` | `raw/fotmob/` — events for all 9 leagues, all seasons | 6 hrs |
| **DC-3** | FIFA game wage data | Kaggle + SoFIFA | `raw/fifa_game/` — FIFA 18–EA FC 25 player attributes + wages | 2 hrs |
| **DC-4** | Transfermarkt attendance gap-fill | transfermarkt-datasets GitHub | `raw/transfermarkt/attendance_expanded.csv` | 1 hr |

### Wave 2: Data Collection (2 parallel polecats)

| Bead | Task | Source | Output | Est. Time |
|------|------|--------|--------|-----------|
| **DC-5** | OddsPortal line trajectory scraping | OddsHarvester | `raw/odds_trajectory/` — O/U 2.5 trajectory per match, Big 5 leagues, 2021-2025 | 8 hrs |
| **DC-6** | Capology wage scraping via FBref | worldfootballR | `raw/wages/capology_expanded.csv` — wages for all 9 leagues | 4 hrs |

### Wave 3: Data Build (3 parallel polecats)

| Bead | Task | Input | Output | Est. Time |
|------|------|-------|--------|-----------|
| **DB-1** | Team name canonicalization | All raw sources | `build/team_name_map.csv`, `build/match_id_crosswalk.csv` | 3 hrs |
| **DB-2** | Match panel construction | Crosswalk + all match-level sources | `processed/match_panel.csv` | 4 hrs |
| **DB-3** | Betting panel construction | Odds + crosswalk + Betfair + trajectories | `processed/betting_panel.csv` | 4 hrs |

### Wave 4: Remaining Panels (3 parallel polecats)

| Bead | Task | Input | Output | Est. Time |
|------|------|-------|--------|-----------|
| **DB-4** | Player-match panel | TM appearances + match panel | `processed/player_match.csv` | 3 hrs |
| **DB-5** | Injury panel | TM injuries + player registry + match panel | `processed/injury_panel.csv` | 3 hrs |
| **DB-6** | Event summary + referee panel | FotMob events + FBref + ESPN | `processed/event_summary.csv`, `processed/referee_panel.csv` | 4 hrs |

### Wave 5: Validation + Documentation (1 polecat)

| Bead | Task | Est. Time |
|------|------|-----------|
| **DV-1** | Automated validation suite + coverage report + variable dictionary | 3 hrs |

**Total: 13 beads, ~50 polecat-hours, ~15 wall-clock hours at 4-wide parallelism.**

---

## Part 6: Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Betfair free tier insufficient (no volume, gaps) | Medium | Fall back to OddsPortal for 1H lines; use football-data opening/closing as primary |
| FotMob API breaks or rate-limits | Medium | Sofascore backup (DC-2 has backup path) |
| Team name normalization across 6+ sources | High | Dedicate full bead (DB-1) to this; build canonical map before any joins |
| Turkey attendance remains empty | Low | Accept gap; note in paper as limitation |
| Event-level data too sparse for restart duration | Medium | Downgrade IV.B from regression to descriptive; use 266 StatsBomb matches as case study |
| Wage data still unusable after FIFA game + Capology | Low | Drop wage analysis; use market value as proxy (85% coverage) |

---

## Summary: What Changes From V1 to V2

| Dimension | V1 | V2 |
|-----------|----|----|
| Layers | 18 separate CSVs | 5 analytical panels |
| Odds depth | Opening only for O/U | Opening + closing + trajectory + 1H placebo |
| Event coverage | 266 matches (StatsBomb) | 28K+ matches (FotMob event summaries) |
| Wage coverage | ~2% real, 35% FIFA game | ~15% real (Capology) + ~90% FIFA game proxy |
| Attendance | 70.5% | ~85% after TM gap-fill |
| Match ID | Fuzzy join everywhere | Canonical crosswalk |
| Referee | 28% in master | ~95% after FBref + individual file merge |
| Build reproducibility | Partial Makefile | Full DAG with validation |
