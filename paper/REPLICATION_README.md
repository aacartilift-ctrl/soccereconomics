# Replication README

## The Economics of Extended Play: How FIFA's Stoppage-Time Directive Reshaped Football

**Authors:** [Authors]
**Journal:** American Economic Review (submission)
**Last updated:** 2026-03-30

---

## 1. Overview

This replication package reproduces all tables, figures, and in-text statistics
reported in the paper. The pipeline has three stages:

1. **Collection** — Download raw data from external sources
2. **Building** — Construct analytical panels from raw data
3. **Analysis** — Run regressions, produce tables and figures

All code is Python. No manual steps are required beyond initial setup and
data acquisition.

---

## 2. Data Sources

| Source | URL | Data Used | Access |
|--------|-----|-----------|--------|
| Football-Data.co.uk | https://www.football-data.co.uk | Match results, betting odds, referees (9 top-flight + 4 second-tier leagues, 2014–2025) | Free download, no registration |
| FBref | https://fbref.com | Match-level statistics, shots, referee assignments | Free, robots.txt rate limits apply |
| Understat | https://understat.com | Expected goals (xG), goal timing by minute | Free, no registration |
| Transfermarkt | https://www.transfermarkt.com | Player appearances, injuries, market values, transfers | Free, scraping requires care |
| ESPN | https://www.espn.com | Stoppage time (inferred from last-event timestamps) | Free API, no key required |
| StatsBomb Open Data | https://github.com/statsbomb/open-data | World Cup & La Liga event data | Free, CC BY 4.0 |
| FotMob | https://www.fotmob.com | Match events, tournament IDs, player/team stats | Partial access (Turnstile-gated as of 2025-03) |
| Open-Meteo | https://open-meteo.com | Match-day weather (temperature, precipitation, wind) | Free API, no key required |
| Capology / predicted | https://www.capology.com | Player wages | Free (partial), some predicted |
| CIES / ESPN | Various | Ball-in-play / effective playing time | Manual collection |
| API-Football | https://www.api-football.com | Alternative stoppage times | API key required (free tier available) |
| FIFA game databases | SoFIFA / Kaggle | Player attribute ratings, wage proxies (FIFA 18–25) | Kaggle: free download; SoFIFA: scraping blocked |
| Stadium attendance | Various league sources | Match-level attendance figures | Manual collection |

**Note on data redistribution:** Raw data from Football-Data.co.uk, FBref,
Transfermarkt, ESPN, and similar sources cannot be redistributed due to
terms of service. Collector scripts in `src/collectors/` automate download
where possible. Some sources require manual acquisition (see Section 5 below).

---

## 3. Software Requirements

### Python

- **Python 3.10+** (developed and tested on Python 3.12)
- Package manager: `pip`

### Required packages

Install all dependencies:

```bash
pip install -r requirements.txt
```

Key dependencies (see `requirements.txt` for exact version pins):

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | ≥ 2.0.0 | Data manipulation |
| numpy | ≥ 1.24.0 | Numerical computing |
| statsmodels | ≥ 0.14.0 | OLS, WLS, robust SEs, formula API |
| linearmodels | ≥ 5.3.0 | Panel data, IV/2SLS, fixed effects |
| scipy | ≥ 1.10.0 | Statistical distributions, optimization |
| matplotlib | ≥ 3.7.0 | Publication-quality figures |
| requests | ≥ 2.28.0 | HTTP requests for data collection |
| beautifulsoup4 | ≥ 4.12.0 | HTML parsing (FIFA game scraping) |
| soccerdata | ≥ 1.8.0 | Football data API wrappers |
| understatapi | ≥ 0.7.0 | Understat xG data |
| statsbombpy | ≥ 1.0.0 | StatsBomb open data |
| lxml | ≥ 4.9.0 | XML/HTML parsing |
| tqdm | ≥ 4.65.0 | Progress bars |
| pyarrow | ≥ 12.0.0 | Fast CSV/Parquet I/O |
| thefuzz | ≥ 0.20.0 | Fuzzy string matching (team names) |
| python-Levenshtein | ≥ 0.21.0 | Fast Levenshtein distance |
| openpyxl | ≥ 3.1.0 | Excel file reading |

### Operating system

Tested on Ubuntu 22.04 (WSL2) and macOS 14. Should work on any POSIX system
with Python 3.10+.

