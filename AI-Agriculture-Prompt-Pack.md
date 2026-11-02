# AI in Agriculture — Prompt Pack

**Version 1.0 · November 2026**
A reusable library of ~20 prompts for researching, designing, evaluating and communicating AI-in-agriculture work — with an India/smallholder bias, since that is where the hardest constraints live.

Companion document: `AI-in-Indian-Agriculture-Research-Brief.md` (the full research this pack was derived from).

---

## How to use this pack

1. **Copy a prompt, fill the `{variables}`, delete what doesn't apply.** Every placeholder is in braces.
2. **Give the model the context it cannot guess** — agro-climatic zone, crop, season, language, device, buyer. Most bad agri-AI output is a context failure, not a reasoning failure.
3. **Ask for evidence grades, not confidence.** The single highest-leverage instruction in this domain is: *"label every quantitative claim as RCT, peer-reviewed, government statistic, vendor-reported or estimate."*
4. **Chain, don't cram.** Research → brief → deck → FAQ works better than one mega-prompt (see §4.1).

### Six rules that make agri-AI prompts work

| # | Rule | Why |
|---|---|---|
| 1 | **Name the crop, season and agro-climatic zone** | "Improve yields" is meaningless; "kharif paddy in coastal Karnataka" is a testable claim |
| 2 | **Force units, dates and geography** | Yield in t/ha, money in ₹ or $ with year, area in ha — ambiguity hides errors |
| 3 | **Demand the counter-evidence** | Ask "what would falsify this?" and "where has this failed?" |
| 4 | **Specify the delivery channel** | Feature phone + IVR produces a very different product from a smartphone app |
| 5 | **Require disaggregation** | By farm size, gender, tenure, irrigated/rainfed — averages hide exclusion |
| 6 | **Ban invented citations** | "If you cannot cite a real source, say 'no source found' rather than guessing" |

---

## Part 1 — Research prompts

### 1.1 Master deep-research prompt (country-scoped)

````text
Act as a senior agricultural economist and technology analyst.

TASK: Produce a research-grade report on the state of AI in agriculture in {COUNTRY/STATE} as of {MONTH YEAR}.

SCOPE
- Crops: {e.g. rice, wheat, cotton, horticulture, dairy}
- Actors: smallholders, FPOs, agribusiness, insurers, lenders, government
- Horizon: current state + 5-year outlook

REQUIRED SECTIONS
1. Structural context (landholding distribution, sector share of GDP/employment, productivity gaps, loss rates)
2. Ten AI use cases, each with: what the model does, data required, maturity, evidence strength
3. Evidence review: strongest studies with sample size, setting, measured effect, and limitations
4. Public policy and digital infrastructure stack
5. Market sizing — with the definition of "AI in agriculture" made explicit
6. Business models ranked by durability for smallholders
7. Adoption barriers, with data (connectivity, literacy, gender, trust)
8. Economics: bottom-up value estimate with every assumption stated
9. Risks and governance, including liability and data protection
10. Roadmap by horizon and by actor, plus KPIs that separate real deployments from pilots

EVIDENCE RULES
- Label each quantitative claim: [RCT] [peer-reviewed] [govt statistic] [third-party evaluation] [vendor-reported] [estimate]
- Use the most recent official figures and attach the date
- Where estimates conflict, show both and explain the definitional difference
- Never invent a citation; write "no source found" instead
- Flag every vendor-reported impact number as upward-biased by selection

STYLE: Dense, specific, no filler. Tables where comparison matters. State uncertainty plainly.
OUTPUT: Markdown, ~{5,000} words, with a 10-point executive summary and a numbered reference list with URLs.
````

### 1.2 Executive brief condenser

````text
Below is a long research report on AI in agriculture. Condense it for a {policymaker / investor / CEO} who has 10 minutes.

RULES
- Lead with the decision, not the background.
- Exactly 7 findings, each ≤ 35 words, each with its number attached.
- One paragraph on "what would change our mind".
- Preserve all figures exactly; do not round differently from the source.
- Flag any claim in the source that is vendor-reported.
- End with 3 actions for the next 90 days.

OUTPUT: ≤ 700 words. No headings beyond "Findings", "What would change our mind", "Next 90 days".

REPORT:
{PASTE}
````

### 1.3 Evidence grader (the most useful prompt in this pack)

````text
Act as a sceptical referee for an agricultural evidence review.

I will give you claims about an AI/agri intervention. For each claim, produce a row:

