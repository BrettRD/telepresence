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
            #print("frame\n")
            #img = frame.to_ndarray("rgb24")
            #print(frame.format.name)
            frame = frame.to_rgb()
            #print(frame.format.name)
            img = frame.to_ndarray()
            #print("img\n")
            try:
                msg = self.__br.cv2_to_imgmsg(img)
                #msg = self.__br.cv2_to_imgmsg(img,  encoding='rgb8')
                msg.encoding = "rgb8"
            except CvBridgeError as e:
                print(e)
            #print("convert\n")

            pub.publish(msg)

            # This format conversion is hard won. Most obvious methods to convert the image format seem to hang the converter.
            # Image format conversions in pyav or cvbridge both silently fail (hang), no exceptions or return values.
            # the freeze doesn't seem to affect the rest of the async library, the data channel keeps going.
            # only passthrough seems to work.
