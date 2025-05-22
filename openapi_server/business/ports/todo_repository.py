from abc import ABC, abstractmethod

from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate
from openapi_server.models.task_update import TaskUpdate


class TodoRepository(ABC):
    """ToDoリポジトリの抽象インターフェース (ポート).

    ToDo情報の取得・作成・更新・削除などの操作を定義する。
    """

    @abstractmethod
    async def list_tasks(
        self,
        title: str | None = None,
        is_done: bool | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
    ) -> list[Task]:
        """タスク一覧を取得する."""
        ...

    @abstractmethod
    async def get_task(self, task_id: str) -> Task | None:
        """タスクIDでタスクを取得する."""
        ...

    @abstractmethod
    async def create_task(self, task_create: TaskCreate) -> Task:
        """新しいタスクを作成する."""
        ...

    @abstractmethod
    async def update_task(self, task_id: str, task_update: TaskUpdate) -> Task | None:
        """タスクを更新する."""
        ...

    @abstractmethod
    async def delete_task(self, task_id: str) -> bool:
        """タスクを削除する."""
        ...
