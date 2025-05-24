from datetime import datetime

from openapi_server.apis.task_api_base import BaseTaskApi
from openapi_server.business.usecase.create_task_usecase import create_task_usecase
from openapi_server.business.usecase.list_tasks_usecase import list_tasks_usecase
from openapi_server.logger import log_function
from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate


class TaskApiController(BaseTaskApi):
    """タスクAPIコントローラ."""

    @log_function("INFO")
    async def create_task(
        self,
        task_create: TaskCreate,
    ) -> Task:
        """新しいタスクを作成するエンドポイント.

        Args:
            task_create (TaskCreate): 作成するタスク情報

        Returns:
            Task: 作成されたタスクオブジェクト

        """
        return await create_task_usecase(task_create)

    @log_function("INFO")
    async def list_tasks(
        self,
        title: str | None = None,
        is_done: bool | None = None,
        created_from: datetime | None = None,
        created_to: datetime | None = None,
    ) -> list[Task]:
        """タスク一覧を取得するエンドポイント.

        Args:
            title (str | None): タイトルの部分一致検索
            is_done (bool | None): 完了フラグでの絞り込み
            created_from (datetime | None): 作成日(開始)での絞り込み
            created_to (datetime | None): 作成日(終了)での絞り込み

        Returns:
            list[Task]: タスクオブジェクトのリスト

        """
        return await list_tasks_usecase(
            title=title,
            is_done=is_done,
            created_from=created_from,
            created_to=created_to,
        )
