import abc

from ..api import DLNApi
from ..errors import DLNException
from ..types import *


class SPISlave(DLNApi):

    def __init__(self, shared_library_path='C:\\Program Files\\Diolan\\DLN\\redistributable\\direct_library\\dln.dll',
                 port: int = 0):
        super().__init__(shared_library_path=shared_library_path)
        self._port = ctypes.c_uint8(port)

    @abc.abstractmethod
    def on_callback_notification(self,
                                 event_count: int,
                                 event_type: int,
                                 port: int,
                                 buffer: bytearray) -> None:
        pass

    @staticmethod
    @callback_function_prototype
    def _callback_function(_: HDLN, context: ctypes.py_object) -> None:
        self: DLNApi = ctypes.cast(context, ctypes.py_object).value
        buffer = (ctypes.c_uint8 * DLN_MAX_MSG_SIZE)()
        event = DLN_SPI_SLAVE_DATA_RECEIVED_EV.from_buffer(buffer)
        while True:
            api_result = DLN_RESULT(self._library.DlnGetMessage(self._handle, buffer, DLN_MAX_MSG_SIZE))
            if dln_succeeded(api_result):
                self.on_callback_notification(event.eventCount,
                                              event.eventType,
                                              event.port,
                                              bytearray(event.buffer[0:event.size]))
            else:
                break

    @property
    def c_pol(self) -> int:
        """
        Retrieves the current value of clock polarity (CPOL).
        :return: The current clock polarity (CPOL) value.
        """
        c_pol = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveGetCpol(self._handle, self._port, ctypes.byref(c_pol)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return c_pol.value

    @c_pol.setter
    def c_pol(self, c_pol: int):
        """
        Sets the clock polarity (CPOL) value.
        :param c_pol: The clock polarity (CPOL) value. Can be 0 or 1.
        """
        c_pol = ctypes.c_uint8(c_pol)
        if api_result := DLN_RESULT(self._library.DlnSpiSlaveSetCpol(self._handle, self._port, c_pol)):
            raise DLNException(api_result)

    @property
    def c_pha(self) -> int:
        """
        Retrieves the current value of clock phase (CPHA).
        :return: The current clock phase (CPHA) value.
        """
        c_pha = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveGetCpha(self._handle, self._port, ctypes.byref(c_pha)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return c_pha.value

    @c_pha.setter
    def c_pha(self, c_pha: int):
        """
        Sets the clock phase (CPHA) value.
        :param c_pha: The clock phase (CPHA) value. Can be 0 or 1.
        """
        c_pha = ctypes.c_uint8(c_pha)
        api_result = DLN_RESULT(self._library.DlnSpiSlaveSetCpha(self._handle, self._port, c_pha))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def frame_size(self) -> int:
        """
        Retrieves the current size setting for SPI data frames.
        :return: The number of bits transmitted in a single frame. The DLN-series adapter supports 8 to 16 bits per
        frame.
        """
        frame_size = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveGetFrameSize(self._handle,
                                                                      self._port,
                                                                      ctypes.byref(frame_size)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return frame_size.value

    @frame_size.setter
    def frame_size(self, frame_size: int):
        """
        Sets the size of a single SPI data frame.
        :param frame_size: A number of bits to be transmitted during the single frame. The DLN-series adapter supports
        8 to 16 bits per frame.
        The frameSize parameter does not limit the size of the buffer transmitted to/from the SPI slave device, it only
         defines the minimum portion of data in this buffer.
        """
        frame_size = ctypes.c_uint8(frame_size)
        api_result = DLN_RESULT(self._library.DlnSpiSlaveSetFrameSize(self._handle, self._port, frame_size))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def idle_timeout(self) -> int:
        """
        Retrieves the current value of SS idle timeout.
        :return: The current SS idle timeout value in milliseconds.
        """
        timeout = ctypes.c_uint32()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveGetSSIdleTimeout(self._handle,
                                                                          self._port,
                                                                          ctypes.byref(timeout)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return timeout.value

    @idle_timeout.setter
    def idle_timeout(self, timeout: int):
        """
        Sets SS idle timeout.
        :param timeout: The SS idle timeout value specified in milliseconds (ms). The minimum value is 1ms, the maximum
        value is 1000ms.
        """
        timeout = ctypes.c_uint32(timeout)
        api_result = DLN_RESULT(self._library.DlnSpiSlaveSetSSIdleTimeout(self._handle, self._port, timeout))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def event(self) -> bool:
        """
        Retrieves information whether the SPI slave events are active or not.
        :return: Information whether the SPI slave port events are activated or not. There are two possible values:
        - True if SPI slave events are enabled.
        - False if SPI slave events are disabled.
        """
        enabled = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveIsEventEnabled(self._handle,
                                                                        self._port,
                                                                        ctypes.byref(enabled)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return bool(enabled.value)

    @event.setter
    def event(self, enable: bool):
        if enable:
            api_result = DLN_RESULT(self._library.DlnSpiSlaveEnableEvent(self._handle, self._port))
        else:
            api_result = DLN_RESULT(self._library.DlnSpiSlaveDisableEvent(self._handle, self._port))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def idle_event(self) -> bool:
        enabled = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveIsIdleEventEnabled(self._handle,
                                                                            self._port,
                                                                            ctypes.byref(enabled)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return bool(enabled.value)

    @idle_event.setter
    def idle_event(self, enable: bool):
        if enable:
            api_result = DLN_RESULT(self._library.DlnSpiSlaveEnableIdleEvent(self._handle, self._port))
        else:
            api_result = DLN_RESULT(self._library.DlnSpiSlaveDisableIdleEvent(self._handle, self._port))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def ss_rise_event(self) -> bool:
        enabled = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveIsSSRiseEventEnabled(self._handle,
                                                                              self._port,
                                                                              ctypes.byref(enabled)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return bool(enabled.value)

    @ss_rise_event.setter
    def ss_rise_event(self, enable: bool):
        if enable:
            api_result = DLN_RESULT(self._library.DlnSpiSlaveEnableSSRiseEvent(self._handle, self._port))
        else:
            api_result = DLN_RESULT(self._library.DlnSpiSlaveDisableSSRiseEvent(self._handle, self._port))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def event_size(self) -> int:
        event_size = ctypes.c_uint16()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveGetEventSize(self._handle,
                                                                      self._port,
                                                                      ctypes.byref(event_size)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return event_size.value

    @event_size.setter
    def event_size(self, size: int):
        size = ctypes.c_uint16(size)
        api_result = DLN_RESULT(self._library.DlnSpiSlaveSetEventSize(self._handle, self._port, size))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    def load_reply(self, size: int = 1, buffer: bytearray = bytearray((1, 2, 3, 4, 5, 6, 7, 8))):
        buffer = (ctypes.c_uint8 * size)(*buffer)
        size = ctypes.c_uint16(size)
        api_result = DLN_RESULT(self._library.DlnSpiSlaveLoadReply(self._handle, self._port, size, buffer))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    @property
    def enabled(self):
        enable = ctypes.c_uint8()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveIsEnabled(self._handle, self._port, ctypes.byref(enable)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return bool(enable.value)

    def enable(self):
        conflicts = ctypes.c_uint16()
        api_result = DLN_RESULT(self._library.DlnSpiSlaveEnable(self._handle, self._port, ctypes.byref(conflicts)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        if conflicts.value:
            raise RuntimeError(conflicts.value)

    def disable(self, wait_for_transfer_completion: bool = False):
        wait_for_transfer_completion = ctypes.c_uint8(int(wait_for_transfer_completion))
        api_result = DLN_RESULT(self._library.DlnSpiSlaveDisable(self._handle,
                                                                 self._port,
                                                                 wait_for_transfer_completion))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
