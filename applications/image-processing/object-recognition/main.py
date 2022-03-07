from quixstreaming import SecurityOptions, QuixStreamingClient, ParameterData, StreamReader
import time

client = QuixStreamingClient()

# for more samples, please see library or docs

output_topic = client.open_output_topic("{placeholder:topic-processed}")
stream = output_topic.create_stream("input-image")



import cv2
import numpy as np

from datetime import datetime
import base64
import sys
import signal
import threading


#Load YOLO Algorithm
net=cv2.dnn.readNet("yolov3.weights","yolov3.cfg")
#To load all objects that have to be detected
classes=[]
with open("coco.names","r") as f:
    read=f.readlines()
for i in range(len(read)):
    classes.append(read[i].strip("\n"))
#Defining layer names
layer_names=net.getLayerNames()
output_layers=[]
for i in net.getUnconnectedOutLayers():
    output_layers.append(layer_names[i[0]-1])


def imgFromBase64(string):
    jpg_original = base64.b64decode(string)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    return img

def imgToBase64(img):
    return base64.b64encode(cv2.imencode('.png', img)[1]).decode()


def processImage(img):
    #Loading the Image
    height,width,channels=img.shape
    #Extracting features to detect objects
    blob=cv2.dnn.blobFromImage(img,0.00392,(416,416),(0,0,0),True,crop=False)
                                                            #Inverting blue with red
                                                            #bgr->rgb
    #We need to pass the img_blob to the algorithm
    net.setInput(blob)
    outs=net.forward(output_layers)
    #print(outs)
    #Displaying informations on the screen
    class_ids=[]
    confidences=[]
    boxes=[]
    for output in outs:
        for detection in output:
            #Detecting confidence in 3 steps
            scores=detection[5:]                #1
            class_id=np.argmax(scores)          #2
            confidence =scores[class_id]        #3
            if confidence >0.5: #Means if the object is detected
                center_x=int(detection[0]*width)
                center_y=int(detection[1]*height)
                w=int(detection[2]*width)
                h=int(detection[3]*height)
                #Drawing a rectangle
                x=int(center_x-w/2) # top left value
                y=int(center_y-h/2) # top left value
                boxes.append([x,y,w,h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    #Removing Double Boxes
    indexes=cv2.dnn.NMSBoxes(boxes,confidences,0.3,0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = classes[class_ids[i]]  # name of the objects
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, label, (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

    return img
    # cv2.imshow("Output",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# is_success, im_buf_arr = cv2.imencode(".jpg")
# byte_im = im_buf_arr.tobytes()

# img = cv2.imdecode(img, cv2.IMREAD_GRAYSCALE)

input_topic = client.open_input_topic('{placeholder:topic-raw}')
def read_stream(new_stream: StreamReader):

    buffer = new_stream.parameters.create_buffer()

    print("Received new stream")

    def on_parameter_data_handler(data: ParameterData):
        print("Received new parameter")
        for timestamp in data.timestamps:
            ts = timestamp.timestamp_nanoseconds
            string = timestamp.parameters['image'].string_value
            img=imgFromBase64(string)
            # img=cv2.imread("traffic.jpg")
            start = time.time()
            img=processImage(img)
            delta = start - time.time()

            print(delta)
            # imgstr = imgToBase64(img)

            stream.parameters.buffer.add_timestamp(datetime.now()) \
                .add_value("image", imgToBase64(img)) \
                .add_value("delta", delta) \
                .write()
            # cv2.imwrite('traffic_old.jpg',img)

        print("Done processing parameters")
        # print("ParameterA - " + str(timestamp) + ": " + str(num_value))

    buffer.on_read += on_parameter_data_handler

input_topic.on_stream_received += read_stream
input_topic.start_reading()

# Hook up to termination signal (for docker image) and CTRL-C
print("Listening to streams. Press CTRL-C to exit.")

event = threading.Event()
def signal_handler(sig, frame):
    print('Exiting...')
    event.set()

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
event.wait()