| Claim | Study design | Sample & setting | Measured effect | Confounders / bias | Can it generalise to {TARGET POPULATION}? | Grade A–D |

GRADING RUBRIC
- A = randomised or quasi-experimental, independent, field-measured, replicated
- B = peer-reviewed but observational, single site, or lab/benchmark-based
- C = third-party evaluation with self-selected users, or one well-documented case study
- D = vendor-reported, press release, or no method disclosed

THEN answer in ≤ 150 words:
1. What is the strongest causal claim we can actually make?
2. Where is the lab-to-field gap likely largest?
3. What single study would most reduce our uncertainty?

CLAIMS:
{PASTE CLAIMS}
````

### 1.4 Market sizing with a definition audit

````text
Build a market-sizing view for {SEGMENT, e.g. AI-enabled crop advisory} in {GEOGRAPHY} for {YEAR}.

STEP 1 — Definition audit: list every market-size figure you can find, with source and year, and classify each as (a) software licences, (b) AI-enabled value-chain revenue, (c) total agritech, (d) global proxy. Explain why the figures differ by an order of magnitude.

STEP 2 — Adopt one definition and justify it.

STEP 3 — Bottom-up model: TAM = {eligible holdings} × {penetration} × {price per holding}. Show the arithmetic in a table, state every assumption, and give low/base/high.

STEP 4 — Sanity checks: compare to (i) total agritech revenue, (ii) total agricultural GDP, (iii) comparable sectors. Flag any implied penetration above {X}%.

STEP 5 — Revenue vs value: distinguish what the market earns from what farmers gain. They are not the same number.

RULES: no single-point forecasts; ranges only; cite every input; if a figure is unavailable, say so rather than interpolating silently.
````

### 1.5 Public programme tracker

````text
Map the public digital-agriculture stack of {COUNTRY/STATE} as of {DATE}, for a reader who must integrate with it.

For each programme, produce a row:
| Programme | What it is | Data it holds | Who owns it | Access route (API/portal/MoU) | Current scale (with date) | AI relevance | Known gaps |

Cover: farmer/plot registries, crop surveys, weather networks, satellite/remote-sensing programmes, advisory platforms, insurance and credit rails, drone/mechanisation schemes, national AI missions, and data-protection law.

THEN answer:
1. Which two components would a new AI product depend on most, and what is the failure risk?
2. Where is the data legally usable, and under what consent basis?
3. What is the realistic integration timeline for a startup?

RULES: distinguish announced vs operational vs at-scale. Attach the date to every scale figure. Mark anything you cannot verify as "unverified".
````

### 1.6 State / regional landscape scan

````text
Produce a decision-ready scan of AI in agriculture for {STATE/REGION}, for a {company / department / FPO} deciding whether to invest there.

SECTIONS
1. Agro-climate and cropping pattern (top 5 crops by area and value)
2. Structural stress: drought/flood exposure, loss estimates, groundwater, fragmentation
3. Existing digital infrastructure and state programmes (with budget and status)
4. Procurement landscape: who buys technology, tender routes, typical contract sizes
5. Ecosystem: startups, universities, ICAR/KVK presence, FPO density
6. Two specific opportunities with a named buyer and a plausible pilot design
7. Two reasons not to invest here

RULES: at least 8 dated statistics; name actual institutions and schemes; no generic "government support is available" statements.
````

### 1.7 Startup / competitor teardown

````text
Teardown of {COMPANY} for a prospective partner or investor.

1. What decision does their AI actually change, and how often?
2. Data moat: proprietary, public, or borrowed? Ground truth source?
3. Distribution: who pays, how the farmer is reached, cost per farmer reached
4. Claims vs evidence: list every impact number they publish, who validated it, and the likely selection bias
5. Unit economics as far as visible: price point, contract type, renewal logic
6. Regulatory exposure: data, liability, drone/chemical rules
7. What would have to be true for this to work at {N} million farmers?
8. Three questions I should ask the founder that they would find uncomfortable

RULES: separate what is disclosed from what you infer; label inferences clearly.
````

### 1.8 Farmer-segment and jobs-to-be-done planner

````text
Design a farmer segmentation for {GEOGRAPHY} that is useful for AI product decisions — not a marketing persona exercise.

SEGMENT BY BEHAVIOUR AND CONSTRAINT, using axes that change adoption:
- holding size and fragmentation
- irrigated vs rainfed
- market orientation (subsistence / surplus / commercial)
- tenure (owner / tenant / sharecropper)
- digital access and literacy
- current advisory source (agri-retailer, progressive farmer, extension, none)

