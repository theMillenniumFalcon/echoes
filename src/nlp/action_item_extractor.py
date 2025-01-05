import spacy
from typing import List, Dict
import re

class ActionItemExtractor:
    def __init__(self, model: str = "en_core_web_sm"):
        self.nlp = spacy.load(model)
        
    def extract_action_items(self, text: str) -> List[Dict[str, str]]:
        """Extract action items from text."""
        doc = self.nlp(text)
        action_items = []
        
        action_patterns = [
            r"need to (\w+)",
            r"should (\w+)",
            r"must (\w+)",
            r"will (\w+)",
            r"going to (\w+)"
        ]
        
        for sent in doc.sents:
            sent_text = sent.text.lower()
            
            for pattern in action_patterns:
                matches = re.finditer(pattern, sent_text)
                for match in matches:
                    action_items.append({
                        "action": match.group(1),
                        "context": sent.text,
                        "priority": "medium"
                    })
        
        return action_items