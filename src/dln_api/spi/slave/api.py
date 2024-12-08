import ctypes

from dln_api.api import DLNApi
from dln_api.types import *


class SPISlave(DLNApi):

    def __init__(self, shared_library_path='C:\\Program Files\\Diolan\\DLN\\redistributable\\direct_library\\dln.dll',
                 port: int = 0):
        super().__init__(shared_library_path=shared_library_path)
        self._port = ctypes.c_uint8(port)

    @staticmethod
    def get_instance_from_context(context: ctypes.py_object):
        return ctypes.cast(context, ctypes.py_object).value

    @property
    def c_pol(self) -> int:
        c_pol = ctypes.c_uint8()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveGetCpol(self._handle, self._port, ctypes.byref(c_pol))):
            raise RuntimeError(str(api_result))
        return c_pol.value

    @c_pol.setter
    def c_pol(self, c_pol: int):
        c_pol = ctypes.c_uint8(c_pol)
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveSetCpol(self._handle, self._port, c_pol)):
            raise RuntimeError(str(api_result))

    @property
    def c_pha(self) -> int:
        c_pha = ctypes.c_uint8()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveGetCpha(self._handle, self._port, ctypes.byref(c_pha))):
            raise RuntimeError(str(api_result))
        return c_pha.value

    @c_pha.setter
    def c_pha(self, c_pha: int):
        c_pha = ctypes.c_uint8(c_pha)
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveSetCpha(self._handle, self._port, c_pha)):
            raise RuntimeError(str(api_result))

    @property
    def frame_size(self) -> int:
        frame_size = ctypes.c_uint8()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveGetFrameSize(self._handle,
                                                                          self._port,
                                                                          ctypes.byref(frame_size))):
            raise RuntimeError(str(api_result))
        return frame_size.value

    @frame_size.setter
    def frame_size(self, frame_size: int):
        frame_size = ctypes.c_uint8(frame_size)
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveSetFrameSize(self._handle, self._port, frame_size)):
            raise RuntimeError(str(api_result))

    @property
    def idle_timeout(self) -> int:
        timeout = ctypes.c_uint32()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveGetSSIdleTimeout(self._handle,
                                                                              self._port,
                                                                              ctypes.byref(timeout))):
            raise RuntimeError(str(api_result))
        return timeout.value

    @idle_timeout.setter
    def idle_timeout(self, timeout: int):
        timeout = ctypes.c_uint32(timeout)
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveSetSSIdleTimeout(self._handle, self._port, timeout)):
            raise RuntimeError(str(api_result))

    @property
    def event(self) -> bool:
        enabled = ctypes.c_uint8()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveIsEventEnabled(self._handle,
                                                                            self._port,
                                                                            ctypes.byref(enabled))):
            raise RuntimeError(str(api_result))
        return bool(enabled.value)

    @event.setter
    def event(self, enable: bool):
        if enable:
            if api_result := DLN_RESULT(self._library.DlnSpiSlaveEnableEvent(self._handle, self._port)):
                raise RuntimeError(str(api_result))
        else:
            if api_result := DLN_RESULT(self._library.DlnSpiSlaveDisableEvent(self._handle, self._port)):
                raise RuntimeError(str(api_result))

    @property
    def idle_event(self) -> bool:
        enabled = ctypes.c_uint8()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveIsIdleEventEnabled(self._handle,
                                                                                self._port,
                                                                                ctypes.byref(enabled))):
            raise RuntimeError(str(api_result))
        return bool(enabled.value)

    @idle_event.setter
    def idle_event(self, enable: bool):
        if enable:
            if api_result := DLN_RESULT(self._library.DlnSpiSlaveEnableIdleEvent(self._handle, self._port)):
                raise RuntimeError(str(api_result))
        else:
            if api_result := DLN_RESULT(self._library.DlnSpiSlaveDisableIdleEvent(self._handle, self._port)):
                raise RuntimeError(str(api_result))

    @property
    def ss_rise_event(self) -> bool:
        enabled = ctypes.c_uint8()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveIsSSRiseEventEnabled(self._handle,
                                                                                  self._port,
                                                                                  ctypes.byref(enabled))):
            raise RuntimeError(str(api_result))
        return bool(enabled.value)

    @ss_rise_event.setter
    def ss_rise_event(self, enable: bool):
        if enable:
            if api_result := DLN_RESULT(self._library.DlnSpiSlaveEnableSSRiseEvent(self._handle, self._port)):
                raise RuntimeError(str(api_result))
        else:
            if api_result := DLN_RESULT(self._library.DlnSpiSlaveDisableSSRiseEvent(self._handle, self._port)):
                raise RuntimeError(str(api_result))

    @property
    def event_size(self) -> int:
        event_size = ctypes.c_uint16()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveGetEventSize(self._handle,
                                                                          self._port,
                                                                          ctypes.byref(event_size))):
            raise RuntimeError(str(api_result))
        return event_size.value

    @event_size.setter
    def event_size(self, size: int):
        size = ctypes.c_uint16(size)
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveSetEventSize(self._handle, self._port, size)):
            raise RuntimeError(str(api_result))

    def load_reply(self, size: int = 1, buffer: bytearray = bytearray((1, 2, 3, 4, 5, 6, 7, 8))):
        buffer = (ctypes.c_uint8 * size)(*buffer)
        size = ctypes.c_uint16(size)
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveLoadReply(self._handle, self._port, size, buffer)):
            raise RuntimeError(str(api_result))

    def enable(self):
        conflicts = ctypes.c_uint16()
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveEnable(self._handle, self._port, ctypes.byref(conflicts))):
            raise RuntimeError(str(api_result))
        if conflicts.value:
            raise RuntimeError(conflicts.value)

    def disable(self, wait_for_transfer_completion: bool = False):
        wait_for_transfer_completion = ctypes.c_uint8(int(wait_for_transfer_completion))
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveDisable(self._handle,
                                                                     self._port,
                                                                     wait_for_transfer_completion)):
            raise RuntimeError(str(api_result))
