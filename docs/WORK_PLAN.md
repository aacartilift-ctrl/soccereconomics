# 907 Work Plan: Data Gap Resolution

**Date**: 2026-03-30
**Status**: Active
**Base branch**: `master`

---

## Overview

15 data gaps identified in the current pipeline. This plan organizes them into
parallelizable work streams, assigns each to the right execution mode
(Mayor-direct, polecat-slung, or acknowledged limitation), and sequences
dependencies.

**Gas Town execution model:**
- **Mayor** (me): coordinates, creates beads, slings work, reviews results
- **Polecats** (907 rig): execute builder/analysis tasks in worktrees via `gt sling`
- **bd**: all issue tracking — no TodoWrite, no markdown TODOs
- **gt nudge**: routine coordination; `gt mail` only for durable handoffs

---

## Work Streams

### Stream A: Score-at-90 and Drama Measures (P0 — Descriptive Foundation)

These feed the descriptive core (Paper Plan Tier 0) and the DiD outcome variables.

#### A1. Derive score-at-90 from shots data
- **Source**: `data/raw/understat/shots_all.csv` (43K goals with minute data)
- **Coverage**: 16,212 matches with understat_id (29% of panel). Big 5 only.
- **Method**: For each match, cumulate home/away goals from shots where
  `result ∈ {Goal, OwnGoal}` and `minute <= 90`. Yields `home_score_90`,
  `away_score_90`, `score_diff_90`, `is_close_at_90` (|diff| <= 1).
- **Where**: New columns in `build_event_summary.py`, merged into match_panel
- **Execution**: `gt sling → 907` polecat. ~30 min task.
- **Limitation**: Only Understat-covered leagues (Big 5 + some). Control leagues
  won't have this. Document as "available for treated leagues only" in paper.

#### A2. Build drama/entropy measure
- **Source**: Same shots data + event_summary time bins
- **Method**: Match-level entropy from goal timing distribution across 15-min bins.
  Also: comeback indicator, lead-change count, goals-in-final-15.
- **Where**: New columns in `build_event_summary.py`
- **Execution**: Bundle with A1 in same polecat task.
- **Paper use**: "Did stoppage time make matches more dramatic?" — descriptive
  section question.

#### A3. Reconcile compliance definitions (78.6% vs 96.9%)
- **Issue**: Two valid but different compliance measures exist in the analysis.
  78.6% = individual match-level adoption (post > pre for each match).
  96.9% = period-average comparison with >=20 match threshold.
- **Action**: Not a code fix — a paper clarity task. Both numbers are correct.
  The paper must define each clearly and explain why they differ.
- **Execution**: Mayor notes this for paper-writing phase. Create a bead tagged
  `paper` as a reminder, not a code task.

---

### Stream B: Restart Duration & Effective Time (P0 — Mechanism Analysis)

These are the "what changed on the pitch" variables — critical for mechanism
decomposition (Paper Plan Section V).

#### B1. Bring restart_duration forward from old L2 layer
- **Source**: `_v1/data/layers/layer2_events.csv` — 1.35M events, 998K from
  StatsBomb with 99.9% restart_duration coverage.
- **Method**: Port the algorithm from `_v1/src/builders/build_layer2.py` (lines
  427-452). Aggregate per match: `mean_restart_duration`, `median_restart_duration`,
  `total_dead_ball_time`, `restart_count`, `restarts_2h`, `restarts_stoppage`.
- **Where**: New builder `build_restart_summary.py` → `data/processed/restart_summary.csv`
- **Merge**: Join to match_panel on match ID crosswalk
- **Coverage**: ~4,000 StatsBomb matches (EPL + select others). Small but
  high-quality. Enough for mechanism analysis.
- **Execution**: `gt sling → 907` polecat. ~1 hour task.

#### B2. Effective time as league-level context (not match-level)
- **Source**: 3 files in `data/raw/effective_time/`:
  - `effective_playing_time.csv` (36 rows, league × season)
  - `cies_effective_time.csv` (35 rows, league × season_period)
  - `stoppage_and_effective_time_espn.csv` (20 rows, league × period)
- **Limitation**: These are aggregate statistics (league-season averages), not
  match-level. Only ~90 total observations across all sources.
- **Action**: Merge into a single `effective_time_context.csv` for use as
  league-level descriptive stats in the paper. NOT a match-level variable.
- **Paper use**: "Ball-in-play time in treated leagues averages X minutes vs Y
  in controls." Framing context, not regression input.
- **Execution**: Mayor-direct or small polecat task. 20 min.

---

