#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge
import cv2
import av
import numpy as np

class H264Decoder:
    def __init__(self):
        self.codec = av.CodecContext.create("h264", "r")

    def decode(self, encoded_frame):
        try:
            packet = av.Packet(encoded_frame)
            frames = self.codec.decode(packet)
        except av.AVError as e:
            print(("failed to decode, skipping package: " + str(e)))
            return []

        return frames


class DecoderNode:
    def __init__(self):
        
        self.image_pub = rospy.Publisher('/camera/decoded_image_raw', Image, queue_size=1)
        self.subscriber = rospy.Subscriber('/AGV_type_4_5_29/sensors/cameras/front_left/image_raw/h264', CompressedImage, self.callback, queue_size=1)
        self.decoder = H264Decoder()

    def callback(self, msg):

        frames = self.decoder.decode(msg.data)        
        
        if len(frames) == 0:
            return
        
        frame = cv2.cvtColor(frames[0].to_rgb().to_ndarray(), cv2.COLOR_RGB2BGR)
        # print(frame)

        bridge = CvBridge()
        ros_img_msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

        self.image_pub.publish(ros_img_msg)


        

if __name__ == '__main__':
    rospy.init_node('h264_decoder', anonymous=True)
    DecoderNode()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
