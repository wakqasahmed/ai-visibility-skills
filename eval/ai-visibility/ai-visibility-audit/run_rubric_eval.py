#!/usr/bin/env python3
"""Deterministic eval for the V3 scoring rubric (docs/SCORING_RUBRIC.md, also
bundled at skills/ai-visibility/ai-visibility-audit/references/scoring_rubric.md
for self-contained single-skill installs -- see issue #91; the two copies must
stay in sync).

PR #82 added a composite Overall Readiness Score built from six pillar scores,
but nothing enforced that those pillar scores were derived mechanically from
specific check results rather than a free-form LLM estimate. This script
encodes the deduction table from docs/SCORING_RUBRIC.md as data, scores a set
of known fixture finding-sets against it, and asserts:

1. The worked example in docs/SCORING_RUBRIC.md itself reproduces the exact
   score documented there (89/100) — the doc and the rubric-scoring logic
   cannot silently drift apart.
2. Scoring is deterministic: shuffling the order findings are supplied in
   never changes the resulting score.
3. Per-check deduction caps are enforced (e.g. Pillar 1 check 1.1 caps at
   -50 even if more than two crawler families are blocked).
4. A pillar with every check marked N/A is excluded from the composite and
   the remaining pillar weights are reproportioned rather than defaulting
   the excluded pillar to 0 or 100.
5. PR #86 wired ecommerce-technical-seo-audit's checks (1.9-1.11 in Discovery,
   4.7 in Answer Readiness) into the rubric — they score with the same flat/
   per-occurrence/capped arithmetic as every other check, and are cleanly
   absent (no deduction) on a non-ecommerce site.

This does not invoke an LLM — it proves the rubric's arithmetic is
well-defined and reproducible, which is the property the reporting
architecture needs regardless of who (human or model) applies the table.

Exit code 0 = pass, 1 = fail.
"""
from __future__ import annotations

import random
import sys
from dataclasses import dataclass, field

# --- Rubric data (docs/SCORING_RUBRIC.md) --------------------------------
# Each pillar: weight (of 100) and its checks. A check's "cap" limits the
# total deduction it can contribute even if triggered multiple times
# (e.g. Pillar 1's 1.1 blocks several crawler families but is capped).

PILLAR_WEIGHTS = {
    "discovery": 20,
    "technical_accessibility": 20,
    "machine_understanding": 20,
    "answer_readiness": 20,
    "trust_authority": 15,
    "agent_readiness": 5,
}

RUBRIC = {
    "discovery": {
        "1.1": {"deduction": 25, "cap": 50, "per_occurrence": True},
        "1.2": {"deduction": 25},
        "1.3": {"deduction": 15},
        "1.4": {"deduction": 10},
        "1.5": {"deduction": 10, "cap": 10, "per_occurrence": True},  # per 10% broken
        "1.6": {"deduction": 10},
        "1.7": {"deduction": 5},
        "1.8": {"deduction": 5},
        "1.9": {"deduction": 10},
        "1.10": {"deduction": 5},
        "1.11": {"deduction": 15},
        "1.12": {"deduction": 10},
    },
    "technical_accessibility": {
        "2.1": {"deduction": 30},
        "2.2": {"deduction": 25},
        "2.3": {"deduction": 20},
        "2.4": {"deduction": 15},
        "2.5": {"deduction": 10},
        "2.6": {"deduction": 10},
        "2.7": {"deduction": 5},
    },
    "machine_understanding": {
        "3.1": {"deduction": 25},
        "3.2": {"deduction": 20},
        "3.3": {"deduction": 15},
        "3.4": {"deduction": 20},
        "3.5": {"deduction": 10},
        "3.6": {"deduction": 10},
    },
    "answer_readiness": {
        "4.1": {"deduction": 25},
        "4.2": {"deduction": 15},
        "4.3": {"deduction": 15},
        "4.4_missing": {"deduction": 10},
        "4.4_vague": {"deduction": 5},
        "4.5_missing": {"deduction": 5},
        "4.5_vague": {"deduction": 3},
        "4.6": {"deduction": 10},
        "4.7": {"deduction": 10, "cap": 20, "per_occurrence": True},  # per flagged thin category page
    },
    "trust_authority": {
        "5.1": {"deduction": 25},
        "5.2": {"deduction": 25},
        "5.3": {"deduction": 20},
        "5.4": {"deduction": 15},
        "5.5": {"deduction": 15},
        "5.6": {"deduction": 10},
        "5.7": {"deduction": 10},
    },
    "agent_readiness": {
        "6.1": {"deduction": 40},
        "6.2": {"deduction": 40},
        "6.3": {"deduction": 15},
        "6.4": {"deduction": 15},
    },
}


