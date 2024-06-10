import cv2
import numpy as np
import HandTrackModule as hm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
wCam, hCam = 1000, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = hm.handDetector(detectionCon=0.7)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange =volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
vol=0
volBar=400
volPer=0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) !=0:
        #print(lmlist[4], lmlist[0])

        x1, y1= lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1, y1), 8, (0, 255, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (0, 255, 255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (0,255,255), 2)
        cv2.circle(img, (cx, cy), 5, (0, 255, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #print(length)

        vol = np.interp(length,[30,300], [minVol, maxVol])
        volBar = np.interp(length, [30, 300], [400, 150])
        volPer = np.interp(length, [30, 300], [0, 100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<30:
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400), (0,255,0),3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,250,0), 3)

    cv2.imshow("image", img)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()