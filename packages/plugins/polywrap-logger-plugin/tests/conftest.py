import logging
import pytest
from polywrap_logger_plugin import LoggerConfig, LoggerLogLevel
from typing import Callable


@pytest.fixture
def valid_logger_config() -> Callable[[LoggerLogLevel], LoggerConfig]:
    def _valid_logger_config(level: LoggerLogLevel) -> LoggerConfig:
        return LoggerConfig(logger=logging.getLogger("test_logger"), level=level)
    return _valid_logger_config

