#!/usr/bin/python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy




def callback(stick):
    vel = Twist()
    vel.angular.z = stick.axes[0]
    vel.linear.x = stick.axes[1]
    pub.publish(vel)

def main():
    rospy.Subscriber("diggy_joy", Joy, callback)
    rospy.init_node('turtle_joy', anonymous=True)
    rospy.spin()



if __name__ == '__main__':
    pub = rospy.Publisher('diggy_twist', Twist, queue_size=10)
    main()