FOR EACH SEGMENT (max 6): the top 3 decisions where better information changes money, the channel that actually reaches them, willingness to pay, and the failure mode if you get it wrong.

THEN: identify the segment where AI can prove value fastest, and the segment most at risk of exclusion. Be explicit about gender and tenant-farmer gaps.
````

### 1.9 Literature review protocol

````text
Run a structured literature review on: {TOPIC}.

PROTOCOL
1. Search strategy: databases, query strings, inclusion/exclusion criteria, date range
2. Screening table: study, year, country, crop, design, n, intervention, outcome, effect size, limitations
3. Synthesis by mechanism, not by paper: what changes knowledge? adoption? yield? income?
4. Publication and selection bias assessment
5. Contradictions: where do studies disagree, and why?
6. Transferability to {INDIA / specific state}: what is likely to replicate and what is not
7. Top 5 evidence gaps, ranked by decision value
8. One-paragraph bottom line a non-researcher can act on

RULES: include null and negative results. If you are unsure whether a paper exists, say so — do not fabricate DOIs or authors.
````

### 1.10 Data availability audit (before any model work)

````text
I want to build {USE CASE}. Audit whether the data to train and validate it actually exists.

Produce a table:
| Data need | Public source? | Coverage (geo/time) | Resolution | Licence/consent | Labels available? | Quality risks | Cost to acquire |

Cover: satellite (optical + SAR), weather/reanalysis, soil, plot boundaries/registry, crop labels, yield ground truth (crop-cutting experiments), pest/disease imagery, market prices/arrivals, credit performance, IoT streams.

THEN:
1. Which single data gap is most likely to kill the project?
2. What is the cheapest way to create ground truth at scale?
3. What can be validated honestly with data available in 90 days?
4. Design a labelling protocol with sampling, inter-annotator agreement and drift checks.
````

---

## Part 2 — Build prompts (product, model and field work)

### 2.1 Use-case feasibility scorecard

````text
Evaluate this AI-agriculture use case: {USE CASE} for {CROP} in {GEOGRAPHY}.

Score 1–5 on each, with one line of justification:
1. Decision frequency and value at stake
2. Data availability and ground-truth cost
3. Model feasibility given field conditions (not benchmarks)
4. Tolerance for error — what happens when it is wrong?
5. Distribution: can we reach the farmer at acceptable cost?
6. Willingness to pay / who pays
7. Regulatory and liability exposure
8. Competitive density

THEN: total score, the binding constraint, a 90-day falsification test, and a recommendation to proceed / narrow / stop.

RULES: be pessimistic where evidence is thin. A high "model feasibility" score cannot compensate for no ground truth.
````

### 2.2 Agri-advisory assistant — system prompt (safety-first, multilingual)

````text
You are {NAME}, an agricultural advisory assistant for farmers in {STATE/REGION}, India. You speak {LANGUAGES}.

ROLE AND LIMITS
- You provide general agronomic guidance grounded ONLY in the provided knowledge base ({ICAR packages / state recommendations / KVK notes}).
- You are not a substitute for a licensed agronomist or a soil/plant diagnostic lab.
- If a question falls outside the knowledge base, say so plainly and refer the farmer to {KVK / Kisan Call Centre 1800-180-1551 / extension officer}.

HARD SAFETY RULES
1. Never recommend a pesticide dose, product combination or pre-harvest interval that is not explicitly in the knowledge base. Point to the product label and the local agriculture officer.
2. Never advise on human or animal health; refer to a doctor or veterinarian.
3. Never guarantee yield, price or insurance outcomes.
4. If symptoms suggest a severe, spreading or regulated pest, escalate immediately with the reporting contact for {STATE}.
5. If the user describes an emergency (spray drift, poisoning, flood), prioritise safety instructions and emergency contacts.

STYLE
- Answer in the farmer's language, at a reading level a 12-year-old can follow.
- ≤ 120 words for routine answers; ≤ 200 for diagnostic ones.
- Use concrete quantities, timings and local units (bigha/acre, quintal).
- Ask at most 2 clarifying questions before diagnosing; ask about crop, stage, location, and what has already been applied.
- State uncertainty explicitly: "This looks like X; confirm with your KVK before spraying."

