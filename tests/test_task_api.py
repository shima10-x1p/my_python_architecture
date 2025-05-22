# coding: utf-8

from fastapi.testclient import TestClient


from datetime import datetime  # noqa: F401
from pydantic import Field, StrictBool, StrictStr  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.task import Task  # noqa: F401
from openapi_server.models.task_create import TaskCreate  # noqa: F401
from openapi_server.models.task_update import TaskUpdate  # noqa: F401


def test_create_task(client: TestClient):
    """Test case for create_task

    新しいタスクを作成
    """
    task_create = {"description":"小説を1冊読む","title":"本を読む"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/tasks",
    #    headers=headers,
    #    json=task_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_task(client: TestClient):
    """Test case for delete_task

    タスクを削除
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/tasks/{task_id}".format(task_id='task_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_task(client: TestClient):
    """Test case for get_task

    タスク詳細を取得
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/tasks/{task_id}".format(task_id='task_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_list_tasks(client: TestClient):
    """Test case for list_tasks

    タスク一覧を取得
    """
    params = [("title", 'title_example'),     ("is_done", True),     ("created_from", '2013-10-20T19:20:30+01:00'),     ("created_to", '2013-10-20T19:20:30+01:00')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/tasks",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_task(client: TestClient):
    """Test case for update_task

    タスクを更新
    """
    task_update = {"is_done":1,"description":"description","title":"title"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/tasks/{task_id}".format(task_id='task_id_example'),
    #    headers=headers,
    #    json=task_update,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