@dataclass
class PillarResult:
    score: float
    excluded: bool = False


def score_pillar(pillar: str, triggered: dict) -> PillarResult:
    """triggered: {check_id: occurrence_count} for checks that failed.

    A check absent from `triggered` is treated as passed (0 deduction).
    A check_id of literal "N/A_ALL" means every check in the pillar is
    inapplicable to this site — the pillar is excluded from the composite.
    """
    if triggered.get("N/A_ALL"):
        return PillarResult(score=0.0, excluded=True)

    checks = RUBRIC[pillar]
    total_deduction = 0.0
    for check_id, count in triggered.items():
        if check_id not in checks:
            raise KeyError(f"unknown check id '{check_id}' for pillar '{pillar}'")
        spec = checks[check_id]
        occurrences = count if spec.get("per_occurrence") else 1
        deduction = spec["deduction"] * occurrences
        if "cap" in spec:
            deduction = min(deduction, spec["cap"])
        total_deduction += deduction

    return PillarResult(score=max(0.0, 100.0 - total_deduction))


def composite_score(pillar_results: dict) -> float:
    """Weighted sum across non-excluded pillars, reproportioning weights of
    any excluded pillar across the remaining ones so weights still sum to
    100 (docs/SCORING_RUBRIC.md, "Handling inapplicable checks and pillars")."""
    included = {p: r for p, r in pillar_results.items() if not r.excluded}
    if not included:
        raise ValueError("all pillars excluded — cannot compute a composite score")

    excluded_weight = sum(PILLAR_WEIGHTS[p] for p in pillar_results if pillar_results[p].excluded)
    reweight_factor = 100.0 / (100.0 - excluded_weight)

    total = 0.0
    for pillar, result in included.items():
        adjusted_weight = PILLAR_WEIGHTS[pillar] * reweight_factor
        total += result.score * (adjusted_weight / 100.0)
    return total


# --- Fixtures --------------------------------------------------------------

def worked_example_findings() -> dict:
    """docs/SCORING_RUBRIC.md's "Worked example" section, verbatim."""
    return {
        "discovery": {"1.1": 1},
        "machine_understanding": {"3.1": 1},
        "answer_readiness": {"4.5_missing": 1},
        "technical_accessibility": {},
        "trust_authority": {},
        "agent_readiness": {},
    }


def run_worked_example() -> list:
    failures = []
    findings = worked_example_findings()
    results = {pillar: score_pillar(pillar, triggered) for pillar, triggered in findings.items()}

    expected_pillar_scores = {
        "discovery": 75.0,
        "machine_understanding": 75.0,
        "answer_readiness": 95.0,
        "technical_accessibility": 100.0,
        "trust_authority": 100.0,
        "agent_readiness": 100.0,
    }
    for pillar, expected in expected_pillar_scores.items():
        actual = results[pillar].score
        if actual != expected:
            failures.append(
                f"worked example: {pillar} scored {actual}, docs/SCORING_RUBRIC.md says {expected}"
            )

    overall = composite_score(results)
    if round(overall, 2) != 89.0:
        failures.append(f"worked example: overall scored {round(overall, 2)}, docs/SCORING_RUBRIC.md says 89")

    return failures


def run_determinism_check() -> list:
    """Same triggered-check set, different dict insertion order, must score identically."""
    failures = []
    base = {"1.1": 1, "1.3": 1, "1.6": 1}
    shuffled_keys = list(base.keys())
    scores = set()
    for _ in range(20):
        random.shuffle(shuffled_keys)
        reordered = {k: base[k] for k in shuffled_keys}
        scores.add(score_pillar("discovery", reordered).score)
    if len(scores) != 1:
        failures.append(f"scoring is not order-independent: got scores {scores} for the same triggered checks")
    return failures


def run_cap_enforcement() -> list:
    """1.1 deducts 25 per blocked crawler family but caps combined loss at 50."""
    failures = []
    # 3 blocked families would be 75 uncapped; must cap at 50 -> score 50.
    result = score_pillar("discovery", {"1.1": 3})
    if result.score != 50.0:
        failures.append(f"expected cap to hold 1.1 at -50 (score 50), got score {result.score}")
    return failures


def run_na_pillar_reweighting() -> list:
    """A docs site with no commerce/conversion actions excludes Pillar 6 entirely
    and reproportions the remaining five pillars (20/20/20/20/15 -> /0.95)."""
    failures = []
    findings = {
        "discovery": {},
        "technical_accessibility": {},
        "machine_understanding": {},
        "answer_readiness": {},
        "trust_authority": {},
        "agent_readiness": {"N/A_ALL": True},
    }
    results = {pillar: score_pillar(pillar, triggered) for pillar, triggered in findings.items()}
    if not results["agent_readiness"].excluded:
        failures.append("agent_readiness should be excluded when N/A_ALL is set")

    overall = composite_score(results)
    # All included pillars score 100, so a correctly-reweighted composite must
    # still be 100 (reweighting must not silently score the excluded pillar
    # as 0, which would drag the composite below 100).
    if round(overall, 2) != 100.0:
        failures.append(
            f"expected a fully-clean site with one N/A pillar to still composite to 100, got {round(overall, 2)}"
        )
    return failures


