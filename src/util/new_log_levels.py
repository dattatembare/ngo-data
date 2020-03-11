import logging
from typing import Any

PERF = 21
TRACE = 22
PERF_TEXT = 'PERF'
TRACE_TEXT = 'TRACE'


class MyLogger(logging.Logger):

    def trace(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)  # type: ignore

    def perf(self, msg: str, *args: Any, **kwargs: Any) -> None:
        if self.isEnabledFor(PERF):
            self._log(PERF, msg, args, **kwargs)  # type: ignore