### Stream C: Substitution & Player-Level Fixes (P1)

#### C1. Address TM substitution minute cap at 89
- **Current state**: Transfermarkt caps `sub_on_minute` at 89 for all
  substitutions made after the 89th minute. Cannot distinguish 89th-minute subs
  from 95th-minute subs.
- **Implication**: Regular-time substitution patterns (minutes 1-85) are fully
  analyzable. Stoppage-time substitution timing is NOT.
- **Action**:
  - Add `sub_is_capped = (sub_on_minute >= 89)` flag to substitution panel
  - Analysis can study: "Did managers make more subs total?" and "Did the timing
    of regular-time subs shift?" — but NOT "Did subs happen later in stoppage?"
  - Document limitation clearly in paper
- **Execution**: Small edit to `build_substitution_panel.py`. Polecat task. 15 min.

#### C2. Build substitution panel (existing bead hq-cv-zs2ge)
- **Status**: Already has a ready bead. Sling it.
- **Execution**: `gt sling hq-cv-zs2ge 907`

---

### Stream D: Injury & Player Health (P1)

#### D1. Rebuild injury-match linkage
- **Current state**: `injury_panel.csv` has 5.6 MB of injury data but linkage
  to specific matches (the match where injury occurred) is weak.
- **Source**: TM injury data has `from_date` but not `match_id`. Need to join
  on `player_id + date` proximity to `player_match.csv`.
- **Method**: For each injury, find the closest match the player appeared in
  within ±3 days of `from_date`. Flag confidence level (same-day = high,
  ±1 day = medium, ±3 days = low).
- **Where**: Enhancement to `build_injury_panel.py`
- **Execution**: `gt sling → 907` polecat. 30 min.

#### D2. Injury body region enrichment
- **Current state**: TM provides `injury` text description (e.g., "Knee Injury",
  "Hamstring Injury"). No structured body region field.
- **Method**: Build a lookup table mapping TM injury strings to body regions
  (lower_leg, upper_leg, knee, ankle, head, back, etc.) and injury types
  (muscular, ligament, fracture, concussion).
- **Where**: Static CSV `data/build/injury_classification.csv` + merge in builder
- **Paper use**: "Did extended play increase muscular injuries specifically?"
- **Execution**: Polecat task. 45 min (mostly the classification mapping).

---

### Stream E: Betting & Market Data (P0 — Co-Priority #1)

#### E1. 1H betting line absence — alternative placebo
- **Current state**: We have pre-match and full-time odds. No 1st-half lines.
- **Why it matters**: 1H lines would be the perfect placebo (1H stoppage time
  didn't change, so 1H odds shouldn't respond to the policy).
- **Alternatives**:
  1. **Use 1H goals as placebo outcome** — we HAVE `ht_home_goals`, `ht_away_goals`
     in match_panel. DiD on 1H goals should show null effect. This is actually
     better than 1H odds because it tests the mechanism directly.
  2. **Use 1H stoppage time as placebo treatment** — `stoppage_1h` is in the panel.
     Show it didn't change post-policy (or changed less).
  3. **Betfair 1H lines** — bead `bd_907-yoj` exists but is blocked (requires
     Betfair API access). Park this.
- **Action**: The 1H-goals placebo is implementable now and is arguably stronger
  than odds. Create analysis bead, not data bead.
- **Execution**: Analysis-phase task. Create bead now, execute later.

#### E2. Betting panel quality check
- **Current state**: `betting_panel.csv` at 30.8 MB. Already built.
- **Action**: Verify coverage rates by league and season. Flag thin markets.
- **Execution**: Quick validation. Mayor-direct or polecat.

---

### Stream F: Attendance & Stadium (P2)

#### F1. Attendance gap-fill
- **Current state**: `attendance` column exists in match_panel. Coverage unknown.
  Bead `bd_907-m2i` exists for TM attendance gap-fill.
- **Action**: Check fill rate. If < 80%, sling the existing bead for gap-fill.
- **Execution**: Check first (Mayor), then sling if needed.

---

### Stream G: Minute-Level Fouls/Cards (Acknowledged Limitation)

- **Current state**: FBref provides match-total fouls/cards (in match_panel).
  StatsBomb provides minute-level event data but only for ~266 matches.
- **Implication**: Cannot do minute-level foul analysis at scale. CAN analyze:
  - Match-total fouls/cards as outcome (DiD: did total fouls change?)
  - StatsBomb subset for mechanism illustration (non-causal)
- **Action**: Document limitation. No new data work needed.
- **Execution**: Paper note. Create bead tagged `paper`.