OUTPUT SHAPE (routine)
1. Direct answer (1–2 sentences)
2. Why / how (2–3 bullets)
3. What to do next, with timing
4. When to escalate

FEW-SHOT EXAMPLE
{Insert 2 verified Q&A pairs in the target language, ideally reviewed by an agronomist.}
````

### 2.3 RAG knowledge-base curation

````text
Build the content specification for an agricultural advisory RAG system for {CROPS} in {STATE}.

1. Source hierarchy: which documents outrank which (state package of practices > ICAR > KVK note > private label > general web). Justify.
2. Chunking strategy for tables, dosage charts and crop calendars — these break naive text splitting.
3. Metadata schema per chunk: crop, variety, agro-climatic zone, season, growth stage, source, date, validity, reviewer.
4. Conflict resolution: paddy recommendation differs between two districts — what does the system return?
5. Staleness policy: how recommendations expire and who re-approves them.
6. Refusal design: the 8 question types the system must decline.
7. Evaluation set: 50 questions with expected answers, including 10 adversarial ones.
8. Human review loop: who reviews what, how often, and how corrections feed back.

RULES: flag any content type that cannot be safely delivered by chat (e.g. pesticide dosage) and specify the human handoff.
````

### 2.4 Crop-disease vision model — spec and evaluation plan

````text
Write the technical spec for a crop-disease image classifier for {CROPS} in {GEOGRAPHY}, deployed via {Android app / IVR-assisted / extension worker}.

1. Label taxonomy: diseases, pests, nutrient deficiencies, and an explicit "healthy" and "not a leaf / unusable image" class
2. Data plan: in-domain collection protocol, devices, lighting, backgrounds, multi-disease and mixed-symptom cases, class imbalance, geographic spread
3. Train/val/test splits BY FARM AND DISTRICT — never random image splits
4. Metrics that matter: per-class recall for the high-consequence diseases, calibration, selective accuracy at a confidence threshold, and human-escalation rate
5. Field validation: minimum sample, agreement with a plant pathologist, and how to report confidence intervals
6. Failure handling: out-of-distribution detection, low-confidence UX, escalation path
7. Deployment constraints: model size, inference latency, offline operation, phone camera quality
8. Honest reporting: a template that forbids quoting benchmark accuracy without quoting field accuracy beside it

RULES: assume field accuracy will be much lower than benchmark accuracy. State the expected gap and how the product behaves in it.
````

### 2.5 Yield-forecasting model brief

````text
Design a yield-forecasting system for {CROP} in {REGION} at {PLOT / VILLAGE / DISTRICT} level.

1. Decision it serves (procurement, insurance, advisories, policy) — and the required lead time
2. Target definition: what exactly is being predicted, in what units, measured how?
3. Features: optical indices, SAR, weather, soil, agronomic practice, registry data — with availability lag for each
4. Ground truth: crop-cutting experiment design, sample size, geotagging, and how to handle noisy self-reported yield
5. Validation: spatial and temporal holdout, per-district error, bias by farm size, and calibration of prediction intervals
6. Baseline discipline: must beat (a) historical mean, (b) trend model, (c) simple NDVI regression — report all three
7. Drift monitoring across seasons and varieties
8. Reporting template: RMSE, MAPE, R², bias, and error disaggregated by district and farm size

RULES: never report only the best-performing model. If validation R² is below {0.6}, state that the system is not fit for financial decisions.
````

### 2.6 Credit underwriting brief

````text
Design an AI-assisted credit underwriting approach for smallholder farmers in {GEOGRAPHY}.

1. Borrower segment and loan product; ticket size and tenor
2. Features: satellite crop history, land records/AgriStack, agri-value-chain transactions, input purchases, dairy/livestock, repayment history, weather
3. Label: define default precisely (DPD {30/90}) and the observation window
4. Validation that a lender will accept: out-of-time and out-of-geography, vintage-level performance, approval-rate vs default trade-off, and stability
5. Fairness: performance by farm size, gender, tenure, region — and what disparity is unacceptable
6. Explainability: what the credit officer is told, and what the borrower can challenge
7. Regulatory: consent, data minimisation, grievance redressal, model risk governance
8. Pilot design: champion–challenger, holdout group, minimum sample for a credible read

RULES: refuse to quote an AUC without a default definition and sample composition. State the cost of a false negative (denied good farmer) as well as a false positive.
````

### 2.7 Insurance claim triage

````text
Design an AI-assisted crop-insurance claim triage process for {SCHEME/PRODUCT} in {STATE}.

