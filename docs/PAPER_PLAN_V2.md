# Paper Redesign: The Economics of Extended Play

**Date:** 2026-03-30

---

## Working Title

**"The Economics of Extended Play: Labor, Behavioral, and Welfare Effects of Exogenous Time Expansion in Competitive Environments"**

## Core Thesis

When a regulator exogenously extends the duration of a high-stakes competitive interaction, what happens — to enforcers, to strategic behavior, to workers, to markets, and to welfare? We answer this using FIFA's 2022 directive mandating full restoration of lost match time, observed across professional football matches in 16 European leagues.

Football is the **laboratory**, not the **subject** — but that framing is only earned after the soccer story is airtight. The general economics connections (Pencavel, Roth-Ockenfels, Croxson-Reade) rest entirely on the credibility of the sport-specific analysis. If the descriptive picture of what happened on the pitch is thin or hand-waved, no amount of general framing saves the paper. The best sports-as-lab papers — Garicano et al. (2005), Duggan & Levitt (2002), Price & Wolfers (2010) — lead with the domain-specific story and let the general economics emerge. We follow that model.

**The priority order is therefore:** (1) nail the descriptive first stage — what happened to match time, and what happened in the matches; (2) establish the causal identification is clean; (3) build the analytical layers (compliance, decomposition, behavior, health, markets, welfare); (4) connect to broader economics where the connection is natural, not forced. Sections that genuinely generalize (compliance, quantity vs. intensity, market efficiency) carry the general framing. Sections that don't (worker outcomes, welfare) are honest contributions to sports economics.

---

## Result Hierarchy

### Tier 0: Descriptive Foundation (the soccer story — must come first)

0a. **The first stage** — What happened to stoppage time? Distributions, trends, league heterogeneity, match-state dependence. This is the visual and statistical bedrock. If this isn't compelling, nothing else matters.
0b. **How the game changed** — Goal timing profiles across time bins, foul and card patterns, match outcomes (result changes in added time, home/away asymmetries, competitive balance shifts). Rich descriptive analysis of the on-pitch effects, presented so a reader who follows football finds it credible and a reader who doesn't finds it accessible.

### Tier 1: Airtight (core analytical pillars — must be iron-clad)

1. **Compliance and enforcement** — What share of enforcers complied? How did the mandate transmit through institutional channels?
2. **Quantity vs. intensity decomposition** — How much of any outcome change is attributable to additional time (quantity) vs. changes in per-unit-time rates (intensity)?
3. **Market efficiency for structural regime changes** — How quickly did betting markets incorporate the structural shift? Measured via over/under lines, odds drift, bookmaker disagreement.

### Tier 2: Suggestive extensions (honest about power)

4. **Behavioral adaptation** — Do strategic agents re-optimize when the time horizon expands? Restart duration, substitution timing, goal displacement.
5. **Worker outcomes** — Does the additional playing time affect worker health? Workload increase, injury rates, severity distribution.
6. **Welfare accounting** — Who gained (consumers/entertainment) and who lost (workers, clubs) from the directive? Competitive balance implications.

---

## Paper Structure

**Section ordering follows a show-then-tell structure:** First show what happened (descriptive), then explain why (causal), then trace consequences (analytical). The descriptive sections (III-IV) build the reader's intuition and establish credibility before the analytical sections (V-IX) make causal claims. Markets come after we establish what actually changed, so the reader understands what markets needed to incorporate.

**Writing discipline:** Every section opener must be readable by a QJE referee who does not follow football. No domain jargon in the general framing. Technical football terms appear only in the domain-specific answer, with plain-language equivalents parenthesized on first use. But the soccer-specific detail must be *rich*, not apologetic — this is where the paper earns the reader's trust.

### I. Introduction

**General problem:** Regulators frequently extend the duration of competitive or productive interactions — overtime mandates, extended trading hours, longer tournament formats. Theory makes conflicting predictions. Does more time produce proportionally more output (quantity effect), or does it change how agents behave within that time (intensity effect)? Who bears the costs?

**The experiment:** FIFA's November 2022 directive. Clean policy shock with staggered adoption, minute-level measurement, granular behavioral data, real-time market reactions.

