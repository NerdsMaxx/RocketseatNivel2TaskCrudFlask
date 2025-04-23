from itertools import takewhile
from typing import Any

import pytest
import requests
from requests import Response

# CRUD
BASE_URL: str = 'http://127.0.0.1:5000'
tasks: list[int] = []

def test_create_task():
    new_task_data = {
        "title": "Nova tarefa",
        "description": "Descrição da nova tarefa"
    }
    
    response: Response = requests.post(f"{BASE_URL}/tasks", json=new_task_data)
    assert response.status_code == 200
    response_json: Any = response.json()
    assert "message" in response_json
    assert "id" in response_json
    tasks.append(response_json['id'])
    
def test_get_tasks():
    response: Response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json: Any = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json
    
def test_get_task():
    if len(tasks) > 0:
        task_id: int = tasks[0]
        response: Response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json: Any = response.json()
        assert "id" in response_json
        assert task_id == response_json['id']
        assert "title" in response_json
        assert "description" in response_json
        assert "completed" in response_json
        
def test_update_task():
    if len(tasks) > 0:
        task_id: int = tasks[0]
        payload = {
            "completed": False,
            "description": "",
            "title": "Titulo atualizado"
        }
        
        response: Response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=payload)
        assert response.status_code == 200
        response_json: Any = response.json()
        assert "message" in response_json
        
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        
        assert response_json["title"] == payload["title"]
        assert response_json["description"] == payload["description"]
        assert response_json["completed"] == payload["completed"]
        
def test_delete_task():
    if len(tasks) > 0:
        task_id: int = tasks[0]
        
        response: Response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json: Any = response.json()
        assert "message" in response_json

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404