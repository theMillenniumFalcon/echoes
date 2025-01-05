import pytest
from src.nlp.action_item_extractor import ActionItemExtractor

def test_action_item_extractor_initialization():
    extractor = ActionItemExtractor()
    assert extractor.nlp is not None

def test_extract_action_items():
    extractor = ActionItemExtractor()
    text = "We need to schedule a follow-up meeting. John must prepare the report."
    action_items = extractor.extract_action_items(text)
    
    assert isinstance(action_items, list)
    assert len(action_items) > 0
    assert all(isinstance(item, dict) for item in action_items)
    assert all("action" in item for item in action_items)
    assert all("context" in item for item in action_items)
    assert all("priority" in item for item in action_items)