from .types import DLN_RESULT


class DLNException(Exception):
    def __init__(self, result: DLN_RESULT):
        super(DLNException, self).__init__(f'code {"{:02X}h".format(result.value)}: {str(result)}')
