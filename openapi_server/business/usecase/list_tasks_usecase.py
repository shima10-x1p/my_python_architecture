"""ToDoリスト取得ユースケース."""
from datetime import datetime
import injector

from openapi_server.business.adapters.todo_repository_postgres import TodoRepositoryPostgres
from openapi_server.business.const import settings
from openapi_server.business.ports.todo_repository import TodoRepository
from openapi_server.logger import get_logger, log_function
from openapi_server.models.task import Task

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
async def list_tasks_usecase(
    title: str | None = None,
    is_done: bool | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    injector_instance: injector.Injector = None,
) -> list[Task]:
    """タスク一覧を取得するユースケース.

    Args:
        title (str | None): タイトルの部分一致検索
        is_done (bool | None): 完了フラグでの絞り込み
        created_from (str | None): 作成日(開始)での絞り込み
        created_to (str | None): 作成日(終了)での絞り込み
        injector_instance (injector.Injector, optional): Injectorインスタンス。
            デフォルトはNoneで、configure_injector()を使用してInjectorを取得する。

    Returns:
        list[Task]: タスクオブジェクトのリスト

    """
    # Injectorを取得
    if injector_instance is None:
        # configure_injector()を使用してInjectorを取得
        injector_instance = configure_injector()
    # created_from, created_toをISOフォーマット文字列に変換
    created_from_str = created_from.isoformat() if created_from else None
    created_to_str = created_to.isoformat() if created_to else None
    # TodoRepositoryを取得
    todo_repository: TodoRepository = injector_instance.get(TodoRepository)
    # タスク一覧を取得
    return await todo_repository.list_tasks(title, is_done, created_from_str, created_to_str)
