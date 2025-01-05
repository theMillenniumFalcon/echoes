from src.nlp.summarizer import ContentSummarizer

def test_summarizer_initialization():
    summarizer = ContentSummarizer()
    assert summarizer.summarizer is not None

def test_summarize_short_text():
    summarizer = ContentSummarizer()
    text = "This is a short test text that doesn't need summarization."
    summary = summarizer.summarize(text)
    assert isinstance(summary, str)
    assert len(summary) <= 130

def test_extract_key_points():
    summarizer = ContentSummarizer()
    text = """
    First important point about the meeting. 
    Second key detail that was discussed. 
    Third major decision that was made.
    """
    key_points = summarizer.extract_key_points(text)
    assert isinstance(key_points, list)
    assert len(key_points) > 0
    assert all(isinstance(point, str) for point in key_points)