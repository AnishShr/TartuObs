import rosbag
from sensor_msgs.msg import CompressedImage
import av
import cv2
import matplotlib.pyplot as plt
from collections import deque
import numpy as np


h264_front_left_camera_topic = '/AGV_type_4_5_29/sensors/cameras/front_left/image_raw/h264'
h264_front_right_camera_topic = '/AGV_type_4_5_29/sensors/cameras/front_right/image_raw/h264'
h264_rear_left_camera_topic = '/AGV_type_4_5_29/sensors/cameras/rear_left/image_raw/h264'
h264_rear_right_camera_topic = '/AGV_type_4_5_29/sensors/cameras/rear_right/image_raw/h264'

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


class CountDecodables:

    def __init__(self):
        self.bag_path = "/home/adl/obs_ws/src/h264_decoder/bags/_2023-06-28-12-23-25_37.bag"


    def process_bag(self):
        bag = rosbag.Bag(self.bag_path, 'r')

        count_front_left_images = 0
        count_front_right_images = 0
        count_rear_left_images = 0
        count_rear_right_images = 0

        decoder = H264Decoder()
        for _, msg, _ in bag.read_messages(topics=h264_front_left_camera_topic):
            frames = decoder.decode(msg.data)        
    
            if len(frames) > 0:
                count_front_left_images += 1

        decoder = H264Decoder()
        for _, msg, _ in bag.read_messages(topics=h264_front_right_camera_topic):
            frames = decoder.decode(msg.data)        
    
            if len(frames) > 0:
                count_front_right_images += 1
        
        decoder = H264Decoder()
        for _, msg, _ in bag.read_messages(topics=h264_rear_left_camera_topic):
            frames = decoder.decode(msg.data)        
    
            if len(frames) > 0:
                count_rear_left_images += 1

        decoder = H264Decoder()
        for _, msg, _ in bag.read_messages(topics=h264_rear_right_camera_topic):
            frames = decoder.decode(msg.data)        
    
            if len(frames) > 0:
                count_rear_right_images += 1


        print("Finished processing bag...")
        print("----------------------------------------")
        print(f"Decodable front left images: {count_front_left_images}")
        print(f"Decodable front right images: {count_front_right_images}")
        print(f"Decodable rear left images: {count_rear_left_images}")
        print(f"Decodable rear right images: {count_rear_right_images}")
        print("----------------------------------------")


if __name__ == "__main__":
    count_decoded = CountDecodables()
    count_decoded.process_bag()
    