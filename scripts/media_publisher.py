from sensor_msgs.msg import Image


class VideoPublisher:


    def __init__(self, ros_publisher):
        self.__track = None
        self.__pub = ros_publisher
        self.__task = None
        self.br = CvBridge()

    def addTrack(self, track):
        """
        Add a track to be recorded.
        :param track: A :class:`aiortc.MediaStreamTrack`.
        """
        if track.kind == "video":
            self.__track = track

    async def start(self):
        """
        Start recording.
        """
        if track is not None
            if context.task is None:
                context.task = asyncio.ensure_future(self.__run_track(__track, __pub))

    async def stop(self):
        """
        Stop recording.
        """
        if self.__container:
            for track, context in self.__tracks.items():
                if context.task is not None:
                    context.task.cancel()
                    context.task = None
                    for packet in context.stream.encode(None):
                        self.__container.mux(packet)
            self.__tracks = {}

            if self.__container:
                self.__container.close()
                self.__container = None

    async def __run_track(self, track, pub):
        while True:
            try:
                frame = await track.recv()
            except MediaStreamError:
                return
            img = frame.to_ndarray(format='rgb24')
            pub.publish(br.cv2_to_imgmsg(img))
