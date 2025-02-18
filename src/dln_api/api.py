import abc
import os
import platform
import sys

from .errors import DLNException
from .types import *

notification_struct = DLN_NOTIFICATION()


def bytearray_to_str(byte_array: bytearray) -> str:
    return ' '.join('{:02X}'.format(b) for b in byte_array)


class DLNApi(abc.ABC):
    """
    DLNApi is the base class for all different DLN APIs, such as the SPI-master API, SPI-slave API and so on.
    """

    def __init__(self):
        if sys.platform in ('linux', 'linux2'):
            extension = 'so'
        elif sys.platform == 'win32':
            extension = 'dll'
        else:
            raise Exception(f'Unsupported platform {sys.platform}')

        if platform.architecture()[0] == '64bit':
            name = 'x64'
        elif platform.architecture()[0] == '32bit':
            name = 'x86'
        else:
            raise Exception(f'Unsupported architecture {platform.architecture()[0]}')

        self._library = ctypes.cdll.LoadLibrary(os.path.join(os.path.dirname(__file__), 'libs', f'{name}.{extension}'))
        self._handle = HDLN()
        self._message_buffer = None

    def __enter__(self):
        self.open_usb_device()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._library.DlnCloseHandle(self._handle)

    @staticmethod
    @callback_function_prototype
    @abc.abstractmethod
    def _callback_function(_: HDLN, context: ctypes.py_object) -> None:
        pass

    @property
    def device_sn(self) -> int:
        sn = ctypes.c_uint32()
        api_result = DLN_RESULT(self._library.DlnGetDeviceSn(self._handle, ctypes.byref(sn)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return sn.value

    @property
    def hardware_type(self) -> str:
        hw_type = DLN_HW_TYPE()
        api_result = DLN_RESULT(self._library.DlnGetHardwareType(self._handle, ctypes.byref(hw_type)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return hw_type

    @property
    def device_id(self) -> int:
        identifier = ctypes.c_uint32()
        api_result = DLN_RESULT(self._library.DlnGetDeviceId(self._handle, ctypes.byref(identifier)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return identifier.value

    def restart(self) -> None:
        api_result = DLN_RESULT(self._library.DlnRestart(self._handle))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    def open_device(self, device_number: int = 0) -> None:
        device_number = ctypes.c_uint32(device_number)
        api_result = DLN_RESULT(self._library.DlnOpenDevice(device_number, ctypes.byref(self._handle)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    def open_device_by_sn(self, sn: int) -> None:
        sn = ctypes.c_uint32(sn)
        if api_result := DLN_RESULT(self._library.DlnOpenDeviceBySn(sn, ctypes.byref(self._handle))):
            raise DLNException(api_result)

    def open_usb_device(self) -> None:
        api_result = DLN_RESULT(self._library.DlnOpenUsbDevice(ctypes.byref(self._handle)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    def register_notification(self, notification_type: DLN_NOTIFICATION_TYPE) -> None:
        notification_struct.type = notification_type.value  # callback notification type
        notification_struct.callback.function = self._callback_function
        notification_struct.callback.context = ctypes.py_object(self)

        api_result = DLN_RESULT(self._library.DlnRegisterNotification(self._handle, notification_struct))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    def unregister_notification(self) -> None:
        api_result = DLN_RESULT(self._library.DlnUnregisterNotification(self._handle))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)

    def get_message(self, size: int = DLN_MAX_MSG_SIZE) -> bytearray:
        message_buffer = (ctypes.c_uint8 * DLN_MAX_MSG_SIZE)()
        size = ctypes.c_uint16(size)
        api_result = DLN_RESULT(self._library.DlnGetMessage(self._handle, message_buffer, size))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
        return bytearray(message_buffer)

    def send_message(self) -> None:
        data = ctypes.c_uint16(15)
        api_result = DLN_RESULT(self._library.DlnSendMessage(ctypes.byref(data)))
        if not dln_succeeded(api_result):
            raise DLNException(api_result)