---

## 4. Directory Structure

```
project_root/
├── paper/
│   ├── main.tex                  # Full paper (12 sections + appendices)
│   ├── appendix.tex              # Supplementary appendix
│   ├── references.bib            # Bibliography (72 entries)
│   └── REPLICATION_README.md     # This file
│
├── src/
│   ├── collectors/               # Stage 1: Data download scripts
│   │   ├── collect_extended_data.py
│   │   ├── collect_fifa_game_data.py
│   │   ├── collect_fotmob_events.py
│   │   └── collect_stoppage_espn_extended.py
│   │
│   ├── builders/                 # Stage 2: Panel construction
│   │   ├── build_match_panel.py
│   │   ├── build_betting_panel.py
│   │   ├── build_event_summary.py
│   │   ├── build_player_match_panel.py
│   │   ├── build_injury_panel.py
│   │   ├── build_referee_enrichment.py
│   │   ├── build_referee_panel.py
│   │   └── build_expanded_results.py
│   │
│   ├── analysis/                 # Stage 3: Estimation and output
│   │   ├── a01_first_stage_did.py
│   │   ├── a02_event_study_plot.py
│   │   ├── ...
│   │   └── a15_power.py
│   │
│   ├── build_match_crosswalk.py  # Match ID crosswalk builder
│   └── build_team_name_map.py    # Team name harmonization
│
├── data/
│   ├── raw/                      # Immutable source data (~800 MB)
│   │   ├── football_data_co_uk/  # Match results + odds
│   │   ├── fbref/                # Match stats + referees
│   │   ├── understat/            # xG data
│   │   ├── transfermarkt/        # Players, injuries, values
│   │   ├── espn/                 # Stoppage time
│   │   ├── statsbomb/            # Open event data
│   │   ├── fotmob/               # FotMob match data
│   │   ├── open_meteo/           # Weather data
│   │   ├── wages/                # Wage data
│   │   ├── attendance/           # Stadium attendance
│   │   ├── goal_minutes/         # Goal timing
│   │   ├── effective_time/       # Ball-in-play time
│   │   ├── champions_league/     # European competition data
│   │   ├── stoppage_alternative/ # Alt stoppage sources
│   │   ├── api_football/         # API-Football data
│   │   ├── fifa_game/            # FIFA game databases
│   │   ├── betfair/              # Exchange odds
│   │   ├── odds_trajectory/      # Odds movement data
│   │   └── mls/                  # MLS placebo data
│   │
│   ├── build/                    # Intermediate build artifacts
│   │   ├── match_id_crosswalk.csv
│   │   ├── team_name_map.csv
│   │   ├── all_results_expanded.csv
│   │   └── referee_enrichment.csv
│   │
│   ├── interim/                  # Temporary processing files
│   │
│   └── processed/                # Final analytical panels (~167 MB)
│       ├── match_panel.csv       # 56,534 matches
│       ├── betting_panel.csv     # 55,740 match-odds rows
│       ├── event_summary.csv     # 14,368 match events
│       ├── player_match.csv      # 830,570 player-match appearances
│       ├── injury_panel.csv      # 46,914 player-season injuries
│       ├── referee_match.csv     # 31,094 referee-match rows
│       └── referee_panel.csv     # 2,399 referee-season rows
│
├── output/
│   ├── tables/                   # LaTeX + CSV regression tables
│   │   ├── tab_first_stage.tex
│   │   ├── tab_behavioral.tex
│   │   ├── tab_worker_health.tex
│   │   ├── tab_betting.tex
│   │   ├── tab_descriptive.tex
│   │   ├── tab_balance.tex
│   │   ├── tab_heterogeneity.tex
│   │   ├── tab_robustness.tex
│   │   ├── tab_mechanism.tex
│   │   ├── tab_sensitivity.tex
│   │   ├── tab_welfare.tex
│   │   └── tab_first_stage_summary.tex
│   │
│   ├── figures/                  # Publication figures (PDF + PNG)
│   │   ├── fig1_event_study.*
│   │   ├── fig2_goal_timing.*
│   │   ├── fig3_parallel_trends.*
│   │   ├── fig4_referee_compliance.*
│   │   ├── fig4_spec_curve.*
│   │   ├── fig_heterogeneity_forest.*
│   │   ├── fig_heterogeneity_era.*
│   │   ├── fig_welfare_waterfall.*
│   │   ├── a12_mechanism_waterfall.*
│   │   └── a13_loo_forest.*
│   │
│   └── *.txt, *.csv              # Summary statistics and results
│
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project configuration
└── requirements-lock.txt         # Pinned dependency versions
```

