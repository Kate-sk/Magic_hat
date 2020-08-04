#!/usr/bin/env python
# license removed for brevity

import natnet
import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

global pub
rospy.init_node('kate_talker', anonymous=True)
pub = rospy.Publisher('optitrack_data', PoseStamped, queue_size=10)


def kate_cb(one, two, three):
    global pub
    data = PoseStamped()

    data.header.stamp = rospy.Time.now()
    data.pose.position.x = one[0].position[1] * (-1)
    data.pose.position.y = one[0].position[0]
    data.pose.position.z = one[0].position[2]

    # x = RotationAxis.x * sin(RotationAngle / 2)
    # y = RotationAxis.y * sin(RotationAngle / 2)
    # z = RotationAxis.z * sin(RotationAngle / 2)
    # w = cos(RotationAngle / 2)

    z1 = one[0].orientation[2]
    w1 = one[0].orientation[3]
    alpha = 2 * math.acos(w1)
    if (z1 < 0):
        alpha = -alpha
    if ((alpha > 6) | (alpha < (-6))):
        alpha = 0
    data.pose.orientation.z = alpha
    print(alpha)
    # data.pose.orientation.x = one[0].orientation[0]
    # data.pose.orientation.y = one[0].orientation[1]
    # data.pose.orientation.z = one[0].orientation[2]
    # data.pose.orientation.w = one[0].orientation[3]

    # pub = rospy.Publisher('optitrack_data', PoseStamped, queue_size=10)
    # rospy.init_node('kate_talker', anonymous=True)
    rate = rospy.Rate(100)  # 100hz
    # rospy.sleep(0.01)
    # rate.sleep()
    pub.publish(data)


if __name__ == '__main__':
    client = natnet.Client.connect(server='192.168.2.41')
    try:
        client.set_callback(kate_cb)
        client.spin()
    except rospy.ROSInterruptException:
        pass


