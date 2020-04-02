import asyncio

import numpy as np, cv2

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class VideoPublisher:


    def __init__(self, ros_publisher):
        self.__track = None
        self.__pub = ros_publisher
        self.__task = None
        self.__br = CvBridge()


    def addTrack(self, track):
        """
        Add a track to be recorded.
        :param track: A :class:`aiortc.MediaStreamTrack`.
        """
        if track.kind == "video":
            self.__track = track
            print("added video track\n")

    async def start(self):
        """
        Start recording.
        """
        if self.__track is not None:
            if self.__task is None:
                self.__task = asyncio.ensure_future(self.__run_track(self.__track, self.__pub))
                print("started video rx task\n")

    async def stop(self):
        """
        Stop recording.
        """
        #clean up storage media etc, nothing to do.

    async def __run_track(self, track, pub):
        while True:
            try:
                frame = await track.recv()
            except MediaStreamError as e:
                print("run_track failed with " + e)
                return
            frame = frame.to_rgb()
            img = frame.to_ndarray()
            try:
                msg = self.__br.cv2_to_imgmsg(img)
                msg.encoding = "rgb8"
            except CvBridgeError as e:
                print(e)
            pub.publish(msg)
