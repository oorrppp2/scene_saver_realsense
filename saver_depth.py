## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

###############################################
##      Open CV and Numpy integration        ##
###############################################

import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

align_to = rs.stream.color
align = rs.align(align_to)
# Start streaming
pipeline.start(config)
sq = 0
try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        color_frame = frames.get_color_frame()
        sq += 1
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        aligned_depth_frame = aligned_frames.get_depth_frame()
        aligned_depth_image = np.asanyarray(aligned_depth_frame.get_data())

        # Show images
        cv2.imshow('Color', color_image)
        cv2.imshow('Depth', aligned_depth_image)
        key = cv2.waitKey(1)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        if key == ord('s'):
            cv2.imwrite("/home/vision/kist_datasets/scene2/color_"+str(sq)+".png", color_image)
            cv2.imwrite("/home/vision/kist_datasets/scene2/depth_"+str(sq)+".png", aligned_depth_image)
        if key == ord('q'):
            break

finally:

    # Stop streaming
    pipeline.stop()
