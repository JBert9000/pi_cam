import cv2, time
from datetime import datetime
import pandas as pd
import csv

first_frame=None
status_list=[None,None]
times=[]
video=cv2.VideoCapture(0)

while True:
    check, frame=video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)

    thresh_frame=cv2.threshold(delta_frame,30,255,cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame,None,iterations=2)

    cnts=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y),(x+w, y+h), (0,255,0),3)

    status_list.append(status)
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())

    cv2.imshow("Gray1",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Colour Frame", frame)

    key=cv2.waitKey(1)
    # print(frame)
    # print(delta_frame)

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

while True:
    with open('motion capture time.csv','w',newline='') as csv_file:
        fieldnames=times[0]
        writer=csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writerow({'year':times[0][0],'day':times[0][1],'hour':times[0][2],'minutes':times[0][3]})
        print(csv_file)

video.release()
cv2.destroyAllWindows()
