import faulthandler
import time

from dln_api import *


def bytearray_to_str(byte_array: bytearray) -> str:
    return ' '.join('{:02X}'.format(b) for b in byte_array)


if __name__ == '__main__':
    faulthandler.enable()


    class SPI(SPISlave):
        pass

        def on_callback_notification(self,
                                     event_count: int,
                                     event_type: int,
                                     port: int,
                                     buffer: bytearray) -> None:
            print(f'event_count = {event_count}, '
                  f'event_type = {event_type}, '
                  f'port = {port}, '
                  f'buffer = {bytearray_to_str(buffer)}')


    with SPI(port=0) as dln:
        dln.disable(wait_for_transfer_completion=False)

        dln.idle_timeout = 1000
        dln.c_pol = 0
        dln.c_pha = 0
        dln.event_size = 1
        dln.event = True
        dln.idle_event = False
        dln.ss_rise_event = False
        dln.frame_size = 8

        dln.register_notification(notification_type=DLN_NOTIFICATION_TYPE.DLN_NOTIFICATION_TYPE_CALLBACK)

        print(f'idle timeout = {dln.idle_timeout}, '
              f'CPOL = {dln.c_pol}, '
              f'CPHA = {dln.c_pha}, '
              f'event size = {dln.event_size}, '
              f'event = {dln.event}, '
              f'idle event = {dln.idle_event}, '
              f'SS rise event = {dln.ss_rise_event}, '
              f'frame size = {dln.frame_size}')

        dln.enable()

        time.sleep(2)
        #
        # for i in range(10000):
        #     print(f'loop index = {i}')
        #     try:
        #         result = dln.get_message()
        #         print(f'result = {bytearray_to_str(result)}')
        #     except RuntimeError as e:
        #         print(e)
