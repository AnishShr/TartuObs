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
        self.bag_path = "/home/adl/obs_ws/src/h264_decoder/bags/_2023-06-29-12-21-44_70.bag"
        
        self.topics = [h264_front_left_camera_topic,
                       h264_front_right_camera_topic,
                       h264_rear_left_camera_topic,
                       h264_rear_right_camera_topic]
        
        # self.topics = [h264_front_left_camera_topic,
        #                h264_front_right_camera_topic]
        
        self.decoder = H264Decoder()

    def process_bag(self):
        bag = rosbag.Bag(self.bag_path, 'r')

        count_front_left_images = 0
        count_front_right_images = 0
        count_rear_left_images = 0
        count_rear_right_images = 0

        for topic, msg, t in bag.read_messages(topics=self.topics):             
            
            if topic == h264_front_left_camera_topic:
                img_frame = self.h264_decode(msg)
                
                if img_frame is not None:
                    count_front_left_images += 1
                    print("Front left image decoded")
            
            elif topic == h264_front_right_camera_topic:
                img_frame = self.h264_decode(msg)
                
                if img_frame is not None:
                    count_front_right_images += 1
                    print("Front right image decoded")
            
            elif topic == h264_rear_left_camera_topic:
                img_frame = self.h264_decode(msg)
                
                if img_frame is not None:
                    count_rear_left_images += 1
                    print("Rear left image decoded")

            elif topic == h264_rear_right_camera_topic:
                img_frame = self.h264_decode(msg)
                
                if img_frame is not None:
                    count_rear_right_images += 1
                    print("Rear right image decoded")


        print("Finished processing bag...")
        print("----------------------------------------")
        print(f"Decodable front left images: {count_front_left_images}")
        print(f"Decodable front right images: {count_front_right_images}")
        print(f"Decodable rear left images: {count_rear_left_images}")
        print(f"Decodable rear right images: {count_rear_right_images}")
        print("----------------------------------------")


    def h264_decode(self, msg):
        frames = self.decoder.decode(msg.data)

        if len(frames) == 0:
            return

        frame = cv2.cvtColor(frames[0].to_rgb().to_ndarray(), cv2.COLOR_RGB2BGR)

        return frame

if __name__ == "__main__":
    flow_compute = CountDecodables()
    flow_compute.process_bag()
    