def run_floor_at_zero() -> list:
    """Deductions exceeding 100 must floor the pillar score at 0, not go negative."""
    failures = []
    result = score_pillar("technical_accessibility", {"2.1": 1, "2.2": 1, "2.3": 1, "2.4": 1, "2.5": 1})
    if result.score != 0.0:
        failures.append(f"expected floor at 0 for a pillar with >100 points of deductions, got {result.score}")
    return failures


def run_ecommerce_checks_scoring() -> list:
    """PR #86 wired ecommerce-technical-seo-audit's checks into Discovery (1.9-1.11)
    and Answer Readiness (4.7). Prove they flow through the same arithmetic as every
    other check: flat deductions apply once, and 4.7's per-occurrence cap holds."""
    failures = []

    # 1.9 (facet dup, -10) + 1.10 (orphan, -5) + 1.11 (discontinued soft-404, -15)
    # triggered together on an ecommerce catalog audit -> 100 - 30 = 70.
    discovery = score_pillar("discovery", {"1.9": 1, "1.10": 1, "1.11": 1})
    if discovery.score != 70.0:
        failures.append(f"expected discovery 1.9+1.10+1.11 to total -30 (score 70), got {discovery.score}")

    # 4.7 triggered on 2 sampled thin category pages: 2 x -10 = -20, under the cap.
    answer_two = score_pillar("answer_readiness", {"4.7": 2})
    if answer_two.score != 80.0:
        failures.append(f"expected 4.7 x2 occurrences to deduct exactly -20 (score 80), got {answer_two.score}")

    # 4.7 triggered on 5 sampled thin category pages: 5 x -10 = -50 uncapped,
    # must cap at -20 (score 80) to prevent a small sample from swinging the pillar.
    answer_five = score_pillar("answer_readiness", {"4.7": 5})
    if answer_five.score != 80.0:
        failures.append(f"expected 4.7's cap to hold at -20 regardless of sample size (score 80), got {answer_five.score}")

    return failures


def run_ecommerce_na_pillar() -> list:
    """A non-ecommerce site (docs/SaaS, no catalog) has 1.9-1.11 and 4.7 all
    check-level N/A — they must simply be absent from `triggered`, contributing
    zero deduction, exactly like the worked example's SaaS site."""
    failures = []
    discovery = score_pillar("discovery", {"1.1": 1})  # only 1.1 triggered, 1.9-1.11 N/A
    if discovery.score != 75.0:
        failures.append(f"expected non-ecommerce site's N/A facet/orphan/discontinued checks to add no deduction, got {discovery.score}")
    return failures


def run_hreflang_checks_scoring() -> list:
    """1.12 (hreflang mismatch, -10) triggered on a multilingual site scores correctly."""
    failures = []
    discovery = score_pillar("discovery", {"1.12": 1})
    if discovery.score != 90.0:
        failures.append(f"expected 1.12 to deduct -10 (score 90), got {discovery.score}")
    return failures


def main() -> int:
    all_failures = []
    checks = [
        ("worked example reproduces docs/SCORING_RUBRIC.md", run_worked_example),
        ("scoring is order-independent", run_determinism_check),
        ("per-check deduction caps are enforced", run_cap_enforcement),
        ("N/A pillar exclusion + weight reproportioning", run_na_pillar_reweighting),
        ("pillar score floors at 0", run_floor_at_zero),
        ("ecommerce-technical-seo-audit checks (1.9-1.11, 4.7) score correctly", run_ecommerce_checks_scoring),
        ("ecommerce checks are cleanly N/A on a non-ecommerce site", run_ecommerce_na_pillar),
        ("international-seo-hreflang-audit check (1.12) scores correctly", run_hreflang_checks_scoring),
    ]

    for label, fn in checks:
        failures = fn()
        status = "PASS" if not failures else "FAIL"
        print(f"[{status}] {label}")
        for f in failures:
            print(f"    - {f}")
        all_failures.extend(failures)

    if all_failures:
        print(f"\nFAIL: {len(all_failures)} rubric-scoring violation(s)")
        return 1

    print("\nPASS: rubric scoring is deterministic, reproduces the documented worked example, "
          "enforces per-check caps, and reproportions weights correctly when a pillar is N/A")
    return 0


if __name__ == "__main__":
    sys.exit(main())
