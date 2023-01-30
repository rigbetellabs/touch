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
red_lower_bound = np.array([0, 200, 200])   
red_upper_bound = np.array([10, 225, 210])


class redclipper:

  def __init__(self):
    self.image_pub = rospy.Publisher("rviz1/camera1/image2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("rviz1/camera1/image",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, red_lower_bound, red_upper_bound)

    _ , contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    print((contours[1]))

    #x,y,w,h = cv2.boundingRect(contours[1])
    #mask = cv2.rectangle(mask,(x,y),(x+w,y+h),(0,255,0),2)

    cv2.imshow("Image window", mask)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = redclipper()
  rospy.init_node('red_clipper', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)