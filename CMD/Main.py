import cv2
import time
import PoseModule as pm
import math
import numpy as np
import matplotlib.pyplot as plt
from playsound import playsound
import os



camera = 1 # camera used ( 0 = native camera , 1 = added webcam)

sounds = '/Users/saidalkathairi/PycharmProjects/UOBIRP2022/Sounds/DataScanner.wav'

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
        if angle > 20:
            playsound(sounds)


        if angle > Cutoff_forward:
            Nose_Chest_angle.append(Cutoff_forward)
            cv2.putText(img,'Head forward tilt in Degrees: ' + str(int(angle)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
        else:
            Nose_Chest_angle.append(angle)


    else:
        angle = -((math.acos(Nose_Chest_distance/VD)) * 180 / math.pi)
        cv2.putText(img, 'Head forward tilt in Degrees: ' + str(int(angle)), (70, 100), cv2.FONT_HERSHEY_PLAIN, 3,(0, 0, 255), 3)
        if angle < -10:
            playsound(sounds)

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
        playsound(sounds)


    # shoulders tilt:
    y1 = lmList[11][2] #left shoulder y position
    y2 = lmList[12][2] #right shoulder y position
    ST = pm.Shouldertilt(y1,y2)
    Spine_curvature.append(ST)

    if ST == -1:
        cv2.putText(img, 'Spine Curved Leftwards' , (70, 150), cv2.FONT_HERSHEY_PLAIN, 3,(0, 255, 0), 3)
        playsound(sounds)

    elif ST == 1:
        cv2.putText(img, 'Spine Curved Rightwards', (70, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        playsound(sounds)



    cv2.imshow('Image', img)
    cv2.waitKey(1)  # 1ms delay

else:

    os.remove("CMD/Calibrate.jpg")

    f = open('results.txt','w')
    f.write(str(Nose_Chest_angle))
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write(str(Spine_curvature))
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write('\n')
    f.write(str(OFF_centre_angle))
    f.close()

    # Analysing the data

    # Head forward tilt:

    F = open('Posture.txt', 'w')
    x1, x2, x3 = 0, 0, 0
    for i in Nose_Chest_angle:
        if int(i) >= 20:
            x1 += 1
        elif int(i) <= -10:
            x1 += 1
    bad_posture_percentage = (x1 / len(Nose_Chest_angle)) * 100
    F.write('Forward Head tilt Bad posture: ' + str(bad_posture_percentage) + '%' + '\n')

    for i in OFF_centre_angle:
        if int(abs(i)) >= 10:
            x2 += 1
    bad_posture_percentage = (x2 / len(OFF_centre_angle)) * 100
    F.write('Off Centre Bad Posture: ' + str(bad_posture_percentage) + '%' + '\n')

    for i in OFF_centre_angle:
        if int(abs(i)) == 1:
            x3 += 1
    bad_posture_percentage = (x3 / len(Spine_curvature)) * 100
    F.write('Spinal curvature bad Posture: ' + str(bad_posture_percentage) + '%' + '\n')

    F.close()

    tick_spacing = 100 # every 30 seconds
    length = len(Nose_Chest_angle) # number of samples
    samplingRate = length/duration # duration in seconds
    ticks = np.arange(0, length, tick_spacing*int(samplingRate))
    seconds = [0]
    for i in range(int(duration/tick_spacing)):
        seconds.append((i+1)*tick_spacing)





    # plotting Neck angle
    plt.figure(1)
    plt.title('Head Forward Angle')
    plt.plot(Nose_Chest_angle, color = 'b')
    plt.xticks( ticks , seconds)
    plt.xlim(xmin=0)
    plt.axhline(y=20, color='g', linestyle='-',label='Upper Threshold')
    plt.axhline(y=-10, color='y', linestyle='-',label='Lower Threshold')
    plt.xlabel('Time(s)')
    plt.ylabel('Head Angle (degrees)')

    #neck off centre angle
    plt.figure(2)
    plt.title('Head Off-Centre Angle')
    plt.plot(OFF_centre_angle, color = 'b')
    plt.xticks( ticks , seconds)
    plt.xlim(xmin=0)
    plt.axhline(y=10, color='g', linestyle='-',label='Upper Threshold')
    plt.axhline(y=-10, color='y', linestyle='-',label='Lower Threshold')
    plt.xlabel('Time(s)')
    plt.ylabel('Head Angle (degrees)')

    #Spine curvature
    plt.figure(3)
    plt.title('Spinal Curvature')
    plt.plot(Spine_curvature, color = 'b')
    plt.xticks( ticks , seconds)
    plt.yticks([-1,0,1],['L','N','R'])
    plt.xlim(xmin=0)
    plt.xlabel('Time(s)')
    plt.ylabel('Spine curvature (direction)')

    plt.show()



# Analysing the data

# Head forward tilt:

F = open('Posture.txt','w')
x1,x2,x3 = 0,0,0
for i in Nose_Chest_angle:
    if int(i) >= 20:
        x1+=1
    elif int(i) <= -10:
        x1+=1
bad_posture_percentage = (x1/len(Nose_Chest_angle))*100
F.write('Forward Head tilt Bad posture: ' + str(bad_posture_percentage)+'%'+'\n')

for i in OFF_centre_angle:
    if int(abs(i)) >= 10:
        x2+=1
bad_posture_percentage = (x2/len(OFF_centre_angle))*100
F.write('Off Centre Bad Posture: ' + str(bad_posture_percentage)+'%'+'\n')

for i in OFF_centre_angle:
    if int(abs(i)) == 1:
        x3 += 1
bad_posture_percentage = (x3 / len(Spine_curvature)) * 100
F.write('Spinal curvature bad Posture: ' + str(bad_posture_percentage) + '%'+'\n')

F.close()











