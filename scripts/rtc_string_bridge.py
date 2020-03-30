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


import rospy
from std_msgs.msg import String

channel = None
loop = None

def callback_ros(message):
    global loop
    global channel
    if  loop != None:
        if  channel != None:
            loop.call_soon_threadsafe(channel.send, message.data)
            #channel.send(message.data)
        else:
            rospy.loginfo("channel not ready")
    else:
        rospy.loginfo("loop not ready")


def callback_dc(message):
    pub.publish(message)



async def consume_signaling(pc, signaling):
    while True:
        obj = await signaling.receive()

        if isinstance(obj, RTCSessionDescription):
            await pc.setRemoteDescription(obj)

            if obj.type == "offer":
                # send answer
                await pc.setLocalDescription(await pc.createAnswer())
                await signaling.send(pc.localDescription)
        elif isinstance(obj, RTCIceCandidate):
            pc.addIceCandidate(obj)
        elif obj is BYE:
            print("Exiting")
            break


async def run_answer(pc, signaling):
    await signaling.connect()

    @pc.on("datachannel")
    def on_datachannel(data_channel):
        global channel
        channel = data_channel
        rospy.loginfo("remote created channel " + data_channel.label)
        #channel_log(channel, "-", "created by remote party")

        @channel.on("message")
        def on_message(message):
            rospy.loginfo("received " + message)
            callback_dc(message)

#            channel_log(channel, "<", message)
#            if isinstance(message, str) and message.startswith("ping"):
#                # reply
#                channel_send(channel, "pong" + message[4:])

    await consume_signaling(pc, signaling)


async def run_offer(pc, signaling):
    global channel
    await signaling.connect()

    channel = pc.createDataChannel("chat")
    rospy.loginfo("local created channel " + channel.label)
    #channel_log(channel, "-", "created by local party")

    async def send_pings():
        while True:
            channel_send(channel, "ping %d" % current_stamp())
            await asyncio.sleep(1)

    @channel.on("open")
    def on_open():
        asyncio.ensure_future(send_pings())

    @channel.on("message")
    def on_message(message):
        rospy.loginfo("received " + message)
        callback_dc(message)

#        channel_log(channel, "<", message)
#        if isinstance(message, str) and message.startswith("pong"):
#            elapsed_ms = (current_stamp() - int(message[5:])) / 1000
#            print(" RTT %.2f ms" % elapsed_ms)

    # send offer
    await pc.setLocalDescription(await pc.createOffer())
    await signaling.send(pc.localDescription)

    await consume_signaling(pc, signaling)



if __name__ == '__main__':
    pub = rospy.Publisher('diggy_data_out', String, queue_size=10)
    rospy.Subscriber("diggy_data_in", String, callback_ros)
    rospy.init_node('diggy_webrtc', anonymous=True)

    apprtc_room = rospy.get_param("~room")
    signaling = ApprtcSignaling(apprtc_room)
    pc = RTCPeerConnection()

    role = rospy.get_param("~role")
    if role == "offer":
        coro = run_offer(pc, signaling)
    else:
        coro = run_answer(pc, signaling)

    # run event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(coro)
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(pc.close())
        loop.run_until_complete(signaling.close())

    rospy.spin()