**Contribution:** We trace the complete causal chain — mandate → compliance → output and behavior → worker health → market pricing → welfare — with each link speaking to a distinct economics literature. We are transparent about which links are robust and which are suggestive.

**The Roth-Ockenfels connection (introduce on page 1):** Professional football operates under a soft-close rule — the contest has a nominal end time, but the official adds discretionary extra time. FIFA's directive increased the expected extension. This is structurally related to Roth & Ockenfels (2002, AER), where soft-close auction rules eliminate deadline-driven strategic behavior ("sniping"). But the mapping isn't exact, and that's what makes it interesting: in Roth-Ockenfels, bidders know the extension rule and strategize accordingly. Here, the regime change was unanticipated — agents who built careers under the old equilibrium must *learn* the new one. This is a test of whether the Roth-Ockenfels prediction holds when the soft-close parameters shift mid-stream, which is closer to real-world regulatory changes than the clean mechanism-design setting of their original paper.

**Key citations:**
- Kahn (2000, JEP) — sports as labor market laboratory
- Pencavel (2015, EJ) — nonlinearity of hours-productivity
- Roth & Ockenfels (2002, AER) — deadline effects in competitive settings
- Garicano, Palacios-Huerta & Prendergast (2005, REStat) — referee discretion
- Duflo et al. (2013, QJE) — regulatory compliance
- Croxson & Reade (2014, EJ) — betting market efficiency

### II. Institutional Background & Identification Strategy

**The policy:** FIFA's directive at the 2022 World Cup, formalized for domestic leagues 2022-23. Law 7 (the rule requiring officials to compensate for lost time) already existed; the directive was an *enforcement shift*, not a new rule — a distinction that matters for interpretation.

**League adoption:**

| League | Code | Country | Adoption | Role |
|--------|------|---------|----------|------|
| Premier League | E0 | England | 2023-08-11 | Treated |
| La Liga | SP1 | Spain | 2023-08-11 | Treated |
| Ligue 1 | F1 | France | 2023-08-11 | Treated |
| Bundesliga | D1 | Germany | 2023-08-18 | Treated |
| Serie A | I1 | Italy | 2023-08-19 | Treated |
| Championship | E1 | England | — | Never-treated |
| Eredivisie | N1 | Netherlands | — | Never-treated |
| Primeira Liga | P1 | Portugal | — | Never-treated |
| Super Lig | T1 | Turkey | — | Never-treated |
| La Liga 2 | SP2 | Spain | — | Never-treated |
| Serie B | I2 | Italy | — | Never-treated |
| 2. Bundesliga | D2 | Germany | — | Never-treated |
| Ligue 2 | F2 | France | — | Never-treated |
| Belgian Pro League | B1 | Belgium | — | Never-treated |
| Greek Super League | G1 | Greece | — | Never-treated |
| Scottish Premiership | SC0 | Scotland | — | Never-treated |

**Be honest about what this is:** All 5 treated leagues adopted within an 8-day window (Aug 11-19). This is not staggered adoption in any meaningful sense — it is a simultaneous shock. Calling it "staggered DiD" when a reviewer can see three leagues on the same date and two more within a week invites skepticism. The design is **treated vs. never-treated**, with the 8-day wobble available as a minor robustness check at best. The 11 never-treated leagues (including 2nd divisions of treated countries) provide a rich control group.

**The second-division control group is a strength.** Having the Championship (E1), La Liga 2 (SP2), Serie B (I2), 2. Bundesliga (D2), and Ligue 2 (F2) as never-treated controls within the *same country* as the treated top flights provides a within-country comparison that absorbs country-level confounds. If the Premier League changed but the Championship didn't — in the same country, same season, same football culture — that's powerful.

**Pre-trends:** Must show parallel trends in stoppage time, goals, and fouls for at least 3-4 pre-treatment seasons across treated and never-treated leagues. The paper needs to present event-study plots with confidence intervals for the main outcomes — not just p-value summaries.

