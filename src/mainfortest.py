import time

from dln_api.types import *

library = ctypes.cdll.LoadLibrary('C:\\Program Files\\Diolan\\DLN\\redistributable\\direct_library\\dln.dll')

handle = HDLN(0)
port = ctypes.c_uint8(0)


@callback_function_prototype
def cbk(h: HDLN, __: ctypes.c_void_p):
    print(f'sizeof h = {ctypes.sizeof(HDLN)} sizeof context = {ctypes.sizeof(ctypes.c_void_p)}')
    buffer = (ctypes.c_uint8 * DLN_MAX_MSG_SIZE)()
    event = DLN_SPI_SLAVE_DATA_RECEIVED_EV.from_buffer(buffer)
    while library.DlnGetMessage(h, buffer, DLN_MAX_MSG_SIZE) == 0:
        print(event.buffer[0], h)


notification = DLN_NOTIFICATION()
notification.type = ctypes.c_uint16(1)
notification.callback.function = cbk
notification.callback.context = None

library.DlnOpenUsbDevice(ctypes.byref(handle))
library.DlnSpiSlaveDisable(handle, port, ctypes.c_uint8(1))
library.DlnRegisterNotification(handle, notification)
library.DlnSpiSlaveEnableEvent(handle, port)

conflict = ctypes.c_uint16()
library.DlnSpiSlaveEnable(handle, port, ctypes.byref(conflict))
time.sleep(10)
