from app.browser.session_manager import SessionManager


def test_session_lifecycle():
    manager = SessionManager()
    session = manager.create({"job_id": "job-1"})
    assert manager.get(session.session_id).status == "created"
    assert manager.set_status(session.session_id, "closed").status == "closed"
    assert manager.close(session.session_id)
    assert manager.get(session.session_id) is None