**Identification (reordered by actual identification power):**
- **Primary:** Treated vs. never-treated DiD. Five leagues adopted the directive; four did not. This is the cleanest contrast and provides the majority of identification. CS-DiD is the appropriate estimator (handles never-treated controls correctly), but the identifying variation is treated/never-treated, not early/late adoption timing.
- **Co-primary:** Sharp RDD at November 2022 cutoff (the World Cup start, which triggered the enforcement shift globally). This uses the within-league discontinuity at the policy date and does not require cross-league variation. Triangular kernel, IK-optimal bandwidth, with covariate balance tests at the cutoff.
- **Supporting:** Referee-level dose variation. 490 referees with heterogeneous pre-policy enforcement baselines provide continuous dose variation within treated leagues. Requires Anderson-Rubin or CLR weak-instrument-robust inference if first-stage F is below conventional thresholds. This is valuable as a *within-league* identification strategy that does not depend on the treated/never-treated contrast.
- **Robustness only:** Within-treated-group variation from the 8-day adoption window. Too narrow for meaningful identification but reported for completeness.

**Data assets (rebuilt from raw sources):**
- Match-level: 16 leagues, 12 seasons, ~55K matches — outcomes, stoppage time, referee IDs
- Event-level: ~1.35M in-match events (shots, fouls, passes, restarts with timing)
- Player-match: ~831K observations (minutes played, workload, congestion measures)
- Player health/injuries: ~47K player-season records (type, severity, body region, recurrence)
- Betting: odds from 15+ bookmakers across ~57K match-book pairs (pre-match, closing, Asian handicaps, over/under)
- League standings: ~318K team-matchweek observations (points, position, relegation zone)
- Referee: ~490 referees with career-level panel (~31K referee-match records)
- Player economics: market values (~85% coverage), wages (~2% coverage — likely unusable)
- Context: weather (~50%), attendance (~51%), substitution detail (~424K records)

**Honest scope:** Event-level behavioral data covers only ~1% of matches at full granularity. Wage data is likely unusable. Stoppage coverage varies: >99% for Big 5 leagues, 0% for Turkey (T1). The 5 adopting leagues adopted within an 8-day window, limiting true staggered variation.

### III. The First Stage: What Happened to Match Time

**This section is the paper's foundation.** Everything downstream — compliance, decomposition, behavior, health, markets — depends on the reader believing that a real, material change in match duration occurred. This section provides that evidence with forensic descriptive detail.

**Length discipline: Sections III and IV together must be 8-10 pages, not 15.** The phenomenon is visually obvious — the figures do the heavy lifting. Text should frame and interpret, not narrate. A general-interest referee's patience for descriptive preamble before causal claims begin is real and finite. The economics starts in Section V; readers must reach it by page 18-20 at the latest.

**Why this section must be rich, not perfunctory:** A common failure mode in applied micro papers is treating the first stage as a formality — one regression table showing the treatment is significant, then moving on. For this paper, the first stage IS the phenomenon. The shift from ~3 minutes to ~8+ minutes of second-half added time is visible to the naked eye. The descriptive analysis should make the reader *feel* the magnitude of the change before any regression is run. But let the figures carry the weight — don't write around them.

**Analysis plan:**
- **Raw distributions:** Kernel density plots of second-half added time, pre vs. post, separately for treated and never-treated leagues. The visual should be striking — two clearly separated distributions for treated leagues, overlapping distributions for controls.
- **Time trends:** League-by-league time series of mean and median stoppage time, season by season. Show the break point is sharp and clean for treated leagues, absent for controls.
- **Match-state dependence:** Does the increase depend on the score at 90 minutes? Compare stoppage time in tight matches (within 1 goal) vs. blowouts (3+ goal margin). Pre-policy, referees added more time in tight games (discretion). Post-policy, if compliance is uniform, the score-dependence should *decrease* — referees are restoring actual lost time, not exercising discretion based on match excitement.
- **First-half stoppage (placebo):** The directive nominally applies to both halves, but the first half has always had shorter delays (no tactical time-wasting at 0-0). Show that first-half added time increased modestly or not at all — confirming the second-half change is driven by actual time restoration, not referee over-compensation.
- **Within-match time allocation:** How much of the additional stoppage time is "live ball" (actual play) vs. dead time (restarts, VAR reviews, injury treatment)? If available from event-level data, this decomposition is critical.
- **Heterogeneity across treated leagues:** Did all 5 Big 5 leagues shift by the same amount? Rank leagues by magnitude of change. Any variation here informs the dose-response analysis later.

