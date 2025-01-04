from typing import List
from transformers import pipeline

class ContentSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        self.summarizer = pipeline("summarization", model=model_name)
        
    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """Generate a summary of the input text."""
        summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']

    def extract_key_points(self, text: str) -> List[str]:
        """Extract key points from the text."""

        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) > 5:
            summary = self.summarize(' '.join(sentences))
            key_points = summary.split('.')
        else:
            key_points = sentences
            
        return [point.strip() for point in key_points if point.strip()]