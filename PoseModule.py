import cv2
import mediapipe as mp # Mediapipe uses RGB
import time
import streamlit as st



def Shouldertilt(y1,y2):

    PD = ((y1 - y2)/y2)*100 # percentage difference
    if PD > 5:
        return -1
    elif PD < -5:
        return 1
    else:
        return 0

    # 1 -> Spine curved rightwards (
    # 0 -> spine curved leftwards )

def halfwaypoint(tuple1,tuple2):
    # each tuple has 4 entries id,x,y,z

    half = [(tuple1[0]+tuple2[0])/2,
            (tuple1[1]+tuple2[1])/2,
            (tuple1[2]+tuple2[2])/2,
            (tuple1[3]+tuple2[3])/2]

    return half


def Calibrate_app(camera):

    Calibrate = True
    img_calibrate = st.image([])

    cam = cv2.VideoCapture(camera)

    text = st.empty()
    text.write('Make sure: \n'
               ' * your head is at the centre of the frame \n'
               ' * your shoulders are visible \n '
               ' * nothing is obstructing your body view \n')

    empty = st.empty()
    button = empty.checkbox("Calibrate posture by clicking here")


    while Calibrate:
        ret, img = cam.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_calibrate.image(img)

        if button:
            Calibrate = False
            img_name = "Calibrate.jpg"
            cv2.imwrite(img_name, img)
            print("{} written!".format(img_name))
            empty.empty()
            text.empty()

    # getting calibration data
    detector = poseDetector()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)

    # -----------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------
    Chest = halfwaypoint(lmList[11], lmList[12])
    nose = lmList[0]
    NCVD = Chest[2] - nose[2]  # Nose to chest vertical distance
    NCVD_benchmark = NCVD

    # -----------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------
    #Slouching
    shoulderWIDTH = lmList[12][1]-lmList[11][1]

    return NCVD_benchmark , shoulderWIDTH




def Calibrate_picture(camera):
    cam = cv2.VideoCapture(camera)
    cv2.namedWindow("Calibration")
    img_counter = 0

    while img_counter<1:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("test", frame)

        k = cv2.waitKey(1)

        if k % 256 == 32:
            # SPACE pressed
            img_name = "Calibrate.jpg"
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()

    #getting calibration data
    detector = poseDetector()
    img = detector.findPose(frame)
    lmList = detector.findPosition(img)


#-----------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------
    Chest = halfwaypoint(lmList[11],lmList[12])
    nose = lmList[0]
    NCVD =  Chest[2] - nose[2] #Nose to chest vertical distance
    NCVD_benchmark = NCVD




    return NCVD_benchmark



class poseDetector():

    def __init__(self, mode = False , complexity = 1, smooth = True ,
                 enable_segmentation = False , smooth_segmentation = True,
                 detectionCon = 0.5, trackingCon = 0.5):


        # static_image_mode = False,
        # model_complexity = 1,
        # smooth_landmarks = True,
        # enable_segmentation = False,
        # smooth_segmentation = True,
        # min_detection_confidence = 0.5,
        # min_tracking_confidence = 0.5):

        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation =  smooth_segmentation
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode ,self.complexity, self.smooth,self.enable_segmentation,
                                     self.smooth_segmentation,self.detectionCon, self.trackingCon)



    def findPose(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converting into right format
        self.results = self.pose.process(imgRGB)  # detection of  pose (without drawing)

        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img



    def findPosition(self, img , draw = True):

        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark): # id = point number , lm = landmark
                h,w,c = img.shape
                cx , cy , cz  = round(lm.x,2) , round(lm.y,2) , round(lm.z*-1,2) #x  and y coordinates (pixels)
                lmList.append([id,cx,cy,cz])
                cx,cy = int(lm.x*w) , int(lm.y*h)
                if draw:
                     cv2.circle(img, (cx,cy),8,(255,0,0),cv2.FILLED) # will create blobs on the landmarks
            return lmList
        else:
            print('Could not find Position')
            return(False)






def main():






    cap = cv2.VideoCapture('Videos/aboody.mp4')
    pTime = 0  # previous time
    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.findPosition(img)
        print(lmList)

        # to track specific points we can look at lmlist['point index']

        cTime = time.time()  # current time
        fps = 1 / (cTime - pTime)
        pTime = cTime  # updating previous time

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow('Image', img)

        cv2.waitKey(1)  # 1ms delay




if __name__ == "__main__":
    main()