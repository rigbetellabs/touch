#!/usr/bin/env python3
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
import socket
import json
import numpy as np

click_co = [ 0 , 0 ]
click_flag = 0

# lower bound and upper bound for Green color
green_lower_bound = np.array([55, 155, 250])   
green_upper_bound = np.array([65, 255, 255])

low_bounding = (72,77)
high_bounding = (567,402)

#Screen Selection
ScreenNumber = 3

#Screen Width & Screen Height

#Left Screen
lsw = 1920
lsh = 960

#Middle Screen
msw = 960
msh = 960

#Right Screen
rsw = 1920
rsh = 960




class image_converter:

  def __init__(self):
    self.image_pub = rospy.Publisher("rviz1/camera1/image2",Image)

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("rviz1/camera1/image",Image,self.callback)
    self.ip = '192.168.0.159'  
    self.port = 9050       
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.coordinatelist={'touchlist': []}
  def generate_vector2_data(self,valX,valY):
    
    new_point = {'points': {"X":valX, "Y" :valY}}
    self.coordinatelist['touchlist'].append(new_point)
    return self.coordinatelist

  def callback(self,data):
    
    global click_co , click_flag
    
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
    cropped = hsv[low_bounding[1]:high_bounding[1] , low_bounding[0]:high_bounding[0]]
    mask = cv2.inRange(cropped, green_lower_bound, green_upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(len(contours))
    self.coordinatelist={'touchlist': []}
    vectordata=None
      
    if contours:
      for cnt in contours:
          x,y,w,h = cv2.boundingRect(cnt)
          #print(x,y,w,h)
          click = ( (x+(w/2))/mask.shape[1] , (y+(h/2))/mask.shape[0] )
          #print(click)
          #pyautogui.moveTo(click[0]*sw , click[1]*sh)
          
          if ScreenNumber == 1:
            print(str(click[0]*lsw) + " , " + str(click[1]*lsh))
            vectordata = self.generate_vector2_data(click[0]*lsw,click[1]*lsh)
            
          elif ScreenNumber == 2:
            print(str((click[0]*msw)+lsw) + " , " + str(click[1]*msh))
            vectordata = self.generate_vector2_data(((click[0]*msw)+lsw),click[1]*msh)
            
          elif ScreenNumber == 3:
            print(str((click[0]*rsw)+lsw+msw) + " , " + str(click[1]*rsh))
            vectordata = self.generate_vector2_data(((click[0]*rsw)+lsw+msw),click[1]*rsh)

          #click_co = [ click[0]*sw , click[1]*sh ]
          click_flag = 1
      
      
      
    else:
      if click_flag == 1:
        #pyautogui.click( click_co[0] , click_co[1] )
        click_flag = 0
        
    json_data = json.dumps(vectordata)
    print(f"Sending data: {json_data}")
    self.sock.sendto(json_data.encode("UTF8"), (self.ip, self.port))
    cv2.imshow("Image window", mask)
    cv2.waitKey(1)

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