**Key figures (main text, not appendix):**
- Figure 1: Stoppage time distributions, pre vs. post, treated vs. control (4-panel density plot)
- Figure 2: League-by-league time series of mean 2H stoppage (all 16 leagues on one plot, treated leagues bolded)
- Figure 3: Event-study plot — dynamic DiD coefficients for stoppage time, with pre-trend confidence intervals

**What this section establishes:** The directive produced a large, sharp, persistent increase in second-half playing time in treated leagues, with no corresponding change in control leagues. The effect is not an artifact of referee discretion or match-state selection. The first stage is strong.

### IV. How the Game Changed: On-Pitch Effects

**This section answers the question every football fan asks:** "OK, there's more stoppage time — but did it actually change anything?" Before we decompose into quantity vs. intensity (Section VI), we need to show the reader the raw on-pitch effects. This is the section that makes the paper credible to a sports-literate referee and interesting to a general audience.

**Analysis plan — goals and scoring:**
- **Goal timing profiles:** Plot per-minute scoring rates across 15-minute bins (1-15, 16-30, 31-45, 45+, 46-60, 61-75, 76-84, 85-89, 90+), pre vs. post, for treated and control leagues. The key question: did more goals materialize in added time, and did the timing profile of regular-time goals change?
- **Late goals and match outcomes:** How many more matches now have goals scored after minute 90? What fraction of results were *changed* by added-time goals (draw → win, win → draw)? Compare treated vs. control leagues. This is the "drama dividend" — did the directive produce more exciting finishes?
- **Home vs. away asymmetry:** Does the additional time benefit home or away teams differentially? Theory: home teams may be more likely to score late (crowd energy, referee bias) or away teams may benefit (more time to equalize). Check the data.

**Analysis plan — fouls, cards, and discipline:**
- **Foul rate profiles:** Per-minute foul rates across time bins, pre vs. post. Did tactical fouling (professional fouls to stop counters, time-wasting fouls) change in distribution?
- **Card accumulation:** Yellow and red card rates per match. If more time means more physical contact, cards should increase mechanically. If intensity drops, they might not.
- **Stoppage-time discipline specifically:** Foul and card rates in the 85-89 and 90+ windows. This is where tactical behavior concentrates.

**Analysis plan — match outcomes and competitive balance:**
- **Result distribution:** Did the share of draws change? More time theoretically gives trailing teams more opportunity to equalize, which could increase draws — or increase comebacks, which could decrease them.
- **Points per match by league position:** Did the stoppage-time extension benefit strong teams (deeper squads, can sustain intensity) or weak teams (more time to get lucky)? Compute points-per-match pre vs. post, split by pre-policy league standing tercile.
- **Promotion/relegation margins:** Did the additional randomness from more late goals affect who got promoted or relegated? Counterfactual analysis: which teams would have had different outcomes under pre-policy stoppage norms?

**Analysis plan — substitutions and squad management:**
- **Substitution timing distributions:** When did managers make their substitutions, pre vs. post? If stoppage time is longer, managers might delay substitutions (more time to react) or bring them forward (longer runway for fresh legs to contribute). Plot substitution minute distributions.
- **Late substitutions:** Did the rate of substitutions after minute 85 change? These are often tactical (time-wasting, defensive reinforcement). With more stoppage time, their calculus changes.
- **Squad depth utilization:** Did clubs with deeper squads (measured by roster market value or number of international players) gain more from the directive?

