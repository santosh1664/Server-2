from app.detection.classifier import classify_evidence

def test_turnstile_signature():
    result = classify_evidence("https://example.test",
                               '<div class="cf-turnstile"></div>', "")
    assert result.detected and "turnstile" in result.providers

def test_clean_page():
    result = classify_evidence("https://example.test", "<main>Hi</main>", "Hi")
    assert not result.detected
