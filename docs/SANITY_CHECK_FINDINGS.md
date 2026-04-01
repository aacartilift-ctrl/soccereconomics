# Sanity Check Findings — 2026-03-31

## Executive Summary

Comprehensive fact-checking and robustness analysis reveals the paper's core
descriptive finding is robust (Big 5 leagues clearly increased stoppage time
more than others), but the causal inference framework has critical weaknesses
that must be addressed before submission to a top-5 journal.

## Critical Findings

### 1. The FIFA Directive Was NOT a Law Change

**Fact**: The intervention was a voluntary FIFA refereeing directive announced
by Pierluigi Collina before the 2022 World Cup, NOT a formal IFAB Law 7 amendment.
- Collina: "We don't need any IFAB intervention"
- FIFA President Infantino: "I don't think there is any coercive measure to be taken"
- UEFA explicitly rejected it for Champions League/Europa League
- IFAB used "should" not "must" at March 2023 AGM

**Implication**: The paper must NOT call this "IFAB Law 7 change." Frame as
"FIFA refereeing directive" with heterogeneous voluntary adoption.

### 2. All Control Leagues Also Increased Stoppage Time

| Group | Mean Increase | Positive/Total |
|-------|--------------|----------------|
| Big 5 (treated) | +1.57 min | 5/5 |
| Controls | +0.89 min | 8/10 |

Scottish Premiership (+1.47) and Belgian Pro League (+1.31) — "controls" —
increased more in percentage terms than La Liga (+1.46) and Serie A (+0.73).

**Implication**: No true "untreated" control group exists. The DiD captures the
differential enforcement intensity, not a binary treatment effect. The within-country
specification is the most credible because it compares leagues with the same
referee pool and regulatory body.

### 3. Dose-Response Was Tautological (FIXED)

The original dose variable was computed as `post_mean - pre_mean` per league —
regressing the outcome on a transformation of itself. **Fixed**: replaced with
Big5 × post-treatment trend interaction (exogenous dose). New beta=0.329, p=0.007.

### 4. Wild Cluster Bootstrap Changes Inference

| Spec | β | p(clustered) | p(WCB) |
|------|---|-------------|--------|
| All controls (15 clusters) | 0.747 | 0.007 | **0.060** |
| Clean controls (7 clusters) | 1.400 | 0.003 | **0.110** |
| Within-country (10 clusters) | 0.845 | 0.018 | **0.044** |

**Primary spec should be within-country** (WCB p=0.044, significant at 5%).
Clean controls spec fails under proper inference (7 clusters too few).

### 5. HonestDiD M̄* = 0.0

The treatment effect is NOT robust to any extrapolation of pre-trends.
Event study coefficients are too imprecisely estimated (large SEs due to
league-level clustering) for the relative magnitudes approach to produce
meaningful bounds.

**Implication**: Must not rely on event study for identification. The paper
should acknowledge this honestly and rely on the within-country comparison
(which has stronger institutional motivation) as the primary specification.

### 6. 2022-23 Is Partially Treated

Within the 2022-23 Big 5 season:
- Before WC end (Dec 18): mean = 5.55 min
- After WC end: mean = 5.82 min (+0.27)

Excluding 2022-23 entirely: β=0.810, p=0.004 (strengthens the result).

### 7. Data Quality Issues

- **Duplicates**: 3,606 flagged rows are ALL legitimate playoff rematches (0 true duplicates)
- **Turkey (T1)**: 3,104 matches with 0% stoppage coverage — dead weight
- **Stoppage cap**: Max=20.0 (only 2 matches at cap — negligible)
- **SP2**: No post-treatment data — exclude from analyses

### 8. Decomposition Results

Gelbach quantity-vs-intensity decomposition:
- **Total goals**: 107% quantity, -7% intensity (pure quantity displacement)
- **Fouls**: 56% quantity, 44% intensity (some behavioral change)
- **Goals 90+**: 8% quantity, 92% intensity (strong behavioral — more attacking in stoppage)
- **Yellow cards**: Intensity-dominated (negative quantity share — behavioral effect)

### 9. Goodman-Bacon Decomposition

- Serie A has **negative** bilateral DiD (-0.14) — drags aggregate estimate down
- Premier League (+1.24) drives most of the overall effect
- Weighted average of 45 2x2 comparisons: 0.697

## Recommended Paper Restructuring

1. **Lead with within-country DiD** as primary specification (WCB-robust)
2. **Frame treatment as continuous enforcement intensity**, not binary
3. **Replace "IFAB Law 7 change" with "FIFA refereeing directive"**
4. **Be honest about HonestDiD**: M̄*=0 means event study alone cannot
   establish causality; the institutional argument (within-country, same
   referees, same federation, different enforcement) carries the identification
5. **Remove or relabel dose-response** — old version was tautological
6. **Exclude 2022-23 as robustness check** (shows results strengthen)
7. **Drop T1 and SP2** from analysis sample (no usable data)
8. **Add Premier League 2024-25 partial reversal** as additional identification
