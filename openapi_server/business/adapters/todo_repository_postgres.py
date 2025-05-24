"""PostgreSQL用ToDoリポジトリアダプタ (psycopg2使用)."""

import uuid
from datetime import UTC, datetime

import psycopg2
from injector import inject

from openapi_server.business.ports.todo_repository import TodoRepository
from openapi_server.models.task import Task
from openapi_server.models.task_create import TaskCreate
from openapi_server.models.task_update import TaskUpdate


class TodoRepositoryPostgres(TodoRepository):
    """PostgreSQLを使ったToDoリポジトリの実装クラス."""

    @inject
    def __init__(self, dsn: str) -> None:
        """コンストラクタ.

        Args:
            dsn (str): PostgreSQLのDSN

        """
        # DSN(データベース接続文字列)を保持
        self.dsn = dsn

    async def list_tasks(
        self,
        title: str | None = None,
        is_done: bool | None = None,
        created_from: str | None = None,
        created_to: str | None = None,
    ) -> list[Task]:
        """タスク一覧を取得する.

        Args:
            title (str | None): タイトルで部分一致検索
            is_done (bool | None): 完了フラグで絞り込み
            created_from (str | None): 作成日(開始)
            created_to (str | None): 作成日(終了)

        Returns:
            list[Task]: タスクのリスト

        """
        # 検索条件に応じてクエリを組み立てる
        query = "SELECT * FROM tasks WHERE TRUE"
        params = []
        if title:
            query += " AND title ILIKE %s"
            params.append(f"%{title}%")
        if is_done is not None:
            query += " AND is_done = %s"
            params.append(is_done)
        if created_from:
            query += " AND created_at >= %s"
            params.append(created_from)
        if created_to:
            query += " AND created_at <= %s"
            params.append(created_to)
        tasks = []
        # データベース接続とカーソルをwith文で管理
        with psycopg2.connect(self.dsn) as conn, conn.cursor() as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            # 取得した行をTaskオブジェクトに変換してリストに追加
            tasks.extend([
                Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    is_done=row[3],
                    created_at=row[4].isoformat() if row[4] else None,
                    updated_at=row[5].isoformat() if row[5] else None,
                )
                for row in rows
            ])
        return tasks

    async def get_task(self, task_id: str) -> Task | None:
        """タスクIDでタスクを取得する.

        Args:
            task_id (str): タスクID

        Returns:
            Task | None: 該当するタスク、存在しない場合はNone

        """
        query = "SELECT * FROM tasks WHERE id = %s"
        # 指定IDのタスクを1件取得
        with psycopg2.connect(self.dsn) as conn, conn.cursor() as cur:
            cur.execute(query, (task_id,))
            row = cur.fetchone()
            if row:
                return Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    is_done=row[3],
                    created_at=row[4].isoformat() if row[4] else None,
                    updated_at=row[5].isoformat() if row[5] else None,
                )
        return None

    async def create_task(self, task_create: TaskCreate) -> Task:
        """新しいタスクを作成する.

        Args:
            task_create (TaskCreate): 作成するタスク情報

        Returns:
            Task: 作成されたタスク

        """
        # UUIDで一意なIDを生成
        task_id = str(uuid.uuid4())
        # 現在時刻(UTC)を取得
        now = datetime.now(UTC).isoformat()
        query = (
            "INSERT INTO tasks (id, title, description, is_done, created_at, updated_at) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        # 新規タスクをDBに挿入
        with psycopg2.connect(self.dsn) as conn, conn.cursor() as cur:
            cur.execute(
                query,
                (
                    task_id,
                    task_create.title,
                    getattr(task_create, "description", None),
                    False,
                    now,
                    now,
                ),
            )
            conn.commit()
        # 作成したタスクを取得して返す
        return await self.get_task(task_id)

    async def update_task(self, task_id: str, task_update: TaskUpdate) -> Task | None:
        """タスクを更新する.

        Args:
            task_id (str): タスクID
            task_update (TaskUpdate): 更新内容

        Returns:
            Task | None: 更新後のタスク、存在しない場合はNone

        """
        # 更新日時を現在時刻(UTC)で設定
        now = datetime.now(UTC).isoformat()
        query = (
            "UPDATE tasks SET title = %s, description = %s, is_done = %s, updated_at = %s "
            "WHERE id = %s"
        )
        # 指定IDのタスクを更新
        with psycopg2.connect(self.dsn) as conn, conn.cursor() as cur:
            cur.execute(
                query,
                (
                    task_update.title,
                    getattr(task_update, "description", None),
                    task_update.is_done,
                    now,
                    task_id,
                ),
            )
            conn.commit()
        # 更新後のタスクを取得して返す
        return await self.get_task(task_id)

    async def delete_task(self, task_id: str) -> bool:
        """タスクを削除する.

        Args:
            task_id (str): タスクID

        Returns:
            bool: 削除に成功した場合はTrue、失敗した場合はFalse

        """
        query = "DELETE FROM tasks WHERE id = %s"
        # 指定IDのタスクを削除
        with psycopg2.connect(self.dsn) as conn, conn.cursor() as cur:
            cur.execute(query, (task_id,))
            deleted = cur.rowcount > 0
            conn.commit()
        return deleted