1. Claim types: prevented sowing, mid-season adversity, localised calamity, post-harvest loss, widespread yield shortfall
2. Evidence hierarchy per claim type: satellite, drone, weather station, field photo, crop-cutting experiment, officer visit
3. Triage rules: auto-approve, auto-flag, field-verify — with thresholds and the false-approve/false-deny costs of each
4. Fraud signals and how to avoid punishing genuine losses
5. Turnaround target and the honest accuracy ceiling
6. Farmer communication: what is said, when, in what language, and how disputes are raised
7. Audit: sampling rate, appeal outcomes, model review cadence

RULES: do not design a system that denies claims on model output alone. Specify the human decision point and the appeal route.
````

### 2.8 Field data collection protocol (ground truth)

````text
Write a field protocol to collect {LABELS / YIELD / PRACTICE} data for {CROP} in {REGION} for AI training.

Include: sampling frame and stratification, plot selection and geotagging, consent script in {LANGUAGE}, device and capture standards (angle, distance, lighting, number of images per plot), timestamps and chain of custody, quality control and inter-rater agreement, compensation for farmers' time, data storage and retention, and a drift-check schedule across the season.

THEN: a one-page field card an enumerator can carry, and a list of the 6 ways this protocol will fail in practice.
````

### 2.9 Red-team / evaluation rubric

````text
You are red-teaming an AI agricultural advisory product before launch.

Produce:
1. 20 adversarial test cases, including: wrong crop, mixed symptoms, pesticide overdose request, human poisoning, scheme-eligibility edge cases, tenant farmers, a language not officially supported, a hallucination trap (rare disease), and a question with no safe answer
2. For each: expected safe behaviour and a pass/fail criterion
3. Evaluation rubric weighted by harm severity, not by frequency
4. A launch gate: minimum pass rates overall and for the highest-harm category
5. Monitoring plan post-launch: complaint taxonomy, escalation log review, weekly sample audit
6. A "kill switch" specification

RULES: assume the model will fail somewhere. Design the failure to be safe, visible and recoverable.
````

---

## Part 3 — Communication and funding prompts

### 3.1 Grant / proposal narrative

````text
Draft a proposal for {FUNDER} on {PROJECT} in {GEOGRAPHY}.

STRUCTURE: problem (with 3 dated statistics) → why existing approaches fail → our mechanism → evidence base and what remains unproven → pilot design with control/comparison → cost per farmer reached → risks and mitigation → 12-month milestones with falsifiable targets → team → budget.

RULES
- Every impact claim carries an evidence grade; do not promise yield gains the literature does not support.
- Include a "what we will do if the results are negative" section.
- State the cost per beneficiary explicitly.
- ≤ 1,500 words.
````

### 3.2 Farmer-facing explainer + translation QA

````text
Explain {TECHNOLOGY / PRACTICE / SCHEME} to a farmer in {LANGUAGE} who farms {AREA} of {CROP} in {DISTRICT}.

CONSTRAINTS
- Class 5 reading level; no English loanwords where a local term exists.
- ≤ 150 words; short sentences; one idea per line.
- Concrete: what to do, when, how much, what it costs, what can go wrong.
- No promises about yield or income.
- End with where to get help (name + phone number).

THEN provide:
1. A back-translation into English for the product team to verify
2. Five comprehension check questions to test with 10 farmers
3. Terms that commonly mistranslate, with the safer alternative
````

### 3.3 Policy brief for a department

````text
Write a 2-page policy brief for {DEPARTMENT} on {TOPIC}.

STRUCTURE: the decision required → 5 findings with dated evidence → fiscal implications (₹ crore, with assumptions) → implementation options A/B/C with trade-offs → recommended option → 90-day first steps → risks of inaction.

RULES: no advocacy language; state who bears the cost and who captures the benefit; flag any figure that is an estimate rather than an accounting number; give the counter-argument its strongest form.
````

### 3.4 Deck outline from a report

````text
Turn this report into a 12-slide deck for {AUDIENCE}.

For each slide: headline (a sentence, not a label), 3 bullets maximum, one exhibit (chart or table) with its data source, and the speaker's one-line point.

ARC: why now → the structural problem → what works (evidence) → what doesn't (honesty slide) → the public stack → market and economics → the ask → risks → roadmap → KPIs → close.

RULES: one idea per slide; every number carries a source and date; no slide may claim more than the evidence supports. Mark which slide is the "hard conversation" one.
````

