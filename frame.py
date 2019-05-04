# Program To Read video 
# and Extract Frames
import os
import cv2
import math

# Function to extract frames 
def FrameCapture(path, file):

    # Path to video file
    vidObj = cv2.VideoCapture(path+"\\"+file)
##    print(vidObj.get(5))
    frate = vidObj.get(5)
    # Used as counter variable
    count = 0

    # checks whether frames were extracted
    success = 1

    while success:

        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()
        fid = vidObj.get(1)

        if not os.path.exists("/home/fyp/Desktop\FYP/Frames/{0}".format(file.split(".")[0])):
            os.makedirs("/home/fyp/Desktop/FYP/Frames/{0}".format(file.split(".")[0]))

        if (fid % math.floor(frate) == 0):

        # Saves the frames with frame-count
            cv2.imwrite("/home/fyp/Desktop/FYP/Frames/{0}/frame{1}.jpg".format(file.split(".")[0],str(count)), image)
		
            count += 1

# Driver Code 
if __name__ == '__main__':
    path = "/home/fyp/Desktop/FYP/Videos"
    files = os.listdir(path)
    for file in files:
        # Calling the function 
        FrameCapture(path, file)
    print('done')
