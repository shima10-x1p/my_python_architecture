import injector

from openapi_server.business.adapters.todo_repository_postgres import TodoRepositoryPostgres
from openapi_server.business.ports.todo_repository import TodoRepository
from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate


def configure_injector() -> injector.Injector:
    """依存性注入の設定.

    Returns:
        injector.Injector: Injectorインスタンス

    """
    # PostgreSQLのDSNを指定
    # TODO: 環境変数や設定ファイルから取得するように変更すること
    dsn = "postgresql://user:password@localhost:5432/todo_db"
    # Injectorを作成し、TodoRepositoryPostgresをバインド
    injector_instance = injector.Injector()
    injector_instance.binder.bind(
        TodoRepository,
        to=TodoRepositoryPostgres(dsn),
        scope=injector.singleton,
    )
    return injector_instance


async def create_task_usecase(task_create: TaskCreate) -> Task:
    """タスクを作成するユースケース.

    Args:
        task_create (TaskCreate): タスク作成情報

    Returns:
        Task: 作成されたタスク

    """
    # Injectorを取得
    injector_instance = configure_injector()
    # TodoRepositoryを取得
    todo_repository: TodoRepository = injector_instance.get(TodoRepository)
    # タスクを作成
    return await todo_repository.create_task(task_create)
