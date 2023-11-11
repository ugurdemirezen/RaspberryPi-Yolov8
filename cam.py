import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
if __name__ == '__main__':
    model = YOLO('runs/detect/train9/weights/best.pt')
    HOST=''
    PORT=8485

    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created')

    s.bind((HOST,PORT))
    print('Socket bind complete')
    s.listen(10)
    print('Socket now listening')

    conn,addr=s.accept()

    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += conn.recv(4096)

        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        #results = model.train(data='coco128.yaml', epochs=100, imgsz=640, device="0")
        results = model(frame)
        for r in results:

            annotator = Annotator(frame)

            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
                c = box.cls
                annotator.box_label(b, model.names[int(c)])
        img = annotator.result()
        cv2.imshow('YOLO V8 Detection', img)
        cv2.waitKey(1)