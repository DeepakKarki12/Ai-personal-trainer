# necessary imports
import cv2
import mediapipe as mp
import math
import time
import numpy as np
#
# important declaration of variable
mp_pose = mp.solutions.pose
poses = mp_pose.Pose()
draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture('KneeBendVideo.mp4') #


rep = 0
dir = 0 # it is the direction of the reps -- 0 for knee bent and 1 for knee straight
timer = 0 # initially the timer is zero
one = 1

while True:

    ret, frame = cap.read() # reading the video
    img_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) # converting the image BGR TO RGB
    result = poses.process(img_rgb)
    if result.pose_landmarks:
        for id, lm in enumerate(result.pose_landmarks.landmark):
            h, w, c = frame.shape
            if id == 23: # ID for left hip
                lhx1, lhy1 = int(lm.x*w), int(lm.y*h)
                z1 = lm.z
            if id == 24: # ID for right hip
                rhx1, rhy1 = int(lm.x*w), int(lm.y*h)
                z2 = lm.z
            ############### finding co ordinate to track the legs  #########################
            if id == 26: # right knee
                rkx1, rky1 = int(lm.x*w), int(lm.y*h)

            if id == 28: # right ankle
                rax1, ray1 = int(lm.x*w), int(lm.y*h)

            if id == 25: # left knee
                lkx1, lky1 = int(lm.x*w), int(lm.y*h)

            if id == 27: # left ankel
                lax1, lay1 = int(lm.x*w), int(lm.y*h)
        if z1 < z2 : # if left lef is close to camera track left leg and vice verse
            # left
            cv2.line(frame,(lhx1, lhy1),(lkx1,lky1),(0,0,0),3)
            cv2.line(frame,(lkx1,lky1),(lax1,lay1),(0,0,0),3)
            # calculating the angle of left leg
            angle = math.degrees(math.atan2(lay1-lky1,lax1-lkx1) - math.atan2(lhy1-lky1,lhx1-lkx1))
            abs_angle = abs(angle)
            rect = np.interp(abs_angle,[30,175],[50,400]) # converting the range into desired range
            percent = np.interp(rect,[25,400],[100,0])

            cv2.putText(frame,f'{int(percent)}%',(25,50),cv2.FONT_HERSHEY_TRIPLEX,2,(255,0,0),2)
            cv2.rectangle(frame, (25, 50), (55, 400), (0, 255, 0), 4)
            cv2.line(frame,(30,304),(50,304),(0,0,255),5)

            #  following code is for the colour of trackbar
            if rect>304:
                green= 255
                red = 0
            else :
                green = 0
                red = 255

            # the following code is for 8 sec timer and rep count
            if percent > 27:
                if one:
                    ptime = time.time()
                    one = 0
                ctime = time.time()
                timer = ctime - ptime
                one = 0
                if dir == 0:
                    if timer > 7:
                        rep += 0.5
                        timer = 0
                        dir = 1
            if percent < 27:
                if timer < 7:
                    ptime = time.time()
                    texts = 'keep your knee bent'
                    cv2.putText(frame,texts,(150,600),cv2.FONT_HERSHEY_TRIPLEX,1,(255,255,0),2)
                if dir == 1:
                    rep +=0.5
                    dir = 0
                    ptime = ctime
                    one = 1


            cv2.putText(frame,f'Reps:{rep}',(730,50),cv2.FONT_HERSHEY_TRIPLEX,1,(0,0,0),1)

            cv2.putText(frame,f'timer:{int(timer)}',(350,50),cv2.FONT_HERSHEY_TRIPLEX,2,(255,0,255),2)
            cv2.rectangle(frame, (25, int(rect)), (55, 400), (0, red, green), cv2.FILLED)


        else :
            # right
            cv2.line(frame, (rhx1, rhy1), (rkx1, rky1), (0, 255, 0), 5)
            cv2.line(frame, (rkx1, rky1), (rax1, ray1), (0, 255, 0), 5)
            # calculating the angle of right leg
            angle = math.degrees(math.atan2(ray1 - rky1, rax1 - rkx1) - math.atan2(rhy1 - rky1, rhx1 - rkx1))
            abs_angle = abs(angle)
            rect = np.interp(abs_angle, [30, 175], [50, 400])  # converting the range into desired range
            percent = np.interp(rect, [25, 400], [100, 0])

            cv2.putText(frame, f'{int(percent)}%', (25, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 0), 2)
            cv2.rectangle(frame, (25, 50), (55, 400), (0, 255, 0), 4)
            cv2.line(frame, (30, 304), (50, 304), (0, 0, 255), 5)

            #  following code is for the colour of trackbar
            if rect > 304:
                green = 255
                red = 0
            else:
                green = 0
                red = 255

            # the following code is for 8 sec timer and rep count
            if percent > 27:
                if one:
                    ptime = time.time()
                    one = 0
                ctime = time.time()
                timer = ctime - ptime
                one = 0
                if dir == 0:
                    if timer > 7:
                        rep += 0.5
                        timer = 0
                        dir = 1
            if percent < 27:
                if timer < 7:
                    ptime = time.time()
                    texts = 'keep your knee bent'
                    cv2.putText(frame, texts, (150, 600), cv2.FONT_HERSHEY_TRIPLEX, 1, (255, 255, 0), 2)
                if dir == 1:
                    rep += 0.5
                    dir = 0
                    ptime = ctime
                    one = 1

            cv2.putText(frame, f'Reps:{rep}', (730, 50), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), 1)

            cv2.putText(frame, f'timer:{int(timer)}', (350, 50), cv2.FONT_HERSHEY_TRIPLEX, 2, (255, 0, 255), 2)
            cv2.rectangle(frame, (25, int(rect)), (55, 400), (0, red, green), cv2.FILLED)


    cv2.imshow('window', frame)
    

    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()