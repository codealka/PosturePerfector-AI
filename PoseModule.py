import cv2
import mediapipe as mp # Mediapipe uses RGB
import time

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
                cx , cy  = int(lm.x*w) , int(lm.y*h) #x  and y coordinates (pixels)
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img, (cx,cy),5,(255,0,0),cv2.FILLED) # will create blobs on the landmarks
        return lmList




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