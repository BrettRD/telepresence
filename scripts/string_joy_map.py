#!/usr/bin/python3

import rospy
import json
from std_msgs.msg import String
from sensor_msgs.msg import Joy



def callback_joy(stick):
    msg = {
            "axes": stick.axes,
            "buttons": stick.buttons
            }
    pub_str.publish(json.dumps(msg))

def callback_str(msg):
    stick = Joy()
    joy_packed = json.loads(msg.data)
    stick.axes = joy_packed["axes"]
    stick.buttons = joy_packed["buttons"]
    pub_joy.publish(stick)


def main():
    rospy.Subscriber("diggy_joy_in", Joy, callback_joy)
    rospy.Subscriber("diggy_str_in", String, callback_str)
    rospy.init_node('turtle_joy', anonymous=True)
    rospy.spin()



if __name__ == '__main__':
    pub_joy = rospy.Publisher('diggy_joy_out', Joy, queue_size=10)
    pub_str = rospy.Publisher('diggy_str_out', String, queue_size=10)

    main()
