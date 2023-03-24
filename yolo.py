import cv2
import numpy as np
import threading 
import requests
# from bot_test import forward 

token = '5929554815:AAG6lv0T3UU0lFdtaFHFf6UpZnMkGpFZuOg'
base_url='https://api.telegram.org/bot{}/'.format(token)

def send_photo(chat_id,file_opened):
    method = "sendPhoto"
    params = {'chat_id':1193253139}
    files = {'photo':file_opened}
    resp = requests.post(base_url+method,params,files=files)
    return resp




def frametaking():
    global flag
    while(1):
        if(flag is True):
            webcam = cv2.VideoCapture(0)
            currentframes=0

            while(True):
            #success is boolean either true or false
            #.read is used to extract frame by frame information
                _,frame = webcam.read()
                # to save captured image
                #cv2.imshow('Output',frame)
                cv2.imwrite('C:/Users/keerthi/Desktop/asi/frame' + str(currentframes) +'.jpg',frame)
                send_photo(1193253139,open('C:/Users/keerthi/Desktop/asi/frame'+str(currentframes)+'.jpg','rb'))
                currentframes +=1

                if currentframes==3:
                    flag =False
                    break

    #webCam.release()
    


def findObjects():
    global outputs, img, flag
    while(1):
        try: 
            if img.size != 0:
                hT, wT, cT = img.shape
                bbox = []
                classIds = []
                confs = []

                for output in outputs:
                    for det in output:
                        scores = det[5:]
                        classId = np.argmax(scores)
                        confidence = scores[classId]
                        if confidence > confThreshold:
                            w,h = int(det[2]* wT), int(det[3]*hT)
                            x,y = int((det[0]*wT)-w/2), int((det[1]*hT)-h/2)
                            bbox.append([x,y,w,h])
                            classIds.append(classId)
                            confs.append(float(confidence))

                #print(classIds)

                #print(len(bbox))
                indices = cv2.dnn.NMSBoxes(bbox, confs,confThreshold,nmsThreshold)
                #print(indices)

                for i in indices:
                    i = i
                    box = bbox[i]
                    x,y,w,h = box[0], box[1], box[2], box[3]
                    cv2.rectangle(img, (x,y),(x+w,y+h),(255,0,255),2)
                    j=(classNames[classIds[i]].upper())
                    cv2.putText(img,f'{classNames[classIds[i]].upper()} {int(confs[i]*100)}%',
                                (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6,(255,0,0),2)
                    #print(j)
                    if 'PERSON'==j:
                        flag = True
                        #print(123)
                        
        except:
            continue    
         
def main():
    global outputs, img, flag
    flag=False 


    while True:
        success, img = cap.read()
        try:
            blob = cv2.dnn.blobFromImage(img, 1/255,(whT,whT),[0,0,0],crop=False)
            net.setInput(blob)

            layerNames = net.getLayerNames()
            #print(layerNames)
            # print(len(layerNames))
            # print(net.getUnconnectedOutLayers())
            outputNames = [layerNames[i-1] for i in net.getUnconnectedOutLayers()]
            #print(outputNames)
            outputs = net.forward(outputNames)

            #-cv2.imshow('Image', img)
            cv2.waitKey(1)
        except:
            continue    

if __name__ == '__main__':
    global outputs, img, flag
    whT = 320
    confThreshold = 0.5
    nmsThreshold = 0.3     
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)    
    classesFile = 'C:/Users/keerthi/Desktop/Yolo/person.names'
    classNames = []
    with open(classesFile,'rt') as f:
        for line in f:
            line = line.strip()
            classNames.append(line)
    #print(len(classNames))
    #print(classNames)
    #print(classNames)
    #print(len(classNames))

    modelConfiguration = 'C:/Users/keerthi/Desktop/Yolo/yolov3.cfg'
    modelWeights = 'C:/Users/keerthi/Downloads/yolov3.weights'

    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_DEFAULT)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    thread_main = threading.Thread(target=main)
    thread_findobj = threading.Thread(target=findObjects)
    thread_frame = threading.Thread(target=frametaking)
    # thread_bot = threading.Thread(target=forward)

    thread_main.start()
    thread_frame.start()
    thread_findobj.start()
    # thread_bot.start() 

    thread_main.join()
    thread_frame.join()
    thread_findobj.join()
    # thread_bot.start()