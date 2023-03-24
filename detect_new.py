from tkinter import Frame
import torch
import cv2
import requests
import threading
import time

def yolo_detection(model, img):
    global status
    img = cv2.resize(img, (640, 640))
    result = model(img)
    temp = []
    for obj in result.pandas().xyxy[0].values:
        label = obj[5]
        conf = obj[4]
        print(f"{label}: {conf:.2f}")
        if(label==1):
            status = 1
        else:
            status = 0


def send_photo():
    pass

def main():
    model = torch.hub.load("yolov7", "custom", "pt_files/best.pt", source="local")
    cap = cv2.VideoCapture(0)
    global frame
    while True:
        ret, frame = cap.read()
        
        if ret:
            yolo_detection(model, frame)
            cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    status = 0
    frame = None
    main_thread = threading.Thread(target=main)
    telegram_thread = threading.Thread(target=send_photo)
    main_thread.start()
    telegram_thread.start()
    main_thread.join()
    telegram_thread.join()
    
