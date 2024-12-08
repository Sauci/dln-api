import ctypes
import os.path
import typing

from .types import *

notification_struct = DLN_NOTIFICATION()

class DLNApi(object):
    def __init__(self, shared_library_path: str):
        self._library = ctypes.cdll.LoadLibrary(os.path.abspath(shared_library_path))
        self._handle = HDLN()

    def __enter__(self):
        self.open_usb_device()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._library.DlnCloseHandle(self._handle)

    @property
    def device_sn(self) -> int:
        sn = ctypes.c_uint32()
        if api_result := DLN_RESULT(self._library.DlnGetDeviceSn(self._handle, ctypes.byref(sn))):
            raise RuntimeError(str(api_result))
        return sn.value

    @property
    def hardware_type(self) -> str:
        hw_type = DLN_HW_TYPE()
        if api_result := DLN_RESULT(self._library.DlnGetHardwareType(self._handle, ctypes.byref(hw_type))):
            raise RuntimeError(str(api_result))
        return hw_type

    @property
    def device_id(self) -> int:
        id = ctypes.c_uint32()
        if api_result := DLN_RESULT(self._library.DlnGetDeviceId(self._handle, ctypes.byref(id))):
            raise RuntimeError(str(api_result))
        return id.value

    def open_usb_device(self):
        if api_result := DLN_RESULT(self._library.DlnOpenUsbDevice(ctypes.byref(self._handle))):
            raise RuntimeError(str(api_result))

    def register_notification(self, notification_type: DLN_NOTIFICATION_TYPE, notification: typing.Callable):

        callback_function = callback_function_prototype(notification)

        notification_struct.type = notification_type.value  # callback notification type
        notification_struct.callback.function = callback_function
        notification_struct.callback.context = ctypes.py_object(self)

        if api_result := DLN_RESULT(self._library.DlnRegisterNotification(self._handle, notification_struct)):
            raise RuntimeError(str(api_result))

    def get_message(self, size: int = 8) -> bytearray:
        buffer = (ctypes.c_uint8 * 288)()
        size = ctypes.c_uint16(size)
        if api_result := DLN_RESULT(self._library.DlnGetMessage(ctypes.byref(self._handle), buffer, size)):
            raise RuntimeError(str(api_result))
        return bytearray(buffer)

    def send_message(self):
        data = ctypes.c_uint16(15)
        if api_result := DLN_RESULT(self._library.DlnSendMessage(ctypes.byref(data))):
            raise RuntimeError(str(api_result))