---

### Stream H: VAR Duration (Acknowledged Limitation)

- **Current state**: No match-level VAR review duration data exists publicly.
- **Implication**: Cannot directly measure VAR's contribution to stoppage time.
- **Proxy**: Number of VAR interventions per match (if available from FBref
  match reports). Otherwise, acknowledge and note VAR as a confounder that
  the DiD design handles (affects treated and control similarly).
- **Action**: Check FBref for VAR counts. If not available, document as limitation.
- **Execution**: Quick research task. Mayor-direct.

---

## Execution Sequence

### Phase 1: Create all beads (Mayor, immediate)

```
bd create -t task -p P0 -l "907,data,score-at-90"  "Derive score-at-90 and drama measures from shots data"
bd create -t task -p P0 -l "907,data,restart"       "Port restart_duration from L2 layer into current pipeline"
bd create -t task -p P1 -l "907,data,sub-cap"       "Add sub_is_capped flag and document TM minute cap"
bd create -t task -p P1 -l "907,data,injury"        "Rebuild injury-match linkage and add body region classification"
bd create -t task -p P1 -l "907,data,effective"      "Merge effective time sources into league-level context file"
bd create -t task -p P2 -l "907,paper"               "Document acknowledged limitations: VAR duration, minute-level fouls, compliance definitions"
bd create -t task -p P1 -l "907,analysis"            "1H goals placebo test design"
```

### Phase 2: Parallel polecat dispatch (Mayor, immediate after Phase 1)

Sling up to 4 tasks simultaneously to 907 rig polecats:

| Polecat | Task | Est. Time | Dependencies |
|---------|------|-----------|--------------|
| Polecat 1 | A1+A2: Score-at-90 + drama measures | 45 min | None |
| Polecat 2 | B1: Restart duration from L2 | 1 hour | None |
| Polecat 3 | C1+C2: Sub cap flag + sub panel build | 30 min | None |
| Polecat 4 | D1+D2: Injury linkage + body region | 45 min | None |

```bash
gt sling <score-at-90-bead> 907
gt sling <restart-bead> 907
gt sling <sub-cap-bead> 907        # bundle with hq-cv-zs2ge
gt sling <injury-bead> 907
```

### Phase 3: Mayor-direct tasks (while polecats work)

- B2: Merge effective time files (20 min)
- E2: Betting panel coverage audit (15 min)
- F1: Attendance fill-rate check (10 min)
- H: VAR data availability research (15 min)

### Phase 4: Review and merge (after polecats complete)

- Review each polecat's worktree branch
- Run builders to regenerate processed panels
- Validate row counts and coverage rates
- Merge to master

### Phase 5: Paper documentation beads

- A3: Compliance definition clarity
- G: Minute-level foul limitation
- H: VAR duration limitation
- E1: 1H placebo design note

---

## What's Blocked (Cannot Address Now)

| Gap | Reason | Mitigation |
|-----|--------|------------|
| Betfair 1H lines | Requires API access (bead bd_907-yoj) | Use 1H goals as placebo instead |
| Minute-level fouls at scale | Only StatsBomb has this (~266 matches) | Use match-total fouls; StatsBomb subset for illustration |
| VAR review duration | Data doesn't exist publicly | Acknowledge; DiD design handles it |
| Match-level effective time | Only league-level aggregates exist | Use as context, not regression variable |
| TM sub minutes > 89 | Source caps at 89 | Analyze regular-time patterns; flag cap |

---

## Success Criteria

After all streams complete:

1. **match_panel.csv** gains: `home_score_90`, `away_score_90`, `is_close_at_90`
2. **event_summary.csv** gains: drama/entropy measures, score-at-90 components
3. **New file** `restart_summary.csv`: match-level restart duration stats (~4K matches)
4. **New file** `effective_time_context.csv`: league-level effective time (~90 rows)
5. **substitution_panel.csv** gains: `sub_is_capped` flag
6. **injury_panel.csv** gains: `linked_match_id`, `body_region`, `injury_type`
7. **Documentation**: All acknowledged limitations written up for paper integration
8. **All beads closed** or moved to `deferred` with clear rationale

---

## Scrapers in Flight

Two collectors are still running (started this session):
- **Contract expiry** (PID 1750741): `collect_contract_expiry.py`
- **Manager history** (PID 2069081): `collect_manager_history.py`

When they complete, their output feeds existing beads:
- `hq-cv-6d5eg` (contract expiry)
- `hq-cv-ybxfs` (manager tenure)

These are independent of the data gap work above.
