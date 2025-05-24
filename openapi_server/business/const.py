from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定クラス.

    環境変数から設定値を読み込みます。

    Attributes:
        APP_POSTGRES_USER (str): PostgreSQLのユーザ名.
        APP_POSTGRES_PASSWORD (str): PostgreSQLのパスワード.
        APP_POSTGRES_HOST (str): PostgreSQLのホスト名.
        APP_POSTGRES_PORT (int): PostgreSQLのポート番号.
        APP_POSTGRES_DB (str): PostgreSQLのデータベース名.

    """

    APP_POSTGRES_USER: str = "user"
    APP_POSTGRES_PASSWORD: str = ""  # 必ず環境変数で設定してください
    APP_POSTGRES_HOST: str = "todo_db"
    APP_POSTGRES_PORT: int = 5432
    APP_POSTGRES_DB: str = "todo"

    @property
    def postgres_dsn(self) -> str:
        """PostgreSQLのDSNを生成して返します.

        Returns:
            str: DSN文字列.

        """
        return (
            f"postgresql://{self.APP_POSTGRES_USER}:{self.APP_POSTGRES_PASSWORD}"
            f"@{self.APP_POSTGRES_HOST}:{self.APP_POSTGRES_PORT}/{self.APP_POSTGRES_DB}"
        )


# グローバル設定インスタンス
settings = Settings()
