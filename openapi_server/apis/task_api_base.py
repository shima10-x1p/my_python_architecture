# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from datetime import datetime
from pydantic import Field, StrictBool, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate
from openapi_server.models.task_update import TaskUpdate


class BaseTaskApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseTaskApi.subclasses = BaseTaskApi.subclasses + (cls,)
    async def create_task(
        self,
        task_create: TaskCreate,
    ) -> Task:
        ...


    async def delete_task(
        self,
        task_id: StrictStr,
    ) -> None:
        ...


    async def get_task(
        self,
        task_id: StrictStr,
    ) -> Task:
        ...


    async def list_tasks(
        self,
        title: Annotated[Optional[StrictStr], Field(description="タイトルで部分一致検索")],
        is_done: Annotated[Optional[StrictBool], Field(description="完了フラグで絞り込み")],
        created_from: Annotated[Optional[datetime], Field(description="作成日(開始)で絞り込み (ISO8601形式)")],
        created_to: Annotated[Optional[datetime], Field(description="作成日(終了)で絞り込み (ISO8601形式)")],
    ) -> List[Task]:
        ...


    async def update_task(
        self,
        task_id: StrictStr,
        task_update: TaskUpdate,
    ) -> Task:
        ...
