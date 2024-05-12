import sys
import time
from typing import NoReturn
from core.errors.error import unexpectedInputError
from core.variables.typevar import _ExitStatus

def str_to_bool(y_or_n : str):
    s = y_or_n.lower()
    if s in ['y', 'yes', 'true', 't', '1']:
        return True
    elif s in ['n', 'no', 'false', 'f', '0']:
        return False
    else:
        raise unexpectedInputError

def wait_and_exit(sleep_sec: int = 0, status: _ExitStatus = 0, /) -> NoReturn:
    time.sleep(sleep_sec)  # wait for sleep_sec second.
    sys.exit(status)  # process exit with status
