"""ToDoタスク作成ユースケース."""

import injector

from openapi_server.business.adapters.todo_repository_postgres import TodoRepositoryPostgres
from openapi_server.business.const import settings
from openapi_server.business.ports.todo_repository import TodoRepository
from openapi_server.logger import get_logger, log_function
from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate

# ロガーの取得
logger = get_logger()

@log_function("INFO")
def configure_injector() -> injector.Injector:
    """依存性注入の設定.

    Returns:
        injector.Injector: Injectorインスタンス

    """
    # PostgreSQLのDSNを設定クラスから取得
    dsn = settings.postgres_dsn
    # Injectorを作成し、TodoRepositoryPostgresをバインド
    injector_instance = injector.Injector()
    injector_instance.binder.bind(
        TodoRepository,
        to=TodoRepositoryPostgres(dsn),
        scope=injector.singleton,
    )
    return injector_instance


@log_function("INFO")
async def create_task_usecase(
    task_create: TaskCreate, injector_instance: injector.Injector = None,
) -> Task:
    """タスクを作成するユースケース.

    Args:
        task_create (TaskCreate): タスク作成情報
        injector_instance (injector.Injector, optional): Injectorインスタンス。
            デフォルトはNoneで、configure_injector()を使用してInjectorを取得する。

    Returns:
        Task: 作成されたタスク

    """
    # Injectorを取得
    if injector_instance is None:
        # configure_injector()を使用してInjectorを取得
        injector_instance = configure_injector()
    # TodoRepositoryを取得
    todo_repository: TodoRepository = injector_instance.get(TodoRepository)
    # タスクを作成
    return await todo_repository.create_task(task_create)
