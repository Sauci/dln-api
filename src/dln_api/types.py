import ctypes
import enum

from .constants import *

DLN_HW_TYPE = ctypes.c_uint32
DLN_MSG_ID = ctypes.c_uint16


class DLN_RESULT(ctypes.c_uint16):
    def __str__(self):
        return {
            # define DLN_RES_ERROR_C(x)                                  (((DLN_RESULT)(0x80 + (x))))
            # define DLN_SUCCEEDED(Result)                               ((DLN_RESULT)(Result) < 0x40)
            # define DLN_WARNING(Result)	                                (((DLN_RESULT)(Result) >= 0x20) && ((DLN_RESULT)(Result) < 0x40))
            # define DLN_FAILED(Result)                                  ((DLN_RESULT)(Result) >= 0x40)
            0: 'DLN_RES_SUCCESS',
            1: 'DLN_RES_SUCCESSFUL_REINIT',
            2: 'DLN_RES_PENDING',
            0x20: 'DLN_RES_TRANSFER_CANCELLED',
            0x21: 'DLN_RES_VALUE_ROUNDED',
            0x81: 'DLN_RES_HARDWARE_NOT_FOUND',
            0x82: 'DLN_RES_OUTDATED_DRIVER',
            0x83: 'DLN_RES_FAIL',
            0x84: 'DLN_RES_MESSAGE_ABSENT',
            0x85: 'DLN_RES_BAD_PARAMETER',
            0x86: 'DLN_RES_MEMORY_ERROR',
            0x87: 'DLN_RES_NOT_INITIALIZED',
            0x88: 'DLN_RES_INVALID_COMMAND_SIZE',
            0x89: 'DLN_RES_INVALID_RESPONSE_SIZE',
            0x8A: 'DLN_RES_INVALID_MESSAGE_SIZE',
            0x8B: 'DLN_RES_NOTIFICATION_NOT_REGISTERED',
            0x8D: 'DLN_RES_TRANSACTION_TIMEOUT',
            # define DLN_RES_OPERATION_TIMEOUT                           DLN_RES_TRANSACTION_TIMEOUT
            # define DLN_RES_RESPONSE_WAIT_TIMEOUT                       DLN_RES_TRANSACTION_TIMEOUT
            0x8E: 'DLN_RES_DEVICE_REMOVED',
            0x8F: 'DLN_RES_INVALID_HANDLE',
            0x90: 'DLN_RES_INVALID_MESSAGE_TYPE',
            0x91: 'DLN_RES_NOT_IMPLEMENTED',
            # define DLN_RES_COMMAND_NOT_SUPPORTED                       DLN_RES_NOT_IMPLEMENTED
            0x92: 'DLN_RES_TOO_MANY_CONNECTIONS',
            0x93: 'DLN_RES_ALREADY_INITIALIZED',
            0x94: 'DLN_RES_CONNECTION_FAILED',
            0x95: 'DLN_RES_MUST_BE_DISABLED',
            0x96: 'DLN_RES_INTERNAL_ERROR',
            0x97: 'DLN_RES_DEVICE_NUMBER_OUT_OF_RANGE',
            0x98: 'DLN_RES_HOST_NAME_TOO_LONG',
            0x99: 'DLN_RES_ALREADY_CONNECTED',
            0x9A: 'DLN_RES_SINGLE_INSTANCE',
            0xA0: 'DLN_RES_CONNECTION_LOST',
            0xA1: 'DLN_RES_NOT_CONNECTED',
            0xA2: 'DLN_RES_MESSAGE_SENDING_FAILED',
            0xA3: 'DLN_RES_NO_FREE_STREAM',
            0xA4: 'DLN_RES_HOST_LOOKUP_FAILED',
            0xA5: 'DLN_RES_PIN_IN_USE',
            0xA6: 'DLN_RES_INVALID_LED_NUMBER',
            0xA7: 'DLN_RES_INVALID_LED_STATE',
            0xA8: 'DLN_RES_INVALID_PORT_NUMBER',
            0xA9: 'DLN_RES_INVALID_EVENT_TYPE',
            0xAA: 'DLN_RES_PIN_NOT_CONNECTED_TO_MODULE',
            0xAB: 'DLN_RES_INVALID_PIN_NUMBER',
            0xAC: 'DLN_RES_INVALID_EVENT_PERIOD',
            0xAD: 'DLN_RES_NON_ZERO_RESERVED_BIT',
            0xAE: 'DLN_RES_INVALID_BUFFER_SIZE',
            0xAF: 'DLN_RES_NO_FREE_DMA_CHANNEL',
            0xB3: 'DLN_RES_INVALID_PLANE_NUMBER',
            0xB4: 'DLN_RES_INVALID_ADDRESS',
            0xB5: 'DLN_RES_OVERFLOW',
            0xB6: 'DLN_RES_BUSY',
            0xB7: 'DLN_RES_DISABLED',
            0xB8: 'DLN_RES_SPI_INVALID_FRAME_SIZE',
            # define DLN_RES_INVALID_CHARACTER_LENGTH                    DLN_RES_SPI_INVALID_FRAME_SIZE
            0xB9: 'DLN_RES_SPI_MASTER_INVALID_SS_VALUE',
            # define DLN_RES_SPI_MASTER_INVALID_SS_NUMBER                DLN_RES_SPI_MASTER_INVALID_SS_VALUE
            # define DLN_RES_I2C_MASTER_SENDING_ADDRESS_FAILED           ((DLN_RESULT) 0xBA)
            # define DLN_RES_I2C_MASTER_SENDING_DATA_FAILED              ((DLN_RESULT) 0xBB)
            # define DLN_RES_I2C_MASTER_INVALID_MEM_ADDRESS_LENGTH       ((DLN_RESULT) 0xBC)
            # define DLN_RES_I2C_MASTER_ARBITRATION_LOST                 ((DLN_RESULT) 0xBD)
            # define DLN_RES_I2C_SLAVE_ADDRESS_NEEDED                    ((DLN_RESULT) 0xBE)
            0xBF: 'DLN_RES_INVALID_RESOLUTION',
            0xC0: 'DLN_RES_INVALID_CHANNEL_NUMBER',
            0xC1: 'DLN_RES_CHANNEL_DISABLED',
            0xC2: 'DLN_RES_ALL_CHANNELS_DISABLED',
            0xC3: 'DLN_RES_INVALID_FREQUENCY',
            # define DLN_RES_INVALID_BAUDRATE                            DLN_RES_INVALID_FREQUENCY
            0xC4: 'DLN_RES_PWM_INVALID_DUTY_CYCLE',
            0xC5: 'DLN_RES_INVALID_REPLY_TYPE',
            0xC6: 'DLN_RES_INVALID_DELAY_VALUE',
            0xC7: 'DLN_RES_INVALID_MODE',
            0xC8: 'DLN_RES_INVALID_CPOL',
            0xC9: 'DLN_RES_INVALID_CPHA',
            0xCA: 'DLN_RES_INVALID_TIMEOUT_VALUE',
            0xCB: 'DLN_RES_SPI_SLAVE_SS_IDLE_TIMEOUT',
            0xCC: 'DLN_RES_INVALID_PARITY',
            0xCD: 'DLN_RES_INVALID_STOPBITS',
            0xCE: 'DLN_RES_CONFIGURATION_NOT_SUPPORTED',
            0xD0: 'DLN_RES_NO_FREE_TIMER',
            0xD1: 'DLN_RES_VERIFICATION_ERROR',
            0xE0: 'DLN_RES_SOCKET_INITIALIZATION_FAILED',
            0xE1: 'DLN_RES_INSUFFICIENT_RESOURCES',
            0xE2: 'DLN_RES_INVALID_VALUE',
        }[self.value]


