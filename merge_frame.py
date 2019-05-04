# Program To Read video 
# and Extract Frames
import os
import cv2
import math

# Driver Code 

path = "/home/fyp/Desktop/FYP/Frames"
files = os.listdir(path)
count=0
if not os.path.exists("/home/fyp/Desktop/FYP/Frames/allFrames"):
	os.makedirs("/home/fyp/Desktop/FYP/Frames/allFrames")
for file in files:
	# Calling the function
	images = os.listdir(path + '/' + file)
	for img in images:

		im = cv2.imread(path +'/'+file+'/'+img)
		cv2.imwrite("/home/fyp/Desktop/FYP/Frames/allFrames/{0}.jpg".format(str(count)), im)
		#cv2.imwrite("/home/fyp/Desktop/FYP/Frames/allFrames/{0}".format(str(count)), im)
		count+=1
		


	#FrameCapture(path, file)
	print('done')
