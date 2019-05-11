import cv2

class Detection(object):
    def __init__(self, frame):
        self.frame = frame
        self.face_cascade = cv2.CascadeClassifier("./utility/haarcascade_frontalface_default.xml")
        # Opencvのカメラをセットします。(0)はノートパソコンならば組み込まれているカメラ

    def face_detection(self):
        first_frame = None
        # gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # img = cv2.UMat(self.frame)
        gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        # delta_frame = cv2.absdiff(first_frame, gray)
        # thresh_frame = cv2.threshold(delta_frame, 30,255, cv2.THRESH_BINARY)[1]
        # thresh_frame_dilate = cv2.dilate(thresh_frame, None, iterations=2)

        faces = self.face_cascade.detectMultiScale(self.frame,
                                        scaleFactor=1.1,
                                        minNeighbors=5)

        for x, y, w, h in faces:
            face_img = cv2.rectangle(self.frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        return self.frame
