'''
 # @ Author: J.N. Hayek
 # @ Create Time: 2022-01-27 08:44:46
 # @ Description: Python script to detect and track particles from a given input.
 Aims to track and detect particles on J.D. Coral's microfluidic setup.
 Uses the CV2 library to deal with the video capturing, video output, and user input, as well as detection from external model generated by J.D. Coral.
 As tracking means, it uses a centroid algorithm scheme, described on the lib "CentroidTracker". However it may required an increased frame rate for the video.
'''

# importing cv2 
import cv2 
from datetime import datetime
from Mods.CentroidTracker import CentroidTracker

################ Setup to make the code work on linux, ERASE TO USE IN YOUR IMPLEMENTATION
# path 
path = r'./'
  
mpsCascade = cv2.CascadeClassifier(path+"Input/haarcascades/haarcascade_mps.xml")

cap = cv2.VideoCapture(path+"Input/mps_in_channel.mp4")
##########################################################################################


# Variables
duration = 5
w = 0
CTimes = 0

ct = CentroidTracker(maxDisappeared=10)


while True:
    success, img = cap.read()
    if not success:
        break
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    

    # Register in the variable 'k' a pressed key
    k = cv2.waitKey(100) & 0xFF
    # press 'q' to exit
    if k == ord('q'):
        break
    # press 'c' to increase the CTimes counter and start a timer
    elif k == ord('c'):
        CTimes +=1 # Add 1 to CTimes per pressed c
        print("Pressed c: {} times".format(CTimes))  

        # start a timer
        start_time = datetime.now()


    # As CTimes = 0 is the state where nothing changes, checking for this will reduce the amount of operations per iteration 
    if CTimes!=0:
        # Calculate the difference in seconds between the timestamp and the current time
        diff = (datetime.now() - start_time).seconds
        # If the difference is under the prescribed duration, Print the consecutive number variable and add 1 to it to count for the current iteration 
        if (diff <= duration):
            mps = mpsCascade.detectMultiScale(imgGray, 1.1, 4)
            rects = []
            for x, y, w, h in mps:
                w_0,h_0=15,15
                cv2.rectangle(img, (x, y), (x + w_0, y + h_0), (255, 0, 0), 2)
                cv2.putText(img, "mp", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.3, (0, 0, 0), 1)
                rects.append([x, y, x+w_0, y+h_0])
            
            objects = ct.update(rects)
            for (objectID, centroid) in objects.items():
                # draw both the ID of the object and the centroid of the
                # object on the output frame
                text = "ID {}".format(objectID)
                cv2.putText(img, text, (centroid[0], centroid[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(img, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

            #w += 1
            # print ("My Consecutive number is {}".format(w))

        else: # If the duration is larger than the set time, the CTimes counter resets
            CTimes = 0
            
    cv2.imshow("Video", img) 

  
#closing all open windows 
cv2.destroyAllWindows() 