from ..api import DLNApi
from ..errors import DLNException
from ..types import *


class SPIMaster(DLNApi):

    def __init__(self, port: int = 0):
        super().__init__()
        self._port = ctypes.c_uint8(port)

    @property
    def c_pol(self) -> int:
        c_pol = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiMasterGetCpol(self._handle, self._port, ctypes.byref(c_pol)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return c_pol.value

    @c_pol.setter
    def c_pol(self, c_pol: int = 0):
        c_pol = ctypes.c_uint8(c_pol)
        api_result = DLN_RESULT(self._library.DlnSpiMasterSetCpol(self._handle, self._port, c_pol))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def c_pha(self) -> int:
        c_pha = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiMasterGetCpha(self._handle, self._port, ctypes.byref(c_pha)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return c_pha.value

    @c_pha.setter
    def c_pha(self, c_pha: int):
        c_pha = ctypes.c_uint8(c_pha)
        api_result = DLN_RESULT(self._library.DlnSpiMasterSetCpha(self._handle, self._port, c_pha))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def frame_size(self) -> int:
        frame_size = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiMasterGetFrameSize(self._handle,
                                                                       self._port,
                                                                       ctypes.byref(frame_size)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return frame_size.value

    @frame_size.setter
    def frame_size(self, frame_size: int = 16):
        frame_size = ctypes.c_uint8(frame_size)
        api_result = DLN_RESULT(self._library.DlnSpiMasterSetFrameSize(self._handle, self._port, frame_size))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def frequency(self) -> int:
        frequency = ctypes.c_uint32()
        api_result = DLN_RESULT(
            self._library.DlnSpiMasterGetFrequency(self._handle, self._port, ctypes.byref(frequency)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return frequency.value

    @frequency.setter
    def frequency(self, frequency: int = 1000000):
        frequency = ctypes.c_uint32(frequency)
        actual_frequency = ctypes.c_uint32()
        api_result = DLN_RESULT(self._library.DlnSpiMasterSetFrequency(self._handle,
                                                                       self._port,
                                                                       frequency,
                                                                       ctypes.byref(actual_frequency)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        if frequency.value != actual_frequency.value:
            raise RuntimeError

    def read_write(self, tx_data: bytearray) -> bytearray:
        tx_data = (ctypes.c_uint8 * len(tx_data))(*tx_data)
        rx_data = (ctypes.c_uint8 * len(tx_data))(*([0] * len(tx_data)))
        api_result = DLN_RESULT(self._library.DlnSpiMasterReadWrite(self._handle,
                                                                    self._port,
                                                                    ctypes.c_uint16(len(tx_data)),
                                                                    ctypes.byref(tx_data),
                                                                    ctypes.byref(rx_data)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return bytearray(rx_data)

    def read_write_ss(self, tx_data: bytearray, ss: int) -> bytearray:
        tx_data = (ctypes.c_uint8 * len(tx_data))(*tx_data)
        rx_data = (ctypes.c_uint8 * len(tx_data))(*([0] * len(tx_data)))
        api_result = DLN_RESULT(self._library.DlnSpiMasterReadWriteSS(self._handle,
                                                                      self._port,
                                                                      ctypes.c_uint8(ss),
                                                                      ctypes.c_uint16(len(tx_data)),
                                                                      ctypes.byref(tx_data),
                                                                      ctypes.byref(rx_data)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return bytearray(rx_data)

    @property
    def enabled(self):
        enable = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiMasterIsEnabled(self._handle, self._port, ctypes.byref(enable)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return bool(enable.value)

    def enable(self):
        conflicts = ctypes.c_uint16()
        api_result = DLN_RESULT(self._library.DlnSpiMasterEnable(self._handle, self._port, ctypes.byref(conflicts)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        if conflicts.value:
            raise RuntimeError(conflicts.value)

    def disable(self, wait_for_transfer_completion: bool = False):
        wait_for_transfer_completion = ctypes.c_uint8(int(wait_for_transfer_completion))
        api_result = DLN_RESULT(self._library.DlnSpiMasterDisable(self._handle,
                                                                  self._port,
                                                                  wait_for_transfer_completion))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
