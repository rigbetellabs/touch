#!/usr/bin/env python
from __future__ import print_function, division

import roslib
roslib.load_manifest('touch')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import pyautogui

# lower bound and upper bound for Green color
green_lower_bound = np.array([55, 155, 250])   
green_upper_bound = np.array([65, 255, 255])

low_bounding = (71,101)
high_bounding = (568,378)

sw , sh = pyautogui.size()

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

    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    cropped = hsv[low_bounding[1]:high_bounding[1] , low_bounding[0]:high_bounding[0]]
    mask = cv2.inRange(cropped, green_lower_bound, green_upper_bound)

    _ , contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))

    if contours:
      cnt = contours[0]
      x,y,w,h = cv2.boundingRect(cnt)
      #print(x,y,w,h)
      click = ( (x+(w/2))/mask.shape[1] , (y+(h/2))/mask.shape[0] )
      print(click)
      pyautogui.moveTo(click[0]*sw , click[1]*sh)
      #pyautogui.click(click[0]*sw , click[1]*sh)

    cv2.imshow("Image window", mask)
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
