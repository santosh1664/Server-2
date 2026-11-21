import pytest
from app.captcha.challenge_state import ChallengeState, transition


def test_valid_transition_to_needs_you():
    assert transition(ChallengeState.CHALLENGE_DETECTED, ChallengeState.NEEDS_YOU) is ChallengeState.NEEDS_YOU


def test_terminal_state_cannot_be_reopened():
    with pytest.raises(ValueError):
        transition(ChallengeState.VERIFIED, ChallengeState.RUNNING)
