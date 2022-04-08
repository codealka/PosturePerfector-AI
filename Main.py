import cv2
import time
import PoseModule as pm
import math
import numpy as np
import matplotlib.pyplot as plt


camera = 1 # camera used ( 0 = native camera , 1 = added webcam)



#main code

Benchmark = pm.Calibrate_picture(camera)
cap = cv2.VideoCapture(camera)
pTime = 0  # previous time
detector = pm.poseDetector()

Nose_Chest_angle = []
OFF_centre_angle = []
Spine_curvature = []

duration = 60*int(input("How long do you want to run a session for (in minutes)?"))
run_time = time.time() + duration

while time.time() < run_time:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)


    cTime = time.time()  # current time
    fps = 1 / (cTime - pTime)
    pTime = cTime  # updating previous time
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)







    # to track specific points we can look at lmlist['point index']

    #Nose
    Nose = lmList[0]

    #Chest
    Chest = pm.halfwaypoint(lmList[11],lmList[12])



    # Nose to chest:
    VD = Chest[2] - Nose[2] #vertical distance nose to chest ( real time)
    Nose_Chest_distance = Benchmark      # calibrated Nose to chest distance

    Cutoff_forward = 60
    Cutoff_backward = -30

    if VD <= Nose_Chest_distance:
        angle = (math.acos(VD / Nose_Chest_distance)) * 180 / math.pi
        cv2.putText(img, 'Head forward tilt in Degrees: ' + str(int(angle)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 3,(0, 0, 255), 3)
        if angle > Cutoff_forward:
            Nose_Chest_angle.append(Cutoff_forward)
            cv2.putText(img,'Head forward tilt in Degrees: ' + str(int(angle)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        else:
            Nose_Chest_angle.append(angle)

    else:
        angle = -((math.acos(Nose_Chest_distance/VD)) * 180 / math.pi)
        cv2.putText(img, 'Head forward tilt in Degrees: ' + str(int(angle)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 3,(0, 0, 255), 3)
        if angle < Cutoff_backward:
            Nose_Chest_angle.append(Cutoff_backward)
        else:
            Nose_Chest_angle.append(angle)



    # Head Side to side tilt:
    Chest_x = Chest[1]
    Nose_x = Nose[1]
    OFF_centre_d = Nose_x - Chest_x # if d > 0 then right tilt , if d < 0 then left tilt


    OFF_Centre_Cut_OFF = 50 # cut off value where the angle represnted will no longer be accurate due to awkward body position

    if abs(VD) > abs(OFF_centre_d):

        angle1 = (math.asin(OFF_centre_d / VD) * 180 / math.pi)
        if  angle1 > OFF_Centre_Cut_OFF :
            print('Can not Calculate')
            OFF_centre_angle.append(OFF_Centre_Cut_OFF)
        elif angle1 < -OFF_Centre_Cut_OFF :
            OFF_centre_angle.append(OFF_Centre_Cut_OFF)
        else:
            OFF_centre_angle.append(angle1)





    if abs(angle1) > 10:
        cv2.putText(img, 'Off centre head angle: ' + str(int(angle1)), (70, 200), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)


    # shoulders tilt:
    y1 = lmList[11][2] #left shoulder y position
    y2 = lmList[12][2] #right shoulder y position
    ST = pm.Shouldertilt(y1,y2)
    print(ST)
    Spine_curvature.append(ST)

    if ST == -1:
        cv2.putText(img, 'Spine Curved Leftwards' , (70, 150), cv2.FONT_HERSHEY_PLAIN, 3,(0, 255, 0), 3)
    elif ST == 1:
        cv2.putText(img, 'Spine Curved Rightwards', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)



    cv2.imshow('Image', img)
    cv2.waitKey(1)  # 1ms delay

else:

    tick_spacing = 30 # every 30 seconds
    length = len(Nose_Chest_angle) # number of samples
    samplingRate = length/duration # duration in seconds
    ticks = np.arange(0, length, tick_spacing*int(samplingRate))
    seconds = [0]
    for i in range(int(duration/tick_spacing)):
        seconds.append((i+1)*tick_spacing)

    print (len(ticks),len(seconds))




    # plotting Neck angle
    plt.figure(1)
    plt.title('Neck Forward Angle')
    plt.plot(Nose_Chest_angle, color = 'b')
    plt.xticks( ticks , seconds)
    plt.xlim(xmin=0)
    plt.axhline(y=15, color='g', linestyle='-',label='Upper Threshold')
    plt.axhline(y=-15, color='y', linestyle='-',label='Lower Threshold')
    plt.xlabel('Time(s)')
    plt.ylabel('Neck tilt Angle (degrees)')

    #neck off centre angle
    plt.figure(2)
    plt.title('Neck Off Centre Angle')
    plt.plot(OFF_centre_angle, color = 'b')
    plt.xticks( ticks , seconds)
    plt.xlim(xmin=0)
    plt.axhline(y=10, color='g', linestyle='-',label='Upper Threshold')
    plt.axhline(y=-10, color='y', linestyle='-',label='Lower Threshold')
    plt.xlabel('Time(s)')
    plt.ylabel('Neck off centre Angle (degrees)')

    #Spine curvature
    plt.figure(3)
    plt.title('Spinal Curvature')
    plt.plot(Spine_curvature, color = 'b')
    plt.xticks( ticks , seconds)
    plt.yticks([-1,0,1],['L','N','R'])
    plt.xlim(xmin=0)
    plt.xlabel('Time(s)')
    plt.ylabel('Spine curvature direction')








    plt.show()