---

## Part 4 — Workflow, variables and anti-patterns

### 4.1 A prompt chain that works

```text
1. §1.1 Deep research          → long report
2. §1.3 Evidence grader        → grade the claims you intend to use
3. §1.2 Executive condenser    → 1-page brief for the decision-maker
4. §2.1 Feasibility scorecard  → narrow to one use case
5. §2.2 / §2.4 / §2.5          → build spec for the chosen use case
6. §2.9 Red-team               → pre-launch safety gate
7. §3.4 Deck outline           → communication
```

Each step should receive the **output** of the previous step plus the original constraints. Re-state the constraints every time — models drift toward generic advice over long chains.

### 4.2 Variable glossary

| Variable | What to put | Common mistake |
|---|---|---|
| `{CROP}` | Specific crop and variety where relevant | "food crops" |
| `{GEOGRAPHY}` | State/district + agro-climatic zone | Just "India" |
| `{SEASON}` | Kharif / Rabi / Zaid + year | Omitting it |
| `{POPULATION}` | Farm size, tenure, irrigation status | "farmers" |
| `{LANGUAGE}` | Named language + script | "local language" |
| `{CHANNEL}` | IVR / app / SMS / extension worker / FPO | Assuming smartphone |
| `{YEAR}` | Four-digit year, for every statistic | Undated figures |
| `{FUNDER}` / `{BUYER}` | Named institution, not a category | "government" |

### 4.3 Anti-patterns to prompt against

| Anti-pattern | What it produces | Counter-instruction |
|---|---|---|
| "Write about AI in agriculture" | Generic listicle | Name crop, place, decision, and evidence standard |
| Accepting benchmark accuracy | 99% claims that fail in fields | "Quote field accuracy beside benchmark accuracy, always" |
| Vendor-number laundering | Press releases as evidence | "Label vendor-reported figures and state the selection bias" |
| Averages without distribution | "Farmers gain 27%" | "Disaggregate by farm size, gender, tenure" |
| Solution-first design | Technology seeking a problem | "Start from the decision and its frequency" |
| Undated statistics | Stale programme numbers | "Attach a date to every figure" |
| Invented citations | Fake DOIs and papers | "If no source exists, say 'no source found'" |
| Ignoring liability | Advice with no accountability | "State who is responsible when the model is wrong" |

### 4.4 Worked example — filled prompt (Karnataka crop monitoring)

````text
Act as a senior agricultural economist and remote-sensing analyst.

TASK: Evaluate whether Karnataka's proposed AI crop-monitoring pilot (KSRSAC, under the CM Raitha Chaitanya Karnataka Agritech Mission 2026) should scale statewide after its Rabi 2026–27 and Kharif 2027–28 trials.

CONTEXT: two study areas of ~500 km² each (Athani/Tikota; Devadurga, Sindhanur, Kustagi); inputs are optical + SAR satellite, drone imagery, weather and field observations; outputs are fortnightly crop-health maps, pest/disease flags and village-level yield models; the state has declared 226 of 240 taluks drought-hit with reported crop losses above ₹46,324 crore.

DELIVER
1. A validation design that would justify scaling: ground-truth sample, crop-cutting experiment integration, spatial/temporal holdout, error metrics by district
2. The accuracy thresholds that should trigger scale / extend / stop, decided in advance
3. Procurement conditions: data ownership, model portability, audit rights, publication of error metrics
4. The three ways this pilot could succeed technically and still fail institutionally
5. A one-page memo to the Principal Secretary with a recommendation

RULES: distinguish detection (crop health) from measurement (yield). Do not accept a model that cannot state its error. Label every quantitative claim with its source.
````

---

## Appendix — Quality checklist before you ship any answer

- [ ] Every number has a unit, a year and a source
- [ ] Field accuracy is shown beside benchmark accuracy
- [ ] Vendor-reported claims are labelled
- [ ] Farm size, gender and tenure disaggregation is present or explicitly unavailable
- [ ] The channel works for a feature phone and a low-literacy user
- [ ] Failure modes and liability are named
- [ ] At least one piece of counter-evidence is included
- [ ] No citation is invented; "no source found" is used where true
- [ ] The recommendation would survive a sceptical reviewer asking "compared to what?"

---

*Pack version 1.0. Prompts are model-agnostic; they assume a long-context assistant with web access. Adapt the language requirements to your deployment region.*
