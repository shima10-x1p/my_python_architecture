# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.task_api_base import BaseTaskApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from datetime import datetime
from pydantic import Field, StrictBool, StrictStr
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate
from openapi_server.models.task_update import TaskUpdate


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/tasks",
    responses={
        201: {"model": Task, "description": "作成されたタスク"},
    },
    tags=["Task"],
    summary="新しいタスクを作成",
    response_model_by_alias=True,
)
async def create_task(
    task_create: TaskCreate = Body(None, description=""),
) -> Task:
    if not BaseTaskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTaskApi.subclasses[0]().create_task(task_create)


@router.delete(
    "/tasks/{task_id}",
    responses={
        204: {"description": "タスク削除成功"},
        404: {"description": "タスクが見つかりません"},
    },
    tags=["Task"],
    summary="タスクを削除",
    response_model_by_alias=True,
)
async def delete_task(
    task_id: StrictStr = Path(..., description=""),
) -> None:
    if not BaseTaskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTaskApi.subclasses[0]().delete_task(task_id)


@router.get(
    "/tasks/{task_id}",
    responses={
        200: {"model": Task, "description": "タスク詳細"},
        404: {"description": "タスクが見つかりません"},
    },
    tags=["Task"],
    summary="タスク詳細を取得",
    response_model_by_alias=True,
)
async def get_task(
    task_id: StrictStr = Path(..., description=""),
) -> Task:
    if not BaseTaskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTaskApi.subclasses[0]().get_task(task_id)


@router.get(
    "/tasks",
    responses={
        200: {"model": List[Task], "description": "タスク一覧"},
    },
    tags=["Task"],
    summary="タスク一覧を取得",
    response_model_by_alias=True,
)
async def list_tasks(
    title: Annotated[Optional[StrictStr], Field(description="タイトルで部分一致検索")] = Query(None, description="タイトルで部分一致検索", alias="title"),
    is_done: Annotated[Optional[StrictBool], Field(description="完了フラグで絞り込み")] = Query(None, description="完了フラグで絞り込み", alias="is_done"),
    created_from: Annotated[Optional[datetime], Field(description="作成日(開始)で絞り込み (ISO8601形式)")] = Query(None, description="作成日(開始)で絞り込み (ISO8601形式)", alias="created_from"),
    created_to: Annotated[Optional[datetime], Field(description="作成日(終了)で絞り込み (ISO8601形式)")] = Query(None, description="作成日(終了)で絞り込み (ISO8601形式)", alias="created_to"),
) -> List[Task]:
    if not BaseTaskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTaskApi.subclasses[0]().list_tasks(title, is_done, created_from, created_to)


@router.put(
    "/tasks/{task_id}",
    responses={
        200: {"model": Task, "description": "更新されたタスク"},
        404: {"description": "タスクが見つかりません"},
    },
    tags=["Task"],
    summary="タスクを更新",
    response_model_by_alias=True,
)
async def update_task(
    task_id: StrictStr = Path(..., description=""),
    task_update: TaskUpdate = Body(None, description=""),
) -> Task:
    if not BaseTaskApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTaskApi.subclasses[0]().update_task(task_id, task_update)
