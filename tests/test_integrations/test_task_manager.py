import pytest
from src.integrations.task_manager import TaskManager
from unittest.mock import patch

@pytest.fixture
def task_manager():
    return TaskManager("test_api_key", "https://api.example.com")

def test_task_manager_initialization(task_manager):
    assert task_manager.api_key == "test_api_key"
    assert task_manager.base_url == "https://api.example.com"
    assert "Bearer test_api_key" in task_manager.headers["Authorization"]

@patch('requests.post')
def test_create_task(mock_post, task_manager):
    mock_post.return_value.json.return_value = {
        "id": "123",
        "title": "Test Task",
        "status": "created"
    }
    
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium"
    }
    
    result = task_manager.create_task(task_data)
    assert result["id"] == "123"
    assert result["title"] == "Test Task"
    assert result["status"] == "created"

@patch('requests.post')
def test_create_tasks_from_action_items(mock_post, task_manager):
    mock_post.return_value.json.return_value = {
        "id": "123",
        "status": "created"
    }
    
    action_items = [
        {
            "action": "Schedule meeting",
            "context": "Need to schedule follow-up meeting",
            "priority": "high"
        },
        {
            "action": "Prepare report",
            "context": "Must prepare quarterly report",
            "priority": "medium"
        }
    ]
    
    results = task_manager.create_tasks_from_action_items(action_items)
    assert len(results) == 2
    assert all(isinstance(result, dict) for result in results)
    assert all("id" in result for result in results)
    assert all("status" in result for result in results)