---

## 5. Instructions to Reproduce

### Step 0: Environment setup

```bash
# Clone the repository
git clone <repository-url>
cd 907

# Create virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 1: Data acquisition

Most raw data can be collected via the scripts in `src/collectors/`. Some
sources require manual download.

**Automated collection:**

```bash
# Download football-data.co.uk CSVs (all leagues, all seasons)
python src/collectors/collect_extended_data.py

# Download stoppage time from ESPN (control/placebo leagues)
python src/collectors/collect_stoppage_espn_extended.py

# Download FIFA game player databases (Kaggle fallback)
python src/collectors/collect_fifa_game_data.py

# Download FotMob match data (partially gated)
python src/collectors/collect_fotmob_events.py
```

**Manual acquisition required:**

The following data must be acquired manually and placed in the appropriate
`data/raw/` subdirectory:

- `data/raw/fbref/` — FBref match statistics and referee data (use `soccerdata`
  library or manual download from fbref.com)
- `data/raw/transfermarkt/` — Player appearances, injuries, market values
  (use Transfermarkt scrapers or manual download)
- `data/raw/understat/` — xG data by match (use `understatapi` library)
- `data/raw/open_meteo/` — Weather data (use Open-Meteo API)
- `data/raw/wages/` — Player wage data from Capology
- `data/raw/attendance/` — Stadium attendance figures
- `data/raw/effective_time/` — Ball-in-play time from CIES/ESPN reports

### Step 2: Build crosswalk and team name map

These must be built before the analytical panels:

```bash
python src/build_match_crosswalk.py
python src/build_team_name_map.py
```

**Output:** `data/build/match_id_crosswalk.csv`, `data/build/team_name_map.csv`

### Step 3: Build analytical panels

Run the builder scripts in the following order (each depends on prior outputs):

```bash
# 1. Expand football-data.co.uk results (adds second-tier leagues)
python src/builders/build_expanded_results.py

# 2. Master match panel (core dataset — all downstream analysis reads this)
python src/builders/build_match_panel.py

# 3. Secondary panels (can run in any order after match_panel)
python src/builders/build_betting_panel.py
python src/builders/build_event_summary.py
python src/builders/build_player_match_panel.py
python src/builders/build_referee_enrichment.py
python src/builders/build_referee_panel.py

# 4. Injury panel (requires player_match.csv)
python src/builders/build_injury_panel.py
```

**Output:** Seven CSV files in `data/processed/` (see directory structure above).

### Step 4: Run analysis scripts

Analysis scripts are numbered `a01`–`a15` and should be run in order. Each
script reads from `data/processed/` and writes to `output/`.

```bash
# Core identification and estimation
python src/analysis/a01_first_stage_did.py      # Table 1: First-stage DiD
python src/analysis/a02_event_study_plot.py      # Figure 1: Event study plot
python src/analysis/a03_betting_market.py        # Table 4: Betting markets
python src/analysis/a04_behavioral_margins.py    # Table 2: Goal timing, fouls
python src/analysis/a05_worker_health.py         # Table 3: Injuries, workload
python src/analysis/a06_referee_compliance.py    # Figure 4: Referee compliance
python src/analysis/a07_robustness.py            # Specification curve, placebo

# Tables and figures
python src/analysis/a08_tables.py                # Consolidated LaTeX tables
python src/analysis/a09_figures.py               # Publication figures (PDF+PNG)

# Extensions
python src/analysis/a10_heterogeneity.py         # Heterogeneity by league, era
python src/analysis/a11_descriptive_stats.py     # Summary statistics, balance
python src/analysis/a11_welfare.py               # Welfare analysis
python src/analysis/a12_mechanism.py             # Gelbach decomposition
python src/analysis/a13_sensitivity.py           # Leave-one-out robustness
python src/analysis/a15_power.py                 # Power analysis, MDE
```

### Step 5: Compile the paper

```bash
cd paper/
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Requires a LaTeX distribution with `booktabs`, `threeparttable`, `natbib`,
`graphicx`, and standard AER class files.

