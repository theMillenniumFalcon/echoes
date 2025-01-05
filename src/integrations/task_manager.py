from typing import Dict, List
import requests

class TaskManager:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_task(self, task_data: Dict) -> Dict:
        """Create a new task in the task management system."""
        endpoint = f"{self.base_url}/tasks"
        response = requests.post(
            endpoint,
            headers=self.headers,
            json=task_data
        )
        return response.json()
    
    def create_tasks_from_action_items(self, action_items: List[Dict]) -> List[Dict]:
        """Create tasks from extracted action items."""
        created_tasks = []
        for item in action_items:
            task_data = {
                "title": item["action"],
                "description": item["context"],
                "priority": item["priority"]
            }
            created_task = self.create_task(task_data)
            created_tasks.append(created_task)
        
        return created_tasks