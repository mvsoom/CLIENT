"""
Write descriptions of a video stream to stdout.

Usage to append to a file in realtime:

    python -u describe_stream.py [...] >> descriptions

The -u flag disables buffering.
"""
import cv2
import threading
import argparse
from time import time, sleep
from describe_frame import describe


MONITOR = "monitor"
CURRENTFRAME = None
EXITCODE = 1


def stream(name, monitor):
    global CURRENTFRAME, EXITCODE

    cap = cv2.VideoCapture(name)
    if not cap.isOpened():
        raise RuntimeError(f"Error opening video stream: {name}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                # Likely EOF or stream closed
                EXITCODE = 0
                break

            global CURRENTFRAME
            CURRENTFRAME = frame

            if monitor:
                cv2.imshow(MONITOR, frame)
                delay_msec = int(1000/fps)
                if cv2.waitKey(delay_msec) & 0xFF == ord('q'):
                    # User pressed q
                    EXITCODE = 0
                    break
            else:
                delay_sec = float(1/fps)
                sleep(delay_sec)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        if monitor:
            cv2.destroyWindow(MONITOR)


def main(args):
    streaming_thread = threading.Thread(target=stream, args=(args.name, args.monitor))
    streaming_thread.daemon = True
    streaming_thread.start()

    timeoffset = time()
    frameindex = 0

    while streaming_thread.is_alive():
        if CURRENTFRAME is None:
            continue

        frame = CURRENTFRAME.copy()
        timestamp = time() - timeoffset
        description = describe(frame)

        if args.timestamp:
            print(timestamp, description)
        else:
            print(description)
        
        if args.dumpframes is not None:
            frameindex += 1
            cv2.imwrite(args.dumpframes % frameindex, frame)
    
    return EXITCODE


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Write descriptions of a video stream to stdout')
    parser.add_argument('name', nargs='?', default=0, help='Name of the device to open with cv2. If not supplied, open device at 0')
    parser.add_argument('--monitor', action='store_true', help='Whether to monitor the stream in realtime')
    parser.add_argument('--timestamp', action='store_true', help='Write timestamps of the described frames')
    parser.add_argument('--dumpframes', nargs='?', const='', help='Write out processed frames. If arg is given, use it as the basename')

    args = parser.parse_args()

    if args.dumpframes is not None:
        basename = args.dumpframes or str(args.name)
        args.dumpframes = basename + '.%.6i.jpg'

    exit(main(args))