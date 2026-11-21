from enum import Enum


class ChallengeState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    PAGE_LOADED = "page_loaded"
    CHALLENGE_DETECTED = "challenge_detected"
    VERIFICATION_PENDING = "verification_pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    NEEDS_YOU = "needs_you"
    FAILED = "failed"


ALLOWED_TRANSITIONS = {
    ChallengeState.QUEUED: {ChallengeState.RUNNING, ChallengeState.FAILED},
    ChallengeState.RUNNING: {ChallengeState.PAGE_LOADED, ChallengeState.CHALLENGE_DETECTED, ChallengeState.FAILED},
    ChallengeState.PAGE_LOADED: {ChallengeState.VERIFICATION_PENDING, ChallengeState.NEEDS_YOU, ChallengeState.FAILED},
    ChallengeState.CHALLENGE_DETECTED: {ChallengeState.VERIFICATION_PENDING, ChallengeState.NEEDS_YOU, ChallengeState.FAILED},
    ChallengeState.VERIFICATION_PENDING: {ChallengeState.VERIFIED, ChallengeState.REJECTED, ChallengeState.NEEDS_YOU, ChallengeState.FAILED},
    ChallengeState.VERIFIED: set(),
    ChallengeState.REJECTED: set(),
    ChallengeState.NEEDS_YOU: set(),
    ChallengeState.FAILED: set(),
}


def transition(current: ChallengeState, target: ChallengeState) -> ChallengeState:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"Invalid challenge-state transition: {current} -> {target}")
    return target
