from app.captcha.challenge_state import ChallengeState
from app.orchestration.coordinator import ChallengeCoordinator


def test_synthetic_verified_result_maps_to_verified():
    state = ChallengeCoordinator.synthetic_verification_state(
        {"accepted": True, "status": "verified"}
    )
    assert state is ChallengeState.VERIFIED


def test_synthetic_failed_result_maps_to_needs_you():
    state = ChallengeCoordinator.synthetic_verification_state(
        {"accepted": False, "status": "failed"}
    )
    assert state is ChallengeState.NEEDS_YOU


def test_synthetic_pending_result_stays_pending():
    state = ChallengeCoordinator.synthetic_verification_state(
        {"accepted": False, "status": "pending"}
    )
    assert state is ChallengeState.VERIFICATION_PENDING
