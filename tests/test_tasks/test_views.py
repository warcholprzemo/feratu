from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from tasks.database import DeleteStatus, UpdateStatus
from tasks.views import app

client = TestClient(app)


def test_hello():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Message": "Hello World"}


@patch("tasks.views.retrieve_tasks")
class TestTaskView:
    def test_response_contains_all_fields(self, m_retrieve_tasks):
        m_retrieve_tasks.return_value = [
            {
                "id": "5678",
                "created": "2023-01-01T07:10:56",
                "finished": "2023-01-10T23:45:12",
                "title": "Buy new bookshelf",
                "description": "Bought in Agata Meble",
                "done": True,
            }
        ]

        response = client.get("/tasks/")

        assert response.status_code == 200
        assert response.json() == [
            {
                "id": "5678",
                "created": "2023-01-01T07:10:56",
                "finished": "2023-01-10T23:45:12",
                "title": "Buy new bookshelf",
                "description": "Bought in Agata Meble",
                "done": True,
            }
        ]

    def test_response_adds_optional_fields(self, m_retrieve_tasks):
        m_retrieve_tasks.return_value = [
            {
                "id": "5678",
                "created": "2023-01-01T07:10:56",
                "title": "Buy new bookshelf",
            }
        ]

        response = client.get("/tasks/")

        assert response.status_code == 200
        assert response.json() == [
            {
                "id": "5678",
                "created": "2023-01-01T07:10:56",
                "finished": None,
                "title": "Buy new bookshelf",
                "description": "",
                "done": False,
            }
        ]

    def test_response_without_mandatory_fields_raises_value_error(
        self, m_retrieve_tasks
    ):
        m_retrieve_tasks.return_value = [
            {
                "created": "2023-01-01T07:10:56",
                "title": "Buy new bookshelf",
            }
        ]

        with pytest.raises(ValueError):
            client.get("/tasks/")


@patch("tasks.views.add_task")
class TestAddTaskView:
    def test_add_new_task_and_return_its_full_instance(self, m_add_task):
        task = {"created": "2023-01-01T07:10:56", "title": "Buy new bookshelf"}
        m_add_task.return_value = {"id": "5678", **task}

        response = client.post("/tasks/", json=task)

        assert response.status_code == 200
        assert response.json() == {
            "created": "2023-01-01T07:10:56",
            "finished": None,
            "title": "Buy new bookshelf",
            "description": "",
            "done": False,
        }


@patch("tasks.views.update_task")
class TestUpdateTaskView:
    def test_task_updated_correctly(self, m_update_task):
        m_update_task.return_value = UpdateStatus(
            updated=True, message="Task 5678 updated correctly (1 rows)"
        )
        task = {"created": "2023-01-01T07:10:56", "title": "Buy new bookshelf"}

        response = client.put("/tasks/5678/", json=task)

        assert response.status_code == 200
        assert response.json() == {"info": "Task 5678 updated correctly (1 rows)"}

    def test_task_not_found(self, m_update_task):
        m_update_task.return_value = UpdateStatus(
            updated=False, message="Task 9999 not found"
        )
        task = {"created": "2023-01-01T07:10:56", "title": "Buy new bookshelf"}

        response = client.put("/tasks/9999/", json=task)

        assert response.status_code == 404
        assert response.json() == {"error": "Task 9999 not found"}


@patch("tasks.views.delete_task")
class TestDeleteTaskView:
    def test_task_deleted_correctly(self, m_update_task):
        m_update_task.return_value = DeleteStatus(
            deleted=True, message="Task 5678 deleted correctly"
        )

        response = client.delete("/tasks/5678/")

        assert response.status_code == 200
        assert response.json() == {"info": "Task 5678 deleted correctly"}

    def test_task_not_found(self, m_update_task):
        m_update_task.return_value = DeleteStatus(
            deleted=False, message="Task 9999 not found"
        )

        response = client.delete("/tasks/9999/")

        assert response.status_code == 404
        assert response.json() == {"error": "Task 9999 not found"}
