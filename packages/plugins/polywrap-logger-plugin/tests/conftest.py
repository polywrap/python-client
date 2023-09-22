import logging
import pytest
from polywrap_logger_plugin import LoggerConfig, LogLevel
from typing import Callable


@pytest.fixture
def valid_logger_config() -> Callable[[LogLevel], LoggerConfig]:
    def _valid_logger_config(level: LogLevel) -> LoggerConfig:
        return LoggerConfig(logger=logging.getLogger("test_logger"), level=level)
    return _valid_logger_config

