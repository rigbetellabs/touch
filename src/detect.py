#!/usr/bin/env python
from __future__ import print_function

import roslib
roslib.load_manifest('touch')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

# lower bound and upper bound for Green color
green_lower_bound = np.array([55, 155, 250])   
green_upper_bound = np.array([65, 255, 255])


class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("rviz1/camera1/image2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("rviz1/camera1/image",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    #(rows,cols,channels) = cv_image.shape
    #if cols > 60 and rows > 60 :
    #  cv2.circle(cv_image, (50,50), 10, 255)

    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, green_lower_bound, green_upper_bound)

    _ , contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    print(len(contours))

    cv2.imshow("Image window", hsv)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)