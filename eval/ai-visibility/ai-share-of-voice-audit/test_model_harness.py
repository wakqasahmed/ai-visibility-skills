"""Deterministic unit tests for model_harness.py's pure logic (no live model
calls, no ANTHROPIC_API_KEY needed) — the routing decision parser, the
per-fixture routing scorer, and the gate that both must satisfy."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import model_harness  # noqa: E402


class ParseRoutingDecisionTest(unittest.TestCase):
    def test_parses_skill_name(self):
        text = "DECISION: ai-share-of-voice-audit\nThe user supplied transcripts."
        self.assertEqual(model_harness.parse_routing_decision(text), "ai-share-of-voice-audit")

    def test_parses_none(self):
        text = "DECISION: none\nNo listed skill applies."
        self.assertEqual(model_harness.parse_routing_decision(text), "none")

    def test_parses_clarify(self):
        text = "DECISION: clarify\nUnclear whether transcripts are supplied."
        self.assertEqual(model_harness.parse_routing_decision(text), "clarify")

    def test_case_insensitive_prefix(self):
        text = "decision: ai-share-of-voice-audit\nreason"
        self.assertEqual(model_harness.parse_routing_decision(text), "ai-share-of-voice-audit")

    def test_missing_decision_line_returns_empty(self):
        self.assertEqual(model_harness.parse_routing_decision("I'll just help directly."), "")


class ScoreRoutingTest(unittest.TestCase):
    def test_should_use_selecting_the_skill_passes(self):
        meta = {"type": "should_use"}
        self.assertEqual(model_harness.score_routing(meta, "ai-share-of-voice-audit"), [])

    def test_should_use_selecting_none_fails(self):
        meta = {"type": "should_use"}
        failures = model_harness.score_routing(meta, "none")
        self.assertTrue(failures)

    def test_should_not_use_selecting_the_skill_fails(self):
        meta = {"type": "should_not_use"}
        failures = model_harness.score_routing(meta, "ai-share-of-voice-audit")
        self.assertTrue(failures)

    def test_should_not_use_selecting_a_decoy_passes(self):
        meta = {"type": "should_not_use"}
        self.assertEqual(model_harness.score_routing(meta, "ai-visibility-audit"), [])

    def test_should_clarify_asking_for_clarification_passes(self):
        meta = {"type": "should_clarify"}
        self.assertEqual(model_harness.score_routing(meta, "clarify"), [])

    def test_should_clarify_selecting_the_skill_outright_fails(self):
        meta = {"type": "should_clarify"}
        failures = model_harness.score_routing(meta, "ai-share-of-voice-audit")
        self.assertTrue(failures)


if __name__ == "__main__":
    unittest.main()
