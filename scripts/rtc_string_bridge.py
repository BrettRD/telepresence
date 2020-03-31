#!/usr/bin/python3

#shamelessly copied from:
#https://github.com/aiortc/aiortc/blob/master/examples/datachannel-cli/cli.py

#

import argparse
import asyncio
import logging
import time

from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import BYE, ApprtcSignaling
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

import rospy
from std_msgs.msg import String

channel = None
loop = None

def callback_ros_data(message):
    global loop
    global channel
    if  loop != None:
        if  channel != None:
            loop.call_soon_threadsafe(channel.send, message.data)
            #channel.send(message.data)
        else:
            rospy.loginfo("channel not ready\n")
    else:
        rospy.loginfo("async_io loop not ready\n")


def callback_rtc_data(message):
    pub_data.publish(message)

#XXX need callbacks for audio and video in and out
#src/aiortc/contrib/media.py:378    handles frames:   frame = await track.recv()
# and it does so without regard for the frame type or content because ffmpeg is awesome.


async def run(pc, player, recorder, signaling, role):
    global channel

    def add_tracks():
        if player and player.audio:
            pc.addTrack(player.audio)
            rospy.loginfo("local created audio\n")

        if player and player.video:
            pc.addTrack(player.video)
            rospy.loginfo("local created video\n")
        #else:
        #    pc.addTrack(FlagVideoStreamTrack())


    @pc.on("track")
    def on_track(track):
        print("Receiving %s" % track.kind)
        recorder.addTrack(track)

    @pc.on("datachannel")
    def on_datachannel(data_channel):
        global channel
        channel = data_channel
        rospy.loginfo("remote created channel " + channel.label + "\n")
        #can there be more than one data channel?

        @channel.on("message")
        def on_message(message):
            #rospy.loginfo("received " + message + "\n")
            callback_rtc_data(message)

    # connect signaling
    await signaling.connect()

    if role == "offer":
        # send offer
        add_tracks()
        #XXX add a configurable label, make channel an argument
        channel = pc.createDataChannel("chat")
        rospy.loginfo("local created channel " + channel.label + "\n")

        await pc.setLocalDescription(await pc.createOffer())
        await signaling.send(pc.localDescription)

    # consume signaling
    while True:
        obj = await signaling.receive()

        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)
            await recorder.start()

            if obj.type == "offer":
                # send answer
                add_tracks()
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            pc.addIceCandidate(obj)
        elif obj is BYE:
            print("Exiting")
            break



if __name__ == '__main__':
    rospy.init_node('webrtc', anonymous=True)
    #pub_video = rospy.Publisher('video_out', Image, queue_size=10)
    pub_data = rospy.Publisher('data_out', String, queue_size=10)
    rospy.Subscriber("data_in", String, callback_ros_data)

    apprtc_room = rospy.get_param("~room")
    role = rospy.get_param("~role")

    #vid_src = rospy.get_param("~vid_src", "'/dev/video0', format='v4l2', options={'video_size': '640x480'")
    vid_src = None

    
    signaling = ApprtcSignaling(apprtc_room)
    #signaling = create_signaling(args)  #XXX eventiually move off apprtc, define a new signallng system.
    pc = RTCPeerConnection()

    # create media source
    #if vid_src:
    #    player = MediaPlayer(vid_src)
    #else:
    player = None

    # create media sink
    #if False:
    #    recorder = VideoPublisher(pub_video)
    #else:
    recorder = MediaBlackhole()


    # run event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            run(
                pc=pc,
                player=player,
                recorder=recorder,
                signaling=signaling,
                role=role,
            )
        )
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(recorder.stop())
        loop.run_until_complete(signaling.close())
        loop.run_until_complete(pc.close())

    rospy.spin()
