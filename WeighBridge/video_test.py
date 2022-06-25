import torch
import cv2
import re
import easyocr
import numpy as np
from imutils.video.videostream import VideoStream


reader = easyocr.Reader(['en'])
model = torch.hub.load(R"yolov5", 'custom',path=R"weights\yolov5n_640pix\train\exp\weights\last.pt",source= 'local')
vs = VideoStream(src=0).start()

while True:
    img = vs.read()
    results = model(img)
    cv2.imwrite("full.png",img)
    try:
        cv2.imshow("Result",np.squeeze(results.render()))
        a = results.xyxy[0].numpy()[0]
        image = img[int(a[1]):int(a[3]),int(a[0]):int(a[2])]
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        cv2.imwrite("saved.png",image)
        ocr_result = reader.readtext(image,detail = 0)
        string = "".join(ocr_result)  
        print(re.sub('\W+','',string).upper())


    except:
        pass

    if cv2.waitKey(10) & 0xFF == ord('q'):
        vs.stop()
        cv2.destroyAllWindows()
        break