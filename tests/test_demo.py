from app.demo.service import SyntheticChallengeService

def test_demo_verifies_correct_answer():
    service = SyntheticChallengeService()
    challenge = service.create()
    answer = service.records[challenge["id"]].answer
    result = service.verify(challenge["id"], str(answer))
    assert result["accepted"] is True
    assert result["status"] == "verified"

def test_attempt_limit():
    service = SyntheticChallengeService(max_attempts=2)
    challenge = service.create()
    assert service.verify(challenge["id"], "999")["status"] == "pending"
    assert service.verify(challenge["id"], "999")["status"] == "failed"

def test_unknown_id():
    result = SyntheticChallengeService().verify("unknown", "1")
    assert result["accepted"] is False
