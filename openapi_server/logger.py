import functools
import inspect
import logging
import sys
from collections.abc import Callable
from logging import Formatter, Logger, StreamHandler


class ApiLogger:
    _instance: "ApiLogger" = None  # 型ヒントは文字列で前方参照
    _logger: Logger | None = None

    def __new__(cls) -> "ApiLogger":
        if cls._instance is None:
            instance = super().__new__(cls)
            instance._initialize_logger()
            cls._instance = instance
        return cls._instance

    def _initialize_logger(self) -> None:
        """ロガーの初期化."""
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

        # ハンドラーを全て削除し重複を防ぐ
        if self._logger.handlers:
            self._logger.handlers.clear()

        # ハンドラーの設定
        handler = StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)

        # フォーマッターの設定
        formatter = Formatter(
            "[%(asctime)s.%(msecs)03d] [%(levelname)s] (%(caller_func)s) %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        # ハンドラーの追加
        self._logger.addHandler(handler)

    def _log(self, level: int, message: str, func_name: str = "") -> None:
        """内部ログメソッド."""
        if not func_name:
            # 呼び出し元の関数名を取得
            frame = inspect.currentframe()
            if frame:
                caller_frame = frame.f_back.f_back  # 2レベル上のフレームを取得
                if caller_frame:
                    func_name = caller_frame.f_code.co_name
                frame = None  # 循環参照を防ぐ

        self._logger.log(level, message, extra={"caller_func": func_name})

    def debug(self, message: str, func_name: str = "") -> None:
        """DEBUGレベルのログを出力."""
        self._log(logging.DEBUG, message, func_name)

    def info(self, message: str, func_name: str = "") -> None:
        """INFOレベルのログを出力."""
        self._log(logging.INFO, message, func_name)

    def warning(self, message: str, func_name: str = "") -> None:
        """WARNINGレベルのログを出力."""
        self._log(logging.WARNING, message, func_name)

    def error(self, message: str, func_name: str = "") -> None:
        """ERRORレベルのログを出力."""
        self._log(logging.ERROR, message, func_name)

    def critical(self, message: str, func_name: str = "") -> None:
        """CRITICALレベルのログを出力."""
        self._log(logging.CRITICAL, message, func_name)


def log_function(level: str = "INFO") -> Callable:
    """関数の実行をログ出力するデコレータ.

    Args:
        level (str): ログレベル('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

    Returns:
        Callable: デコレータ関数.

    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: object, **kwargs: object) -> object:
            logger = get_logger()
            func_name = func.__name__
            log_method = getattr(logger, level.lower())

            # DEBUG時のみ引数をログ出力する
            if level.upper() == "DEBUG":
                args_str = ", ".join([str(arg) for arg in args[1:]])  # self を除外
                kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                logger.debug(
                    "Started with args: [%s], kwargs: {%s]", args_str, kwargs_str,
                )
            else:
                log_method("Started", func_name)

            try:
                result = func(*args, **kwargs)
            except Exception:
                logger.exception("Failed with error:")
                raise
            else:
                log_method("Completed successfully", func_name)
                return result

        return wrapper

    return decorator


def get_logger() -> ApiLogger:
    """ロガーインスタンスを取得."""
    return ApiLogger()
