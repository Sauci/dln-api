import ctypes

DLN_MAX_MSG_SIZE = 288
DLN_SPI_SLAVE_BUFFER_SIZE = 256


def dln_succeeded(result: ctypes.c_uint16) -> bool:
    return result.value < 0x40
