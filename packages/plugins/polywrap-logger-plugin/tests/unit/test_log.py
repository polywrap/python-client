import logging
from polywrap_core import InvokerClient
import pytest
from polywrap_logger_plugin import LoggerConfig, LoggerModule, ArgsLog, LogLevel
from _pytest.logging import LogCaptureFixture
from typing import Callable, cast


@pytest.mark.parametrize("config_level", list(LogLevel))
@pytest.mark.parametrize("log_level", list(LogLevel))
async def test_log_levels(
    caplog: LogCaptureFixture,
    valid_logger_config: Callable[[LogLevel], LoggerConfig],
    config_level: LogLevel,
    log_level: LogLevel,
):
    caplog.set_level(logging.DEBUG)
    logger_module = LoggerModule(valid_logger_config(config_level))
    args_log = ArgsLog(message="Test message", level=log_level)

    assert logger_module.log(args_log, cast(InvokerClient, None), None)
    last_record = caplog.records[-1] if caplog.records else None

    if log_level.value >= config_level.value:
        assert last_record
        assert last_record.levelno == (log_level.value + 1) * 10
        assert last_record.message == "Test message"
    else:
        assert last_record is None
