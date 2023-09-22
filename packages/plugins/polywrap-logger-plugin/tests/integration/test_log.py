import logging
from polywrap_client import PolywrapClient
from polywrap_core import Uri
import pytest
from polywrap_logger_plugin import LoggerLogLevel
from _pytest.logging import LogCaptureFixture


@pytest.mark.parametrize("log_level", [0, 1, 2 ,3])
async def test_log_levels(
    client: PolywrapClient,
    caplog: LogCaptureFixture,
    log_level: LoggerLogLevel,
):
    caplog.set_level(logging.DEBUG)
    args_log = dict(message="Test message", level=log_level)

    assert client.invoke(
        uri=Uri.from_str("plugin/logger"),
        method="log",
        args=args_log,
    )
    last_record = caplog.records[-1] if caplog.records else None

    if log_level >= LoggerLogLevel.INFO:
        assert last_record
        assert last_record.levelno == (log_level + 1) * 10
        assert last_record.message == "Test message"
    else:
        assert last_record is None