**Key figures (main text):**
- Figure 4: Per-minute goal rates by time bin, treated vs. control, pre vs. post (grouped bar chart)
- Figure 5: Match-level result changes in added time — frequency of result-changing goals, treated vs. control
- Table 1: Summary of on-pitch effects — goals, fouls, cards, results, pre/post × treated/control (the paper's first results table)

**What this section establishes:** The descriptive picture of how football actually changed under the directive. This is not yet causal (that comes in Sections V-VI), but it shows the reader the phenomenon with enough richness that the causal analysis has a clear target. A referee who reads Sections III-IV should already find the paper interesting, even before the economics apparatus kicks in.

### V. Compliance: How Do Local Enforcers Implement Global Mandates?

**General question:** When a central authority issues a directive, how completely and uniformly do heterogeneous local enforcers comply? The regulatory compliance literature (Duflo et al. 2013, 2018) typically documents substantial non-compliance and gaming. Is near-universal compliance achievable, and if so, through what mechanism?

**Analysis plan:**
- Measure the raw pre/post change in second-half added time
- Compute referee-level compliance rate: what share of individual referees increased their stoppage time post-directive?
- Test for heterogeneity: does compliance vary by league, referee experience, or pre-policy enforcement style?
- Map the transmission mechanism: global demonstration event → continental guidance → league adoption → individual enforcer adjustment
- Compare compliance rates to benchmarks in the regulatory compliance literature

**Expected domain-specific answer:** If compliance is high, the finding is that a top-down mandate can achieve broad compliance through an unusual transmission channel (norm-based, demonstration-driven) rather than typical enforcement mechanisms (inspections, fines, audits). The key question then shifts from "how to achieve compliance" to "what are the consequences when compliance succeeds?"

### VI. What Does More Time Produce? Aggregate Output and Behavioral Margins

**This section builds on the descriptive evidence in Sections III-IV** by applying the causal framework. Both sub-questions answer "what does more time produce?" at different resolutions. The aggregate answer asks whether output scales proportionally with time. The margin-level answer asks whether strategic agents re-optimize *within* the extended interaction. The reader has already seen the raw patterns; now we decompose them.

#### VI.A. The Aggregate Answer: Quantity vs. Intensity

**General question:** When the duration of a competitive interaction extends, does output increase proportionally (pure quantity) or does the rate of output change (intensity)?

This is the hours-productivity question (Pencavel 2015) tested at an extreme margin — minutes, not hours, at near-maximal physical intensity. Pencavel's framework predicts concavity: beyond a threshold, more time should yield diminishing returns. Our setting tests whether this holds at very short additional time exposures when intensity is already near-maximal.

**Analysis plan:**
- Mechanical decomposition of all outcome changes into quantity (attributable to additional minutes), intensity (attributable to per-minute rate changes), and interaction terms
- Per-minute rate comparison across all time bins, pre vs. post
- Test whether per-minute rates are statistically different pre vs. post for each outcome (goals, fouls, cards)
- Report the decomposition shares with confidence intervals

**The Pencavel tension (deserves a paragraph):** If we find approximate linearity at the minutes margin, where Pencavel would predict concavity, the natural interpretation is that the concavity in the hours-productivity relationship reflects cumulative fatigue over long shifts. At very short additional margins, fatigue may not accumulate fast enough to bend the curve. This would imply that the threshold for diminishing returns depends not just on intensity but on the *duration* of the additional time.

**The alternative interpretation (must acknowledge):** Athletes may already be at near-maximal fatigue by the nominal end time, and an additional 2-3 minutes may simply be too small a dose to detect the declining slope of the concave function. Under this reading, any linearity finding would be a *power* argument, not evidence that the relationship is truly linear. We cannot distinguish between "the curve is flat here" and "the curve bends but our dose is too small to see it." The paper should state this explicitly.

#### VI.B. The Margins: Partial Re-Optimization by Strategic Agents

**General question:** Even when aggregate output rates are unchanged, do strategic agents re-optimize *when* and *how* they act within the extended interaction? Roth & Ockenfels (2002) predict that extending a soft close reduces deadline-driven strategic behavior ("sniping"). Koszegi & Rabin (2006) predict reference-point updating.

**Analysis plan — substitution timing:**
- Compare the distribution of unplanned personnel changes (substitutions) pre vs. post
- Separately test injury-related substitutions (which proxy for strategic vs. forced decisions)
- Test whether managers re-optimized the *timing* of strategic decisions when the time horizon expanded

**Analysis plan — restart duration (untapped, ~998K observations):**
- Aggregate ~998K in-match events with restart delay measurements to match level
- Compare mean and P95 restart delay pre vs. post
- Roth-Ockenfels prediction: extending the soft close should reduce time-wasting, since teams know more time will be added regardless
- **This is the key new behavioral analysis to run**

**Compressed analyses (one paragraph each in paper):**
- *Goal displacement:* Compare per-minute scoring rates in the 85-89 minute window specifically (not lumped with 76-84). If the "desperation zone" displaced later, the 85-89 rate should fall while the 90+ rate stays constant.
- *Tactical fouls:* Test whether match-level foul rates changed post-directive, with appropriate cluster-robust inference.

**Expected domain-specific answer:** We expect to find either (a) partial re-optimization at the margins consistent with deadline-extension theory, or (b) no behavioral change, consistent with the quantity-dominates interpretation. Either result is informative. Note that Section IV already presents the descriptive substitution and goal-timing patterns; this section tests whether those patterns are causal.

### VII. Worker Outcomes: Health Effects of Additional Playing Time

**This is primarily a sports economics contribution** and benefits from the descriptive groundwork in Section IV (substitution timing, squad depth utilization). The parallel to the medical resident literature (Landrigan et al. 2004; Barger et al. 2005) is worth noting briefly — both study how changes in working time affect worker health — but the analogy should not be oversold. Medical residents work 80-hour weeks and the interventions cut hours by 10-20%. We are studying a short extension to an athletic contest. Calling these the same economic question requires the reader to accept that the hours-health relationship is scale-invariant, which is exactly the thing we would need to prove. The honest framing: this is evidence on *whether* athlete health is sensitive to marginal playing time increases, with a nod to the broader working-time literature for context.

**Analysis plan:**
- Measure the workload increase: did workers play more minutes per contest after the policy?
- Test whether injury rates (particularly muscular injuries, which are plausibly fatigue-related) changed post-directive, using DiD with appropriate multiple hypothesis correction (Romano-Wolf)
- Compare the severity distribution of injuries pre vs. post (KS test, compositional analysis)
- Assess statistical power for the injury specification — if power is below conventional thresholds, state this transparently rather than interpreting null results as evidence of no effect

*(Triple-difference specification details, injury-match linkage rates, and robustness to alternative injury definitions belong in appendix tables, not the main text of a section that may end up flagged as suggestive.)*

**Expected domain-specific answer:** This section will report what we find without pre-committing to a narrative. If injury effects are detected and survive multiple hypothesis correction, that's a meaningful finding about the health cost of marginal time extensions. If not, the honest conclusion is that the data cannot resolve the question at current sample size — not that there is no effect.

### VIII. Market Efficiency: How Do Markets Price Structural Regime Changes?

**General question:** Prediction markets are semi-strong efficient for informational shocks — prices update swiftly after within-event news (Croxson & Reade 2014). But how quickly do they incorporate *structural* regime changes that alter the fundamental parameters of the contest itself? This is a test of market efficiency at a different frequency: not real-time event processing, but recognition that the rules of the game have changed.

**Placement rationale:** This section comes *after* we've established what actually changed (Sections III-VII). The reader now knows the descriptive picture, the compliance story, the causal decomposition, the behavioral margins, and the worker-outcome evidence. The question becomes: did markets understand all this, and how quickly?

**Analysis plan (PRIORITY #1 — largest untapped asset):**
- **Over/under adjustment speed:** Did total-goals lines reflect any mechanical output increase? Week-by-week calibration post-policy.
- **Bookmaker disagreement:** Did odds spread (cross-bookmaker variance) increase during an adjustment period? Elevated disagreement = structural uncertainty.
- **Forecast accuracy:** Brier score by matchweek post-policy. Temporary deterioration = market caught off-guard.
- **Closing-line drift:** Did closing lines move systematically in a consistent direction post-policy? Drift direction reveals learning.
- **Sharp vs. retail segmentation:** Pinnacle (sharp/professional book) vs. Bet365 (retail). Do sophisticated market-makers adjust faster?
- **Placebo:** Did 1st-half lines (unaffected by directive) show any adjustment? They shouldn't.

**Data:** ~98%+ coverage on odds, drift measures, implied probabilities, Brier scores from 15+ bookmakers. This is the paper's second-strongest data asset after the time-expansion variable itself.

**Three possible findings (pre-registered):**
- *Fast adjustment (weeks):* Markets incorporated the structural change within 2-3 matchweeks. Finding: semi-strong efficiency extends to regime changes, not just within-event information. Confirmatory, extends Croxson & Reade to a new domain.
- *Gradual adjustment (6-8 weeks, heterogeneous by sophistication):* Sharp bookmakers adjusted faster than retail. Finding: partial efficiency with heterogeneous adjustment speed by market-maker sophistication. **Probably the most likely scenario and arguably the most interesting** — reveals the microstructure of how structural information propagates through tiered markets.
- *Sluggish adjustment (months):* Markets took a full season to fully calibrate. Finding: a new inefficiency — prediction markets are efficient for informational shocks but slow for structural regime changes. Standalone contribution; Levitt (2004) model of bookmaker inertia predicts exactly this.

**Analytical framework:** The analysis should produce a *continuous* adjustment-speed measure, not just a binary classification. Specifically: estimate the half-life of Brier score excess (how many matchweeks until forecast accuracy returns to pre-policy baseline), separately for sharp and retail books. This handles the middle scenario gracefully.

**The 1H placebo (prominently featured):** If first-half-correlated lines showed no adjustment while second-half-correlated lines did, that's clean evidence of market-specific adjustment rather than a confound affecting all odds simultaneously. This placebo should appear in the main text, not the appendix.

**Risk assessment:** If markets adjusted immediately with no sharp/retail gap, the finding is valid but incremental. If there's heterogeneous adjustment speed, that's genuinely new. **We won't know which paper we have until we run this. It is the #1 analysis priority.**

### IX. Welfare Accounting: Winners and Losers from the Directive

**This is a sports economics section** that synthesizes the preceding results into a welfare map. Any asymmetric incidence across clubs is a competitive balance story specific to football — it should not be dressed up as general product-quality regulation. The broader welfare framing (who gains, who pays) is noted briefly as context.

**Analysis plan:**
- **Consumer/entertainment side:** Synthesize the "drama dividend" evidence from Section IV (late goals, result changes) with attendance effects (acknowledging ~51% coverage limitation) and entropy/uncertainty measures
- **Club/competitive balance side:** Build on the competitive balance analysis from Section IV (points by league-position tercile, promotion/relegation margins). Test whether the directive's effects differ by club wealth/strength. If asymmetric incidence exists, investigate the mechanism (deeper squads, substitution capacity, ability to sustain intensity)
- **Worker side:** Synthesize workload and health findings from Section VII
- **Market side:** Synthesize adjustment-speed findings from Section VIII

**Expected domain-specific answer:** This section reports the welfare map as it emerges from the data. We will map *who gained and who lost* from this specific regulatory change. The general lesson — that the incidence of duration-extending regulation is unlikely to be symmetric — is noted but not oversold.

### X. Conclusion

A paper about what happens when you give people more time in a competitive environment — and who bears the consequences. The framework — mandate → what changed on the pitch → compliance → causal decomposition → worker costs → market pricing → welfare — applies to overtime mandates, extended trading hours, longer tournament formats, and any regulatory intervention that changes the time constraint of a competitive interaction.

But it is also, unapologetically, a paper about football. The general economics emerges from the sport-specific detail, not despite it. The descriptive richness of Sections III-IV is what makes the causal claims in Sections V-IX credible. We report what we find, state what is robust and what is suggestive, and let the data determine the narrative.

---

## Data Strategy

### Phase 1: Data Rebuild (from raw sources)
All analytical datasets will be rebuilt from raw source files. Prior processed datasets exist but will be reconstructed to ensure reproducibility and to incorporate any new data collection.

### Phase 2: New Data Collection (if needed)
- Assess whether additional leagues, seasons, or data sources would strengthen identification
- Assess whether event-level coverage (~1% of matches at full granularity) can be expanded
- Assess whether wage data coverage (~2%) is improvable from alternative sources

### Data Assets Available (as of 2026-03-30)

| Asset | Scale | Coverage | Key limitation |
|-------|-------|----------|----------------|
| Match panel | 55,488 matches | 16 leagues, 12 seasons | Stoppage: 68% of played (0% T1, 99%+ Big 5) |
| In-match events | ~1.35M events | Variable by league | Full granularity for ~1% of matches only |
| Player-match workload | 830,569 obs | 9 leagues (TM) | Stoppage exposure complete where ESPN data exists |
| Player health/injuries | 46,913 player-seasons | All leagues | ~50% league assignment for non-Big-5 |
| Betting panel | 56,533 matches | 16 leagues, 15+ books | Limited in-play data |
| League standings | 318,020 team-matchweeks | 16 leagues | Complete |
| Event summary (goals) | 14,441 matches (Understat) | 5 leagues + Championship | Big 5 only for goal-timing analysis |
| Referee panel | 31,093 referee-match records | 485 referees, 10 leagues | Pre-policy baseline available |
| Substitution detail | 424,408 records | 9 leagues (TM) | TM caps sub minute at 89 (stoppage) |
| Player market values | ~56K player-seasons | ~85% | Noisy (crowd-sourced estimates) |
| Attendance | ~51% of matches | Geographically biased | Incomplete |
| Weather | ~50% of matches | FBref-matched only | Complete where available |

## This Is a Paper, Not a Lab Report

The previous draft had 71 analysis modules, 87 tables, and 69 figures. That's a lab notebook. A paper has an *argument* — a claim about the world that the reader either believes or doesn't by the last page.

**The argument this paper makes:** FIFA's stoppage-time directive produced a large, clean, persistent increase in playing time. This increase changed what happens in football matches — more late goals, more result changes, altered tactical behavior — and these effects were absorbed unevenly across players, clubs, and markets. The paper traces the complete chain from mandate to welfare, grounding every claim in the sport-specific evidence before connecting to broader economics.

Every section, table, figure, and robustness check must serve that argument. If it doesn't advance the reader's understanding of the claim, it doesn't belong in the paper — regardless of how much work it took to produce. But the descriptive sections (III-IV) are not scaffolding to be rushed past — they ARE the core of the paper's credibility.

**Concrete guardrails:**
- Main text: ~45-55 pages, ~10-14 tables, ~8-12 figures (the two new descriptive sections add ~2 tables and ~3-5 figures)
- Appendix: robustness, data construction, supplementary results — as long as needed but clearly subordinate
- Every table/figure must be referenced in the text with a sentence explaining *why the reader should care about it*
- No result is reported without interpretation. "The coefficient is 0.47" is not a finding. "Time expansion increased output by 0.47 units per match, consistent with the quantity-only interpretation" is.
- The descriptive sections (III-IV) should be the most visually rich part of the paper — these are where the reader builds intuition

## Design Is Done — Next Step Is Analysis

This document has reached diminishing returns. Further iteration on architecture defers the work that actually determines the paper's identity.

**Priority ordering for analysis:**

The descriptive sections (III-IV) and the betting market analysis (VIII) run in parallel as co-priorities. The logic: the descriptive first stage is foundational but largely mechanical — we already know stoppage time increased, and the analysis is mostly visualization and summary statistics. It should be fast. The betting analysis is the section whose *outcome we don't know*, and that outcome determines the paper's ceiling. Pushing it behind weeks of descriptive work that we're already confident about is comfort-seeking, not sequencing. Confront the uncertainty early.

1. **[PARALLEL] Descriptive first stage + on-pitch effects (Sections III-IV):** Stoppage-time distributions, event-study plots, goal timing profiles, result changes, foul patterns. Fast to produce, foundational, builds the reader's intuition. If the first stage doesn't look strong, nothing else matters.

1. **[PARALLEL] Market efficiency (Section VIII):** Over/under adjustment speed, Brier scores, bookmaker disagreement, sharp vs. retail segmentation. This is the analysis that determines whether the paper is a ReStat piece or a ReStud piece. We won't know which paper we have until we run it. Start immediately.

2. **Compliance (Section V):** Referee-level compliance rates and heterogeneity. Quick to run with existing referee panel — can proceed in parallel with #1.

3. **Causal decomposition (Section VI):** Quantity vs. intensity, behavioral margins. These build directly on the descriptive evidence from Sections III-IV.

4. **Worker outcomes (Section VII) and welfare (Section IX):** These complete the causal chain but are the sections most likely to be power-limited. Run last, report honestly.