HDLN = ctypes.c_uint16
HANDLE = ctypes.c_void_p
HWND = ctypes.c_void_p
UINT = ctypes.c_uint
DWORD = ctypes.c_ulong

callback_function_prototype = ctypes.CFUNCTYPE(None, HDLN, ctypes.c_void_p)


class callback(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('function', callback_function_prototype),
                ('context', ctypes.py_object)]  # originally ctypes.c_void_p


class window_message(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('handle', HWND),
                ('message', UINT)]


class thread_message(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('thread', DWORD),
                ('message', UINT)]


class labview_event(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('eventRef', ctypes.c_void_p)]


class inner_enum(ctypes.Union):
    _fields_ = [("callback", callback),
                ("event", HANDLE),
                ("windowMessage", window_message),
                ("threadMessage", window_message),
                ("labviewEvent", labview_event),
                ("reserved", (ctypes.c_uint8 * 64))]


class DLN_NOTIFICATION(ctypes.Structure):
    _pack_ = 1
    _anonymous_ = ('inner_enum',)
    _fields_ = [('type', ctypes.c_uint16),
                ('inner_enum', inner_enum)]


class DLN_NOTIFICATION_TYPE(enum.Enum):
    DLN_NOTIFICATION_TYPE_NO_NOTIFICATION = 0x00
    DLN_NOTIFICATION_TYPE_CALLBACK = 0x01
    DLN_NOTIFICATION_TYPE_EVENT_OBJECT = 0x02
    DLN_NOTIFICATION_TYPE_WINDOW_MESSAGE = 0x03
    DLN_NOTIFICATION_TYPE_THREAD_MESSAGE = 0x04
    DLN_NOTIFICATION_TYPE_LAB_VIEW_EVENT = 0x05


class DLN_MSG_HEADER(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('size', ctypes.c_uint16),
                ('msgId', DLN_MSG_ID),
                ('echoCounter', ctypes.c_uint16),
                ("handle", HDLN)]


class DLN_SPI_SLAVE_DATA_RECEIVED_EV(ctypes.Structure):
    _pack_ = 1
    _fields_ = [('header', DLN_MSG_HEADER),
                ('eventCount', ctypes.c_uint16),
                ('eventType', ctypes.c_uint8),
                ('port', ctypes.c_uint8),
                ('size', ctypes.c_uint16),
                ("buffer", (ctypes.c_uint8 * DLN_SPI_SLAVE_BUFFER_SIZE))]