---

## 6. Output File Inventory

### Tables (output/tables/)

| File | Paper Location | Description |
|------|---------------|-------------|
| `tab_first_stage.tex` | Table 1 | First-stage DiD: policy → stoppage time |
| `tab_behavioral.tex` | Table 2 | Behavioral margins: goals, fouls, cards |
| `tab_worker_health.tex` | Table 3 | Worker health: injuries, workload |
| `tab_betting.tex` | Table 4 | Betting market efficiency |
| `tab_descriptive.tex` | Table 5 | Summary statistics (3 panels) |
| `tab_balance.tex` | Table 6 | Covariate balance (normalized differences) |
| `tab_first_stage_summary.tex` | Table 7 | Match counts by league-season |
| `tab_heterogeneity.tex` | Table 8 | Treatment heterogeneity |
| `tab_robustness.tex` | Table 9 | Robustness checks |
| `tab_mechanism.tex` | Table 10 | Gelbach mechanism decomposition |
| `tab_sensitivity.tex` | Table 11 | Leave-one-out sensitivity |
| `tab_welfare.tex` | Table 12 | Welfare analysis |

### Figures (output/figures/)

| File | Paper Location | Description |
|------|---------------|-------------|
| `fig1_event_study.pdf` | Figure 1 | Event study: season-by-season treatment effects |
| `fig2_goal_timing.pdf` | Figure 2 | Goal timing distribution shift |
| `fig3_parallel_trends.pdf` | Figure 3 | Parallel trends validation |
| `fig4_referee_compliance.pdf` | Figure 4 | Referee compliance rates |
| `fig4_spec_curve.pdf` | Figure 5 | Specification curve |
| `fig_heterogeneity_forest.pdf` | Figure 6 | Heterogeneity forest plot |
| `fig_heterogeneity_era.pdf` | Figure 7 | Era-specific treatment effects |
| `fig_welfare_waterfall.pdf` | Figure 8 | Welfare decomposition waterfall |
| `a12_mechanism_waterfall.pdf` | Figure 9 | Mechanism decomposition waterfall |
| `a13_loo_forest.pdf` | Figure 10 | Leave-one-out forest plot |

All figures are produced in both PDF (vector, for print) and PNG (300 DPI,
for screen).

### Summary statistics (output/)

Each analysis script also produces a plain-text summary file
(`output/a{NN}_*_summary.txt`) and, where applicable, a CSV of regression
results (`output/a{NN}_*.csv`).

---

## 7. Computational Requirements

| Resource | Requirement |
|----------|------------|
| **Runtime** | ~15–30 minutes total (all stages) on a modern laptop |
| **RAM** | 8 GB minimum; 16 GB recommended (player_match panel is ~830K rows) |
| **Disk** | ~1.5 GB (800 MB raw data + 167 MB processed + outputs) |
| **CPU** | Single-threaded; no GPU required |
| **OS** | Linux, macOS, or Windows (WSL2) |

**Breakdown by stage:**

| Stage | Approximate Time |
|-------|-----------------|
| Collectors (Step 1) | 10–60 min (network-dependent) |
| Builders (Step 3) | 3–5 min |
| Analysis (Step 4) | 5–15 min |
| Paper compilation (Step 5) | < 1 min |

The bottleneck is data collection (network I/O and rate limiting from external
APIs). Once raw data is in place, the build + analysis pipeline completes in
under 20 minutes.

---

## 8. Notes

- **Reproducibility:** All random seeds are fixed where applicable. Results
  may differ at the last decimal place across platforms due to floating-point
  arithmetic differences in NumPy/SciPy.

- **Clustering:** Standard errors are clustered at the league-season level.
  When the number of clusters is fewer than 8, HC1 heteroskedasticity-robust
  standard errors are used as a fallback, with wild cluster bootstrap
  confidence intervals reported for inference.

- **Data vintages:** Web-scraped data (FBref, Transfermarkt, Understat) may
  change over time as sources update historical records. The results in the
  paper were produced from data collected in March 2026.

- **Missing script numbers:** Analysis scripts skip a14 (selection diagnostics
  was merged into other modules). The numbering gaps are intentional and do
  not indicate missing analyses.

---

## Contact

For questions about replication, please contact [corresponding author email].
